#!/usr/bin/env python3
"""
Turns a product pool export into the neutral feed format that import_products.py consumes.

The pool groups items under category headings and carries a supplier cost per item, not a
retail price. Retail price is derived here with a flat multiplier so the pricing rule stays
in one visible place instead of being buried in the importer.

The pool is a sourcing catalogue, not a to-list. The intended production flow takes ONE
category out of the pool per site, which is what --category is for. Converting the whole
pool at once is a volume test, not the normal path.

Supplier cost, unit weight and the supplier listing url are carried through as their own
fields so downstream margin and shipping work does not have to parse them back out of the
description text. import_products.py builds its API payload from named keys, so these
extra fields ride along without reaching WooCommerce.

Usage:
  python feed_from_sourcing.py <pool.json> <out.json> [--markup 3.0] [--limit N]
  python feed_from_sourcing.py <pool.json> <out.json> --category "Sound Healing Tools"
  python feed_from_sourcing.py <pool.json> --list-categories
"""

import argparse
import json
import os
import re
import tempfile
import unicodedata
from pathlib import Path


def slugify(value, fallback):
    """ASCII slug, falling back to a stable id when the name has no ASCII to work with."""
    ascii_form = unicodedata.normalize("NFKD", value).encode("ascii", "ignore").decode()
    slug = re.sub(r"[^a-z0-9]+", "-", ascii_form.lower()).strip("-")
    return slug or fallback


def clean_category(raw):
    """'## 1. Foo (Bar)' -> 'Bar' when there is a parenthetical, otherwise 'Foo'."""
    text = re.sub(r"^#+\s*", "", raw or "").strip()
    text = re.sub(r"^\d+[.\s]*", "", text).strip()
    match = re.search(r"\(([^)]+)\)", text)
    if match:
        return match.group(1).strip()
    return text


def write_json(target, payload):
    """Write via a temp file in the same directory, then replace, so a crash mid-write
    cannot leave the caller with a truncated feed."""
    target = Path(target)
    target.parent.mkdir(parents=True, exist_ok=True)
    handle = tempfile.NamedTemporaryFile(
        "w", encoding="utf-8", dir=str(target.parent), prefix=target.name + ".", suffix=".tmp", delete=False
    )
    try:
        with handle as out:
            json.dump(payload, out, ensure_ascii=False, indent=2)
        os.replace(handle.name, target)
    except BaseException:
        Path(handle.name).unlink(missing_ok=True)
        raise


def matches_category(wanted, raw_title, label, cat_slug):
    """True when --category names this group by slug, cleaned label, or raw heading text."""
    needle = wanted.strip().casefold()
    if not needle:
        return False
    return (
        needle == cat_slug
        or needle == label.casefold()
        or needle == (raw_title or "").strip().casefold()
        or needle in (raw_title or "").casefold()
    )


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("source")
    parser.add_argument("target", nargs="?")
    parser.add_argument("--markup", type=float, default=3.0, help="retail = supplier cost x markup")
    parser.add_argument("--limit", type=int, default=0, help="cap the number of products")
    parser.add_argument(
        "--category",
        help="convert only this one category (slug, cleaned name, or part of the raw heading). "
             "This is the intended per-site path: one category in, one site's catalogue out.",
    )
    parser.add_argument(
        "--list-categories",
        action="store_true",
        help="print the categories in the pool with their slugs and item counts, then exit",
    )
    args = parser.parse_args()

    groups = json.loads(Path(args.source).read_text(encoding="utf-8"))

    if args.list_categories:
        for index, group in enumerate(groups, 1):
            label = clean_category(group.get("title") or group.get("id") or "")
            if not label:
                continue
            print("%-45s %-45s %d items" % (
                slugify(label, "category-%d" % index),
                label,
                len(group.get("items", [])),
            ))
        return

    if not args.target:
        parser.error("target is required unless --list-categories is given")

    categories = []
    products = []
    seen_slugs = set()
    matched_category = False

    for index, group in enumerate(groups, 1):
        raw_title = group.get("title") or group.get("id") or ""
        label = clean_category(raw_title)
        if not label:
            continue
        cat_slug = slugify(label, "category-%d" % index)
        if args.category and not matches_category(args.category, raw_title, label, cat_slug):
            continue
        matched_category = True
        categories.append({"name": label, "slug": cat_slug})

        for item in group.get("items", []):
            name = (item.get("name") or "").strip()
            if not name:
                continue
            item_id = str(item.get("id") or len(products) + 1)
            slug = slugify(name, "item-%s" % item_id)
            if slug in seen_slugs:
                slug = "%s-%s" % (slug, item_id)
            seen_slugs.add(slug)

            cost = float(item.get("price") or 0)
            weight = (item.get("weight") or "").strip()
            supplier_url = (item.get("url") or "").strip()
            details = []
            if weight:
                details.append("Unit weight: %s" % weight)
            if supplier_url:
                details.append("Supplier listing on file.")

            products.append({
                "name": name,
                "slug": slug,
                "sku": "SRC-%s" % item_id,
                "description": " ".join(details),
                "short_description": details[0] if details else "",
                "regular_price": "%.2f" % round(cost * args.markup, 2),
                "sale_price": "",
                "stock_quantity": 100,
                "stock_status": "instock",
                "categories": [cat_slug],
                "images": [],
                # Carried through from the pool. The importer ignores unknown keys, so these
                # stay available for margin, shipping and supplier work instead of being lost.
                "supplier_cost": "%.2f" % round(cost, 2),
                "weight": weight,
                "supplier_url": supplier_url,
            })

            if args.limit and len(products) >= args.limit:
                break
        if args.limit and len(products) >= args.limit:
            break

    if args.category and not matched_category:
        raise SystemExit(
            "No category in %s matches %r. Run with --list-categories to see what is in the pool."
            % (args.source, args.category)
        )

    used = {slug for p in products for slug in p["categories"]}
    feed = {
        "categories": [c for c in categories if c["slug"] in used],
        "products": products,
    }
    write_json(Path(args.target), feed)
    print("Wrote %d products across %d categories to %s"
          % (len(feed["products"]), len(feed["categories"]), args.target))


if __name__ == "__main__":
    main()
