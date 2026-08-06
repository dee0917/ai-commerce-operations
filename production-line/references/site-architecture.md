# 電商網站架構規範 v4（11 類必備頁面，展開為 15 個路由）

本文件定義自動化建站的「最低頁面完成度」。低於此標準的專案視為失敗，禁止交付。

---

> **口徑說明**：本文的「11」指的是**頁面類型**，不是路由數。
> 實作展開後是 **15 個路由**：登入與註冊各一個、會員中心拆成訂單與個人資料兩個、
> 政策頁展開成 FAQ／運送／退換／隱私四個、分類則併進 `/shop` 的篩選。
> README 與 SKILL.md Phase 2.4 用的是同一組數字。

## 1. 必備頁面清單 (The Core 11)

### 商品展示區 (Discovery)
1.  **Home Page (`/`)**: 品牌門面。包含 Hero, Featured Products, Categories, 及至少兩個創意 Section (如 Brand Story, Testimonials)。
2.  **Shop Page (`/shop`)**: 商品大廳。含側邊/頂部篩選器，支援分類、價格、搜尋。
3.  **Category Page (`/shop/:category`)**: 特定分類流。
4.  **Product Detail Page (`/product/:slug`)**: 核心轉換頁。含 Gallery, Specs, Description, Related Products。

### 購物流程 (Conversion)
5.  **Search Page (`/search`)**: 關鍵字結果展示。提供 Empty State 指引。
6.  **Cart Drawer**: 全局抽屜。
7.  **Checkout Flow (`/checkout`)**: 完整三步驟。
    - Step 1: Shipping Details
    - Step 2: Payment Mock Selection
    - Step 3: Order Success Result

### 會員體系 (Authentication)
8.  **Login/Register (`/account/login`)**: 對稱式表單切換。
9.  **Dashboard/Profile (`/account`)**: 用戶中央，包含最近訂單摘要與資料編輯。

### 品牌信任 (Trust Layers)
10. **Policies Hub**: FAQ, Shipping, Returns, Privacy (合併或獨立分流)。內容必須契合品牌主題且多於 200 字。
11. **About Us (`/about`)**: 品牌歷史、創辦理念。

---

## 2. 佈局骨架組合 (Layout Skeletons)

不要每次都做同樣的樣版。在設計時隨機選取一種骨架：

| 骨架名稱 | 導覽模式 | 商品網格風格 | 核心氛圍 |
|---------|---------|-------------|---------|
| **The Classic** | Top Sticky Navbar | Standard Grid (3-4 cols) | 熟悉的、可靠的 |
| **The Sidebar** | Left Fixed Sidebar | Asymmetric Grid | 時尚的、像藝廊的 |
| **The Floating**| Bottom Floating Pill | Masonry Layout | 前衛的、手機優先 |
| **The FullBleed**| Transparent Overlay | Massive Tiles | 沉浸式的、奢華的 |
| **The Bento** | Minimal Header | Bento-style Cards | 資訊密集的、高科技感 |
| **The Story** | Hide/Reveal Nav | Vertical Story Sections | 品牌驅動的、沉浸式故事 |

---

## 3. 分段生成與截斷處理 (Anti-Truncation)

由於一次生成 15 個路由的程式碼量極大：
1. **建議分段**：先產出 `types` 與 `store`，然後是 `components`，最後才是 `pages`。
2. **多代理策略**：你可以啟動並行代理人來分頭開發「會員頁面群」與「商品頁面群」。
3. **驗證**：每完成一頁，確保其在 `App.tsx` 中的路由已正確掛載。

---

## 4. 路由骨架範例 (App.tsx)

> 這是**範例**不是清單，數量對不上 15 是正常的：底下多寫了兩個選配路由
> （`/shop/:category` 與 `/account/dashboard`），也沒有寫出獨立的 `/cart` 頁。
> 必做的 15 個以 SKILL.md Phase 2.4 的清單為準。

```tsx
<Routes>
  {/* Public */}
  <Route path="/" element={<Home />} />
  <Route path="/shop" element={<Shop />} />
  <Route path="/shop/:category" element={<Shop />} />
  <Route path="/product/:slug" element={<ProductDetail />} />
  <Route path="/search" element={<Search />} />
  
  {/* Auth */}
  <Route path="/account/login" element={<Login />} />
  <Route path="/account/register" element={<Register />} />
  
  {/* Protected */}
  <Route path="/account/*" element={<ProtectedRoute><AccountLayout /></ProtectedRoute>}>
    <Route path="dashboard" element={<Dashboard />} />
    <Route path="profile" element={<Profile />} />
    <Route path="orders" element={<Orders />} />
  </Route>

  {/* Flows */}
  <Route path="/checkout" element={<Checkout />} />

  {/* Info */}
  <Route path="/about" element={<About />} />
  <Route path="/policies/:topic" element={<PolicyPage />} />
</Routes>
```
