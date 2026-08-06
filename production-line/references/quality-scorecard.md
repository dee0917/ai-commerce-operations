# 📊 品質計分卡模板 (Quality Scorecard Template)

> 每次電商網站建站交付時，代理人必須產出此計分卡，
> 讓用戶一目了然地掌握交付品質。

---

## 計分卡格式

### 基本資訊
```
品牌名稱：[Brand Name]
建站日期：[YYYY-MM-DD]
商品分類：[Category]
美學風格：[Style Name]
頁面數量：[N]/11
```

### ⛔ 第一段：攔截項（一樣計分，但沒過就擋交付）

**先填這一段，沒有全過就不用往下填分數。**
攔截項是法規與正確性類，**一樣計入總分**，但另外標記為 `blocking`：
只要有一項不通過，不論總分多高，整份判定失敗、不得交付。
分數與交付判定是兩件事。分數看整體，交付判定看攔截項有沒有全過。

| 攔截項 | 檢查內容 | 判定 | 來源 |
|--------|---------|------|------|
| ⚖️ 法規合規 | UK/EU 合規閘門（假評價、假庫存數字、無依據的劃線原價、預設勾選加購、費用未揭露） | PASS / **FAIL** | `ecommerce-checklist.py` P7；[anti-patterns.md](anti-patterns.md) L1–L6 |
| 📄 劃線原價證據檔 | 有劃線原價／折扣標籤者，須有欄位齊全的合規證據檔（30 天最低價基準） | PASS / **FAIL / N/A** | [13-compliance.md](../../departments/13-compliance.md) |
| 🎭 擬真度 Rubric | [site-quality-rubric.md](site-quality-rubric.md) 過關 | PASS / **FAIL** | SKILL.md §4.6 |
| 👁️ Taste Gate | `/frontend-design` 判定「不像 AI 套版、美學及格」 | PASS / **FAIL** | SKILL.md §4.6.5 |

> **為什麼分成兩段**：舊版這份計分卡把所有項目折算成分數加總，跑出 87 分就判定通過，
> 裡面卻帶著法規違規。修正做法寫在 [PITFALLS.md](../PITFALLS.md)「加權分數把違規蓋過去」，
> 被標為這條產線上單一影響最大的修正：**法規與正確性類是攔截項，一樣計入總分，
> 但另外標記為 `blocking`，沒過一律判定失敗並以非零狀態碼結束，分數再高也沒用**；
> 品味與程度類則單純用分數表示、不另外標記。
> 這份模板的第一段就是那條修正的落地，**不要把攔截項的「擋交付」判定拿掉，也不要把它從分數裡剔除**。

### 第二段：品質評分表（僅在攔截項全過後才有意義）

| 維度 | 項目 | 分數 | 狀態 |
|------|------|------|------|
| 🏗️ 建置 | Build 成功（零錯誤） | /100 | ✅/❌ |
| 🗺️ 路由 | 15 個路由全覆蓋 | /100 | ✅/❌ |
| 🛒 商務 | 購物車 + 結帳邏輯完整 | /100 | ✅/❌ |
| 🖼️ 圖片 | SafeImage + 無死圖 | /100 | ✅/❌ |
| 🔍 SEO | Helmet + Schema.org | /100 | ✅/❌ |
| 🎨 設計 | Anti-Pattern 清潔度 | /100 | ✅/❌ |
| 🔒 安全 | 無硬編碼/XSS 風險 | /100 | ✅/❌ |
| **綜合** | **加權平均** | **/100** | **✅/⚠️/❌** |

### 門檻標準

**前提：上面四個攔截項全部 PASS。任一 FAIL 直接落到「❌ 不得交付」，不看本表。**

| 等級 | 分數範圍 | 決策 |
|------|---------|------|
| 🏆 Excellent | 90-100 | ✅ 可立即交付 |
| ✅ Good | 75-89 | ✅ 可交付，備註改進建議 |
| ⚠️ Acceptable | 60-74 | ⚠️ 需要修復後再交付 |
| ❌ Fail | <60 | ❌ 必須重做 |
| ⛔ Blocked | 不適用 | ❌ **有攔截項未通過，不得交付**（分數不予採計） |

---

## 設計決策記錄 (Design Decision Log)

### 決策 #1：色系選擇
```
輸入：品類 = [Category], 情感 = [Emotion]
NotebookLM 靈感：[Benchmark Brand] 的 [Specific Element]
UI UX Pro Max：Palette #[N] ([Colors])
突變因子：[Mutation Factor]
最終決策：[Primary] / [Secondary] / [Accent]
```

### 決策 #2：版型選擇
```
排除原因：避免 [Anti-Pattern]
選用風格：[Layout Style]
說明：[Why this layout fits the brand]
```

### 決策 #3：字體選擇
```
品牌氣質：[Brand Personality]
Display Font：[Font Name] (for headlines)
Body Font：[Font Name] (for body text)  
選擇理由：[Contrast/Harmony rationale]
```

---

## 功能完成度清單

### Layer A (Core Commerce)
- [ ] `/` Home Page — Hero + Featured Products
- [ ] `/shop` — Grid + Filter + Sort
- [ ] `/product/:slug` — Detail + Add to Cart
- [ ] `/cart` — Drawer + Full Page
- [ ] `/checkout` — 3-Step (Shipping/Payment/Success)
- [ ] `/search` — Instant Filter + Not Found State

### Layer B (Member)
- [ ] `/account/login` — Email + Password
- [ ] `/account/register` — Form + Validation
- [ ] `/account/orders` — Order History List
- [ ] `/account/profile` — Edit Profile Form

### Layer C (Policy)
- [ ] `/policies/*` — FAQ / Shipping / Returns / Privacy / About

### 互動完整度
- [ ] "Add to Cart" → Toast/Animation 反饋
- [ ] Checkout Success → 動畫 + Order ID
- [ ] Search → 即時過濾 + 空結果狀態
- [ ] Login → Token 持久化 + Redirect
- [ ] Cart badge → 即時數量更新
