#!/usr/bin/env bash
# Brings up the store backend and configures it far enough to take an order.
# Safe to run more than once: every step checks before it acts.
#
#   ./setup.sh
#
# Override the defaults with environment variables if the ports are taken:
#   WP_PORT=8090 ACP_PREFIX=demo ACP_PROJECT=demo-backend ./setup.sh

set -euo pipefail
cd "$(dirname "$0")"

WP_PORT="${WP_PORT:-8088}"
ACP_PREFIX="${ACP_PREFIX:-acp}"
ACP_PROJECT="${ACP_PROJECT:-acp-backend}"
export WP_PORT ACP_PREFIX ACP_PROJECT

WP_URL="http://localhost:${WP_PORT}"
CLI="${ACP_PREFIX}_wpcli"
SITE_TITLE="${SITE_TITLE:-Demo Store}"
ADMIN_USER="${ADMIN_USER:-admin}"
ADMIN_EMAIL="${ADMIN_EMAIL:-admin@example.com}"
ENV_FILE="${ENV_FILE:-.env.backend}"

# A throwaway local password is generated when the caller does not supply one.
if [ -z "${ADMIN_PASSWORD:-}" ]; then
  if [ -f "$ENV_FILE" ] && grep -q '^WP_ADMIN_PASSWORD=' "$ENV_FILE"; then
    ADMIN_PASSWORD="$(grep '^WP_ADMIN_PASSWORD=' "$ENV_FILE" | cut -d= -f2-)"
  else
    ADMIN_PASSWORD="demo-$(head -c 8 /dev/urandom | od -An -tx1 | tr -d ' \n')"
  fi
fi

wp() { MSYS_NO_PATHCONV=1 docker exec "$CLI" wp "$@"; }

echo "==> 1/8 starting containers"
docker compose up -d

echo "==> 2/8 waiting for the web server on ${WP_URL}"
for _ in $(seq 1 60); do
  code="$(curl -s -o /dev/null -w '%{http_code}' "$WP_URL/" || true)"
  [ "$code" != "000" ] && break
  sleep 3
done
[ "$code" = "000" ] && { echo "web server never answered on ${WP_URL}"; exit 1; }

echo "==> 3/8 installing the site"
if wp core is-installed 2>/dev/null; then
  echo "    already installed, skipping"
else
  wp core install --url="$WP_URL" --title="$SITE_TITLE" \
    --admin_user="$ADMIN_USER" --admin_password="$ADMIN_PASSWORD" \
    --admin_email="$ADMIN_EMAIL" --skip-email
fi

# The bundled core is older than the shop plugin requires on some image tags.
wp core update --force >/dev/null 2>&1 || true
wp core update-db >/dev/null 2>&1 || true

echo "==> 4/8 permalinks (the API will not answer without them)"
wp rewrite structure '/%postname%/' >/dev/null

echo "==> 5/8 shop plugin"
if wp plugin is-active woocommerce 2>/dev/null; then
  echo "    already active, skipping"
else
  wp plugin install woocommerce --activate
fi

echo "==> 6/8 store settings"
wp option update woocommerce_currency "${STORE_CURRENCY:-USD}" >/dev/null
wp option update woocommerce_default_country "${STORE_COUNTRY:-SG}" >/dev/null
wp option update woocommerce_calc_taxes "no" >/dev/null
wp option update woocommerce_enable_guest_checkout "yes" >/dev/null
wp option update woocommerce_checkout_phone_field "optional" >/dev/null
wp option update woocommerce_onboarding_profile '{"skipped":true,"completed":true}' --format=json >/dev/null
wp wc --user="$ADMIN_USER" tool run install_pages >/dev/null

# Without a shipping method the checkout refuses physical goods.
if wp wc shipping_zone_method list 0 --user="$ADMIN_USER" --format=count 2>/dev/null | grep -q '^0$'; then
  wp wc shipping_zone_method create 0 --method_id=free_shipping --user="$ADMIN_USER" >/dev/null
  echo "    free shipping added"
else
  echo "    shipping method already present"
fi

echo "==> 7/8 API credentials"
KEYS="$(wp eval-file /acp/bin/create-api-key.php)"
CK="$(echo "$KEYS" | sed -n 's/.*"consumer_key":"\([^"]*\)".*/\1/p')"
CS="$(echo "$KEYS" | sed -n 's/.*"consumer_secret":"\([^"]*\)".*/\1/p')"
[ -z "$CK" ] && { echo "could not create API credentials"; exit 1; }

TMP_ENV="${ENV_FILE}.tmp"
cat > "$TMP_ENV" <<ENVEOF
# Local demo credentials. Regenerate any time by rerunning setup.sh.
# Ignored by version control. Never reuse these on a store that takes real money.
WOO_URL=${WP_URL}
WOO_CONSUMER_KEY=${CK}
WOO_CONSUMER_SECRET=${CS}
WP_ADMIN_USER=${ADMIN_USER}
WP_ADMIN_PASSWORD=${ADMIN_PASSWORD}
ENVEOF
mv "$TMP_ENV" "$ENV_FILE"

echo "==> 8/8 checking the public product endpoint"
STATUS="$(curl -s -o /dev/null -w '%{http_code}' "$WP_URL/wp-json/wc/store/v1/products")"
echo "    store endpoint returned $STATUS"
[ "$STATUS" = "200" ] || { echo "the public product endpoint is not answering"; exit 1; }

cat <<DONEEOF

Backend is up.
  Storefront admin : ${WP_URL}/wp-admin
  User             : ${ADMIN_USER}
  Password         : ${ADMIN_PASSWORD}
  Credentials file : ${ENV_FILE}

Next: load products with
  python bin/import_products.py feeds/<name>.json --assets-root <site>/public --container ${CLI}
DONEEOF
