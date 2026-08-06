# 🧠 UX 心理學電商應用指南

> 本文件基於 Antigravity Kit 的 `frontend-design/ux-psychology.md` 進行電商化改造，
> 將每條心理學法則都映射到具體的電商場景與 UI 實作。
>
> ⚠️ 出處說明：Antigravity Kit（`.agent/`）**未隨本 repo 發佈**，只存在於產線的本機技能目錄。
> 詳見 [SKILL.md](../SKILL.md) 的「Antigravity Kit 整合說明」。本文內容本身是完整的，不需要該目錄才能讀。

---

## 1. 核心轉換率心理法則

### Hick's Law → 商品選擇漏斗

| 電商場景 | 應用 | 具體實作 |
|----------|------|---------|
| 商品分類導航 | ≤ 6 個頂層分類 | 導覽列最多 6 項 + "More" |
| 商品 Filter | 預設展示最常用 3-4 個 Filter | 隱藏進階 Filter，點擊展開 |
| 結帳流程 | 三步驟漸進式展開 | Shipping → Payment → Confirm |
| 商品變體選擇 | 預選最受歡迎的尺寸/顏色 | Default selection + visual indicator |

### Fitts' Law → CTA 按鈕尺寸

| 元素 | 最小尺寸 | 放置位置 |
|------|---------|---------|
| "Add to Cart" 按鈕 | 48px 高 × 寬如容器 | 商品圖片正下方，拇指自然觸及區 |
| "Checkout" 按鈕 | 52px 高 | 購物車抽屜底部固定 |
| 商品卡片點擊範圍 | 整張卡片可點擊 | 不要只有小文字連結 |
| Mobile Touch Target | 44px × 44px 最低 | 所有互動元素 |

### Miller's Law → 商品呈現

| 電商場景 | 數量限制 | 原因 |
|----------|---------|------|
| 首頁推薦商品 | 4-8 個 | 超過 8 個會導致選擇疲勞 |
| 分類列表每行 | 2-4 列 (Desktop) | 格線不超過 4 列 |
| 商品描述要點 | 5-7 個 bullet points | 超過 7 個用戶不會讀 |
| 顏色/尺寸選項 | 若 > 7，分組顯示 | 如：暖色系 / 冷色系 |

### Von Restorff → 引導注意力

| 電商場景 | 應用 |
|----------|------|
| "限量" 標籤 | 用品牌 Accent 色 badge，與背景形成高反差 |
| "Sale" 價格 | ⚖️ 僅在具備過去 30 天最低價基準時才可原價劃線；無基準 → 只放大現價、不劃線（見 anti-patterns.md §L1）|
| "Best Seller" | 商品卡片頂部 ribbon 或 badge |
| CTA 按鈕 | 唯一的高飽和度色塊，周圍皆為低飽和 |

### Serial Position → 頁面首尾策略

| 位置 | 電商應用 |
|------|---------|
| 頁面頂部（首因效應） | Hero Banner + 核心 CTA（Shop Now） |
| 頁面底部（近因效應） | 重複 CTA + Trust Badges + Newsletter |
| 導覽首位 | "Shop" 或 "Best Sellers" |
| 導覽末位 | "Cart" 圖標（始終可見） |

---

## 2. 電商專屬行為偏差

### Zeigarnik Effect → 結帳進度

```
未完成感 = 繼續的動力

結帳流程進度條設計：
Step 1: Shipping  ────────── 33% ●─────────────○─────────────○
Step 2: Payment   ────────── 66% ●─────────────●─────────────○  
Step 3: Confirm   ────────── Almost done! ●────────────●──────●✓

購物車側邊欄：
"You're 1 step away from free shipping!" (剩餘 $XX)
```

### Goal Gradient → 購物車激勵

```
購物車金額進度條：

$0 ──────────────── $50 ──────────────── $100
                     ↑
              "Free shipping at $50!"
              "You're $12 away from free shipping!"

心理學原理：越接近目標，完成動力越強
```

### Anchoring Bias → 價格展示

> ⚖️ **UK/EU 法規前提**：劃線原價與 `% OFF` 屬「降價宣稱」，DMCCA 2024／Omnibus
> 要求**必須以該商品過去 30 天內的最低售價為基準**。拿不出基準就是不實標價。
> 由 `scripts/ecommerce-checklist.py` P7 Gate 自動攔查。

```tsx
// ✅ 有 30 天最低價基準時（專案存在 compliance/EVIDENCE.md）才可這樣錨定
<div className="price-display">
  <span className="original-price line-through text-muted">$99.00</span>
  <span className="sale-price text-accent text-2xl font-bold">$49.00</span>
  <span className="discount-badge bg-accent text-white px-2 py-1">50% OFF</span>
</div>

// ✅ 預設行為（Mock 站／無基準）：只顯示現價，不劃線、不放折扣 badge
<span className="price text-2xl font-bold">$49.00</span>
```

**無基準時的合法錨定替代方案**（效果一樣，不碰法規）：
- 同系列高價品項並列（Bundle $129 / Single $49），用真實品項價差當錨
- 以「每次使用成本」「每月分攤」呈現價值
- Good / Better / Best 三階定價，中間選項當錨

### Social Proof → 信任建設

| 電商元素 | 放置位置 |
|----------|---------|
| "★★★★★ (127 Reviews)" | 商品標題下方 |
| "Sarah just purchased this" | 浮動通知（右下角）— ⚖️ 必須來自真實訂單資料；捏造即違反 DMCCA 假評價/假活動條款，無真實資料就不要放 |
| "Trusted by 10,000+ customers" | Hero section 或 About 頁 — ⚖️ 數字須有實據，拿不出就改寫成不含數字的敘述 |
| Trust Badges (SSL, Payment icons) | Footer + Checkout 頁 |

### Scarcity → 稀缺效應（注意：避免 Dark Pattern）

```
✅ 合理使用：
  - "Only 3 left in stock" (基於真實庫存)
  - "Limited Edition Collection" (真實限量)
  - "This week's picks" (有時效的推薦)

❌ Dark Pattern（嚴禁，UK CPRs／EU UCPD 可裁罰）：
  - 虛假倒計時（永不結束、或重整就重來的促銷倒數）
  - 虛假庫存低提示（硬寫死或 Math.random 產生的剩餘數量）
  - "10 people viewing this right now"（若為假數據）

⚖️ 預設行為：拿不出真實依據時**不產生該元素**，而不是產生一個假的。
   - 無真實庫存數 → 只顯示 In Stock / Out of Stock
   - 無真實促銷截止時間 → 不放倒數計時器
```

### Peak-End Rule → 結帳成功頁

```
結帳成功頁是用戶體驗的「巔峰」與「結尾」，
必須投入最多設計心力：

✅ 應包含：
  - 成功動畫（confetti / checkmark animation）
  - 訂單摘要（商品、金額、預計送達）
  - Mock Order ID
  - "Continue Shopping" CTA
  - Brand 態度文案（"Thank you for choosing [Brand]"）

❌ 不可：
  - 只顯示 "Order placed." 的白頁
  - 無任何動畫或視覺獎勵
```

---

## 3. 電商 Wow Factor 強制清單

### 視覺體驗層

- [ ] 首頁 Hero 有電影感（使用 `generate-image` 生成品牌圖片）
- [ ] 商品卡片 hover 有微互動（scale 1.02 + shadow elevation）
- [ ] 頁面之間有過場動畫（Framer Motion `AnimatePresence`）
- [ ] 奢華留白（card padding ≥ 24px，section gap ≥ 80px）
- [ ] 至少 1 處使用品牌字體（Google Fonts 非預設體）
- [ ] 背景/前景有層次感（使用 shadow 或 subtle gradient）

### 互動體驗層

- [ ] 加入購物車有「飛入」動畫或 Toast 通知
- [ ] 搜尋有即時過濾效果（非整頁重載）
- [ ] 結帳有三步驟進度指示器
- [ ] 所有按鈕 hover 有明確回饋（scale/color/shadow 變化）
- [ ] 購物車數量 badge 有動態更新效果
- [ ] 空狀態頁面有品牌化插圖或文案（非空白頁）

### 信任體驗層

- [ ] Footer 有完整的品牌資訊與政策連結
- [ ] Checkout 頁有安全標誌（Lock icon + "Secure Checkout"）
- [ ] 商品頁有品質保證文案或退換貨政策提示
- [ ] 結帳成功頁有令人記憶深刻的成功動畫

---

## 4. 電商 Emotional Design 三層次

```
VISCERAL（直覺層，前 50ms）
├── Hero Banner 是否令人「哇」出聲？
├── 品牌色系是否與商品情感一致？
├── 字體是否傳遞正確的品牌氣質？
└── 圖片品質是否達到商業水準？

BEHAVIORAL（行為層，使用中）
├── 加入購物車是否 < 2 次點擊？
├── 結帳流程是否 < 3 步驟？
├── 搜尋是否即時回應？
├── 所有按鈕是否有 hover/active 回饋？
└── Loading 是否有 skeleton screen？

REFLECTIVE（反思層，使用後）
├── "我喜歡這個品牌的風格"
├── "這個結帳體驗很流暢"
├── "我願意分享這個網站給朋友"
└── "這個包裝/成功頁讓我覺得值得"
```
