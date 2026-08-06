#!/usr/bin/env python3
"""
generate_wp_package.py — Phase 6 WP 部署包生成腳本

生成完整的 WordPress + WooCommerce 部署包，包含：
- docker-compose.yml
- setup.sh (一鍵安裝)
- wp-cli-setup.sh (WP 設定自動化)
- 必裝外掛 + 隨機外掛池抽取
- CORS functions.php
- DEPLOYMENT.md

Usage: python scripts/generate_wp_package.py <project_path> [--seed <number>]
"""

import os
import sys
import json
import random
from pathlib import Path
from datetime import datetime

# ─── Plugin Pools ──────────────────────────────────────────────────

REQUIRED_PLUGINS = [
    {'slug': 'woocommerce', 'name': 'WooCommerce', 'purpose': 'Core e-commerce'},
    {'slug': 'simple-jwt-login', 'name': 'Simple JWT Login', 'purpose': 'Frontend JWT auth'},
    {'slug': 'woo-gutenberg-products-block', 'name': 'WooCommerce Blocks', 'purpose': 'Store API'},
    {'slug': 'wp-mail-smtp', 'name': 'WP Mail SMTP', 'purpose': 'Transactional emails'},
    {'slug': 'wordfence', 'name': 'Wordfence Security', 'purpose': 'Basic security'},
]

RANDOM_POOLS = {
    'seo': {
        'pick': 1,
        'probability': 1.0,
        'plugins': [
            {'slug': 'wordpress-seo', 'name': 'Yoast SEO'},
            {'slug': 'seo-by-rank-math', 'name': 'Rank Math SEO'},
            {'slug': 'all-in-one-seo-pack', 'name': 'All in One SEO'},
            {'slug': 'the-seo-framework', 'name': 'The SEO Framework'},
            {'slug': 'squirrly-seo', 'name': 'Squirrly SEO'},
        ],
    },
    'cache': {
        'pick': 1,
        'probability': 1.0,
        'plugins': [
            {'slug': 'wp-super-cache', 'name': 'WP Super Cache'},
            {'slug': 'w3-total-cache', 'name': 'W3 Total Cache'},
            {'slug': 'litespeed-cache', 'name': 'LiteSpeed Cache'},
            {'slug': 'wp-fastest-cache', 'name': 'WP Fastest Cache'},
            {'slug': 'autoptimize', 'name': 'Autoptimize'},
            {'slug': 'wp-optimize', 'name': 'WP-Optimize'},
        ],
    },
    'form': {
        'pick': 1,
        'probability': 0.7,
        'plugins': [
            {'slug': 'contact-form-7', 'name': 'Contact Form 7'},
            {'slug': 'wpforms-lite', 'name': 'WPForms Lite'},
            {'slug': 'forminator', 'name': 'Forminator'},
            {'slug': 'ninja-forms', 'name': 'Ninja Forms'},
            {'slug': 'formidable', 'name': 'Formidable Forms'},
        ],
    },
    'social': {
        'pick': 1,
        'probability': 0.5,
        'plugins': [
            {'slug': 'add-to-any', 'name': 'AddToAny Share Buttons'},
            {'slug': 'shareaholic', 'name': 'Shareaholic'},
            {'slug': 'sassy-social-share', 'name': 'Sassy Social Share'},
        ],
    },
    'backup': {
        'pick': 1,
        'probability': 0.6,
        'plugins': [
            {'slug': 'updraftplus', 'name': 'UpdraftPlus'},
            {'slug': 'backwpup', 'name': 'BackWPup'},
            {'slug': 'duplicator', 'name': 'Duplicator'},
        ],
    },
    'image': {
        'pick': 1,
        'probability': 0.7,
        'plugins': [
            {'slug': 'wp-smushit', 'name': 'Smush'},
            {'slug': 'shortpixel-image-optimiser', 'name': 'ShortPixel'},
            {'slug': 'imagify', 'name': 'Imagify'},
            {'slug': 'ewww-image-optimizer', 'name': 'EWWW Image Optimizer'},
        ],
    },
    'multilingual': {
        'pick': 1,
        'probability': 0.3,
        'plugins': [
            {'slug': 'polylang', 'name': 'Polylang'},
            {'slug': 'translatepress-multilingual', 'name': 'TranslatePress'},
            {'slug': 'gtranslate', 'name': 'GTranslate'},
        ],
    },
    'misc': {
        'pick_range': (1, 2),
        'probability': 1.0,
        'plugins': [
            {'slug': 'akismet', 'name': 'Akismet Anti-Spam'},
            {'slug': 'cookie-law-info', 'name': 'CookieYes GDPR'},
            {'slug': 'google-analytics-for-wordpress', 'name': 'MonsterInsights'},
            {'slug': 'google-site-kit', 'name': 'Site Kit by Google'},
            {'slug': 'really-simple-ssl', 'name': 'Really Simple SSL'},
            {'slug': 'redirection', 'name': 'Redirection'},
            {'slug': 'limit-login-attempts-reloaded', 'name': 'Limit Login Attempts'},
            {'slug': 'classic-editor', 'name': 'Classic Editor'},
            {'slug': 'disable-comments', 'name': 'Disable Comments'},
        ],
    },
}


def select_random_plugins(seed: int) -> dict:
    """Select random plugins from pools using seeded randomness."""
    rng = random.Random(seed)
    selected = {}

    for category, pool in RANDOM_POOLS.items():
        if rng.random() > pool['probability']:
            continue

        plugins = pool['plugins']
        if 'pick_range' in pool:
            n = rng.randint(*pool['pick_range'])
        else:
            n = pool['pick']

        chosen = rng.sample(plugins, min(n, len(plugins)))
        selected[category] = chosen

    return selected


def generate_docker_compose(output_dir: Path):
    """Generate docker-compose.yml."""
    content = """version: '3.8'

services:
  wordpress:
    image: wordpress:latest
    restart: unless-stopped
    ports:
      - "8080:80"
    environment:
      WORDPRESS_DB_HOST: db:3306
      WORDPRESS_DB_USER: ${WP_DB_USER:-wordpress}
      WORDPRESS_DB_PASSWORD: ${WP_DB_PASSWORD:-wordpress}
      WORDPRESS_DB_NAME: ${WP_DB_NAME:-wordpress}
    volumes:
      - wordpress_data:/var/www/html
      - ./theme/functions.php:/var/www/html/wp-content/themes/twentytwentyfour/functions-custom.php
    depends_on:
      db:
        condition: service_healthy
    networks:
      - wp-network

  db:
    image: mysql:8.0
    restart: unless-stopped
    environment:
      MYSQL_DATABASE: ${WP_DB_NAME:-wordpress}
      MYSQL_USER: ${WP_DB_USER:-wordpress}
      MYSQL_PASSWORD: ${WP_DB_PASSWORD:-wordpress}
      MYSQL_ROOT_PASSWORD: ${WP_DB_ROOT_PASSWORD:-rootpassword}
    volumes:
      - db_data:/var/lib/mysql
    healthcheck:
      test: ["CMD", "mysqladmin", "ping", "-h", "localhost"]
      interval: 10s
      timeout: 5s
      retries: 5
    networks:
      - wp-network

  phpmyadmin:
    image: phpmyadmin:latest
    restart: unless-stopped
    ports:
      - "8081:80"
    environment:
      PMA_HOST: db
      PMA_USER: ${WP_DB_USER:-wordpress}
      PMA_PASSWORD: ${WP_DB_PASSWORD:-wordpress}
    depends_on:
      - db
    networks:
      - wp-network

volumes:
  wordpress_data:
  db_data:

networks:
  wp-network:
    driver: bridge
"""
    (output_dir / 'docker-compose.yml').write_text(content.strip() + '\n', encoding='utf-8')


def generate_env_wp_example(output_dir: Path):
    """Generate .env.wp.example."""
    content = """# WordPress Database
WP_DB_NAME=wordpress
WP_DB_USER=wordpress
WP_DB_PASSWORD=changeme
WP_DB_ROOT_PASSWORD=changeme

# WordPress Admin
WP_ADMIN_USER=admin
WP_ADMIN_PASSWORD=changeme
WP_ADMIN_EMAIL=admin@example.com

# Site URL (change to your domain in production)
WP_URL=http://localhost:8080
WP_TITLE=My Store

# Frontend URL (for CORS)
FRONTEND_URL=http://localhost:5173

# JWT Secret (for Simple JWT Login) - generate with: openssl rand -hex 32
JWT_SECRET=changeme
"""
    (output_dir / '.env.wp.example').write_text(content.strip() + '\n', encoding='utf-8')


def generate_setup_script(output_dir: Path, required: list, random_selected: dict):
    """Generate setup.sh one-click install script."""
    all_plugins = [p['slug'] for p in required]
    for category, plugins in random_selected.items():
        all_plugins.extend([p['slug'] for p in plugins])

    plugin_installs = '\n'.join([
        f'wp plugin install {slug} --activate --allow-root'
        for slug in all_plugins
    ])

    content = f"""#!/bin/bash
# ═══════════════════════════════════════════
# WordPress + WooCommerce One-Click Setup
# Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
# ═══════════════════════════════════════════

set -e

# Load environment variables
if [ -f .env.wp ]; then
    export $(cat .env.wp | grep -v '^#' | xargs)
fi

echo "=== Step 1: Starting Docker containers ==="
docker-compose up -d

echo "=== Step 2: Waiting for WordPress to be ready ==="
sleep 30

# Wait for WP to respond
until docker-compose exec -T wordpress curl -s http://localhost > /dev/null 2>&1; do
    echo "  Waiting for WordPress..."
    sleep 5
done

echo "=== Step 3: Running WordPress setup ==="
docker-compose exec -T wordpress bash -c '
    # Install WP-CLI
    curl -O https://raw.githubusercontent.com/wp-cli/builds/gh-pages/phar/wp-cli.phar
    chmod +x wp-cli.phar
    mv wp-cli.phar /usr/local/bin/wp

    # Core install
    wp core install \\
        --url="${{WP_URL:-http://localhost:8080}}" \\
        --title="${{WP_TITLE:-My Store}}" \\
        --admin_user="${{WP_ADMIN_USER:-admin}}" \\
        --admin_password="${{WP_ADMIN_PASSWORD:-admin123}}" \\
        --admin_email="${{WP_ADMIN_EMAIL:-admin@example.com}}" \\
        --allow-root

    # Permalink structure (required for REST API)
    wp rewrite structure "/%%postname%%/" --allow-root

    echo "=== Step 4: Installing plugins ==="
    {plugin_installs}

    echo "=== Step 5: Configuring WooCommerce ==="
    wp option update woocommerce_currency "USD" --allow-root
    wp option update woocommerce_default_country "US:CA" --allow-root
    wp option update woocommerce_calc_taxes "no" --allow-root
    wp option update woocommerce_enable_guest_checkout "yes" --allow-root

    echo "=== Step 6: Configuring Simple JWT Login ==="
    wp option update simple_jwt_login_settings \'{{
        "allow_authentication": true,
        "allow_register": true,
        "jwt_login_by": "email",
        "decryption_key": "'${{JWT_SECRET:-changeme}}'",
        "token_ttl": 86400
    }}\' --format=json --allow-root

    echo "=== Step 7: Injecting CORS config ==="
    cat /var/www/html/wp-content/themes/twentytwentyfour/functions-custom.php >> /var/www/html/wp-content/themes/twentytwentyfour/functions.php

    echo ""
    echo "=========================================="
    echo "  Setup Complete!"
    echo "=========================================="
    echo "  WP Admin:    ${{WP_URL:-http://localhost:8080}}/wp-admin"
    echo "  Username:    ${{WP_ADMIN_USER:-admin}}"
    echo "  phpMyAdmin:  http://localhost:8081"
    echo ""
    echo "  Frontend .env:"
    echo "  VITE_WOO_URL=${{WP_URL:-http://localhost:8080}}"
    echo "=========================================="
'
"""
    script_path = output_dir / 'setup.sh'
    script_path.write_text(content.strip() + '\n', encoding='utf-8')


def generate_cors_functions(output_dir: Path):
    """Generate theme/functions.php for CORS."""
    theme_dir = output_dir / 'theme'
    theme_dir.mkdir(exist_ok=True)

    content = """<?php
/**
 * Custom CORS and REST API configuration for headless WooCommerce.
 * Auto-generated by auto-ecommerce-landing skill.
 */

// CORS Headers for headless frontend
add_filter('rest_pre_serve_request', function($value) {
    $allowed_origins = [
        'http://localhost:5173',   // Vite dev server
        'http://localhost:5174',   // Vite dev server (alt port)
        'http://localhost:3000',   // Next.js dev server
    ];

    // Add production frontend URL from wp_options
    $frontend_url = get_option('headless_frontend_url', '');
    if (!empty($frontend_url)) {
        $allowed_origins[] = rtrim($frontend_url, '/');
    }

    $origin = isset($_SERVER['HTTP_ORIGIN']) ? $_SERVER['HTTP_ORIGIN'] : '';

    if (in_array($origin, $allowed_origins)) {
        header('Access-Control-Allow-Origin: ' . $origin);
        header('Access-Control-Allow-Credentials: true');
        header('Access-Control-Allow-Headers: Content-Type, Nonce, Authorization, X-WC-Store-API-Nonce');
        header('Access-Control-Allow-Methods: GET, POST, PUT, DELETE, OPTIONS');
    }

    return $value;
});

// Handle preflight OPTIONS requests
add_action('init', function() {
    if ($_SERVER['REQUEST_METHOD'] === 'OPTIONS') {
        $origin = isset($_SERVER['HTTP_ORIGIN']) ? $_SERVER['HTTP_ORIGIN'] : '';
        header('Access-Control-Allow-Origin: ' . $origin);
        header('Access-Control-Allow-Credentials: true');
        header('Access-Control-Allow-Headers: Content-Type, Nonce, Authorization, X-WC-Store-API-Nonce');
        header('Access-Control-Allow-Methods: GET, POST, PUT, DELETE, OPTIONS');
        header('Access-Control-Max-Age: 86400');
        exit(0);
    }
});

// Expose WooCommerce Store API nonce in REST API index
add_filter('rest_index', function($response) {
    $response->data['wc-store-api-nonce'] = wp_create_nonce('wc_store_api');
    return $response;
});
"""
    (theme_dir / 'functions.php').write_text(content.strip() + '\n', encoding='utf-8')


def generate_deployment_md(output_dir: Path, required: list, random_selected: dict):
    """Generate DEPLOYMENT.md guide."""
    plugin_list = "### Required Plugins\n"
    for p in required:
        plugin_list += f"- **{p['name']}** (`{p['slug']}`) — {p['purpose']}\n"

    plugin_list += "\n### Randomly Selected Plugins\n"
    for category, plugins in random_selected.items():
        for p in plugins:
            plugin_list += f"- **{p['name']}** (`{p['slug']}`) — Category: {category}\n"

    content = f"""# Deployment Guide

> Auto-generated by auto-ecommerce-landing skill
> Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Prerequisites

- PHP 8.0+ hosting (or Docker for local testing)
- MySQL 5.7+ / MariaDB 10.3+
- At least 512MB RAM
- Node.js 18+ (for sync script)

## Option A: Local Testing with Docker

```bash
cd wp-deployment
cp .env.wp.example .env.wp
# Edit .env.wp with your preferred passwords
docker-compose up -d
# Wait 30 seconds for containers to initialize
bash setup.sh
```

After setup completes:
- WordPress Admin: http://localhost:8080/wp-admin
- phpMyAdmin: http://localhost:8081

## Option B: Production Deployment

1. Install WordPress on your hosting provider
2. Upload `theme/functions.php` content to your active theme's functions.php
3. Install required plugins via WP Admin > Plugins > Add New
4. Configure Simple JWT Login:
   - Allow Register: Enabled
   - Allow Login: Enabled
   - Token TTL: 86400
   - JWT Decryption Key: [your secret]
5. Run product sync:
   ```bash
   cd wp-deployment
   cp .env.wp.example .env.wp
   # Fill in WOO_CONSUMER_KEY, WOO_CONSUMER_SECRET, WOO_URL
   node scripts/sync-to-wp.mjs
   ```

## Connect Frontend

In your frontend project's `.env`:
```
VITE_WOO_URL=https://your-wordpress-site.com
```

Restart the dev server and the frontend will automatically switch from Mock mode to Live mode.

## Installed Plugins

{plugin_list}

## Security Checklist

- [ ] Change default admin password
- [ ] Configure Wordfence firewall rules
- [ ] Set CORS to only allow your frontend domain
- [ ] Remove phpMyAdmin in production
- [ ] Enable SSL/HTTPS
- [ ] Set up automated backups
- [ ] Disable XML-RPC if not needed
- [ ] Change WordPress database table prefix

## Troubleshooting

### CORS Errors
Check that your frontend URL is in the `$allowed_origins` array in `functions.php`.

### JWT Authentication Fails
1. Verify Simple JWT Login plugin is activated
2. Check JWT Decryption Key matches in WP and frontend
3. Ensure "Allow Authentication" is enabled

### Store API Returns 404
WooCommerce Blocks plugin must be installed and activated for Store API endpoints.

### Products Not Syncing
1. Check WooCommerce REST API Consumer Key/Secret
2. Ensure key has Read/Write permissions
3. Verify WP permalink structure is not "Plain"
"""
    (output_dir / 'DEPLOYMENT.md').write_text(content.strip() + '\n', encoding='utf-8')


def generate_plugin_configs(output_dir: Path, required: list, random_selected: dict):
    """Generate plugin config JSON files."""
    plugins_dir = output_dir / 'plugins'
    plugins_dir.mkdir(exist_ok=True)

    # Required plugins
    (plugins_dir / 'required.json').write_text(
        json.dumps(required, indent=2, ensure_ascii=False) + '\n',
        encoding='utf-8'
    )

    # Random pool definition + selected
    pool_data = {
        'selected': {},
        'pools': {},
    }
    for category, plugins in random_selected.items():
        pool_data['selected'][category] = plugins

    for category, pool in RANDOM_POOLS.items():
        pool_data['pools'][category] = {
            'probability': pool['probability'],
            'plugins': pool['plugins'],
        }

    (plugins_dir / 'random-pool.json').write_text(
        json.dumps(pool_data, indent=2, ensure_ascii=False) + '\n',
        encoding='utf-8'
    )


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python scripts/generate_wp_package.py <project_path> [--seed <number>]")
        sys.exit(1)

    project_path = Path(sys.argv[1])

    # Parse seed
    seed = int(datetime.now().timestamp())
    if '--seed' in sys.argv:
        idx = sys.argv.index('--seed')
        if idx + 1 < len(sys.argv):
            seed = int(sys.argv[idx + 1])

    output_dir = project_path / 'wp-deployment'
    output_dir.mkdir(parents=True, exist_ok=True)

    print("=" * 60)
    print("  WP Deployment Package Generator - Phase 6")
    print(f"  Output: {output_dir}")
    print(f"  Seed: {seed}")
    print("=" * 60)

    # Select random plugins
    print("\n\U0001f3b2 Selecting random plugins...")
    random_selected = select_random_plugins(seed)

    print(f"  Required: {len(REQUIRED_PLUGINS)} plugins")
    total_random = sum(len(v) for v in random_selected.values())
    print(f"  Random: {total_random} plugins from {len(random_selected)} categories")

    for category, plugins in random_selected.items():
        names = ', '.join(p['name'] for p in plugins)
        print(f"    [{category}] {names}")

    # Generate files
    print("\n\U0001f4c4 Generating deployment files...")

    generate_docker_compose(output_dir)
    print("  \u2705 docker-compose.yml")

    generate_env_wp_example(output_dir)
    print("  \u2705 .env.wp.example")

    generate_setup_script(output_dir, REQUIRED_PLUGINS, random_selected)
    print("  \u2705 setup.sh")

    generate_cors_functions(output_dir)
    print("  \u2705 theme/functions.php")

    generate_plugin_configs(output_dir, REQUIRED_PLUGINS, random_selected)
    print("  \u2705 plugins/required.json")
    print("  \u2705 plugins/random-pool.json")

    generate_deployment_md(output_dir, REQUIRED_PLUGINS, random_selected)
    print("  \u2705 DEPLOYMENT.md")

    print("\n" + "=" * 60)
    print("  \u2705 WP Deployment Package generated!")
    print(f"  Location: {output_dir}")
    print("=" * 60)
