<?php
/**
 * Plugin Name: ACP Mock Payment Gateway
 * Description: Demo-only gateway. Approves every payment without contacting a processor.
 *
 * This exists so the order flow can be walked end to end before a real processor is
 * connected. It moves the order straight to a paid state. It must never be enabled on
 * a store that takes real money.
 */

if (!defined('ABSPATH')) {
    exit;
}

add_action('plugins_loaded', function () {
    if (!class_exists('WC_Payment_Gateway')) {
        return;
    }

    class ACP_Mock_Gateway extends WC_Payment_Gateway {
        public function __construct() {
            $this->id                 = 'acp_mock';
            $this->method_title       = 'Mock Card (demo only)';
            $this->method_description = 'Approves every payment. Demo use only.';
            $this->title              = 'Credit Card (demo)';
            $this->description        = 'Demo checkout. No card is charged and no processor is contacted.';
            $this->has_fields         = false;
            $this->supports           = array('products');
            $this->enabled            = 'yes';

            $this->init_form_fields();
            $this->init_settings();
        }

        public function init_form_fields() {
            $this->form_fields = array(
                'enabled' => array(
                    'title'   => 'Enable/Disable',
                    'type'    => 'checkbox',
                    'label'   => 'Enable the demo gateway',
                    'default' => 'yes',
                ),
            );
        }

        public function process_payment($order_id) {
            $order = wc_get_order($order_id);
            $order->payment_complete('MOCK-' . $order_id);
            $order->add_order_note('Paid via demo gateway. No real transaction took place.');
            WC()->cart->empty_cart();

            return array(
                'result'   => 'success',
                'redirect' => $this->get_return_url($order),
            );
        }
    }

    add_filter('woocommerce_payment_gateways', function ($gateways) {
        $gateways[] = 'ACP_Mock_Gateway';
        return $gateways;
    });
}, 11);
