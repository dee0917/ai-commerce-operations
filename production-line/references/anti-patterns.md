# 🚫 設計反模式防護清單 (Anti-Pattern Shield)

> 基於 Antigravity Kit 的 `frontend-design/SKILL.md` Anti-Pattern 清單，
> 專為電商場景定制的「禁止事項」與替代方案。
>
> ⚠️ 出處說明：Antigravity Kit（`.agent/`）**未隨本 repo 發佈**，只存在於產線的本機技能目錄。
> 詳見 [SKILL.md](../SKILL.md) 的「Antigravity Kit 整合說明」。本文內容本身是完整的，不需要該目錄才能讀。

---

## 🔴 ZERO TOLERANCE（零容忍，違反即重做）

### 1. 空函數 / Placeholder 邏輯
```tsx
// ❌ BANNED
onClick={() => {}}
onClick={() => console.log('TODO')}
// TODO: Implement cart logic

// ✅ REQUIRED
onClick={() => addToCart(product)}
onClick={() => toast.success('Added to cart!')}
```

### 2. 死圖 / Broken Images
```tsx
// ❌ BANNED
<img src="https://via.placeholder.com/300" />
<img src="/images/product.jpg" />  // 不存在的圖片

// ✅ REQUIRED
<SafeImage src={product.image} alt={product.name} className="..." />
```

### 3. 半殘頁面
```
❌ BANNED: 只完成首頁 + 商品列表頁，其他頁面留白
✅ REQUIRED: 定義了 15 個路由，就必須實作 15 個
```

### 4. 無效連結
```tsx
// ❌ BANNED
<Link to="#">About Us</Link>
<a href="javascript:void(0)">Contact</a>

// ✅ REQUIRED
<Link to="/policies/about">About Us</Link>
```

### 4.5 絕對定位控制項壓住內容（2026-08 實證新增）
輪播箭頭、浮動按鈕、返回頂部等絕對定位控制項，**不得疊在文字或 CTA 上**。
實證案例：hero 輪播箭頭用 `inset-y-0 left-6` 垂直置中，1440px 寬時左箭頭圓鈕直接蓋住標題首字。
```
❌ BANNED: 垂直置中的箭頭疊在文字欄上（left-6 + inset-y-0 落在標題行高內）
✅ REQUIRED（三選一）:
  1. 箭頭錨定在容器的留白區（如底部 padding 帶：top-auto bottom-0）
  2. 為箭頭保留專用車道（內容區加對稱的水平 padding ≥ 箭頭直徑 + 16px）
  3. 箭頭放在內容流之外（輪播下方的獨立控制列）
✅ VERIFY: 1280px 與 1440px 兩檔寬度都要實際打開檢查每一張 slide（含文字左右互換的變體）
```

---

## 🟡 AI TENDENCY PATTERNS（AI 傾向警告）

### 5. 紫色濫用 (Purple Ban)
```
❌ 除非品牌色板明確包含紫色，否則禁止以紫/紫羅蘭作為主色
❌ #7C3AED, #6D28D9, #8B5CF6 等紫色系不可作為 Primary Color

✅ 替代方案：深靛藍 #1E3A5F、翡翠綠 #065F46、琥珀金 #B45309
✅ 例外：若 UI UX Pro Max 明確輸出紫色作為品牌色
```

### 6. 同質化版面 (Vercel Clone Ban)
```
❌ 每個專案都是「左文右圖」Hero → 三列商品卡 → CTA → Footer
❌ 千篇一律的 dark hero + gradient text

✅ 替代方案：
  - Asymmetric Hero（45/55 不等分布局）
  - Full-Bleed Image Hero + Floating Product Cards
  - Vertical Scroll Storytelling
  - Split-Screen Navigation
  - Oversized Typography Hero
```

### 7. 暗黑+霓虹作為預設 (Dark Neon Ban)
```
❌ 除非品牌情感為「科技電競」，否則不可預設使用 dark + neon 配色
❌ #000000 背景 + #00FF88 文字 不是萬能方案

✅ 替代方案：
  - 奢華精品 → Cream + Deep Navy + Gold
  - 自然有機 → Off-White + Forest Green + Terracotta
  - 手工藝品 → Warm Linen + Burnt Sienna + Olive
  - 極簡美學 → Pure White + Charcoal + Single Accent
```

### 8. Mesh Gradient 泛濫
```
❌ 一個頁面不可超過 1 處 mesh/aurora gradient 裝飾
❌ 不可用 mesh gradient 作為商品展示區域的背景（干擾視覺焦點）

✅ 適用場景：
  - Hero Section 背景（唯一一處）
  - 結帳成功頁的慶祝氛圍
```

### 9. Bento Grid 濫用
```
❌ 不可在每個專案都使用 Bento Grid 作為主要布局
❌ 商品列表頁不需要 Bento Grid（標準 Grid 更適合瀏覽）

✅ 適用場景：
  - "About Us" 故事頁面（混合圖文內容）
  - 首頁的 Feature/Benefit 展示區域
```

### 10. 相同字體堆疊
```
❌ 每個專案都使用 Inter + Poppins
❌ 不顧品牌情感直接套用預設字體

✅ 流程：
  1. 根據品牌情感選擇字體（UI UX Pro Max 的 50 組字體對照）
  2. Hero/Display 字體必須與 Body 字體有足夠反差
  3. 至少引入 1 組非預設的 Google Font
```

---

## 🟠 E-COMMERCE DARK PATTERNS（電商黑暗模式，嚴禁）

| Dark Pattern | 說明 | 嚴禁原因 |
|--------------|------|---------|
| 虛假倒計時 | 永不結束的促銷倒數 | 欺騙消費者 |
| 虛假庫存低 | "Only 2 left!" 但庫存無限 | 虛假稀缺 |
| 隱藏費用 | 結帳最後才顯示高額運費或稅 | 損害信任 |
| 強制加購 | 預設勾選加購商品 | 操縱消費 |
| 取消困難 | 無法在 1-2 步內取消訂閱 | 留客策略 |
| 確認羞辱 | "No thanks, I don't want to save money" | 情緒操控 |

---

## ⚖️ UK / EU 法律禁區（違反會吃罰單，不是風格問題）

> **適用範圍**：任何以英國或歐盟消費者為對象的站台（公司 2026 第一刀＝英國）。
> **法源**：英國 Digital Markets, Competition and Consumers Act 2024（DMCCA，2025-04 生效）、
> Consumer Protection from Unfair Trading Regulations（CPRs）、EU Omnibus Directive、EU UCPD。
> **這一節是 Phase 0 必讀，且由 `scripts/ecommerce-checklist.py` 的 **P7 UK/EU Compliance Gate** 自動攔查。**

### L1. 劃線原價必須有 30 天最低價基準（最容易誤觸的一條）

DMCCA + Omnibus：任何「降價宣稱」（劃線原價、`% OFF`、`Save $X`、`Was/Now`）
**必須以該商品過去 30 天內的最低售價為基準**。拿不出這個基準就是不實標價。

```tsx
// ❌ BANNED（無基準的劃線價，生成站台最常犯，直接違法）
<span className="line-through">$99.00</span>
<span>$49.00</span>
<span className="discount-badge">50% OFF</span>

// ✅ 預設行為：拿不出基準 → 只顯示現價，不劃線、不放折扣 badge
<span className="text-2xl font-bold">$49.00</span>
```

**允許劃線的唯一條件**：專案根目錄存在 `compliance/EVIDENCE.md`，且該 SKU 通過結構化驗證。
英國站是我們自己的 Shopify 店，價格歷史是自家資料，所以格式就照我們產得出來的東西定：

```markdown
| sku | window_start | window_end | lowest_price | currency | was_price | source | generated_at |
|-----|--------------|------------|--------------|----------|-----------|--------|--------------|
| UK-TEE-001 | 2026-07-01 | 2026-07-31 | 59.00 | GBP | 59.00 | shopify-price-history-export | 2026-07-31 |
```

| 欄位 | 規則 |
|------|------|
| `sku` | 商品識別碼，逐 SKU 一列 |
| `window_start` / `window_end` | `YYYY-MM-DD`，需涵蓋 30 天；`window_end` 不得早於生成日前 1 天 |
| `lowest_price` + `currency` | 該視窗內的**最低售價**與幣別 |
| `was_price` | 劃線要顯示的原價，**不得高於 `lowest_price`** |
| `source` | 只能是 `shopify-price-history-export`／`internal-price-log`／`manual-verified` |
| `generated_at` | 產生時間戳 |

**缺任一欄，該 SKU 的劃線價就不予豁免。** 空殼檔（只寫一句「我們確認過了」）會被 P7 直接擋下。
**某 SKU 真的沒有 30 天歷史（新品）→ 正確做法是不劃線，不是放寬驗證。**
**Mock 資料站（Phase 1-4）永遠不具備這個基準 → 一律不得劃線。**

> ⚠️ **已知邊界（開店後補，不是現在的缺陷）**：P7 只驗 EVIDENCE.md 的**格式**
> 欄位齊全、日期在有效視窗內、`was_price` 不高於 `lowest_price`。
> **它不驗數字本身是不是真的。** 有人手打一列假數字、`source` 填 `manual-verified`，機器會放行。
> 等英國站 Shopify 真的開了，再接價格歷史 API 做對帳。在那之前，
> **EVIDENCE.md 的內容真實性是由填寫的人負責，不是由這支腳本背書。**

> ⚠️ **資料端才是源頭**：`compareAtPrice` / `salePrice` / `originalPrice` 這類欄位如果帶著值
> 出現在 `data/products.json`、`src/data/mockData.ts` 裡，即使畫面上暫時沒渲染出來，
> P7 一樣會擋。只堵渲染出口不堵資料源頭，換個寫法就繞過去了。

### L2. 倒數計時器必須對應真實截止時間

```
❌ BANNED：重整頁面就重新開始的倒數（`useState(3600)` + `setInterval` 遞減）
❌ BANNED：無對應促銷結束時間的「Ends in 02:14:33」
✅ REQUIRED：倒數目標是一個固定的絕對時間戳（來自真實促銷設定），重整不重置，
             到期後元件消失或改顯示「Offer ended」
✅ 預設行為：沒有真實截止時間 → 不要放倒數計時器
```

### L3. 庫存數字必須接真實庫存

```
❌ BANNED：硬寫 "Only 3 left!"、`Math.random()` 產生的剩餘數量
❌ BANNED："12 people are viewing this right now"（假數據）
❌ BANNED："Sold 500+ times"（無銷售紀錄支撐）
✅ REQUIRED：數字來自 stock_quantity 等真實欄位，且僅在真的低於門檻時顯示
✅ 預設行為：Mock 站只顯示布林狀態 In Stock / Out of Stock，不顯示數字
```

### L4. 評價、推薦、媒體背書不得虛構（DMCCA 明文禁止假評價）

```
❌ BANNED：捏造的評論（"Elena M., Portland OR"）、捏造的星等與評論數
❌ BANNED："As Seen In" 放虛構或無授權的媒體 logo
✅ REQUIRED：真實資料，或做出「尚無評價」的空狀態（空狀態才是成熟站的樣子）
```

### L5. 加購／訂閱不得預設勾選（需明示同意）

```
❌ BANNED：`defaultChecked` / `checked={true}` 出現在加購、保險、禮物包裝、
          訂閱制、電子報同意等選項上
✅ REQUIRED：一律預設未勾選，由使用者主動勾選
```

### L6. 全部費用必須在結帳前揭露

```
❌ BANNED：運費／稅／手續費只在最後一步才出現
✅ REQUIRED：購物車頁即顯示運費與稅的估算或明確規則
```

> **判斷原則（給生成站台用）**：這些手法**不是全面禁止**，是「有真實依據才可以用」。
> 拿不出依據時的**預設行為是不產生該元素**，而不是產生一個假的。

---

## ✅ 正面模式清單（鼓勵的設計）

| Pattern | 說明 | 效果 |
|---------|------|------|
| 漸進式展開 | 先顯示核心資訊，點擊展開更多 | 降低認知負擔 |
| 智慧預設 | 預選最常見的選項 | 加速決策 |
| 即時回饋 | 每個操作都有視覺回應 | 增強控制感 |
| Skeleton Loading | 載入時顯示骨架而非白屏 | 降低跳出率 |
| 麵包屑導航 | 讓用戶知道自己在哪裡 | 降低迷失感 |
| 無障礙設計 | 高對比文字、鍵盤導航 | 擴大受眾 |
