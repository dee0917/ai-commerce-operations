# Hybrid Cart System — Complete Specification

> Reference for `auto-ecommerce-landing` skill.
> This spec defines the 3-mode cart system used in React+Vite+TypeScript SPAs that connect to a WooCommerce headless backend.

---

## 1. Three Operating Modes

| Condition | Storage | API | Auth Required |
|-----------|---------|-----|---------------|
| **Mock mode** — `VITE_WOO_URL` is not set | localStorage only | None | No |
| **Live mode, guest** — `VITE_WOO_URL` set, user not logged in | localStorage only | None | No |
| **Live mode, authenticated** — `VITE_WOO_URL` set, user logged in | WooCommerce Store API | `/wc/store/v1/cart/*` | Yes (Nonce + cookie) |

Mode detection utility:

```typescript
// src/utils/cartMode.ts
export type CartMode = 'mock' | 'local' | 'remote';

export function getCartMode(isAuthenticated: boolean): CartMode {
  const hasBackend = !!import.meta.env.VITE_WOO_URL;
  if (!hasBackend) return 'mock';
  if (!isAuthenticated) return 'local';
  return 'remote';
}
```

---

## 2. Data Structures

### 2.1 LocalStorage Types

```typescript
// src/types/cart.ts

/** 本地端購物車項目 — 只存最小資料，product 詳情從快取或 API 解析 */
interface LocalCartItem {
  productId: number;
  quantity: number;
  addedAt: string; // ISO 8601 — 用於 merge 衝突解決
}

interface LocalCart {
  items: LocalCartItem[];
  updatedAt: string; // ISO 8601
}
```

### 2.2 WooCommerce Store API Types (Remote)

```typescript
/** WooCommerce Store API 回傳的購物車項目（精簡版，完整型別見 woocommerce-api.md） */
interface RemoteCartItem {
  key: string;          // WC 產生的唯一 cart item key
  id: number;           // product ID
  quantity: number;
  name: string;
  prices: {
    price: string;          // 含稅或不含稅，取決於 WC 設定
    regular_price: string;
    sale_price: string;
    currency_code: string;
    currency_symbol: string;
    currency_minor_unit: number;
    currency_decimal_separator: string;
    currency_thousand_separator: string;
    currency_prefix: string;
    currency_suffix: string;
  };
  images: Array<{
    id: number;
    src: string;
    thumbnail: string;
    srcset: string;
    sizes: string;
    name: string;
    alt: string;
  }>;
  totals: {
    line_subtotal: string;
    line_subtotal_tax: string;
    line_total: string;
    line_total_tax: string;
    currency_code: string;
    currency_minor_unit: number;
  };
}

/** WooCommerce Store API 回傳的完整購物車 */
interface RemoteCart {
  items: RemoteCartItem[];
  coupons: Array<{
    code: string;
    discount_type: string;
    totals: { total_discount: string; currency_code: string; };
  }>;
  totals: {
    total_items: string;
    total_items_tax: string;
    total_shipping: string;
    total_shipping_tax: string;
    total_discount: string;
    total_discount_tax: string;
    total_price: string;
    total_tax: string;
    currency_code: string;
    currency_minor_unit: number;
  };
  shipping_rates: Array<{
    package_id: number;
    name: string;
    destination: Record<string, string>;
    items: Array<{ key: string; quantity: number; }>;
    shipping_rates: Array<{
      rate_id: string;
      name: string;
      price: string;
      currency_code: string;
      selected: boolean;
    }>;
  }>;
  items_count: number;
  items_weight: number;
  needs_payment: boolean;
  needs_shipping: boolean;
}
```

### 2.3 Unified Cart Item (Used by UI Components)

```typescript
/** 所有 UI 元件只認這個型別 — 不直接碰 Local 或 Remote 型別 */
interface CartItem {
  key: string;            // localStorage index (e.g. "local_0") OR WC cart item key
  productId: number;
  quantity: number;
  product: WooProduct;    // 解析後的完整商品資料
  lineTotal: number;      // 已計算的小計（數字，非字串）
}

interface CartTotals {
  subtotal: number;
  shipping: number;
  tax: number;
  discount: number;
  total: number;
}
```

---

## 3. LocalStorage Cart Engine

### 3.1 Storage Rules

| Rule | Value |
|------|-------|
| Storage key | `ecom_cart` |
| Serialization | `JSON.stringify` / `JSON.parse` |
| Max items | 50 |
| Quantity range | 1–99 per item |
| Duplicate handling | Increment quantity (capped at 99) |
| Clear trigger | Explicit `clearCart()` or after successful merge to remote |

### 3.2 Implementation

```typescript
// src/services/localCart.ts

const STORAGE_KEY = 'ecom_cart';
const MAX_ITEMS = 50;
const MAX_QTY = 99;
const MIN_QTY = 1;

function readCart(): LocalCart {
  try {
    const raw = localStorage.getItem(STORAGE_KEY);
    if (!raw) return { items: [], updatedAt: new Date().toISOString() };
    const parsed: LocalCart = JSON.parse(raw);
    // 防禦：過濾非法資料
    parsed.items = parsed.items.filter(
      (i) => i.productId > 0 && i.quantity >= MIN_QTY && i.quantity <= MAX_QTY
    );
    return parsed;
  } catch {
    // localStorage 損毀 → 重置
    localStorage.removeItem(STORAGE_KEY);
    return { items: [], updatedAt: new Date().toISOString() };
  }
}

function writeCart(cart: LocalCart): void {
  cart.updatedAt = new Date().toISOString();
  localStorage.setItem(STORAGE_KEY, JSON.stringify(cart));
}

export function addItem(productId: number, quantity: number = 1): LocalCart {
  const cart = readCart();
  const existing = cart.items.find((i) => i.productId === productId);

  if (existing) {
    existing.quantity = Math.min(existing.quantity + quantity, MAX_QTY);
    existing.addedAt = new Date().toISOString();
  } else {
    if (cart.items.length >= MAX_ITEMS) {
      throw new Error(`Cart full: maximum ${MAX_ITEMS} unique items`);
    }
    cart.items.push({
      productId,
      quantity: Math.min(Math.max(quantity, MIN_QTY), MAX_QTY),
      addedAt: new Date().toISOString(),
    });
  }

  writeCart(cart);
  return cart;
}

export function updateQuantity(productId: number, quantity: number): LocalCart {
  const cart = readCart();
  const item = cart.items.find((i) => i.productId === productId);
  if (!item) throw new Error(`Product ${productId} not in cart`);

  if (quantity <= 0) {
    cart.items = cart.items.filter((i) => i.productId !== productId);
  } else {
    item.quantity = Math.min(quantity, MAX_QTY);
  }

  writeCart(cart);
  return cart;
}

export function removeItem(productId: number): LocalCart {
  const cart = readCart();
  cart.items = cart.items.filter((i) => i.productId !== productId);
  writeCart(cart);
  return cart;
}

export function clearCart(): void {
  localStorage.removeItem(STORAGE_KEY);
}

export function getCart(): LocalCart {
  return readCart();
}

export function getItemCount(): number {
  return readCart().items.reduce((sum, i) => sum + i.quantity, 0);
}
```

---

## 4. WooCommerce Store API Cart Engine

### 4.1 Authentication & Session

All requests require:
- `Nonce` header from the authenticated session (sourced from `api.ts` shared config)
- `credentials: 'include'` to maintain WC session cookies

```typescript
// src/services/remoteCart.ts

import { apiFetch } from './api'; // 共用的 fetch wrapper，自動帶 nonce + credentials

const CART_BASE = '/wc/store/v1/cart';

/**
 * apiFetch 已經處理：
 *   - Base URL: import.meta.env.VITE_WOO_URL
 *   - Headers: { 'Nonce': nonce, 'Content-Type': 'application/json' }
 *   - credentials: 'include'
 *   - Error handling → throws ApiError
 */
```

### 4.2 Endpoints

```typescript
// --- GET 購物車 ---
export async function fetchCart(): Promise<RemoteCart> {
  return apiFetch<RemoteCart>(CART_BASE);
}

// --- 新增商品 ---
export async function addToCart(
  id: number,
  quantity: number = 1
): Promise<RemoteCart> {
  return apiFetch<RemoteCart>(`${CART_BASE}/add-item`, {
    method: 'POST',
    body: JSON.stringify({ id, quantity }),
  });
}

// --- 更新數量 ---
export async function updateCartItem(
  key: string,
  quantity: number
): Promise<RemoteCart> {
  return apiFetch<RemoteCart>(`${CART_BASE}/update-item`, {
    method: 'POST',
    body: JSON.stringify({ key, quantity }),
  });
}

// --- 移除商品 ---
export async function removeCartItem(key: string): Promise<RemoteCart> {
  return apiFetch<RemoteCart>(`${CART_BASE}/remove-item`, {
    method: 'POST',
    body: JSON.stringify({ key }),
  });
}

// --- 套用優惠券 ---
export async function applyCoupon(code: string): Promise<RemoteCart> {
  return apiFetch<RemoteCart>(`${CART_BASE}/apply-coupon`, {
    method: 'POST',
    body: JSON.stringify({ code }),
  });
}

// --- 移除優惠券 ---
export async function removeCoupon(code: string): Promise<RemoteCart> {
  return apiFetch<RemoteCart>(`${CART_BASE}/remove-coupon`, {
    method: 'POST',
    body: JSON.stringify({ code }),
  });
}
```

---

## 5. Merge Logic (Local → Remote on Login)

This is the most critical flow. It runs once when the user transitions from guest to authenticated.

### 5.1 Algorithm

```
1. Read localStorage cart (localItems)
2. Fetch remote WC cart (remoteCart)
3. Build a map: remoteMap = { [productId]: RemoteCartItem }
4. For each localItem:
   a. If localItem.productId exists in remoteMap:
      → newQty = MAX(localItem.quantity, remoteMap[productId].quantity)
      → POST update-item { key: remoteMap[productId].key, quantity: newQty }
   b. If localItem.productId NOT in remoteMap:
      → POST add-item { id: localItem.productId, quantity: localItem.quantity }
   c. If request fails (404 = product gone, 400 = out of stock):
      → Record failure, skip item, notify user
   d. If request fails (network/5xx):
      → Keep item in localStorage for retry next time
5. Remove successfully merged items from localStorage
6. If all items merged → clearCart()
7. Return final remote cart state
```

### 5.2 Implementation

```typescript
// src/services/cartMerge.ts

import * as local from './localCart';
import * as remote from './remoteCart';

interface MergeResult {
  cart: RemoteCart;
  /** 合併失敗的項目（商品下架等，需通知用戶） */
  skipped: Array<{ productId: number; reason: string }>;
  /** 網路錯誤保留在 localStorage 的項目（下次重試） */
  retained: Array<{ productId: number; reason: string }>;
}

export async function mergeLocalToRemote(): Promise<MergeResult> {
  const localCart = local.getCart();
  const skipped: MergeResult['skipped'] = [];
  const retained: MergeResult['retained'] = [];

  if (localCart.items.length === 0) {
    // 本地無商品，直接回傳遠端狀態
    const cart = await remote.fetchCart();
    return { cart, skipped, retained };
  }

  // 取得目前遠端購物車
  let remoteCart = await remote.fetchCart();
  const remoteMap = new Map<number, RemoteCartItem>();
  for (const item of remoteCart.items) {
    remoteMap.set(item.id, item);
  }

  const successfullyMerged: number[] = [];

  // 逐一合併（循序執行，避免 race condition）
  for (const localItem of localCart.items) {
    try {
      const remoteItem = remoteMap.get(localItem.productId);

      if (remoteItem) {
        // 商品已在遠端 → 取較大數量
        const newQty = Math.max(localItem.quantity, remoteItem.quantity);
        if (newQty !== remoteItem.quantity) {
          remoteCart = await remote.updateCartItem(remoteItem.key, newQty);
        }
      } else {
        // 商品不在遠端 → 新增
        remoteCart = await remote.addToCart(localItem.productId, localItem.quantity);
      }

      successfullyMerged.push(localItem.productId);
    } catch (err: unknown) {
      const error = err as { status?: number; message?: string };

      if (error.status === 404 || error.status === 400) {
        // 商品不存在或無庫存 → 跳過，通知用戶
        skipped.push({
          productId: localItem.productId,
          reason: error.message || 'Product unavailable',
        });
        successfullyMerged.push(localItem.productId); // 也要從 local 移除
      } else {
        // 網路/伺服器錯誤 → 保留在 localStorage
        retained.push({
          productId: localItem.productId,
          reason: 'Network error — will retry on next login',
        });
      }
    }
  }

  // 清理 localStorage：只移除成功合併的 + 已跳過的
  if (retained.length === 0) {
    local.clearCart();
  } else {
    // 部分合併：只保留失敗項目
    const retainedIds = new Set(retained.map((r) => r.productId));
    const remainingCart = local.getCart();
    remainingCart.items = remainingCart.items.filter((i) =>
      retainedIds.has(i.productId)
    );
    // 直接寫回（用內部方法重建）
    local.clearCart();
    for (const item of remainingCart.items) {
      local.addItem(item.productId, item.quantity);
    }
  }

  return { cart: remoteCart, skipped, retained };
}
```

### 5.3 Edge Cases

| Edge Case | Handling |
|-----------|----------|
| Product deleted or unpublished | WC returns 404 → skip, notify user via toast |
| Product out of stock | WC returns 400 → skip, notify user |
| Network failure mid-merge | Partial merge OK — unmerged items stay in localStorage |
| User logs out | Remote cart stays on WC server (session cookie), localStorage starts fresh |
| User logs in again | Merge runs again — retained items get another chance |
| Quantity exceeds stock | WC auto-caps to max available, returns updated cart |
| Same product in both local & remote | `MAX(local, remote)` quantity wins |

---

## 6. Zustand Store: `useCartStore`

```typescript
// src/stores/cartStore.ts

import { create } from 'zustand';
import { subscribeWithSelector } from 'zustand/middleware';
import * as localEngine from '../services/localCart';
import * as remoteEngine from '../services/remoteCart';
import { mergeLocalToRemote } from '../services/cartMerge';
import { getCartMode, type CartMode } from '../utils/cartMode';
import { useAuthStore } from './authStore';
import { resolveProducts } from '../services/productResolver';
import type { CartItem, CartTotals } from '../types/cart';

/** Mock 模式的假資料計算 */
const MOCK_SHIPPING = 5.0;
const MOCK_TAX_RATE = 0.05;
const MOCK_COUPON_RATE = 0.1;

interface CartState {
  items: CartItem[];
  isLoading: boolean;
  error: string | null;
  couponCode: string | null;
  couponDiscount: number;
  mode: CartMode;

  // --- Actions ---
  initialize: () => Promise<void>;
  addItem: (productId: number, quantity?: number) => Promise<void>;
  updateQuantity: (key: string, quantity: number) => Promise<void>;
  removeItem: (key: string) => Promise<void>;
  clearCart: () => Promise<void>;
  applyCoupon: (code: string) => Promise<void>;
  removeCoupon: () => Promise<void>;

  // --- Internal ---
  syncFromRemote: () => Promise<void>;
  mergeLocalToRemote: () => Promise<void>;
  _refreshMode: () => void;

  // --- Computed ---
  getItemCount: () => number;
  getTotals: () => CartTotals;
}

export const useCartStore = create<CartState>()(
  subscribeWithSelector((set, get) => ({
    items: [],
    isLoading: false,
    error: null,
    couponCode: null,
    couponDiscount: 0,
    mode: getCartMode(false),

    // ──────────────────────────────────────────────
    // 初始化：根據模式載入購物車
    // ──────────────────────────────────────────────
    initialize: async () => {
      const { mode } = get();
      set({ isLoading: true, error: null });

      try {
        if (mode === 'remote') {
          await get().syncFromRemote();
        } else {
          // mock 或 local：從 localStorage 載入
          const localCart = localEngine.getCart();
          const products = await resolveProducts(
            localCart.items.map((i) => i.productId)
          );

          const items: CartItem[] = localCart.items
            .map((li, index) => {
              const product = products.get(li.productId);
              if (!product) return null;
              const price = parseFloat(product.price || product.regular_price || '0');
              return {
                key: `local_${index}`,
                productId: li.productId,
                quantity: li.quantity,
                product,
                lineTotal: price * li.quantity,
              };
            })
            .filter(Boolean) as CartItem[];

          set({ items, isLoading: false });
        }
      } catch (err) {
        set({ error: (err as Error).message, isLoading: false });
      }
    },

    // ──────────────────────────────────────────────
    // 新增商品
    // ──────────────────────────────────────────────
    addItem: async (productId, quantity = 1) => {
      const { mode } = get();
      set({ isLoading: true, error: null });

      try {
        if (mode === 'remote') {
          await remoteEngine.addToCart(productId, quantity);
          await get().syncFromRemote();
        } else {
          localEngine.addItem(productId, quantity);
          await get().initialize(); // 重新載入
        }
      } catch (err) {
        set({ error: (err as Error).message, isLoading: false });
      }
    },

    // ──────────────────────────────────────────────
    // 更新數量
    // ──────────────────────────────────────────────
    updateQuantity: async (key, quantity) => {
      const { mode, items } = get();
      set({ isLoading: true, error: null });

      try {
        if (mode === 'remote') {
          if (quantity <= 0) {
            await remoteEngine.removeCartItem(key);
          } else {
            await remoteEngine.updateCartItem(key, quantity);
          }
          await get().syncFromRemote();
        } else {
          const item = items.find((i) => i.key === key);
          if (!item) throw new Error('Item not found');
          localEngine.updateQuantity(item.productId, quantity);
          await get().initialize();
        }
      } catch (err) {
        set({ error: (err as Error).message, isLoading: false });
      }
    },

    // ──────────────────────────────────────────────
    // 移除商品
    // ──────────────────────────────────────────────
    removeItem: async (key) => {
      const { mode, items } = get();
      set({ isLoading: true, error: null });

      try {
        if (mode === 'remote') {
          await remoteEngine.removeCartItem(key);
          await get().syncFromRemote();
        } else {
          const item = items.find((i) => i.key === key);
          if (!item) throw new Error('Item not found');
          localEngine.removeItem(item.productId);
          await get().initialize();
        }
      } catch (err) {
        set({ error: (err as Error).message, isLoading: false });
      }
    },

    // ──────────────────────────────────────────────
    // 清空購物車
    // ──────────────────────────────────────────────
    clearCart: async () => {
      const { mode } = get();
      set({ isLoading: true, error: null });

      try {
        if (mode === 'remote') {
          // WC Store API 沒有 clear-cart endpoint，需逐一移除
          const remoteCart = await remoteEngine.fetchCart();
          for (const item of remoteCart.items) {
            await remoteEngine.removeCartItem(item.key);
          }
        }
        localEngine.clearCart();
        set({ items: [], couponCode: null, couponDiscount: 0, isLoading: false });
      } catch (err) {
        set({ error: (err as Error).message, isLoading: false });
      }
    },

    // ──────────────────────────────────────────────
    // 優惠券
    // ──────────────────────────────────────────────
    applyCoupon: async (code) => {
      const { mode } = get();
      set({ isLoading: true, error: null });

      try {
        if (mode === 'remote') {
          await remoteEngine.applyCoupon(code);
          await get().syncFromRemote();
        } else {
          // Mock/Local：固定 10% 折扣
          set({
            couponCode: code,
            couponDiscount: MOCK_COUPON_RATE,
            isLoading: false,
          });
        }
      } catch (err) {
        set({ error: (err as Error).message, isLoading: false });
      }
    },

    removeCoupon: async () => {
      const { mode, couponCode } = get();
      set({ isLoading: true, error: null });

      try {
        if (mode === 'remote' && couponCode) {
          await remoteEngine.removeCoupon(couponCode);
          await get().syncFromRemote();
        } else {
          set({ couponCode: null, couponDiscount: 0, isLoading: false });
        }
      } catch (err) {
        set({ error: (err as Error).message, isLoading: false });
      }
    },

    // ──────────────────────────────────────────────
    // 從遠端同步（Remote mode only）
    // ──────────────────────────────────────────────
    syncFromRemote: async () => {
      const remoteCart = await remoteEngine.fetchCart();
      const productIds = remoteCart.items.map((i) => i.id);
      const products = await resolveProducts(productIds);

      const items: CartItem[] = remoteCart.items
        .map((ri) => {
          const product = products.get(ri.id);
          if (!product) return null;
          const minorUnit = ri.totals.currency_minor_unit || 2;
          return {
            key: ri.key,
            productId: ri.id,
            quantity: ri.quantity,
            product,
            lineTotal: parseInt(ri.totals.line_total, 10) / Math.pow(10, minorUnit),
          };
        })
        .filter(Boolean) as CartItem[];

      const coupon = remoteCart.coupons?.[0] || null;

      set({
        items,
        couponCode: coupon?.code || null,
        isLoading: false,
      });
    },

    // ──────────────────────────────────────────────
    // 合併（登入時觸發）
    // ──────────────────────────────────────────────
    mergeLocalToRemote: async () => {
      set({ isLoading: true, error: null });
      try {
        const result = await mergeLocalToRemote();

        // 通知用戶被跳過的商品
        if (result.skipped.length > 0) {
          const names = result.skipped.map((s) => `Product #${s.productId}`).join(', ');
          console.warn(`[Cart Merge] Skipped: ${names}`);
          // 可接 toast notification
        }

        if (result.retained.length > 0) {
          console.warn(`[Cart Merge] ${result.retained.length} items retained for retry`);
        }

        await get().syncFromRemote();
      } catch (err) {
        set({ error: (err as Error).message, isLoading: false });
      }
    },

    // ──────────────────────────────────────────────
    // 模式切換
    // ──────────────────────────────────────────────
    _refreshMode: () => {
      const isAuth = useAuthStore.getState().isAuthenticated;
      set({ mode: getCartMode(isAuth) });
    },

    // ──────────────────────────────────────────────
    // Computed
    // ──────────────────────────────────────────────
    getItemCount: () => {
      return get().items.reduce((sum, i) => sum + i.quantity, 0);
    },

    getTotals: (): CartTotals => {
      const { items, mode, couponCode, couponDiscount } = get();
      const subtotal = items.reduce((sum, i) => sum + i.lineTotal, 0);

      if (mode === 'mock' || mode === 'local') {
        const discount = couponCode ? subtotal * couponDiscount : 0;
        const afterDiscount = subtotal - discount;
        const tax = afterDiscount * MOCK_TAX_RATE;
        const shipping = items.length > 0 ? MOCK_SHIPPING : 0;
        return {
          subtotal,
          shipping,
          tax: Math.round(tax * 100) / 100,
          discount: Math.round(discount * 100) / 100,
          total: Math.round((afterDiscount + tax + shipping) * 100) / 100,
        };
      }

      // Remote mode: totals 已由 WC 計算，但我們仍可從 items 算 subtotal
      // 精確 total 應在 checkout 時從 WC 取得
      return {
        subtotal,
        shipping: 0,    // 由 WC 在 checkout 計算
        tax: 0,         // 由 WC 在 checkout 計算
        discount: 0,    // 由 WC coupon 處理
        total: subtotal, // 近似值；checkout 頁會用 WC 精確金額
      };
    },
  }))
);
```

### 6.1 Auth State Subscription (Auto-Merge on Login)

```typescript
// src/stores/cartStore.ts (放在 store 定義之後)

/** 監聽登入狀態變化 → 自動觸發 merge */
useAuthStore.subscribe(
  (state) => state.isAuthenticated,
  (isAuthenticated, wasAuthenticated) => {
    const store = useCartStore.getState();
    store._refreshMode();

    if (isAuthenticated && !wasAuthenticated) {
      // 用戶剛登入 → merge localStorage → remote
      store.mergeLocalToRemote();
    }

    if (!isAuthenticated && wasAuthenticated) {
      // 用戶登出 → 重新初始化為 local mode
      store.initialize();
    }
  }
);
```

---

## 7. Product Resolver

Components need full product data, but localStorage only stores IDs. The resolver fetches and caches product details.

```typescript
// src/services/productResolver.ts

import { apiFetch } from './api';
import type { WooProduct } from '../types/woo';

/** 記憶體快取 — SPA 生命週期內有效 */
const cache = new Map<number, WooProduct>();

/**
 * 批次解析商品資料
 * 先查快取，未命中的一次性從 API 拿
 */
export async function resolveProducts(
  ids: number[]
): Promise<Map<number, WooProduct>> {
  const result = new Map<number, WooProduct>();
  const missing: number[] = [];

  for (const id of ids) {
    const cached = cache.get(id);
    if (cached) {
      result.set(id, cached);
    } else {
      missing.push(id);
    }
  }

  if (missing.length > 0) {
    const hasBackend = !!import.meta.env.VITE_WOO_URL;

    if (hasBackend) {
      // WC REST API 支援 include 參數批次查詢
      const products = await apiFetch<WooProduct[]>(
        `/wp-json/wc/v3/products?include=${missing.join(',')}&per_page=${missing.length}`
      );
      for (const p of products) {
        cache.set(p.id, p);
        result.set(p.id, p);
      }
    } else {
      // Mock mode：從 mockProducts 解析
      const { getMockProducts } = await import('../mocks/products');
      const mocks = getMockProducts();
      for (const id of missing) {
        const mock = mocks.find((p) => p.id === id);
        if (mock) {
          cache.set(id, mock);
          result.set(id, mock);
        }
      }
    }
  }

  return result;
}
```

---

## 8. Cart Drawer Component

Slide-in from right, triggered by cart icon in header.

```typescript
// src/components/CartDrawer.tsx

import { useEffect, useRef } from 'react';
import { AnimatePresence, motion } from 'motion/react';
import { X, Minus, Plus, Trash2, ShoppingBag } from 'lucide-react';
import { useCartStore } from '../stores/cartStore';
import { formatPrice } from '../utils/format';

interface CartDrawerProps {
  isOpen: boolean;
  onClose: () => void;
}

export function CartDrawer({ isOpen, onClose }: CartDrawerProps) {
  const { items, isLoading, error, getItemCount, getTotals, updateQuantity, removeItem } =
    useCartStore();
  const backdropRef = useRef<HTMLDivElement>(null);
  const totals = getTotals();
  const itemCount = getItemCount();

  // ESC 關閉
  useEffect(() => {
    const handler = (e: KeyboardEvent) => {
      if (e.key === 'Escape') onClose();
    };
    if (isOpen) document.addEventListener('keydown', handler);
    return () => document.removeEventListener('keydown', handler);
  }, [isOpen, onClose]);

  // 點擊 backdrop 關閉
  const handleBackdropClick = (e: React.MouseEvent) => {
    if (e.target === backdropRef.current) onClose();
  };

  // Free shipping 進度條（可選：設定 threshold）
  const FREE_SHIPPING_THRESHOLD = 100;
  const shippingProgress = Math.min((totals.subtotal / FREE_SHIPPING_THRESHOLD) * 100, 100);
  const needsMore = FREE_SHIPPING_THRESHOLD - totals.subtotal;

  return (
    <AnimatePresence>
      {isOpen && (
        <>
          {/* Backdrop */}
          <motion.div
            ref={backdropRef}
            className="fixed inset-0 z-40 bg-black/50"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            onClick={handleBackdropClick}
          />

          {/* Drawer */}
          <motion.aside
            className="fixed right-0 top-0 z-50 flex h-full w-full max-w-md flex-col bg-white shadow-2xl"
            initial={{ x: '100%' }}
            animate={{ x: 0 }}
            exit={{ x: '100%' }}
            transition={{ type: 'spring', damping: 25, stiffness: 200 }}
          >
            {/* Header */}
            <div className="flex items-center justify-between border-b px-6 py-4">
              <h2 className="text-lg font-semibold">
                Shopping Cart ({itemCount})
              </h2>
              <button
                onClick={onClose}
                className="rounded-full p-2 transition-colors hover:bg-gray-100"
                aria-label="Close cart"
              >
                <X className="h-5 w-5" />
              </button>
            </div>

            {/* Free Shipping Progress */}
            {items.length > 0 && needsMore > 0 && (
              <div className="border-b px-6 py-3">
                <p className="mb-2 text-sm text-gray-600">
                  Add {formatPrice(needsMore)} more for free shipping!
                </p>
                <div className="h-2 w-full overflow-hidden rounded-full bg-gray-200">
                  <motion.div
                    className="h-full rounded-full bg-green-500"
                    initial={{ width: 0 }}
                    animate={{ width: `${shippingProgress}%` }}
                    transition={{ duration: 0.5 }}
                  />
                </div>
              </div>
            )}

            {/* Items */}
            <div className="flex-1 overflow-y-auto px-6 py-4">
              {isLoading && items.length === 0 && (
                <div className="flex h-full items-center justify-center">
                  <div className="h-8 w-8 animate-spin rounded-full border-2 border-gray-300 border-t-black" />
                </div>
              )}

              {!isLoading && items.length === 0 && (
                <div className="flex h-full flex-col items-center justify-center gap-4 text-gray-400">
                  <ShoppingBag className="h-16 w-16" />
                  <p className="text-lg">Your cart is empty</p>
                </div>
              )}

              <ul className="space-y-4">
                {items.map((item) => (
                  <motion.li
                    key={item.key}
                    layout
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    exit={{ opacity: 0, x: 100 }}
                    className="flex gap-4 rounded-lg border p-3"
                  >
                    <img
                      src={item.product.images?.[0]?.src || '/placeholder.jpg'}
                      alt={item.product.name}
                      className="h-20 w-20 rounded-md object-cover"
                    />
                    <div className="flex flex-1 flex-col justify-between">
                      <div>
                        <h3 className="line-clamp-1 font-medium">{item.product.name}</h3>
                        <p className="text-sm text-gray-500">
                          {formatPrice(item.lineTotal / item.quantity)} each
                        </p>
                      </div>
                      <div className="flex items-center justify-between">
                        <div className="flex items-center gap-2 rounded-full border">
                          <button
                            onClick={() => updateQuantity(item.key, item.quantity - 1)}
                            disabled={item.quantity <= 1}
                            className="rounded-full p-1.5 transition-colors hover:bg-gray-100 disabled:opacity-30"
                            aria-label="Decrease quantity"
                          >
                            <Minus className="h-3 w-3" />
                          </button>
                          <span className="w-8 text-center text-sm font-medium">
                            {item.quantity}
                          </span>
                          <button
                            onClick={() => updateQuantity(item.key, item.quantity + 1)}
                            disabled={item.quantity >= 99}
                            className="rounded-full p-1.5 transition-colors hover:bg-gray-100 disabled:opacity-30"
                            aria-label="Increase quantity"
                          >
                            <Plus className="h-3 w-3" />
                          </button>
                        </div>
                        <div className="flex items-center gap-3">
                          <span className="font-semibold">{formatPrice(item.lineTotal)}</span>
                          <button
                            onClick={() => removeItem(item.key)}
                            className="rounded-full p-1.5 text-gray-400 transition-colors hover:bg-red-50 hover:text-red-500"
                            aria-label="Remove item"
                          >
                            <Trash2 className="h-4 w-4" />
                          </button>
                        </div>
                      </div>
                    </div>
                  </motion.li>
                ))}
              </ul>
            </div>

            {/* Footer */}
            {items.length > 0 && (
              <div className="border-t px-6 py-4">
                {error && (
                  <p className="mb-3 rounded-md bg-red-50 p-2 text-sm text-red-600">{error}</p>
                )}
                <div className="mb-4 space-y-1 text-sm">
                  <div className="flex justify-between">
                    <span className="text-gray-600">Subtotal</span>
                    <span>{formatPrice(totals.subtotal)}</span>
                  </div>
                  {totals.discount > 0 && (
                    <div className="flex justify-between text-green-600">
                      <span>Discount</span>
                      <span>-{formatPrice(totals.discount)}</span>
                    </div>
                  )}
                  {totals.shipping > 0 && (
                    <div className="flex justify-between">
                      <span className="text-gray-600">Shipping</span>
                      <span>{formatPrice(totals.shipping)}</span>
                    </div>
                  )}
                  {totals.tax > 0 && (
                    <div className="flex justify-between">
                      <span className="text-gray-600">Tax</span>
                      <span>{formatPrice(totals.tax)}</span>
                    </div>
                  )}
                  <div className="flex justify-between border-t pt-1 text-base font-semibold">
                    <span>Total</span>
                    <span>{formatPrice(totals.total)}</span>
                  </div>
                </div>
                <a
                  href="/cart"
                  className="block w-full rounded-lg bg-black py-3 text-center font-medium text-white transition-colors hover:bg-gray-800"
                >
                  View Cart & Checkout
                </a>
              </div>
            )}
          </motion.aside>
        </>
      )}
    </AnimatePresence>
  );
}
```

---

## 9. Cart Page

Full-page view at `/cart` with quantity editors, coupon input, and order summary.

```typescript
// src/pages/CartPage.tsx

import { useEffect, useState } from 'react';
import { Minus, Plus, Trash2, Tag, ArrowLeft, ShoppingBag } from 'lucide-react';
import { motion, AnimatePresence } from 'motion/react';
import { useCartStore } from '../stores/cartStore';
import { formatPrice } from '../utils/format';

export default function CartPage() {
  const {
    items, isLoading, error, couponCode,
    getItemCount, getTotals, updateQuantity, removeItem,
    applyCoupon, removeCoupon, clearCart, initialize,
  } = useCartStore();

  const [couponInput, setCouponInput] = useState('');
  const [couponError, setCouponError] = useState('');
  const totals = getTotals();

  useEffect(() => { initialize(); }, [initialize]);

  const handleApplyCoupon = async () => {
    if (!couponInput.trim()) return;
    setCouponError('');
    try {
      await applyCoupon(couponInput.trim().toUpperCase());
      setCouponInput('');
    } catch (err) {
      setCouponError((err as Error).message || 'Invalid coupon code');
    }
  };

  if (!isLoading && items.length === 0) {
    return (
      <div className="mx-auto flex min-h-[60vh] max-w-4xl flex-col items-center justify-center px-4 text-center">
        <ShoppingBag className="mb-6 h-24 w-24 text-gray-300" />
        <h1 className="mb-2 text-2xl font-bold">Your cart is empty</h1>
        <p className="mb-8 text-gray-500">Looks like you haven't added anything yet.</p>
        <a href="/shop" className="rounded-lg bg-black px-8 py-3 font-medium text-white transition-colors hover:bg-gray-800">
          Continue Shopping
        </a>
      </div>
    );
  }

  return (
    <div className="mx-auto max-w-6xl px-4 py-8">
      <div className="mb-8 flex items-center justify-between">
        <h1 className="text-2xl font-bold">Shopping Cart ({getItemCount()})</h1>
        <button onClick={() => clearCart()} className="text-sm text-gray-500 transition-colors hover:text-red-500">
          Clear All
        </button>
      </div>

      <div className="grid gap-8 lg:grid-cols-3">
        {/* Cart Items */}
        <div className="lg:col-span-2">
          <div className="mb-4 hidden grid-cols-12 gap-4 border-b pb-2 text-sm font-medium text-gray-500 md:grid">
            <span className="col-span-6">Product</span>
            <span className="col-span-2 text-center">Quantity</span>
            <span className="col-span-2 text-right">Price</span>
            <span className="col-span-2 text-right">Total</span>
          </div>

          <AnimatePresence>
            {items.map((item) => {
              const unitPrice = item.lineTotal / item.quantity;
              return (
                <motion.div
                  key={item.key} layout
                  exit={{ opacity: 0, height: 0, marginBottom: 0 }}
                  transition={{ duration: 0.3 }}
                  className="mb-4 grid grid-cols-12 items-center gap-4 rounded-lg border p-4"
                >
                  <div className="col-span-12 flex gap-4 md:col-span-6">
                    <img src={item.product.images?.[0]?.src || '/placeholder.jpg'} alt={item.product.name} className="h-24 w-24 rounded-md object-cover" />
                    <div className="flex flex-col justify-center">
                      <h3 className="font-medium">{item.product.name}</h3>
                      <p className="text-sm text-gray-500">{formatPrice(unitPrice)}</p>
                      <button onClick={() => removeItem(item.key)} className="mt-1 flex items-center gap-1 text-sm text-red-500 md:hidden">
                        <Trash2 className="h-3 w-3" /> Remove
                      </button>
                    </div>
                  </div>
                  <div className="col-span-4 flex items-center justify-center md:col-span-2">
                    <div className="flex items-center gap-1 rounded-lg border">
                      <button onClick={() => updateQuantity(item.key, item.quantity - 1)} disabled={item.quantity <= 1} className="p-2 transition-colors hover:bg-gray-100 disabled:opacity-30">
                        <Minus className="h-4 w-4" />
                      </button>
                      <input type="number" min={1} max={99} value={item.quantity}
                        onChange={(e) => { const val = parseInt(e.target.value, 10); if (val >= 1 && val <= 99) updateQuantity(item.key, val); }}
                        className="w-12 border-x bg-transparent py-1 text-center text-sm [appearance:textfield] [&::-webkit-inner-spin-button]:appearance-none [&::-webkit-outer-spin-button]:appearance-none"
                      />
                      <button onClick={() => updateQuantity(item.key, item.quantity + 1)} disabled={item.quantity >= 99} className="p-2 transition-colors hover:bg-gray-100 disabled:opacity-30">
                        <Plus className="h-4 w-4" />
                      </button>
                    </div>
                  </div>
                  <div className="col-span-4 text-right md:col-span-2">
                    <span className="text-sm md:text-base">{formatPrice(unitPrice)}</span>
                  </div>
                  <div className="col-span-4 flex items-center justify-end gap-2 md:col-span-2">
                    <span className="font-semibold">{formatPrice(item.lineTotal)}</span>
                    <button onClick={() => removeItem(item.key)} className="hidden rounded-full p-1.5 text-gray-400 transition-colors hover:bg-red-50 hover:text-red-500 md:inline-flex" aria-label="Remove item">
                      <Trash2 className="h-4 w-4" />
                    </button>
                  </div>
                </motion.div>
              );
            })}
          </AnimatePresence>
          <a href="/shop" className="mt-4 inline-flex items-center gap-2 text-sm text-gray-500 transition-colors hover:text-black">
            <ArrowLeft className="h-4 w-4" /> Continue Shopping
          </a>
        </div>

        {/* Order Summary */}
        <div className="lg:col-span-1">
          <div className="rounded-xl border bg-gray-50 p-6">
            <h2 className="mb-4 text-lg font-semibold">Order Summary</h2>
            <div className="mb-4">
              {couponCode ? (
                <div className="flex items-center justify-between rounded-lg bg-green-50 p-3">
                  <div className="flex items-center gap-2 text-sm text-green-700">
                    <Tag className="h-4 w-4" />
                    <span className="font-medium">{couponCode}</span>
                  </div>
                  <button onClick={() => removeCoupon()} className="text-sm text-green-600 hover:text-green-800">Remove</button>
                </div>
              ) : (
                <div>
                  <div className="flex gap-2">
                    <input type="text" value={couponInput} onChange={(e) => setCouponInput(e.target.value)}
                      onKeyDown={(e) => e.key === 'Enter' && handleApplyCoupon()} placeholder="Coupon code"
                      className="flex-1 rounded-lg border px-3 py-2 text-sm focus:border-black focus:outline-none focus:ring-1 focus:ring-black"
                    />
                    <button onClick={handleApplyCoupon} disabled={!couponInput.trim()}
                      className="rounded-lg bg-gray-200 px-4 py-2 text-sm font-medium transition-colors hover:bg-gray-300 disabled:opacity-50">
                      Apply
                    </button>
                  </div>
                  {couponError && <p className="mt-1 text-sm text-red-500">{couponError}</p>}
                </div>
              )}
            </div>
            <div className="space-y-2 border-t pt-4 text-sm">
              <div className="flex justify-between"><span className="text-gray-600">Subtotal</span><span>{formatPrice(totals.subtotal)}</span></div>
              {totals.discount > 0 && <div className="flex justify-between text-green-600"><span>Discount</span><span>-{formatPrice(totals.discount)}</span></div>}
              <div className="flex justify-between"><span className="text-gray-600">Shipping</span><span>{totals.shipping > 0 ? formatPrice(totals.shipping) : items.length > 0 ? 'Calculated at checkout' : '$0.00'}</span></div>
              {totals.tax > 0 && <div className="flex justify-between"><span className="text-gray-600">Estimated Tax</span><span>{formatPrice(totals.tax)}</span></div>}
              <div className="flex justify-between border-t pt-2 text-base font-bold"><span>Total</span><span>{formatPrice(totals.total)}</span></div>
            </div>
            <a href="/checkout" className="mt-6 block w-full rounded-lg bg-black py-3 text-center font-medium text-white transition-colors hover:bg-gray-800">
              Proceed to Checkout
            </a>
            {error && <p className="mt-3 rounded-md bg-red-50 p-2 text-center text-sm text-red-600">{error}</p>}
          </div>
        </div>
      </div>
    </div>
  );
}
```

---

## 10. Mock Mode Defaults

When `VITE_WOO_URL` is not set, the cart runs entirely on localStorage with these simulated values:

| Parameter | Value |
|-----------|-------|
| Coupon discount | 10% off subtotal (any code accepted) |
| Shipping | Flat rate $5.00 |
| Tax | 5% of (subtotal - discount) |
| Free shipping threshold | $100.00 |

This ensures the generated site is fully functional as a standalone demo without any backend.

---

## 11. File Structure

```
src/
├── types/
│   └── cart.ts              # LocalCartItem, LocalCart, RemoteCartItem, RemoteCart, CartItem, CartTotals
├── utils/
│   ├── cartMode.ts          # getCartMode()
│   └── format.ts            # formatPrice()
├── services/
│   ├── api.ts               # apiFetch() — shared fetch wrapper with nonce + credentials
│   ├── localCart.ts          # localStorage CRUD engine
│   ├── remoteCart.ts         # WooCommerce Store API calls
│   ├── cartMerge.ts         # mergeLocalToRemote()
│   └── productResolver.ts   # Batch product lookup with in-memory cache
├── stores/
│   ├── authStore.ts         # useAuthStore (isAuthenticated, login, logout)
│   └── cartStore.ts         # useCartStore (hybrid cart Zustand store)
├── components/
│   └── CartDrawer.tsx       # Slide-in mini cart
├── pages/
│   └── CartPage.tsx         # Full /cart page
└── mocks/
    └── products.ts          # getMockProducts() for mock mode
```

---

## 12. Key Implementation Rules for the Skill

1. **Always generate all three engines** — `localCart.ts`, `remoteCart.ts`, and `cartMerge.ts` — even if the site starts as mock-only. The mode switch is runtime, not build-time.

2. **Never import WooCommerce API directly in components.** Components only talk to `useCartStore`. The store decides which engine to use.

3. **Cart Drawer and Cart Page share the same store.** Never duplicate state.

4. **The merge function is sequential, not parallel.** Each item is merged one-by-one to avoid race conditions with the WC session.

5. **Format prices with `formatPrice()` everywhere.** Never inline `$${num.toFixed(2)}`.

6. **localStorage must be wrapped in try/catch.** Private browsing, storage quota, or corrupt data must not crash the app.

7. **The `key` field in `CartItem` is the bridge between UI and engine.** For local mode it is a synthetic key (`local_0`), for remote mode it is the WC cart item key.

8. **On logout, do NOT clear the remote cart.** The server-side cart persists via session cookies and will be there when the user logs back in.
