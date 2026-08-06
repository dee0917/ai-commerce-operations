// 完整對應 WooCommerce REST API v3 結構
export interface WooCategory { id: number; name: string; slug: string; }
export interface WooImage { id: number; src: string; alt: string; name: string; }
export interface WooAttribute { id: number; name: string; options: string[]; }

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
    product: WooProduct;
    quantity: number;
}

export interface CheckoutPayload {
    billing_address: {
        first_name: string; last_name: string;
        address_1: string; city: string;
        postcode: string; country: string;
        email: string; phone: string;
    };
    shipping_address: CheckoutPayload['billing_address'];
    payment_method: string;
    payment_data?: Record<string, string>;
}

// ─── 会员認證相關型別 ────────────────────────────────────────────

/**
 * JWT 登入成功的回傳結構 (Simple JWT Login 外掛格式)
 */
export interface AuthResponse {
    data: {
        jwt: string;
        user?: {
            ID: number;
            display_name: string;
            user_email: string;
        };
    };
    success: boolean;
}

/**
 * 會員用戶資料 (對應 /wp/v2/users/me)
 * NOTE: 只取前端顯示所需欄位，避免傳遞多餘敏感資訊
 */
export interface WpUser {
    id: number;
    name: string;         // display_name
    email: string;        // 需 context=edit 才回傳
    first_name: string;
    last_name: string;
    meta?: {
        billing_phone?: string;
        billing_address_1?: string;
        billing_city?: string;
        billing_postcode?: string;
        billing_country?: string;
    };
}

/**
 * WooCommerce 訂單摘要 (用於訂單清單頁)
 */
export interface WooOrder {
    id: number;
    number: string;       // 顯示用訂單號，如 "1001"
    status: 'pending' | 'processing' | 'on-hold' | 'completed' | 'cancelled' | 'refunded';
    date_created: string; // ISO 8601
    total: string;        // 字串，顯示時 parseFloat()
    currency: string;
    line_items: WooOrderLineItem[];
}

export interface WooOrderLineItem {
    id: number;
    name: string;
    quantity: number;
    total: string;
    image?: { src: string };
}

/**
 * AuthContext 全域狀態
 */
export interface AuthState {
    user: WpUser | null;
    isAuthenticated: boolean;
    isLoading: boolean;
    token: string | null;
}

