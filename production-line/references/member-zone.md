# 會員專區規範 v1.0 (Member Zone Specification)

> **Phase 5 整合說明**：此文件定義會員認證的 API 規格和頁面規格。
> AuthService 完整實作規格見 **[service-layer-spec.md](service-layer-spec.md)**（Phase 5.4）。
> 登入後購物車合併邏輯見 **[cart-hybrid-spec.md](cart-hybrid-spec.md)**。

本文件定義 `auto-ecommerce` 技能的會員認證系統實作標準。
涵蓋：API 端點、TypeScript 型別、Mock 模式、WP 整合規應與頁面規格。

> [!IMPORTANT]
> **雙模式設計鐵律**：所有會員功能必須在 Mock 模式下完全可運作（無需 WP 後端）。
> 切換至真實後端只需在 `.env` 填入 `VITE_WOO_URL`。

---

## 1. WP 後端前置需求 (Live Mode)

WP 站點須安裝以下免費外掛，**前端程式碼無需更動**：

| 外掛名稱 | 用途 | WordPress.org 連結 |
|:--------|:---|:---|
| **Simple JWT Login** | 提供 JWT 登入、註冊 API | `plugins/simple-jwt-login` |
| **WooCommerce** (已裝) | 提供訂單查詢 API | 內建 |

> **Simple JWT Login 配置要求**：
> - Allow Register: ✅ Enabled
> - JWT Decryption Key: 填入隨機字串（不外洩）
> - Token TTL: 86400（24 小時）
> - Allow Login: ✅ Enabled
> - JWT Payload: 包含 `user_id`, `email`

---

## 2. API 端點清單 (Authentication Endpoints)

### 認證相關

```
POST /wp-json/simple-jwt-login/v1/auth              → 登入，回傳 JWT Token
POST /wp-json/simple-jwt-login/v1/auth/refresh      → 刷新 Token（舊 Token 換新）
POST /wp-json/simple-jwt-login/v1/users             → 新用戶註冊
DELETE /wp-json/simple-jwt-login/v1/auth            → 登出（伺服器端 Token 失效）
```

### 用戶資料相關（Bearer Token 認證）

```
GET  /wp-json/wp/v2/users/me?context=edit           → 取得當前用戶完整資料
PUT  /wp-json/wp/v2/users/me                        → 更新用戶名稱 / 電話
GET  /wp-json/wc/v3/orders?customer=me&per_page=10  → 取得用戶訂單記錄
GET  /wp-json/wc/v3/orders/{id}                     → 取得單筆訂單詳情
```

### CORS 規範補充

WP 的 `functions.php` 必須在現有 CORS 設定中加入 `Authorization` Header 允許：

```php
header('Access-Control-Allow-Headers: Content-Type, Nonce, Authorization');
```

---

## 3. TypeScript 型別定義

以下型別定義統一放入 `src/types/index.ts`：

```typescript
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
```

---

## 4. Mock 資料規範

`src/data/mockData.ts` 補充以下會員 Mock 資料：

```typescript
// NOTE: Mock 模式下用於示範的測試帳號
export const MOCK_USER: WpUser = {
  id: 1,
  name: 'Alex Johnson',
  email: 'demo@example.com',
  first_name: 'Alex',
  last_name: 'Johnson',
  meta: {
    billing_phone: '+886 912 345 678',
    billing_address_1: '123 Design Street',
    billing_city: 'Taipei',
    billing_postcode: '100',
    billing_country: 'TW',
  },
};

export const MOCK_CREDENTIALS = {
  email: 'demo@example.com',
  password: 'demo1234',
};

// NOTE: Mock 訂單資料，展示訂單清單頁各種狀態
export const mockOrders: WooOrder[] = [
  {
    id: 1001,
    number: '1001',
    status: 'completed',
    date_created: '2026-02-15T10:30:00',
    total: '2580.00',
    currency: 'TWD',
    line_items: [/* 取 mockProducts[0..1] */],
  },
  {
    id: 1002,
    number: '1002',
    status: 'processing',
    date_created: '2026-03-01T14:20:00',
    total: '1290.00',
    currency: 'TWD',
    line_items: [/* 取 mockProducts[2] */],
  },
];
```

---

## 5. 核心服務：`src/services/auth.ts`

```typescript
// src/services/auth.ts
// NOTE: 此檔案為認證服務的唯一出口，禁止在 Component 直接 fetch 認證 API

import type { AuthResponse, WpUser, WooOrder } from '../types';
import { MOCK_USER, MOCK_CREDENTIALS, mockOrders } from '../data/mockData';

const WOO_URL = import.meta.env.VITE_WOO_URL;
const TOKEN_KEY = 'auth_token'; // localStorage key

// ─── Token 管理 ──────────────────────────────────────────────────
export const getToken = (): string | null => localStorage.getItem(TOKEN_KEY);
export const setToken = (token: string): void => localStorage.setItem(TOKEN_KEY, token);
export const clearToken = (): void => localStorage.removeItem(TOKEN_KEY);

const authHeaders = () => ({
  'Authorization': `Bearer ${getToken()}`,
  'Content-Type': 'application/json',
});

// ─── 登入 ────────────────────────────────────────────────────────
/**
 * @param email 用戶電子郵件
 * @param password 用戶密碼
 * @returns WpUser 用戶資料
 */
export const login = async (email: string, password: string): Promise<WpUser> => {
  // MOCK MODE
  if (!WOO_URL) {
    if (email === MOCK_CREDENTIALS.email && password === MOCK_CREDENTIALS.password) {
      setToken('mock_jwt_token_for_demo');
      return MOCK_USER;
    }
    throw new Error('Invalid credentials. Use demo@example.com / demo1234');
  }
  // LIVE MODE
  const res = await fetch(`${WOO_URL}/wp-json/simple-jwt-login/v1/auth`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ email, password }),
  });
  if (!res.ok) throw new Error('Login failed');
  const data: AuthResponse = await res.json();
  setToken(data.data.jwt);
  return fetchCurrentUser();
};

// ─── 註冊 ────────────────────────────────────────────────────────
/**
 * @param email 用戶電子郵件
 * @param password 用戶密碼
 * @param firstName 名字
 * @param lastName 姓氏
 * @returns WpUser 已建立的用戶資料
 */
export const register = async (
  email: string, password: string, firstName: string, lastName: string
): Promise<WpUser> => {
  if (!WOO_URL) {
    // MOCK MODE: 模擬成功並自動登入
    setToken('mock_jwt_token_for_demo');
    return { ...MOCK_USER, email, name: `${firstName} ${lastName}`, first_name: firstName, last_name: lastName };
  }
  const res = await fetch(`${WOO_URL}/wp-json/simple-jwt-login/v1/users`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ email, password, first_name: firstName, last_name: lastName }),
  });
  if (!res.ok) throw new Error('Registration failed');
  const data: AuthResponse = await res.json();
  setToken(data.data.jwt);
  return fetchCurrentUser();
};

// ─── 取得當前用戶 ─────────────────────────────────────────────────
export const fetchCurrentUser = async (): Promise<WpUser> => {
  if (!WOO_URL || getToken() === 'mock_jwt_token_for_demo') return MOCK_USER;
  const res = await fetch(`${WOO_URL}/wp-json/wp/v2/users/me?context=edit`, {
    headers: authHeaders(),
  });
  if (!res.ok) { clearToken(); throw new Error('Session expired'); }
  return res.json();
};

// ─── 更新用戶資料 ─────────────────────────────────────────────────
export const updateProfile = async (data: Partial<WpUser>): Promise<WpUser> => {
  if (!WOO_URL) return { ...MOCK_USER, ...data };
  const res = await fetch(`${WOO_URL}/wp-json/wp/v2/users/me`, {
    method: 'PUT',
    headers: authHeaders(),
    body: JSON.stringify(data),
  });
  if (!res.ok) throw new Error('Update failed');
  return res.json();
};

// ─── 取得訂單 ────────────────────────────────────────────────────
export const fetchMyOrders = async (): Promise<WooOrder[]> => {
  if (!WOO_URL) return mockOrders;
  const res = await fetch(`${WOO_URL}/wp-json/wc/v3/orders?customer=me&per_page=10`, {
    headers: authHeaders(),
  });
  if (!res.ok) return [];
  return res.json();
};

// ─── 登出 ────────────────────────────────────────────────────────
export const logout = (): void => clearToken();
```

---

## 6. `useAuth` Hook 規範

```typescript
// src/hooks/useAuth.ts
import React, { createContext, useContext, useState, useEffect } from 'react';
import type { WpUser, AuthState } from '../types';
import { fetchCurrentUser, getToken, login, register, logout as authLogout } from '../services/auth';

const AuthContext = createContext<AuthContextType | null>(null);

interface AuthContextType extends AuthState {
  signIn: (email: string, password: string) => Promise<void>;
  signUp: (email: string, password: string, firstName: string, lastName: string) => Promise<void>;
  signOut: () => void;
}

export const AuthProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [state, setState] = useState<AuthState>({
    user: null, isAuthenticated: false, isLoading: true, token: null
  });

  // NOTE: 頁面刷新時，若 localStorage 有 Token，自動恢復登入狀態
  useEffect(() => {
    const token = getToken();
    if (token) {
      fetchCurrentUser()
        .then(user => setState({ user, isAuthenticated: true, isLoading: false, token }))
        .catch(() => setState(s => ({ ...s, isLoading: false })));
    } else {
      setState(s => ({ ...s, isLoading: false }));
    }
  }, []);

  const signIn = async (email: string, password: string) => {
    const user = await login(email, password);
    setState({ user, isAuthenticated: true, isLoading: false, token: getToken() });
  };

  const signUp = async (email: string, password: string, firstName: string, lastName: string) => {
    const user = await register(email, password, firstName, lastName);
    setState({ user, isAuthenticated: true, isLoading: false, token: getToken() });
  };

  const signOut = () => {
    authLogout();
    setState({ user: null, isAuthenticated: false, isLoading: false, token: null });
  };

  return <AuthContext.Provider value={{ ...state, signIn, signUp, signOut }}>{children}</AuthContext.Provider>;
};

/** @returns 必須在 AuthProvider 內使用 */
export const useAuth = () => {
  const ctx = useContext(AuthContext);
  if (!ctx) throw new Error('useAuth must be used within AuthProvider');
  return ctx;
};
```

---

## 7. `ProtectedRoute` 元件規範

```typescript
// src/components/ProtectedRoute.tsx
// NOTE: 未登入訪問受保護頁面時自動重導至登入頁，並保留 returnUrl
import { Navigate, useLocation } from 'react-router-dom';
import { useAuth } from '../hooks/useAuth';

interface ProtectedRouteProps { children: React.ReactNode; }

const ProtectedRoute: React.FC<ProtectedRouteProps> = ({ children }) => {
  const { isAuthenticated, isLoading } = useAuth();
  const location = useLocation();

  if (isLoading) return <div className="flex items-center justify-center h-screen">Loading...</div>;
  if (!isAuthenticated) return <Navigate to="/account/login" state={{ from: location }} replace />;
  return <>{children}</>;
};

export default ProtectedRoute;
```

---

## 8. 頁面規格

### `/account/login` — 登入頁
- **中心佈局**：品牌 Logo + 表單卡片（陰影、圓角）
- **欄位**：Email + 密碼（眼球 Toggle 顯示/隱藏）
- **行動**：「登入」CTA + 「忘記密碼？」文字連結 + 「還沒帳號？立即加入」連結
- **提示**：Mock 模式下顯示示範帳號 `demo@example.com / demo1234`

### `/account/register` — 註冊頁
- **欄位**：名字 + 姓氏 + Email + 密碼 + 確認密碼
- **驗證**：密碼長度 (≥8)，兩次密碼一致，Email 格式
- **條款**：「我同意《服務條款》及《隱私政策》」CheckBox

### `/account/dashboard` — 會員中心（選配，不算在必做 15 個裡）

> `/account/dashboard` 是範例多寫的**選配路由**，不算在必做的 15 個路由裡。
> Layer B 必做的只有 `/account/login`、`/account/register`、`/account/orders`、`/account/profile` 四個
> （以 SKILL.md Phase 2.4 的清單為準，另見 `site-architecture.md` §4 與 `quality-scorecard.md`）。
> 底下這一節與第 10 節路由範例中的 dashboard 相關內容，做了是加分，沒做不算缺件。

- **歡迎橫幅**：@name 歡迎詞 + 會員頭像 (首字母頭像)
- **快速卡片**：訂單數量 / 地址已設定 / 生日優惠（3 格）
- **近期訂單**：最近 3 筆，快速入口到訂單頁

### `/account/orders` — 訂單記錄
- **狀態 Badge**：`completed`（綠） / `processing`（黃） / `cancelled`（紅） / `pending`（灰）
- **每行顯示**：訂單號 + 日期 + 金額 + 商品縮圖（最多 3 個） + 總計

### `/account/profile` — 個人資料
- **三個 Section**：基本資料 / 聯絡資訊 / 送貨地址
- **UX**：點擊「Edit」進入編輯模式，「Save」觸發 API 更新
- **成功提示**：Toast 通知「Profile updated successfully ✓」

---

## 9. Header 整合

`<Header />` 元件必須整合 `useAuth()`：

```
未登入：顯示 👤 User Icon → 點擊導至 /account/login
已登入：顯示 首字母圓形頭像（品牌色底） → 點擊展開下拉選單
  下拉項目：
  ├─ My Account (→/account/dashboard)
  ├─ Orders (→/account/orders)
  ├─ Profile (→/account/profile)
  └─ Sign Out (執行 signOut())
```

---

## 10. 路由整合（`App.tsx` 補充）

> 底下是**範例**。`dashboard` 是選配路由，不算在必做 15 個裡（見上方 `/account/dashboard` 一節）。
> 若不做 dashboard，`/account` 的預設導向請改成 `orders`。

```tsx
<Route path="/account/login" element={<LoginPage />} />
<Route path="/account/register" element={<RegisterPage />} />
<Route path="/account" element={<ProtectedRoute><AccountLayout /></ProtectedRoute>}>
  <Route index element={<Navigate to="dashboard" />} />   {/* 選配；未做 dashboard 時改導向 "orders" */}
  <Route path="dashboard" element={<DashboardPage />} />  {/* 選配 */}
  <Route path="orders" element={<OrdersPage />} />
  <Route path="profile" element={<ProfilePage />} />
</Route>
```
