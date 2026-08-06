# Service Layer Specification

> Reference for `auto-ecommerce-landing` skill. All services operate in **Dual Mode**: Mock (no backend, instant demo) and Live (WooCommerce headless).

---

## Table of Contents

1. [Environment & Configuration](#environment--configuration)
2. [src/services/api.ts -- Shared Foundation](#srcservicesapits----shared-foundation)
3. [src/services/product.ts -- ProductService](#srcservicesproductts----productservice)
4. [src/services/cart.ts -- CartService (Hybrid)](#srcservicescartts----cartservice-hybrid)
5. [src/services/auth.ts -- AuthService](#srcservicesauthts----authservice)
6. [src/services/order.ts -- OrderService](#srcservicesorderts----orderservice)
7. [src/services/checkout.ts -- CheckoutService](#srcservicescheckoutts----checkoutservice)
8. [Zustand Store Integration](#zustand-store-integration)
9. [Error Handling Patterns](#error-handling-patterns)

---

## Environment & Configuration

> [!CAUTION]
> **前端不得持有 Consumer Key 與 Secret（實測確認）**
>
> Vite 會把所有 `VITE_` 開頭的變數**編譯進瀏覽器 bundle**。實測：把 `VITE_WOO_URL` 設成某個網址後建置，
> 該網址原封不動出現在 `dist/assets/index-*.js` 裡，任何人按檢視原始碼就看得到。
> 因此若把 `VITE_WC_CONSUMER_KEY` 與 `VITE_WC_CONSUMER_SECRET` 寫進去，等於把商店的
> **讀寫全權金鑰公開發佈**，任何訪客都能改商品、讀訂單、看客戶個資。
>
> 本規格先前確實這樣寫，**已於此版移除**。正確的分工是：
>
> | 用途 | 走哪條 | 認證 |
> |------|--------|------|
> | 商品與分類（公開展示） | `wc/store/v1` | 不需認證 |
> | 購物車與結帳 | `wc/store/v1` | Nonce 加 Cart-Token |
> | 會員自己的訂單 | `wc/v3/orders?customer=me` | JWT Bearer（使用者自己的 token） |
> | 批量上架與改商品 | `wc/v3/products` | Consumer Key，**只在後端腳本，永不進前端** |
>
> 換句話說：前端能拿到的最高權限就是「這個登入者自己的資料」。店主權限的金鑰只存在於伺服器端腳本。

### .env.example

```env
# ============================================
# E-Commerce Service Layer Configuration
# ============================================

# Backend URL. LEAVE EMPTY for mock mode (frontend-only demo).
# Filling it in switches the site to live mode. There is no separate mode flag:
# empty means mock. This matches scripts/inject_services.py and
# scripts/validate_mock_flow.py, which both key off this variable.
#
# NOTE: everything prefixed VITE_ is compiled into the browser bundle and is public.
# Never put a consumer key or secret here. See the CAUTION block below.
VITE_WOO_URL=

# WooCommerce Store API nonce endpoint (Live mode)
VITE_WC_NONCE_ENDPOINT=/wp-json/custom/v1/nonce

# JWT Auth (Live mode)
VITE_JWT_AUTH_URL=/wp-json/jwt-auth/v1

# Feature Flags
VITE_ENABLE_GUEST_CHECKOUT=true
VITE_ENABLE_CART_MERGE=true
```

---

## src/services/api.ts -- Shared Foundation

The shared HTTP layer used by every other service. Handles mode detection, authenticated requests, nonce management, retry logic, and auto-logout on 401.

```typescript
// src/services/api.ts

// --- Mode Detection ---
export function isMockMode(): boolean {
  return !import.meta.env.VITE_WOO_URL;
}

const BASE_URL = import.meta.env.VITE_WOO_URL || '';

// --- Nonce Management ---
let cachedNonce: string | null = null;
let nonceExpiry = 0;

async function fetchNonce(): Promise<string> {
  const now = Date.now();
  if (cachedNonce && now < nonceExpiry) return cachedNonce;

  const endpoint = import.meta.env.VITE_WC_NONCE_ENDPOINT || '/wp-json/custom/v1/nonce';
  const res = await fetch(`${BASE_URL}${endpoint}`, { credentials: 'include' });
  if (!res.ok) throw new Error(`Nonce fetch failed: ${res.status}`);
  const data = await res.json();
  cachedNonce = data.nonce;
  nonceExpiry = now + 10 * 60 * 1000; // 10 min TTL
  return cachedNonce!;
}

export function clearNonce(): void {
  cachedNonce = null;
  nonceExpiry = 0;
}

// --- Auth Token Accessor ---
function getAuthToken(): string | null {
  try {
    const raw = localStorage.getItem('auth_token');
    if (!raw) return null;
    const parsed = JSON.parse(raw);
    if (parsed.expiry && Date.now() > parsed.expiry) {
      localStorage.removeItem('auth_token');
      return null;
    }
    return parsed.token;
  } catch {
    return localStorage.getItem('auth_token');
  }
}

// --- Auto-Logout on 401 ---
function handle401(): never {
  localStorage.removeItem('auth_token');
  localStorage.removeItem('user_profile');
  clearNonce();
  window.dispatchEvent(new CustomEvent('auth:logout'));
  throw new ApiError('Session expired. Please log in again.', 401);
}

// --- Custom Error Class ---
export class ApiError extends Error {
  constructor(
    message: string,
    public status: number,
    public code?: string,
    public data?: unknown
  ) {
    super(message);
    this.name = 'ApiError';
  }
}

// --- Retry with Exponential Backoff (429 / 5xx) ---
async function fetchWithRetry(
  url: string,
  options: RequestInit,
  retries = 3,
  baseDelay = 1000
): Promise<Response> {
  for (let attempt = 0; attempt <= retries; attempt++) {
    const res = await fetch(url, options);

    if (res.status === 429 || (res.status >= 500 && attempt < retries)) {
      const retryAfter = res.headers.get('Retry-After');
      const delay = retryAfter
        ? parseInt(retryAfter, 10) * 1000
        : baseDelay * Math.pow(2, attempt) + Math.random() * 500;
      await new Promise((r) => setTimeout(r, delay));
      continue;
    }

    return res;
  }

  throw new ApiError('Max retries exceeded', 503);
}

// --- WooCommerce REST API Wrapper ---
// Used for: the logged-in member's OWN records only (e.g. /orders?customer=me).
// Auth is the user's JWT Bearer token, never a consumer key.
// Public product/category reads must NOT come through here -- use storeFetchPaged.
export async function wooFetch<T>(
  endpoint: string,
  options: RequestInit & { params?: Record<string, string> } = {}
): Promise<T> {
  if (isMockMode()) {
    throw new Error('wooFetch called in mock mode -- this is a bug');
  }

  const { params, ...fetchOptions } = options;
  const url = new URL(`${BASE_URL}/wp-json/wc/v3${endpoint}`);

  // No consumer key here by design. Without a JWT this call will 401, and that is
  // correct: the browser is not allowed to hold store-owner credentials.

  if (params) {
    Object.entries(params).forEach(([k, v]) => url.searchParams.set(k, v));
  }

  const token = getAuthToken();
  const headers: Record<string, string> = {
    'Content-Type': 'application/json',
    ...(fetchOptions.headers as Record<string, string>),
  };
  if (token) {
    headers['Authorization'] = `Bearer ${token}`;
  }

  const res = await fetchWithRetry(url.toString(), {
    ...fetchOptions,
    headers,
    credentials: 'include',
  });

  if (res.status === 401) handle401();

  if (!res.ok) {
    const body = await res.json().catch(() => ({}));
    throw new ApiError(
      body.message || `WooCommerce API error: ${res.status}`,
      res.status,
      body.code,
      body.data
    );
  }

  return res.json();
}

// --- Store API Cart Token ---
let cartToken: string | null = null;

export function rememberStoreHeaders(res: Response): void {
  const t = res.headers.get('Cart-Token');
  if (t) cartToken = t;
}

// --- Store API paged read (public, no credentials) ---
// Products and categories go through here. Returns the pagination metadata that
// the plain JSON body does not carry.
export async function storeFetchPaged<T>(
  endpoint: string,
  params: Record<string, string> = {}
): Promise<{ data: T[]; total: number; totalPages: number }> {
  const url = new URL(`${BASE_URL}/wp-json/wc/store/v1${endpoint}`);
  Object.entries(params).forEach(([k, v]) => url.searchParams.set(k, v));

  const res = await fetchWithRetry(url.toString(), { credentials: 'include' }, 3, 1000);
  rememberStoreHeaders(res);

  if (!res.ok) {
    const body = await res.json().catch(() => ({}));
    throw new ApiError(body.message || `Store API error: ${res.status}`, res.status);
  }

  return {
    data: (await res.json()) as T[],
    total: parseInt(res.headers.get('X-WP-Total') || '0', 10),
    totalPages: parseInt(res.headers.get('X-WP-TotalPages') || '1', 10),
  };
}

// --- WooCommerce Store API Wrapper ---
// Used for: cart, checkout (nonce auth, session-based)
export async function storeFetch<T>(
  endpoint: string,
  options: RequestInit = {}
): Promise<T> {
  if (isMockMode()) {
    throw new Error('storeFetch called in mock mode -- this is a bug');
  }

  const nonce = await fetchNonce();
  const url = `${BASE_URL}/wp-json/wc/store/v1${endpoint}`;

  const token = getAuthToken();
  const headers: Record<string, string> = {
    'Content-Type': 'application/json',
    'Nonce': nonce,
    // The Store API identifies a guest cart by this token. It comes back in the
    // response headers and must be echoed on every later call, otherwise each
    // request gets a fresh empty cart and checkout fails. (Verified.)
    ...(cartToken ? { 'Cart-Token': cartToken } : {}),
    ...(options.headers as Record<string, string>),
  };
  if (token) {
    headers['Authorization'] = `Bearer ${token}`;
  }

  const res = await fetchWithRetry(url, {
    ...options,
    headers,
    credentials: 'include',
  });

  if (res.status === 401) handle401();

  if (!res.ok) {
    const body = await res.json().catch(() => ({}));
    throw new ApiError(
      body.message || `Store API error: ${res.status}`,
      res.status,
      body.code,
      body.data
    );
  }

  return res.json();
}
```

### Key Behaviors

| Concern | Implementation |
|---|---|
| Mode detection | `isMockMode()` reads `VITE_WOO_URL` at build time; empty means mock |
| Consumer key auth | **不使用。已於此版移除**（舊版曾以 URL query params 附加，理由見本文開頭 CAUTION 區塊）。店主權限金鑰只存在於後端腳本 |
| Nonce | Fetched once, cached 10 min, passed as `Nonce` header on Store API |
| Bearer token | Read from `localStorage`, injected when present |
| 401 handling | Clears all auth state, dispatches `auth:logout` event, throws |
| 429 / 5xx retry | Exponential backoff (1s, 2s, 4s) + jitter, respects `Retry-After` |

---

## src/services/product.ts -- ProductService

```typescript
// src/services/product.ts

import { isMockMode, wooFetch, ApiError } from './api';
import { mockProducts, mockCategories } from '../data/mockData';

// --- Types ---
export interface Product {
  id: number;
  name: string;
  slug: string;
  description: string;
  short_description: string;
  price: string;
  regular_price: string;
  sale_price: string;
  on_sale: boolean;
  featured: boolean;
  images: ProductImage[];
  categories: ProductCategory[];
  attributes: ProductAttribute[];
  variations: number[];
  stock_status: 'instock' | 'outofstock' | 'onbackorder';
  stock_quantity: number | null;
  average_rating: string;
  rating_count: number;
  tags: { id: number; name: string; slug: string }[];
  sku: string;
  weight: string;
  dimensions: { length: string; width: string; height: string };
  meta_data: { key: string; value: string }[];
}

export interface ProductImage {
  id: number;
  src: string;
  alt: string;
}

export interface ProductCategory {
  id: number;
  name: string;
  slug: string;
  parent: number;
  count: number;
  image?: ProductImage;
}

export interface ProductAttribute {
  id: number;
  name: string;
  options: string[];
  visible: boolean;
  variation: boolean;
}

export interface ProductQueryParams {
  page?: number;
  per_page?: number;
  category?: number;
  search?: string;
  orderby?: 'date' | 'price' | 'popularity' | 'rating' | 'title';
  order?: 'asc' | 'desc';
  featured?: boolean;
  on_sale?: boolean;
  min_price?: string;
  max_price?: string;
  tag?: string;
  status?: 'publish' | 'draft' | 'pending';
}

export interface PaginatedResponse<T> {
  data: T[];
  total: number;
  totalPages: number;
  page: number;
  perPage: number;
}

// --- Store API product shape and mapping ---
// The Store API does not return the same fields as wc/v3. Each of these three
// differences produces a visibly wrong page if skipped, so mapping is not optional.
export interface StoreApiProduct {
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
  images: { id: number; src: string; alt: string }[];
}

// Prices arrive as integer strings in minor units. Rendering them raw shows 100x.
const toMajor = (minor: string, unit: number): string =>
  minor === '' || minor == null ? '' : (Number(minor) / 10 ** unit).toFixed(2);

// Titles arrive HTML-encoded, e.g. &#8220;. Rendering them raw shows the entity.
const decodeEntities = (v: string): string => {
  if (!v || typeof document === 'undefined') return v ?? '';
  const el = document.createElement('textarea');
  el.innerHTML = v;
  return el.value;
};

export function mapStoreProduct(raw: StoreApiProduct): Product {
  const unit = raw.prices?.currency_minor_unit ?? 2;
  const regular = toMajor(raw.prices?.regular_price ?? '', unit);
  const sale = toMajor(raw.prices?.sale_price ?? '', unit);
  const onSale = raw.on_sale && sale !== '' && sale !== regular;

  return {
    id: raw.id,
    name: decodeEntities(raw.name),
    slug: raw.slug,
    sku: raw.sku ?? '',
    description: raw.description ?? '',
    short_description: raw.short_description ?? '',
    price: toMajor(raw.prices?.price ?? '', unit),
    regular_price: regular,
    sale_price: onSale ? sale : '',
    on_sale: onSale,
    purchasable: raw.is_purchasable,
    stock_status: raw.is_in_stock ? 'instock' : 'outofstock',
    stock_quantity: raw.low_stock_remaining ?? null,
    categories: (raw.categories ?? []).map((c) => ({
      id: c.id,
      name: decodeEntities(c.name),
      slug: c.slug,
    })),
    images: (raw.images ?? []).map((i) => ({
      id: i.id,
      src: i.src,
      alt: decodeEntities(i.alt || raw.name),
    })),
    attributes: [],
    related_ids: [],
  } as unknown as Product;
}

// --- ProductService ---
export const ProductService = {
  async getProducts(
    params: ProductQueryParams = {}
  ): Promise<PaginatedResponse<Product>> {
    if (isMockMode()) {
      return mockGetProducts(params);
    }

    const queryParams: Record<string, string> = {};
    if (params.page) queryParams.page = String(params.page);
    if (params.per_page) queryParams.per_page = String(params.per_page);
    if (params.category) queryParams.category = String(params.category);
    if (params.search) queryParams.search = params.search;
    if (params.orderby) queryParams.orderby = params.orderby;
    if (params.order) queryParams.order = params.order;
    if (params.featured !== undefined) queryParams.featured = String(params.featured);
    if (params.on_sale !== undefined) queryParams.on_sale = String(params.on_sale);
    if (params.min_price) queryParams.min_price = params.min_price;
    if (params.max_price) queryParams.max_price = params.max_price;
    if (params.tag) queryParams.tag = params.tag;

    // Public read: Store API, no credentials. See the CAUTION block at the top.
    const { data: raw, total, totalPages } = await storeFetchPaged<StoreApiProduct>(
      '/products',
      queryParams
    );
    const data: Product[] = raw.map(mapStoreProduct);

    return {
      data,
      total,
      totalPages,
      page: params.page || 1,
      perPage: params.per_page || 10,
    };
  },

  async getProduct(idOrSlug: number | string): Promise<Product> {
    if (isMockMode()) {
      const product = mockProducts.find(
        (p) =>
          p.id === idOrSlug ||
          p.slug === idOrSlug ||
          String(p.id) === String(idOrSlug)
      );
      if (!product) throw new ApiError('Product not found', 404);
      return { ...product } as Product;
    }

    if (typeof idOrSlug === 'number' || /^\d+$/.test(String(idOrSlug))) {
      return wooFetch<Product>(`/products/${idOrSlug}`);
    }

    const products = await wooFetch<Product[]>('/products', {
      params: { slug: String(idOrSlug) },
    });
    if (products.length === 0) throw new ApiError('Product not found', 404);
    return products[0];
  },

  async getCategories(): Promise<ProductCategory[]> {
    if (isMockMode()) {
      return [...mockCategories] as ProductCategory[];
    }
    return wooFetch<ProductCategory[]>('/products/categories', {
      params: { per_page: '100', hide_empty: 'true' },
    });
  },

  async getFeaturedProducts(limit = 8): Promise<Product[]> {
    const result = await this.getProducts({
      featured: true,
      per_page: limit,
      page: 1,
    });
    return result.data;
  },
};

// --- Mock Helpers ---
function mockGetProducts(
  params: ProductQueryParams
): PaginatedResponse<Product> {
  let filtered = [...mockProducts] as Product[];

  if (params.category) {
    filtered = filtered.filter((p) =>
      p.categories.some((c) => c.id === params.category)
    );
  }

  if (params.search) {
    const q = params.search.toLowerCase();
    filtered = filtered.filter(
      (p) =>
        p.name.toLowerCase().includes(q) ||
        p.description.toLowerCase().includes(q)
    );
  }

  if (params.featured) {
    filtered = filtered.filter((p) => p.featured);
  }

  if (params.on_sale) {
    filtered = filtered.filter((p) => p.on_sale);
  }

  if (params.min_price) {
    filtered = filtered.filter(
      (p) => parseFloat(p.price) >= parseFloat(params.min_price!)
    );
  }
  if (params.max_price) {
    filtered = filtered.filter(
      (p) => parseFloat(p.price) <= parseFloat(params.max_price!)
    );
  }

  const orderby = params.orderby || 'date';
  const order = params.order || 'desc';
  filtered.sort((a, b) => {
    let cmp = 0;
    switch (orderby) {
      case 'price':
        cmp = parseFloat(a.price) - parseFloat(b.price);
        break;
      case 'title':
        cmp = a.name.localeCompare(b.name);
        break;
      case 'rating':
        cmp = parseFloat(a.average_rating) - parseFloat(b.average_rating);
        break;
      case 'popularity':
        cmp = a.rating_count - b.rating_count;
        break;
      default:
        cmp = a.id - b.id;
    }
    return order === 'asc' ? cmp : -cmp;
  });

  const page = params.page || 1;
  const perPage = params.per_page || 10;
  const start = (page - 1) * perPage;
  const paginated = filtered.slice(start, start + perPage);

  return {
    data: paginated,
    total: filtered.length,
    totalPages: Math.ceil(filtered.length / perPage),
    page,
    perPage,
  };
}
```

---
