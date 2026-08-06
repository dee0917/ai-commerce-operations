# WooCommerce REST API v3 + Store API 對接規範 v2

> **Phase 5 整合說明**：此文件定義 WooCommerce API 的資料結構和端點。
> Service 層實作規格見 **[service-layer-spec.md](service-layer-spec.md)**。
> 購物車混合模式見 **[cart-hybrid-spec.md](cart-hybrid-spec.md)**。

## 核心原則：API 職責拆分（Split API）

> [!CAUTION]
> **Admin Consumer Key 永遠不進前端 bundle。**
> 前端只知道 WP 網址，所有需要 Admin Key 的操作只在 `scripts/sync-to-wp.mjs` 中執行。

| 用途 | API | 認證方式 |
|------|-----|---------|
| 商品查詢（展示） | `GET /wc/store/v1/products` | 無需認證（公開端點） |
| 分類查詢 | `GET /wc/store/v1/products/categories` | 無需認證 |
| 購物車操作 | `wc/store/v1/cart/*` | Nonce + Session Cookie |
| 結帳（含金流） | `POST wc/store/v1/checkout` | Nonce + Session Cookie |
| **會員登入** | `POST /simple-jwt-login/v1/auth` | Username + Password |
| **新用戶註冊** | `POST /simple-jwt-login/v1/users` | Email + Password |
| **訂單查詢** | `GET /wc/v3/orders?customer=me` | JWT Bearer Token |
| 批量上傳商品 | `POST /wc/v3/products/batch` | Consumer Key（**僅 sync 腳本**） |

> [!CAUTION]
> **更正（實測結果，2026-08-04 於本機 WooCommerce 10.9.4 驗證）**
>
> 本文件先前寫「`GET /wc/v3/products` 無需認證」，**這是錯的**。實測：
>
> | 請求 | 結果 |
> |------|------|
> | `GET /wc/v3/products` 不帶認證 | `401` |
> | `GET /wc/v3/products` 帶 HTTP Basic | `401`（WooCommerce 只在 HTTPS 下接受 Basic） |
> | `GET /wc/store/v1/products` 不帶認證 | `200` |
>
> 結論：
> 1. **前端展示一律走 `wc/store/v1`。** 這是官方設計給公開前端用的端點。
> 2. **`wc/v3` 一律需要認證。** 明文 HTTP 下必須用 OAuth 1.0a one-legged 簽章（HMAC-SHA256），Basic 只在 HTTPS 下有效。因此 `wc/v3` 只能留在後端腳本裡。
> 3. 若前端誤用 `wc/v3`，多數實作會 catch 住 401 然後**靜默退回 mock 資料**。畫面看起來正常，實際上完全沒有連到商店，這是最難發現的一種壞法。

---

## 產品物件（WooProduct Interface）

WooCommerce REST API v3 標準回傳結構：

```typescript
// src/types/index.ts
export interface WooCategory {
  id: number;
  name: string;
  slug: string;
}

export interface WooImage {
  id: number;
  src: string;
  name: string;
  alt: string;
}

export interface WooAttribute {
  id: number;
  name: string;       // e.g. "Color", "Size"
  options: string[];  // e.g. ["Red", "Blue"] or ["S", "M", "L"]
}

export interface WooProduct {
  id: number;
  name: string;
  slug: string;
  permalink: string;
  type: 'simple' | 'variable' | 'grouped';
  status: 'publish' | 'draft';
  description: string;        // HTML rich content
  short_description: string;  // HTML
  sku: string;
  price: string;              // NOTE: WooCommerce 回傳字串，前端顯示時用 parseFloat()
  regular_price: string;
  sale_price: string;         // 空字串表示無折扣
  on_sale: boolean;
  purchasable: boolean;
  stock_quantity: number | null;
  stock_status: 'instock' | 'outofstock' | 'onbackorder';
  manage_stock: boolean;
  categories: WooCategory[];
  images: WooImage[];
  attributes: WooAttribute[];
  related_ids: number[];
  upsell_ids: number[];
}

export interface CartItem {
  product: WooProduct;
  quantity: number;
}

// NOTE: payment_method 的值來自 GET wc/store/v1/checkout 回傳的 payment_methods[].id
// 讓金流插件自動注入，前端不 hardcode 任何金流 ID
export interface CheckoutPayload {
  billing_address: Address;
  shipping_address: Address;
  payment_method: string;
  payment_data?: Record<string, string>;
  customer_note?: string;
}

interface Address {
  first_name: string;
  last_name: string;
  company?: string;
  address_1: string;
  address_2?: string;
  city: string;
  state?: string;
  postcode: string;
  country: string;
  email: string;
  phone: string;
}
```

---

## Store API：購物車與結帳

### Nonce 取得方式

WooCommerce Store API 使用 Nonce 驗證，並透過 Session Cookie 維持購物車狀態：

```typescript
// 方法一（推薦）：從 wc-store-api Nonce endpoint 取得
const getNonce = async (wooUrl: string): Promise<string> => {
  const res = await fetch(`${wooUrl}/wp-json/`);
  const data = await res.json();
  // WP 在 REST API discovery 端點會帶出 nonce（需 WooCommerce Blocks 外掛啟用）
  return data?.['wc-store-api-nonce'] ?? data?.nonce ?? '';
};
```

### 購物車操作端點

```
GET    /wp-json/wc/store/v1/cart              取得目前購物車狀態
POST   /wp-json/wc/store/v1/cart/add-item     加入商品 { id, quantity }
POST   /wp-json/wc/store/v1/cart/update-item  更新數量 { key, quantity }
POST   /wp-json/wc/store/v1/cart/remove-item  移除 { key }
```

### 結帳流程（金流插件自動接入）

```typescript
// Step 1：取得可用金流清單
// ⚠️ 更正：金流清單掛在 cart 回應上，不是 checkout 回應。而且要等購物車有東西才會出現。
//    對空購物車呼叫 GET /checkout 會回錯誤物件，不會回 payment_methods。（實測）
const cart = await fetch('/wp-json/wc/store/v1/cart', {
  credentials: 'include',
  headers: { 'Nonce': nonce }
}).then(r => r.json());

// cart.payment_methods 是「字串陣列」，不是物件陣列。實測回傳例：
// ["your_custom_gateway", "cod"]
const paymentMethod = cart.payment_methods[0];

// Step 2：使用者選擇金流後送出
const result = await fetch('/wp-json/wc/store/v1/checkout', {
  method: 'POST',
  credentials: 'include',
  headers: { 'Content-Type': 'application/json', 'Nonce': nonce },
  body: JSON.stringify({
    payment_method: paymentMethod,
    billing_address: { ... },
    shipping_address: { ... },
  })
}).then(r => r.json());

// result 包含 order_id、payment_result 等，WP 自動觸發你的金流插件
```

---

## Store API 與 v3 的欄位差異（前端必看）

`WooProduct` 那組欄位描述的是 `wc/v3` 的形狀。前端實際拿到的是 `wc/store/v1`，形狀不同，需要轉換。以下對照表是實際接通後整理的：

| 前端要的 | Store API 給的 | 轉換方式 |
|---------|---------------|---------|
| `price` `regular_price` `sale_price` | `prices.price` 等，**單位是「分」的字串** | 除以 `10 ** prices.currency_minor_unit`。直接顯示會變成 100 倍 |
| `purchasable` | `is_purchasable` | 改名 |
| `stock_status` | `is_in_stock`（布林） | `true` 轉 `instock`，`false` 轉 `outofstock` |
| `stock_quantity` | 沒有，只有 `low_stock_remaining` | 前端拿不到精確庫存數，庫存數只有後台看得到 |
| `name` `alt` | 帶 HTML 實體，例如 `&#8220;` | 要先解碼，否則商品名稱會出現亂碼 |
| `attributes` `related_ids` | 形狀不同 | 展示用不到就給空陣列 |

另外 Store API 的購物車與結帳要帶兩個標頭：`Nonce` 和 `Cart-Token`，兩者都由伺服器在回應標頭裡給，之後每次請求都要帶回去，否則購物車會對不上。

---

## Mock 數據標準

`src/data/mockData.ts` 必須完全符合 `WooProduct` interface：

```typescript
// 必填欄位清單，不得缺少
const requiredFields = [
  'id', 'name', 'slug', 'price', 'regular_price', 'sale_price',
  'on_sale', 'purchasable', 'stock_status', 'categories', 'images'
];

// Mock 資料品質要求
// ✅ 至少 1 個 on_sale: true（展示 Sale Badge）
// ✅ 至少 1 個 stock_status: 'outofstock'（展示 Sold Out Badge）
// ✅ 至少 2 個商品有多張 images（展示 Hover 換圖）

// 🖼️ 圖片策略 (Crucial)
// ✅ 優先使用 `.agent/skills/generate-image/` 生成在地化圖片存於 public/images/
// ✅ 初期可使用 Unsplash URL: https://images.unsplash.com/photo-{ID}?auto=format&fit=crop&w=800&q=80
// ✅ 必須配合 <SafeImage /> 組件使用，防止任何來源失效
```

---

## 批量上傳腳本（`scripts/sync-to-wp.mjs`）

```javascript
// ⚠️ 此腳本為 Node.js ESM，永不被 Vite 打包到前端
// 執行：node scripts/sync-to-wp.mjs

import { mockProducts, mockCategories } from '../src/data/mockData.js';

const WOO_URL = process.env.WOO_URL;
const CK = process.env.WOO_CONSUMER_KEY;
const CS = process.env.WOO_CONSUMER_SECRET;

const auth = 'Basic ' + Buffer.from(`${CK}:${CS}`).toString('base64');
const headers = { 'Authorization': auth, 'Content-Type': 'application/json' };

// Step 1: 批量建立分類
await fetch(`${WOO_URL}/wp-json/wc/v3/products/categories/batch`, {
  method: 'POST', headers,
  body: JSON.stringify({ create: mockCategories }),
});

// Step 2: 批量建立商品
const result = await fetch(`${WOO_URL}/wp-json/wc/v3/products/batch`, {
  method: 'POST', headers,
  body: JSON.stringify({ create: mockProducts }),
}).then(r => r.json());

console.log(`✅ 同步完成：${result.create.length} 個商品已上傳至 WP 後台`);
```

---

## CORS 設定要求（WP 後端必做）

在 WP 的 `functions.php` 或自訂外掛中加入：

```php
// NOTE: 允許前端 Vite dev server 和正式網域訪問 WooCommerce REST API
add_filter('rest_pre_serve_request', function($value) {
    $allowed = ['http://localhost:5174', 'https://your-frontend.com'];
    $origin  = $_SERVER['HTTP_ORIGIN'] ?? '';
    if (in_array($origin, $allowed)) {
        header('Access-Control-Allow-Origin: ' . $origin);
        header('Access-Control-Allow-Credentials: true');
        header('Access-Control-Allow-Headers: Content-Type, Nonce, Authorization');
        header('Access-Control-Allow-Methods: GET, POST, PUT, DELETE, OPTIONS');
    }
    return $value;
});
```

---

## 插件擴展相容性

以下金流或功能插件安裝後，**前端無需任何改動**即可自動對接：

| 插件類型 | 對接點 | 備註 |
|---------|-------|------|
| 自家金流插件 | `wc/store/v1/checkout` → `payment_methods` | 插件只需實作 WooCommerce Payment Gateway 介面即可自動出現 |
| 優惠碼 | `POST /wc/store/v1/cart/apply-coupon` | 前端加入優惠碼輸入框呼叫此端點即可 |
| 紅利點數 | 依插件 Store API extension | 大多數點數插件已支援 Store API |
| 運費計算 | `POST /wc/store/v1/cart/select-shipping-rate` | 結帳填寫地址後自動呼叫 |
