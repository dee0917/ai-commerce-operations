<?php
/**
 * Creates a WooCommerce REST API key pair for the admin user and prints it as JSON.
 * Run through WP-CLI:  wp eval-file /acp/bin/create-api-key.php
 *
 * The secret is only recoverable at creation time, so the caller must capture stdout
 * and store it outside the container (see .env.backend).
 */

global $wpdb;

$user = get_user_by('login', 'admin');
if (!$user) {
    fwrite(STDERR, "admin user not found\n");
    exit(1);
}

$description = 'ACP storefront sync';
$table       = $wpdb->prefix . 'woocommerce_api_keys';

// Reuse nothing: a rerun should replace the previous key so the printed secret is valid.
$wpdb->delete($table, array('user_id' => $user->ID, 'description' => $description));

$consumer_key    = 'ck_' . wc_rand_hash();
$consumer_secret = 'cs_' . wc_rand_hash();

$wpdb->insert(
    $table,
    array(
        'user_id'         => $user->ID,
        'description'     => $description,
        'permissions'     => 'read_write',
        'consumer_key'    => wc_api_hash($consumer_key),
        'consumer_secret' => $consumer_secret,
        'truncated_key'   => substr($consumer_key, -7),
    ),
    array('%d', '%s', '%s', '%s', '%s', '%s')
);

if (!$wpdb->insert_id) {
    fwrite(STDERR, "failed to insert api key\n");
    exit(1);
}

echo json_encode(array(
    'consumer_key'    => $consumer_key,
    'consumer_secret' => $consumer_secret,
)) . "\n";
