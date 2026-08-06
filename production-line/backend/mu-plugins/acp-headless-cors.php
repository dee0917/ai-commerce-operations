<?php
/**
 * Plugin Name: ACP Headless CORS
 * Description: Allows a separately hosted storefront to call the WooCommerce REST and Store APIs.
 */

if (!defined('ABSPATH')) {
    exit;
}

/**
 * Origins permitted to call the API. Set ACP_ALLOWED_ORIGINS in wp-config or the
 * environment as a comma separated list to override the local defaults.
 */
function acp_allowed_origins() {
    $raw = getenv('ACP_ALLOWED_ORIGINS');
    if (!$raw) {
        $raw = 'http://localhost:5173,http://localhost:5174,http://127.0.0.1:5173,http://127.0.0.1:5174';
    }
    return array_filter(array_map('trim', explode(',', $raw)));
}

function acp_send_cors_headers() {
    $origin = isset($_SERVER['HTTP_ORIGIN']) ? $_SERVER['HTTP_ORIGIN'] : '';
    if ($origin && in_array($origin, acp_allowed_origins(), true)) {
        header('Access-Control-Allow-Origin: ' . $origin);
        header('Access-Control-Allow-Credentials: true');
        header('Access-Control-Allow-Headers: Content-Type, Nonce, X-WC-Store-API-Nonce, Authorization');
        header('Access-Control-Allow-Methods: GET, POST, PUT, DELETE, OPTIONS');
        header('Access-Control-Expose-Headers: Nonce, X-WC-Store-API-Nonce, X-WP-Total, X-WP-TotalPages, Link');
        header('Vary: Origin');
    }
}

add_action('rest_api_init', function () {
    remove_filter('rest_pre_serve_request', 'rest_send_cors_headers');
    add_filter('rest_pre_serve_request', function ($value) {
        acp_send_cors_headers();
        return $value;
    });
}, 15);

// Answer preflight before WordPress routes the request.
add_action('init', function () {
    if (isset($_SERVER['REQUEST_METHOD']) && $_SERVER['REQUEST_METHOD'] === 'OPTIONS') {
        acp_send_cors_headers();
        status_header(200);
        exit;
    }
});
