import { mockProducts, mockCategories } from '../data/mockData';
import type { WooProduct, WooCategory, CartItem, CheckoutPayload } from '../types';

const WOO_URL = import.meta.env.VITE_WOO_URL;

const getNonce = async (): Promise<string> => {
    const res = await fetch(`${WOO_URL}/wp-json/`);
    const data = await res.json();
    return data?.nonce ?? '';
};

export const fetchProducts = async (params?: {
    category?: string;
    per_page?: number;
}): Promise<WooProduct[]> => {
    if (!WOO_URL) {
        console.log('[API] Mock mode: returning mockProducts', mockProducts.length);
        return mockProducts;
    }
    try {
        const query = new URLSearchParams({
            status: 'publish',
            per_page: String(params?.per_page ?? 16),
            ...(params?.category ? { category: params.category } : {}),
        });
        const res = await fetch(`${WOO_URL}/wp-json/wc/v3/products?${query}`);
        if (!res.ok) throw new Error('Products fetch failed');
        return await res.json();
    } catch (err) {
        console.warn('[API] Products fallback to mock:', err);
        return mockProducts;
    }
};

export const fetchProduct = async (slug: string): Promise<WooProduct | null> => {
    if (!WOO_URL) return mockProducts.find(p => p.slug === slug) ?? null;
    try {
        const res = await fetch(`${WOO_URL}/wp-json/wc/v3/products?slug=${slug}`);
        const data = await res.json();
        return data[0] ?? null;
    } catch {
        return mockProducts.find(p => p.slug === slug) ?? null;
    }
};

export const fetchCategories = async (): Promise<WooCategory[]> => {
    if (!WOO_URL) return mockCategories;
    try {
        const res = await fetch(`${WOO_URL}/wp-json/wc/v3/products/categories?hide_empty=true`);
        return await res.json();
    } catch {
        return mockCategories;
    }
};

export const storeAddToCart = async (productId: number, quantity: number): Promise<CartItem[]> => {
    if (!WOO_URL) throw new Error('Mock mode: use useCart local state');
    const nonce = await getNonce();
    const res = await fetch(`${WOO_URL}/wp-json/wc/store/v1/cart/add-item`, {
        method: 'POST',
        credentials: 'include',
        headers: { 'Content-Type': 'application/json', 'Nonce': nonce },
        body: JSON.stringify({ id: productId, quantity }),
    });
    if (!res.ok) throw new Error('Add to cart failed');
    const cart = await res.json();
    return cart.items;
};

export const fetchCheckoutData = async () => {
    if (!WOO_URL) return null;
    const nonce = await getNonce();
    const res = await fetch(`${WOO_URL}/wp-json/wc/store/v1/checkout`, {
        credentials: 'include',
        headers: { 'Nonce': nonce },
    });
    return res.json();
};

export const submitCheckout = async (payload: CheckoutPayload) => {
    if (!WOO_URL) return { success: true, mock: true };
    const nonce = await getNonce();
    const res = await fetch(`${WOO_URL}/wp-json/wc/store/v1/checkout`, {
        method: 'POST',
        credentials: 'include',
        headers: { 'Content-Type': 'application/json', 'Nonce': nonce },
        body: JSON.stringify(payload),
    });
    return res.json();
};
