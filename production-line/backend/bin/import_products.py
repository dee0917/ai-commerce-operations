#!/usr/bin/env python3
"""
Pushes a product feed into a WooCommerce store over the REST API.

Idempotent: products are matched on SKU, so rerunning updates instead of duplicating.
Categories are matched on slug. Images are optional; when an assets root is given the
files are copied into the WordPress container and registered in the media library once,
then referenced by attachment id.

Usage:
  python import_products.py feeds/vanguard.json --assets-root <site>/public
  python import_products.py feeds/sourcing.json --skip-images

Credentials are read from the environment or --env-file. Nothing is hardcoded.
"""

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from woo_client import WooClient, WooError, load_env  # noqa: E402

BATCH_SIZE = 50
CONTAINER_MEDIA_DIR = "/tmp/acp-media"


def sync_categories(client, categories):
    """Return {slug: id}, creating any category the store does not have yet."""
    existing = {c["slug"]: c["id"] for c in client.paged("products/categories")}
    to_create = [c for c in categories if c["slug"] not in existing]

    if to_create:
        result = client.post("products/categories/batch", {"create": to_create})
        for created in result.get("create", []):
            if created.get("id"):
                existing[created["slug"]] = created["id"]
            else:
                print("  category failed: %s -> %s" % (created.get("slug"), created.get("error")))

    return existing


def upload_images(container, assets_root, image_paths):
    """Copy local image files into the container and register them in the media library.

    Returns {feed_path: attachment_id}. Files that do not exist on disk are skipped and
    reported, rather than failing the whole import.
    """
    resolved = {}
    missing = []
    for feed_path in image_paths:
        local = Path(assets_root) / feed_path.lstrip("/")
        if local.is_file():
            resolved[feed_path] = local
        else:
            missing.append(feed_path)

    if missing:
        print("  %d image(s) not found on disk, products will be created without them:" % len(missing))
        for item in missing[:10]:
            print("    %s" % item)

    if not resolved:
        return {}

    subprocess.run(
        ["docker", "exec", container, "sh", "-c", "rm -rf %s && mkdir -p %s" % (CONTAINER_MEDIA_DIR, CONTAINER_MEDIA_DIR)],
        check=True,
        capture_output=True,
    )
    for local in resolved.values():
        subprocess.run(
            ["docker", "cp", str(local), "%s:%s/%s" % (container, CONTAINER_MEDIA_DIR, local.name)],
            check=True,
            capture_output=True,
        )

    script = (
        'for f in %s/*; do id=$(wp media import "$f" --porcelain 2>/dev/null); '
        'echo "$(basename "$f")\t$id"; done' % CONTAINER_MEDIA_DIR
    )
    proc = subprocess.run(
        ["docker", "exec", container, "sh", "-c", script],
        check=True,
        capture_output=True,
        text=True,
    )

    by_filename = {}
    for line in proc.stdout.splitlines():
        if "\t" not in line:
            continue
        name, attachment_id = line.split("\t", 1)
        attachment_id = attachment_id.strip()
        if attachment_id.isdigit():
            by_filename[name] = int(attachment_id)

    return {
        feed_path: by_filename[local.name]
        for feed_path, local in resolved.items()
        if local.name in by_filename
    }


def build_payload(product, category_ids, media_ids):
    payload = {
        "name": product["name"],
        "slug": product.get("slug") or "",
        "type": "simple",
        "status": "publish",
        "sku": product.get("sku") or "",
        "description": product.get("description", ""),
        "short_description": product.get("short_description", ""),
        "regular_price": str(product.get("regular_price", "0")),
        "sale_price": str(product.get("sale_price") or ""),
        "manage_stock": product.get("stock_quantity") is not None,
        "stock_status": product.get("stock_status", "instock"),
        "categories": [
            {"id": category_ids[slug]}
            for slug in product.get("categories", [])
            if slug in category_ids
        ],
        "images": [
            {"id": media_ids[src]} for src in product.get("images", []) if src in media_ids
        ],
    }
    if payload["manage_stock"]:
        payload["stock_quantity"] = product["stock_quantity"]
    return payload


def chunks(items, size):
    for start in range(0, len(items), size):
        yield items[start:start + size]


def main():
    parser = argparse.ArgumentParser(description="Import a product feed into WooCommerce.")
    parser.add_argument("feed", help="Path to the feed JSON file")
    parser.add_argument("--assets-root", help="Directory that the feed's image paths are relative to")
    parser.add_argument("--container", default="acp_wpcli", help="WP-CLI container name")
    parser.add_argument("--skip-images", action="store_true")
    parser.add_argument("--env-file", default=str(Path(__file__).resolve().parent.parent / ".env.backend"))
    args = parser.parse_args()

    load_env(args.env_file)
    client = WooClient()

    feed = json.loads(Path(args.feed).read_text(encoding="utf-8"))
    products = feed.get("products", [])
    if not products:
        raise SystemExit("Feed contains no products")

    print("Feed: %d products, %d categories" % (len(products), len(feed.get("categories", []))))

    category_ids = sync_categories(client, feed.get("categories", []))
    print("Categories in store: %d" % len(category_ids))

    media_ids = {}
    if not args.skip_images and args.assets_root:
        wanted = sorted({src for p in products for src in p.get("images", [])})
        media_ids = upload_images(args.container, args.assets_root, wanted)
        print("Images registered in media library: %d" % len(media_ids))

    existing_by_sku = {
        p["sku"]: p["id"] for p in client.paged("products", status="any") if p.get("sku")
    }

    to_create, to_update = [], []
    for product in products:
        payload = build_payload(product, category_ids, media_ids)
        sku = payload["sku"]
        if sku and sku in existing_by_sku:
            payload["id"] = existing_by_sku[sku]
            to_update.append(payload)
        else:
            to_create.append(payload)

    created = updated = failed = 0
    failures = []

    for group_name, group in (("create", to_create), ("update", to_update)):
        for batch in chunks(group, BATCH_SIZE):
            try:
                result = client.post("products/batch", {group_name: batch})
            except WooError as exc:
                failed += len(batch)
                failures.append("batch of %d failed: %s" % (len(batch), exc))
                continue
            for item in result.get(group_name, []):
                if item.get("id") and not item.get("error"):
                    if group_name == "create":
                        created += 1
                    else:
                        updated += 1
                else:
                    failed += 1
                    failures.append("%s: %s" % (item.get("sku", "?"), item.get("error")))

    print("Created: %d   Updated: %d   Failed: %d" % (created, updated, failed))
    for line in failures[:20]:
        print("  FAIL %s" % line)

    total = len(list(client.paged("products", status="any")))
    print("Products now in store: %d" % total)

    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
