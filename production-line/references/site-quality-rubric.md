# 🎯 擬真度自我評分 Rubric (Site Quality Rubric)

> **定位**：交付前「像不像 AI 做的」最終自我評分閘門。
> 它把 [anti-patterns.md](anti-patterns.md) 與 [maturity-signals.md](maturity-signals.md) 的禁令，變成一個「打分 → 沒過就再改」的迭代閘門。
> 方法源自 Anthropic frontend-design 的 Evaluation 做法：評審看「截圖畫面」打分，不看程式碼。

## 校準錨點（用戶真實案例，2026-05-28）
由三個真實站歸納而成。刻意放兩種相反風格的正例，避免把每個站都逼成同一個長相：

- ❌ 反例（很 AI）：苔蘚生態瓶站。Inter + Playfair 假高級配對、漸層裁字、模糊光暈 hero、placehold.co 佔位圖、假評論（Elena M., Portland OR）、破折號堆形容詞、單頁 demo 沒結帳。
- ✅ 正例 A：街頭籃球潮牌。Brutalist 風（Oswald/Teko、直角、偏移硬陰影、斜跑馬燈）、真實照片、有態度文案、多頁完整商務。
- ✅ 正例 B：中式開運風水站。宮廷中式（Noto Serif TC、宮廷紅/帝王金命名色票、祥雲與 ☯ 裝飾）、真實產品圖、SEO 加法務頁齊全。

> 啟示：好風格可以是任何方向，重點是刻意且一致。

## 評分方式
- 用 browser_subagent / Playwright 截圖（首頁、商品詳情、結帳、行動版各一張），對著畫面打分。
- 六個維度各 0 到 5 分。**原創性、設計品質、品牌文案權重 x2**（AI 最會露餡、模型最弱的三項）。
- 過關門檻：三個權重維度各 ≥ 4，其餘 ≥ 3，且禁令零出現。沒過就回去改，迭代到過或卡住為止。

## 六個維度

### 1. 原創性（x2）
- 主視覺字體禁用 Inter / Roboto / Arial / 系統字當識別（細節見 anti-patterns.md §10）。
- 主標禁漸層裁字。hero 禁模糊光暈 blob 當主角；低透明度漸層或噪點當襯底可以，差別在它是主角還是襯底（見 anti-patterns.md §6 §8）。
- 禁全站只用預設圓角膠囊鈕加圓角卡交差，造型要刻意。
- 校準：遮掉 logo，旁人講得出風格名才算過。

### 2. 設計品質（x2）
- 配色要克制（主色加中性底加強調色），最好有意義、能對應品牌（例：宮廷紅、帝王金）。
- 字級階層與字體對比明確。中文站用合適 CJK 字體（Noto Serif/Sans TC），別拿純拉丁字體硬撐中文。

### 3. 品牌文案（x2）
- 禁破折號黏兩個短句當節奏。禁「不是 A，而是 B」句型。禁空形容詞（self-sustaining、game changer 那類）。
- 禁假評論「首字母縮寫加美國城市州」格式（Elena M., Portland OR）。要真資料或乾脆不放。
- 校準：要有觀點、有具體畫面的品牌聲音。

### 4. 商業真實感
- 多頁齊全，商品資料含尺寸/顏色/庫存/價格/評分，且真能走完結帳。
- ⚖️ 「原價特價」不列為必備：無 30 天最低價基準時只顯示現價才是正確答案（見 anti-patterns.md §L1），不得為了湊豐富度製造假折扣。
- 成熟度訊號 ≥ 12/21 與 Forbidden AI Tells 清單見 maturity-signals.md。

### 5. 技術執行
- RWD 不破版、互動有回饋不浮誇、Lighthouse 行動版 > 80、無 console error、同類字級間距一致。

### 6. 可用性
- 主 CTA 一眼可見、首頁到結帳 ≤ 3 次點擊、價格與加購與庫存狀態清楚。

## 與既有計分卡的關係
[quality-scorecard.md](quality-scorecard.md) 是交付給用戶看的成績單。本 Rubric 是交付前自己先過的擬真度閘門。先過本 Rubric，再填計分卡。
