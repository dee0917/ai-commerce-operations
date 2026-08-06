import { mockProducts, mockCategories } from '../data/mockData';
import type { WooProduct, WooCategory, CheckoutPayload, CartItem } from '../types';

const WOO_URL = import.meta.env.VITE_WOO_URL;
const STORE = `${WOO_URL}/wp-json/wc/store/v1`;

/**
 * Reads go through the Store API, not /wc/v3. The v3 product routes reject every
 * unauthenticated request, and the only way to authenticate them is a consumer key,
 * which must never reach the browser bundle. Store API is the public read surface and
 * is also what owns the server-side cart.
 */

// The Store API hands back a cart token and a nonce that must be echoed on writes.
let cartToken = '';
let nonce = '';

const captureHeaders = (res: Response) => {
    const token = res.headers.get('Cart-Token');
    const n = res.headers.get('Nonce');
    if (token) cartToken = token;
    if (n) nonce = n;
};

const storeFetch = async (path: string, init: RequestInit = {}) => {
    const headers: Record<string, string> = {
        'Content-Type': 'application/json',
        ...(init.headers as Record<string, string> | undefined),
    };
    if (cartToken) headers['Cart-Token'] = cartToken;
    if (nonce) headers['Nonce'] = nonce;

    const res = await fetch(`${STORE}${path}`, { ...init, headers, credentials: 'include' });
    captureHeaders(res);
    return res;
};

// WordPress returns titles with HTML entities. Components render them as plain text.
const decodeEntities = (value: string): string => {
    if (!value || typeof document === 'undefined') return value ?? '';
    const el = document.createElement('textarea');
    el.innerHTML = value;
    return el.value;
};

const toMajorUnits = (minor: string, minorUnit: number): string => {
    if (minor === '' || minor == null) return '';
    return (Number(minor) / 10 ** minorUnit).toFixed(2);
};

interface StoreApiProduct {
    id: number;
    name: string;
    slug: string;
    sku: string;
    description: string;
    short_description: string;
    on_sale: boolean;
    is_purchasable: boolean;
    is_in_stock: boolean;
    low_stock_remaining: number | null;
    prices: {
        price: string;
        regular_price: string;
        sale_price: string;
        currency_minor_unit: number;
    };
    categories: { id: number; name: string; slug: string }[];
    images: { id: number; src: string; alt: string; name?: string }[];
}

/** Maps a Store API record onto the product shape the UI was built against. */
const mapProduct = (raw: StoreApiProduct): WooProduct => {
    const unit = raw.prices?.currency_minor_unit ?? 2;
    const regular = toMajorUnits(raw.prices?.regular_price ?? '', unit);
    const sale = toMajorUnits(raw.prices?.sale_price ?? '', unit);
    const onSale = raw.on_sale && sale !== '' && sale !== regular;

    return {
        id: raw.id,
        name: decodeEntities(raw.name),
        slug: raw.slug,
        type: 'simple',
        status: 'publish',
        description: raw.description ?? '',
        short_description: raw.short_description ?? '',
        sku: raw.sku ?? '',
        price: toMajorUnits(raw.prices?.price ?? '', unit),
        regular_price: regular,
        sale_price: onSale ? sale : '',
        on_sale: onSale,
        purchasable: raw.is_purchasable,
        stock_quantity: raw.low_stock_remaining ?? null,
        stock_status: raw.is_in_stock ? 'instock' : 'outofstock',
        categories: (raw.categories ?? []).map((c) => ({
            id: c.id,
            name: decodeEntities(c.name),
            slug: c.slug,
        })),
        images: (raw.images ?? []).map((img) => ({
            id: img.id,
            src: img.src,
            alt: decodeEntities(img.alt || raw.name),
        })),
        attributes: [],
        related_ids: [],
    };
};

export const fetchProducts = async (params?: {
    category?: string;
    per_page?: number;
}): Promise<WooProduct[]> => {
    if (!WOO_URL) return mockProducts;
    try {
        const query = new URLSearchParams({
            per_page: String(params?.per_page ?? 16),
            ...(params?.category ? { category: params.category } : {}),
        });
        const res = await storeFetch(`/products?${query}`);
        if (!res.ok) throw new Error(`Products fetch failed: ${res.status}`);
        const data: StoreApiProduct[] = await res.json();
        if (!Array.isArray(data) || data.length === 0) throw new Error('Store returned no products');
        return data.map(mapProduct);
    } catch (err) {
        console.warn('[API] Products fallback to mock:', err);
        return mockProducts;
    }
};

export const fetchProduct = async (slug: string): Promise<WooProduct | null> => {
    if (!WOO_URL) return mockProducts.find((p) => p.slug === slug) ?? null;
    try {
        const res = await storeFetch(`/products?slug=${encodeURIComponent(slug)}`);
        if (!res.ok) throw new Error(`Product fetch failed: ${res.status}`);
        const data: StoreApiProduct[] = await res.json();
        return data[0] ? mapProduct(data[0]) : null;
    } catch (err) {
        console.warn('[API] Product fallback to mock:', err);
        return mockProducts.find((p) => p.slug === slug) ?? null;
    }
};

export const fetchCategories = async (): Promise<WooCategory[]> => {
    if (!WOO_URL) return mockCategories;
    try {
        const res = await storeFetch('/products/categories');
        if (!res.ok) throw new Error(`Categories fetch failed: ${res.status}`);
        const data: { id: number; name: string; slug: string }[] = await res.json();
        if (!Array.isArray(data) || data.length === 0) throw new Error('Store returned no categories');
        return data.map((c) => ({ id: c.id, name: decodeEntities(c.name), slug: c.slug }));
    } catch (err) {
        console.warn('[API] Categories fallback to mock:', err);
        return mockCategories;
    }
};

/**
 * Picks the gateway the store actually offers, so no gateway id is hardcoded here.
 * The list lives on the cart response, not the checkout response, and it is only
 * populated once the cart holds something.
 */
const resolvePaymentMethod = async (): Promise<string> => {
    const res = await storeFetch('/cart');
    if (!res.ok) throw new Error(`Cart read failed: ${res.status}`);
    const data = await res.json();
    const methods: string[] = data?.payment_methods ?? [];
    if (!methods.length) throw new Error('Store has no payment method enabled');
    return methods[0];
};

/**
 * Rebuilds the browser cart on the server, then places the order. The local cart is a
 * client-side store; WooCommerce will only record an order for a cart it owns.
 */
export const submitCheckout = async (payload: CheckoutPayload, items: CartItem[]) => {
    if (!WOO_URL) return { success: true, mock: true };

    // Prime the session so a cart token and nonce exist before any write.
    await storeFetch('/cart');

    const clear = await storeFetch('/cart/items', { method: 'DELETE' });
    if (!clear.ok && clear.status !== 404) {
        console.warn('[API] Could not clear server cart:', clear.status);
    }

    for (const item of items) {
        const res = await storeFetch('/cart/add-item', {
            method: 'POST',
            body: JSON.stringify({ id: item.product.id, quantity: item.quantity }),
        });
        if (!res.ok) {
            const detail = await res.text();
            throw new Error(`Could not add ${item.product.name} to the cart: ${detail}`);
        }
    }

    const paymentMethod = payload.payment_method || (await resolvePaymentMethod());

    const res = await storeFetch('/checkout', {
        method: 'POST',
        body: JSON.stringify({
            billing_address: payload.billing_address,
            shipping_address: payload.shipping_address ?? payload.billing_address,
            payment_method: paymentMethod,
            ...(payload.payment_data ? { payment_data: payload.payment_data } : {}),
        }),
    });

    const body = await res.json();
    if (!res.ok) {
        throw new Error(body?.message ?? `Checkout failed: ${res.status}`);
    }
    return body;
};
