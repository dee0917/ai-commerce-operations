# 🔍 SEO & Testing Standards (SEO與測試標準)

為了確保交付的專案具備商業影響力，並防止後續修改引發預期外的錯誤，
本規範將 Vitest 自動化驗證與 Schema.org SEO 實作設定為「不可妥協」的強制流程。

## 1. 交付前自我驗證 (Self-Verification / Vitest)

- **基本配置**：確保 Vite 環境能夠順利建立測試執行緒。在建立好基礎組件與邏輯 (特別是購物車邏輯) 後，**強烈建議**寫入對應的測試檔案 (例如 `.test.ts`)。
- **針對核心模組撰寫基礎 Unit Tests**：
  例如，若你寫了 `useCart.ts`，你必須撰寫 `useCart.test.ts` 以確保「加入購物車」、「清除購物車」、「總結算」等函式能順利運作。
- **防禦性構建 (Defensive Build)**：
  在最終把「預覽連結」交付給使用者前，**【極度強制】** 你必須暗中執行 `npm run build` (或對應測試指令)。
- 若編譯或測試過程有**任何報錯**，你不准直接向使用者展示失敗報告。**必須在後台自動修正**直到 `build` 靜態檢查通過，且沒有任何 Type Errors 後再進行交付。

## 2. 搜尋引擎最佳化 (SEO & Schema.org)

電商網站的命脈在於流量。所有的頁面（無論是首頁、商品列表頁或單一商品詳情頁）必須包含以下基礎建設：

- **動態 Meta Tags**：利用 `react-helmet-async` (或其他你選擇的方式)，根據當前的商場主題與所選的「美學原型品牌名稱」，動態渲染 `<title>` 與 `<meta name="description">`。
- **Schema.org 結構化標記**：
  - 首頁必須置入 `Organization` 或是 `WebSite` 標記。
  - **商品詳情頁**：這是最重要的部分！必須植入符合 Google 規範的 `Product` Schema (包含 JSON-LD 內的 `name`, `image`, `description`, `offers` -> `price`, `priceCurrency` 等欄位)。
  
這樣當這個 mock 專案未來接上真實的 WordPress / WooCommerce API 時，前端已經全部準備好 Google 爬蟲的抓取。
