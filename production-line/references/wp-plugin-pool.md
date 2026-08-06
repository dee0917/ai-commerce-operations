# WordPress Plugin Pool Reference

> Used by Phase 6 (WordPress Deployment Package) of auto-ecommerce-landing.
> Random plugin selection makes each WP site appear hand-configured by a different person,
> so no two generated sites end up with the same plugin fingerprint.

---

## Required Plugins (Always Installed)

These are installed and activated on every generated site. Non-negotiable.

| Slug | Name | Purpose | Config Notes |
|------|------|---------|--------------|
| `woocommerce` | WooCommerce | Core e-commerce engine | Auto-configure currency, country, weight unit from DNA |
| `simple-jwt-login` | Simple JWT Login | Frontend JWT authentication | Enable register endpoint, set TTL to `86400` (24h), auto-generate secret key per site |
| `woo-gutenberg-products-block` | WooCommerce Blocks | Store API support for headless/block themes | No extra config needed; provides `/wc/store/v1/` REST endpoints |
| `wp-mail-smtp` | WP Mail SMTP | Transactional email delivery | Configure SMTP host/port from env vars; fallback to PHP mail if not set |
| `wordfence` | Wordfence Security | Basic firewall + brute-force protection | Enable rate limiting, disable live traffic view (performance), auto-enable login security |

---

## Random Plugin Pool

Each category has a **pick count** and a **probability** of being included at all.
The selection algorithm (below) handles both.

### SEO (Pick 1, prob 1.0)

Every site gets exactly one SEO plugin.

| Slug | Name | Notes |
|------|------|-------|
| `wordpress-seo` | Yoast SEO | Most popular; generates recognizable meta box in admin |
| `seo-by-rank-math` | Rank Math SEO | Feature-rich free tier; setup wizard auto-configures |
| `all-in-one-seo-pack` | All in One SEO | Legacy favorite; lightweight |
| `the-seo-framework` | The SEO Framework | Minimalist, no upsell ads in admin |
| `squirrly-seo` | Squirrly SEO | AI-assisted; less common = higher uniqueness signal |

### Cache (Pick 1, prob 1.0)

Every site gets exactly one caching plugin.

| Slug | Name | Notes |
|------|------|-------|
| `wp-super-cache` | WP Super Cache | Automattic-maintained; static file caching |
| `w3-total-cache` | W3 Total Cache | Complex config = looks like a power user set it up |
| `litespeed-cache` | LiteSpeed Cache | Best on LiteSpeed servers; skip if not on LS hosting |
| `wp-fastest-cache` | WP Fastest Cache | Simple toggle UI; popular with beginners |
| `autoptimize` | Autoptimize | CSS/JS optimization focus; pairs well with other caches |
| `wp-optimize` | WP-Optimize | Cache + DB cleanup combo |

### Forms (Pick 0-1, prob 0.7)

| Slug | Name | Notes |
|------|------|-------|
| `contact-form-7` | Contact Form 7 | The classic; shortcode-based |
| `wpforms-lite` | WPForms Lite | Drag-and-drop builder; modern UX |
| `forminator` | Forminator | WPMU DEV; includes quizzes/polls |
| `ninja-forms` | Ninja Forms | Extensible; action-based workflow |
| `formidable` | Formidable Forms | Advanced calculations and views |

### Social Sharing (Pick 0-1, prob 0.5)

| Slug | Name | Notes |
|------|------|-------|
| `add-to-any` | AddToAny Share Buttons | Lightweight; universal share menu |
| `shareaholic` | Shareaholic | Related content + sharing combo |
| `sassy-social-share` | Sassy Social Share | Customizable floating/inline buttons |

### Backup (Pick 0-1, prob 0.6)

| Slug | Name | Notes |
|------|------|-------|
| `updraftplus` | UpdraftPlus | Most popular backup plugin; cloud storage support |
| `backwpup` | BackWPUp | Scheduled backups to Dropbox/S3/etc. |
| `duplicator` | Duplicator | Migration + backup; common in agency setups |

### Image Optimization (Pick 0-1, prob 0.7)

| Slug | Name | Notes |
|------|------|-------|
| `wp-smushit` | Smush | Bulk optimize; lazy load built-in |
| `shortpixel-image-optimiser` | ShortPixel | Lossy/glossy/lossless modes; WebP support |
| `imagify` | Imagify | By WP Rocket team; simple UI |
| `ewww-image-optimizer` | EWWW Image Optimizer | Local compression option (no API key needed) |

### Multilingual (Pick 0-1, prob 0.3)

| Slug | Name | Notes |
|------|------|-------|
| `polylang` | Polylang | Per-post translations; lightweight |
| `translatepress-multilingual` | TranslatePress | Visual front-end translation editor |
| `gtranslate` | GTranslate | Google Translate wrapper; zero-effort setup |

### Misc Authenticity (Pick 1-2, prob 1.0)

These add "lived-in" signals -- the kind of plugins a real store owner installs over time.

| Slug | Name | Notes |
|------|------|-------|
| `akismet` | Akismet Anti-Spam | Pre-installed on most WP; leaving it active looks natural |
| `cookie-law-info` | CookieYes | GDPR cookie consent banner |
| `google-analytics-for-wordpress` | MonsterInsights | GA integration; adds tracking code |
| `google-site-kit` | Site Kit by Google | Official Google dashboard in WP admin |
| `really-simple-ssl` | Really Simple SSL | Auto-detects and forces HTTPS |
| `redirection` | Redirection | 301 redirect manager; common in maintained sites |
| `limit-login-attempts-reloaded` | Limit Login Attempts Reloaded | Brute-force protection; complements Wordfence |
| `classic-editor` | Classic Editor | Disables Gutenberg; many store owners prefer it |
| `disable-comments` | Disable Comments | Clean up product pages; looks intentional |

---

## Selection Algorithm

Seeded random ensures reproducibility per site. The seed is derived from the site DNA hash.

```python
import random
import hashlib
import json

# Category definitions
PLUGIN_POOL = {
    "seo": {
        "slugs": [
            "wordpress-seo", "seo-by-rank-math", "all-in-one-seo-pack",
            "the-seo-framework", "squirrly-seo"
        ],
        "pick": (1, 1),
        "prob": 1.0
    },
    "cache": {
        "slugs": [
            "wp-super-cache", "w3-total-cache", "litespeed-cache",
            "wp-fastest-cache", "autoptimize", "wp-optimize"
        ],
        "pick": (1, 1),
        "prob": 1.0
    },
    "forms": {
        "slugs": [
            "contact-form-7", "wpforms-lite", "forminator",
            "ninja-forms", "formidable"
        ],
        "pick": (0, 1),
        "prob": 0.7
    },
    "social": {
        "slugs": ["add-to-any", "shareaholic", "sassy-social-share"],
        "pick": (0, 1),
        "prob": 0.5
    },
    "backup": {
        "slugs": ["updraftplus", "backwpup", "duplicator"],
        "pick": (0, 1),
        "prob": 0.6
    },
    "image_optimization": {
        "slugs": [
            "wp-smushit", "shortpixel-image-optimiser",
            "imagify", "ewww-image-optimizer"
        ],
        "pick": (0, 1),
        "prob": 0.7
    },
    "multilingual": {
        "slugs": ["polylang", "translatepress-multilingual", "gtranslate"],
        "pick": (0, 1),
        "prob": 0.3
    },
    "misc_authenticity": {
        "slugs": [
            "akismet", "cookie-law-info", "google-analytics-for-wordpress",
            "google-site-kit", "really-simple-ssl", "redirection",
            "limit-login-attempts-reloaded", "classic-editor", "disable-comments"
        ],
        "pick": (1, 2),
        "prob": 1.0
    }
}

REQUIRED_PLUGINS = [
    "woocommerce",
    "simple-jwt-login",
    "woo-gutenberg-products-block",
    "wp-mail-smtp",
    "wordfence"
]


def select_plugins(dna_hash: str) -> dict:
    """
    Select plugins for a WP site based on its DNA hash.

    Args:
        dna_hash: SHA-256 hex string from the site design DNA.

    Returns:
        dict with required list, random dict of {category: [slugs]},
        and all combined flat list.
    """
    seed = int(dna_hash[:16], 16)
    rng = random.Random(seed)

    selected = {}

    for category, config in PLUGIN_POOL.items():
        # Roll probability check
        if rng.random() > config["prob"]:
            selected[category] = []
            continue

        min_pick, max_pick = config["pick"]
        count = rng.randint(min_pick, max_pick)

        # If prob passed but min is 0, we still pick at least 1
        # (probability gate already handled the skip case)
        if count == 0:
            count = 1

        picked = rng.sample(config["slugs"], k=min(count, len(config["slugs"])))
        selected[category] = picked

    return {
        "required": REQUIRED_PLUGINS,
        "random": selected,
        "all": REQUIRED_PLUGINS + [s for slugs in selected.values() for s in slugs]
    }


# Example usage:
# dna_hash = hashlib.sha256("luxe-minimalist-2026-04-10".encode()).hexdigest()
# plugins = select_plugins(dna_hash)
# print(json.dumps(plugins, indent=2))
```

---

## wp-cli Installation Commands

Generated from the `all` list returned by `select_plugins()`. Run inside the WP container or via SSH.

```bash
#!/bin/bash
# --- Required Plugins ---
wp plugin install woocommerce --activate --force
wp plugin install simple-jwt-login --activate --force
wp plugin install woo-gutenberg-products-block --activate --force
wp plugin install wp-mail-smtp --activate --force
wp plugin install wordfence --activate --force

# --- Random Plugins (example output) ---
# These lines are dynamically generated per site
wp plugin install wordpress-seo --activate --force
wp plugin install wp-fastest-cache --activate --force
wp plugin install contact-form-7 --activate --force
wp plugin install updraftplus --activate --force
wp plugin install wp-smushit --activate --force
wp plugin install akismet --activate --force
wp plugin install really-simple-ssl --activate --force
```

### Generation Template (Bash)

```bash
generate_wp_plugin_script() {
    local plugins=("$@")
    for slug in "${plugins[@]}"; do
        echo "wp plugin install ${slug} --activate --force"
    done
}

# Usage from Python output:
# generate_wp_plugin_script woocommerce simple-jwt-login ... wordpress-seo wp-fastest-cache ...
```

### Flags Explained

| Flag | Purpose |
|------|---------|
| `--activate` | Activate immediately after install |
| `--force` | Overwrite if already exists (idempotent deploys) |

---

## design-history.json Integration

The selected plugins are recorded in `design-history.json` alongside the site DNA so that:
1. Plugin choices are reproducible (same DNA hash = same plugins).
2. Audits can verify no two consecutive sites share identical plugin sets.
3. Future deploys can diff against history to maximize variation.

### Schema Addition

```jsonc
{
  "site_id": "luxe-minimalist-20260410-a3f7",
  "generated_at": "2026-04-10T14:30:00Z",
  "dna": {
    "aesthetic": "luxe-minimalist",
    "palette": "monochrome-gold",
    "typography": "serif-modern"
  },
  "wordpress": {
    "theme": "flavor-flavor-flavor",
    "plugins": {
      "required": [
        "woocommerce",
        "simple-jwt-login",
        "woo-gutenberg-products-block",
        "wp-mail-smtp",
        "wordfence"
      ],
      "random": {
        "seo": ["seo-by-rank-math"],
        "cache": ["litespeed-cache"],
        "forms": ["wpforms-lite"],
        "social": [],
        "backup": ["duplicator"],
        "image_optimization": ["imagify"],
        "multilingual": [],
        "misc_authenticity": ["cookie-law-info", "classic-editor"]
      },
      "all_slugs": [
        "woocommerce", "simple-jwt-login", "woo-gutenberg-products-block",
        "wp-mail-smtp", "wordfence", "seo-by-rank-math", "litespeed-cache",
        "wpforms-lite", "duplicator", "imagify", "cookie-law-info", "classic-editor"
      ],
      "selection_seed": "a3f7b2c1e9d04568"
    }
  }
}
```

### Uniqueness Check

Before finalizing plugin selection, compare against the last N entries in `design-history.json`:

```python
def ensure_uniqueness(new_plugins: list[str], history: list[dict], lookback: int = 5) -> bool:
    """
    Verify the new plugin set does not exactly match any of the last N sites.
    Returns True if unique, False if a collision is found.
    """
    new_set = set(new_plugins)
    for entry in history[-lookback:]:
        old_set = set(entry.get("wordpress", {}).get("plugins", {}).get("all_slugs", []))
        if new_set == old_set:
            return False
    return True
```

If a collision is detected, increment the seed by 1 and re-run `select_plugins()` until unique.
