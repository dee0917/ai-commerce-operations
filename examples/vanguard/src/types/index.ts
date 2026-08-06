export interface WooCategory {
    id: number;
    name: string;
    slug: string;
}

export interface WooImage {
    id: number;
    src: string;
    alt: string;
    name?: string;
}

export interface WooAttribute {
    id: number;
    name: string;
    options: string[];
}

export interface WooProduct {
    id: number;
    name: string;
    slug: string;
    type: string;
    status: string;
    description: string;
    short_description: string;
    sku: string;
    price: string;
    regular_price: string;
    sale_price: string;
    on_sale: boolean;
    purchasable: boolean;
    stock_quantity: number | null;
    stock_status: 'instock' | 'outofstock' | 'onbackorder';
    categories: WooCategory[];
    images: WooImage[];
    attributes: WooAttribute[];
    related_ids: number[];
}

export interface CartItem {
    id: string; // Internal unique ID for cart items (often product.id + variant)
    product: WooProduct;
    quantity: number;
}

export interface CheckoutPayload {
    billing_address: {
        first_name: string;
        last_name: string;
        address_1: string;
        city: string;
        postcode: string;
        country: string;
        email: string;
        phone: string;
    };
    shipping_address: CheckoutPayload['billing_address'];
    payment_method: string;
    payment_data?: Record<string, string>;
}
