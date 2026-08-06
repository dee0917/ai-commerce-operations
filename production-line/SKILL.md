---
name: auto-ecommerce-landing
description: 一鍵生成頂級電商網站。基於 66 個真實電商 DNA 模板 + 現代 UI 框架（shadcn/DaisyUI/Radix），生成具備成熟品牌質感的電商網站，每一個站的視覺與結構都不重複。觸發時機：用戶說「幫我生成一個隨機的電商網站」「幫我建立一個電商網站」「幫我做一個電商網站」或任何自動產生電商 Landing Page 的請求。台灣口語觸發：「開個站」「弄個賣場」「這個產品做個頁面」「上架這批貨」「先做個能賣的頁」「客戶要看網站」「做個店」「架個購物網」。
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, Task, SlashCommand, TodoWrite, mcp__StitchMCP__*
---

# 全自動頂級電商架站引擎 v11.1（Real DNA + Modern UI + AI 整合版）

> **核心哲學：一次到位，絕不敷衍。自動化驗證，量化交付。**
> 目標是生成一個**前端功能完整、可直接部署**的電商網站，包含完整的業務邏輯、UI 狀態與工程架構，
> 並通過 **8 層自動化品質門檻** 驗證後才可交付。
>
> ⚠️ **交付的是前端，不是一間可以收錢的店。** 結帳流程走得完，但**付款是模擬的**，按下確認即當作已付款，沒有接任何真實金流。要真的開賣，還缺金流、寄信服務、稅金與運費設定。實際狀態與限制清單見 `docs/backend-poc.md`。對外說明一律照這個口徑，不要說「可立即商用」。
>
> **設計引擎**：基於 66 個真實電商 DNA 骨架 + 6 種現代 UI 框架 + UI-UX-PRO-MAX 設計系統 + Stitch AI 設計變體，產出具備成熟品牌質感、每站不重複的電商網站。

**執行語言**：所有品牌名稱、UI 文案、商品名稱 → **English Only**
**回報語言**：所有對用戶的進度回報、技術說明 → **繁體中文**

---

## 💡 使用範例

```
用戶: "幫我生成一個隨機的電商網站"

執行流程:
┌─ Phase 0: 零容忍守則載入
│  ├─ ✅ 讀取 anti-patterns.md
│  └─ ✅ 讀取 ux-psychology-ecommerce.md
│
├─ Phase 1: 創意種子 (AI 設計系統生成)
│  ├─ 🎲 從 extracted_products.json 隨機抽取分類
│  ├─ 🔍 調用 NotebookLM 研究標竿品牌
│  ├─ 🧠 載入 UX 心理學法則
│  ├─ 🧬 DNA 混血選取：主 DNA (骨架) × 副 DNA (靈感) = 12,870 種組合（66×65÷2 × 6 框架，算式見 Phase 1.05）
│  ├─ 🏗️ 選取現代 UI 框架 (shadcn/DaisyUI/Radix...)
│  ├─ 🎨 調用 UI-UX-PRO-MAX 生成設計系統 (受 DNA 約束)
│  ├─ 🎨 調用 Stitch AI 生成設計變體 (解決同質化)
│  └─ 📝 生成 design-system/MASTER.md + DECISIONS.md
│
├─ Phase 2: 工程實作 (11 類頁面完全實作，展開 15 個路由)
│  ├─ 🏗️ 初始化 Vite + React + TypeScript + Tailwind
│  ├─ 📦 安裝依賴 (zustand, react-router-dom, motion...)
│  ├─ 🗂️ 創建 Types, Mock Data, SafeImage 組件
│  ├─ 🛒 實作狀態管理 (useCart, useAuth, useSearch)
│  └─ 📄 完成 11 類頁面、共 15 個路由:
│      • Layer A: Home, Shop, Product, Cart, Checkout, Search
│      • Layer B: Login, Register, Orders, Profile
│      • Layer C: FAQ, Shipping, Returns, Privacy, About
│
├─ Phase 3: 圖片與 SEO 強化
│  ├─ 🖼️ 生成 Hero Banner (.agent/skills/generate-image)
│  ├─ 🖼️ 生成 3 張分類封面圖
│  └─ 🔍 植入 Schema.org + react-helmet-async
│
├─ Phase 4: 交付驗收 (100% 覆蓋率測試)
│  ├─ 🔨 執行 npm run build (隱藏錯誤，自動修復)
│  ├─ ✅ 運行 scripts/ecommerce-checklist.py --preview
│  ├─ 🌐 啟動預覽伺服器 (http://localhost:5173)
│  ├─ 🤖 瀏覽器子代理深度測試 (導航/圖片/購物流)
│  └─ ⏸️ 階段一完成 → 等待用戶驗收前端
│
├─ Phase 5: 後端服務層注入（用戶確認後）
│  ├─ 🔌 注入 src/services/ (api/product/cart/auth/order/checkout)
│  ├─ 🛒 混合購物車 (localStorage ↔ WooCommerce Store API)
│  ├─ 🔐 JWT 認證 + 自動 Token 刷新
│  ├─ 💳 結帳框架（金流接口預留）
│  ├─ 🔄 改寫 Zustand Stores 串接 Service 層
│  └─ ✅ Mock 全流程 QA 驗證
│
└─ Phase 6: WP 部署包生成（可選）
   ├─ 🐳 docker-compose.yml (WP + MySQL)
   ├─ 📦 必裝外掛 (5個) + 隨機外掛池 (3-5個，避免模板感)
   ├─ 🔧 wp-cli 一鍵設定腳本
   └─ 📖 DEPLOYMENT.md 部署指南
   └─ 📊 輸出品質計分卡 + 設計決策記錄

交付物:
✅ 完整可運行的電商網站 (11 類頁面／15 個路由 100% 實作)
✅ 品質計分卡 (quality-scorecard.md 格式)
✅ 設計決策記錄 (design-system/DECISIONS.md)
✅ 預覽網址 (http://localhost:5173)
```

---

## 🔧 Antigravity Kit 整合說明

> [!IMPORTANT]
> **`.agent/` 子系統未隨本 repo 發佈。**
> 本文（以及 `references/` 底下數份文件）提到的 `.agent/` 目錄，存在於**產線的本機技能目錄**
> （`~/.claude/skills/auto-ecommerce-landing/.agent/`），**不在這個 repo 裡**。
> 本 repo 收錄的是產線的文件與腳本部分，`.agent/` 是通用能力層，刻意不複製進來
> （其中含 `mcp_config.json` 等本機設定，不適合隨 repo 發佈）。
>
> 因此：
> - **在本機執行產線的人**：底下所有 `.agent/...` 路徑引用照用，東西在本機技能目錄下。
> - **clone 這個 repo 的人**：不會有這個目錄，相關步驟需改用各自環境的等效工具，或改走本文標註的 Fallback。
>
> 全文其餘約 30 處 `.agent/` 引用一律適用本段但書，不逐處重複標註。

本技能已整合 Antigravity Kit（`.agent/` 目錄），可直接調用以下子系統：

> ⚠️ 下表數量為真實統計（清點自本機技能目錄），但**這些東西不在本 repo 內**，見上方但書。

| 子系統 | 路徑 | 用途 |
|--------|------|------|
| **20 個專業代理** | `.agent/agents/` | 前端/後端/安全/測試等角色專家 |
| **36 個領域技能** | `.agent/skills/` | 設計/React/SEO/安全等知識模組 |
| **11 個工作流** | `.agent/workflows/` | `/create`, `/debug`, `/deploy` 等 |
| **4 個核心腳本** | `.agent/scripts/` | `checklist.py`, `verify_all.py`, `auto_preview.py`, `session_manager.py` |
| **UX 心理學** | `.agent/skills/frontend-design/ux-psychology.md` | 🔴 **設計前必讀** |
| **Anti-Pattern 清單** | `.agent/skills/frontend-design/SKILL.md` §9 | 避免 AI 同質化設計 |

> **重要**：當需要特定領域知識時，可直接讀取 `.agent/skills/[skill-name]/SKILL.md`（僅限本機執行環境）。

---

## 🎯 選擇性閱讀規則 (Selective Reading Rule)

**根據執行階段讀取對應文件，避免不必要的 token 消耗：**

| 文件 | 狀態 | 何時讀取 | 用途 |
|------|------|----------|------|
| [anti-patterns.md](references/anti-patterns.md) | 🔴 **必讀** | Phase 0 開始前 | 零容忍守則與設計反模式 |
| [ux-psychology-ecommerce.md](references/ux-psychology-ecommerce.md) | 🔴 **必讀** | Phase 1.0.5 UX 引擎 | 電商專用心理學法則 |
| [real-ecommerce-dna.md](references/real-ecommerce-dna.md) | 🔴 **必讀** | Phase 1.05 DNA 選取 | 66 個真實電商網站 DNA 模板 |
| [modern-ui-frameworks.md](references/modern-ui-frameworks.md) | 🔴 **必讀** | Phase 1.06 框架選取 | 現代 UI 框架整合指南 |
| [structural-variation.md](references/structural-variation.md) | 🔴 **必讀** | Phase 1.07 結構隨機化 | 區塊組成/順序、分頁組合、組件變體隨機化規則 |
| [maturity-signals.md](references/maturity-signals.md) | 🔴 **必讀** | Phase 2.5 成熟度特徵實作 | 成熟電商特徵清單（避免模板感）|
| [engineering-standards.md](references/engineering-standards.md) | 🟡 條件讀取 | Phase 2 工程實作 | SafeImage、Zustand 標準 |
| [site-architecture.md](references/site-architecture.md) | 🟡 條件讀取 | Phase 2.4 頁面開發 | 11 類頁面、15 個路由的架構詳解 |
| [woocommerce-api.md](references/woocommerce-api.md) | 🟡 條件讀取 | Phase 2.2 數據結構 | WooCommerce API 接口 |
| [member-zone.md](references/member-zone.md) | 🟡 條件讀取 | Phase 2.4 會員功能 | 登入/註冊/訂單實作 |
| [seo-and-testing.md](references/seo-and-testing.md) | 🟡 條件讀取 | Phase 3.2 SEO 植入 | Schema.org 與 SEO 標準 |
| [security-checklist.md](references/security-checklist.md) | ⚪ 可選讀取 | Phase 4 驗收 | 安全自檢清單 |
| [quality-scorecard.md](references/quality-scorecard.md) | ⚪ 可選讀取 | Phase 4.6 交付報告 | 品質計分卡模板 |
| [site-quality-rubric.md](references/site-quality-rubric.md) | 🔴 **必讀** | Phase 0 開始前＋Phase 4.6 交付前 | 擬真度自我評分閘門（用戶真實案例校準）|

> 🔴 **必讀** = 每次執行都必須載入
> 🟡 **條件讀取** = 執行到該階段時才讀取
> ⚪ **可選讀取** = 需要時才讀取

---

## Phase -1：系統預檢 (Preflight Check)

> **自動化執行**: 在開始生成前，自動驗證系統環境與資源可用性

**執行腳本**: `python scripts/preflight_check.py`

### 檢查項目

| 檢查項 | 必要性 | 失敗處理 |
|--------|--------|----------|
| Node.js 版本 >= 18 | 🔴 必須 | 提示用戶升級 Node.js |
| 商品數據源可用 | 🟡 建議 | 啟用 Fallback 模式 |
| generate-image MCP | 🟡 建議 | 使用 Unsplash/Placeholder |
| ui-ux-pro-max 技能 | 🔴 必須 | 停止執行 |
| 磁碟空間 >= 500MB | 🔴 必須 | 提示清理空間 |

### 執行範例

```python
# scripts/preflight_check.py 會自動執行以下檢查：
✅ Node.js v20.10.0 detected
✅ Product data source available (523 products)
⚠️ generate-image MCP not configured (will use Unsplash)
✅ ui-ux-pro-max skill installed
✅ Disk space: 12.5 GB available

Result: PASS (with warnings)
Mode: Standard (with image fallback)
```

### Fallback 模式

如果商品數據源不可用，自動啟用內建的 5 個 Fallback 分類：
1. Luxury Jewelry
2. Artisan Coffee
3. Sustainable Home Goods
4. Tech Gadgets
5. Organic Skincare

> **實作細節**: 見 [scripts/preflight_check.py](scripts/preflight_check.py)

---

## Phase 0：零容忍守則 (Zero Placeholder Policy)

> **開始前必讀**: [anti-patterns.md](references/anti-patterns.md) + [ux-psychology-ecommerce.md](references/ux-psychology-ecommerce.md) + [site-quality-rubric.md](references/site-quality-rubric.md)

### 🔧 環境檢查（開始前必須執行）

**如果找不到 UI UX Pro Max**：那是 `.agent/` 子系統的一部分，**未隨本 repo 發佈**（見上方「Antigravity Kit 整合說明」）。
改走底下的 Fallback 策略，不必再去 PITFALLS.md 找，PITFALLS.md 沒有這一節。

```bash
# 快速檢查清單
✅ 確認當前目錄: pwd
✅ 確認 UI UX Pro Max 存在: ls .agent/skills/ui-ux-pro-max/
✅ 確認自動化腳本存在: ls scripts/auto_fix_build.py
```

**Fallback 策略**:
- ❌ 如果找不到 UI UX Pro Max → 使用 **NotebookLM 智能決策**（Phase 1.15）
- ❌ 如果找不到自動化腳本 → 手動執行對應步驟（build 錯誤自行修，預覽用 `npm run dev`）。
  Windows 上找不到 `npm` 這類環境問題見 [PITFALLS.md](PITFALLS.md) §二「Windows 上找不到 npm」。

---

作為資深架構師，你必須確保生成的代碼中**嚴禁出現以下行為**：

### 🔴 零容忍清單 (11 條鐵律)

| # | 守則 | 違反後果 |
|---|------|---------|
| 1 | **嚴禁空函數/Placeholder** | `onClick={() => {}}` → 重做 |
| 2 | **嚴禁死圖** | 未使用 `SafeImage` → 重做 |
| 3 | **嚴禁半殘頁面** | 定義 15 個路由只做 5 個 → 重做 |
| 4 | **嚴禁無效連結** | `<Link to="#">` → 重做 |
| 5 | **嚴禁紫色濫用** | 預設紫色主色 → 重新選色 |
| 6 | **嚴禁同質化版面** | 每次都是「左文右圖」Hero → 重新設計 |
| 7 | **嚴禁暗黑+霓虹預設** | 黑底+螢光色 (非電競品類) → 重新選色 |
| 8 | **嚴禁 Mesh Gradient 泛濫** | 超過 1 處 Mesh Gradient → 移除 |
| 9 | **嚴禁電商 Dark Pattern** | 虛假倒計時/庫存/隱藏費用 → 移除 |
| 10 | **嚴禁相同字體堆疊** | 每次都用 Inter + Poppins → 重新選字體 |
| 11 | **嚴禁無 30 天基準的劃線價** | `line-through` 原價 / `% OFF` 無價格基準 → 移除（UK DMCCA 違法）|

> 📖 **詳細說明與替代方案**: 見 [anti-patterns.md](references/anti-patterns.md)
> ⚖️ **UK/EU 法律禁區（英國站必讀）**: 見 [anti-patterns.md §UK / EU 法律禁區](references/anti-patterns.md)
> 由 Phase 4.2 的 **P7 UK/EU Compliance Gate** 自動攔查，不通過不得交付。

---

## Phase 1：創意種子（Real DNA + Modern UI + AI 設計系統生成）
> **目標**：基於真實電商網站 DNA 骨架 + 現代 UI 框架 + UI-UX-PRO-MAX + Stitch AI，生成看起來像經營 5 年以上、具備成熟品牌質感的電商網站。每次生成保證結構、風格、框架三重不重複。

### 1.0 AI 美學研究 (Aesthetic Extraction)
**必須執行**：在開始任何設計前，調用 NotebookLM 針對當前品牌進行深度研究。
- **目標筆記本 ID**: `<notebook-id>` (Top-100-Modern-Ecommerce-Frontend-Patterns)
- **指令範例**：
  ```bash
  /notebooklm notebook_query "根據筆記本中的前百大電商實踐，有哪些最適合 [品牌分類，例如：奢華珠寶] 的前端設計模式、微互動（Micro-interactions）與配色方案？請參考 Apple/Nike/Allbirds 的成功要素。"
  ```

### 1.0.5 UX 心理學載入 (Psychology Engine)
**必須執行**：在設計前載入 UX 心理學知識。
- **讀取** `.agent/skills/frontend-design/ux-psychology.md`（完整心理學法則庫）
- **讀取** **[ux-psychology-ecommerce.md](references/ux-psychology-ecommerce.md)**（電商化應用指南）
- **特別關注**：
  - Hick's Law → 商品分類導航 ≤ 6 項
  - Fitts' Law → CTA 按鈕 ≥ 48px
  - Von Restorff → CTA 是頁面唯一高飽和色塊
  - Peak-End Rule → 結帳成功頁必須投入最多設計心力
  - Zeigarnik Effect → 結帳進度條

### 1.05 真實電商 DNA 混血選取 (Real Ecommerce DNA Crossbreeding)
**必須執行**：每次生成基於兩個真實電商網站的 DNA 混血，產生從未見過的獨特風格。

**讀取** [real-ecommerce-dna.md](references/real-ecommerce-dna.md)

**混血規則（主從分明，不可混亂）**：

1. **選取主 DNA（骨架主人）**：跑 `python scripts/design_history.py plan --pool`，只從印出來的清單隨機抽一個作為「主 DNA」——不再是任意生成 1-66 隨機數；池子已經先剔除近期撞 family／紫色／字體範式的選項，抽到池外 `reserve` 會直接拒絕。細節見 [uniqueness-guarantee.md](references/uniqueness-guarantee.md)
2. **選取副 DNA（靈感注入）**：再生成一個隨機數，選定另一個不同 Family 的 DNA 作為「副 DNA」
3. **防重複檢查**：跑 `python scripts/design_history.py plan`，它會讀 `data/design-history.json` 印出本次要避開的底色系與字體；確認最近 5 次未使用相同的主 DNA Family
4. **連續視覺去重（2026-08 新增，強制）**：讀取 `data/design-history.json` **最近 3 筆**的 `bg_tone` 與 `fonts.display`：
   - 本次的**底色系**不得與前 3 筆中出現 2 次以上的底色系相同。底色系分四類：`warm-paper`（米白／奶油／暖紙底）、`cool-white`（冷白／純白）、`dark`（深色底）、`tinted`（有彩色底）。舊筆缺 `bg_tone` 時由 `colors.secondary` 的色溫與亮度推斷。
   - 本次的 **display 字體**不得與前 3 筆任何一筆相同；同一襯線大標範式（如 Fraunces / Cormorant / DM Serif Display 這類「襯線大標＋暖紙底」組合）連續出現 2 次後，第 3 次強制改用其他字體類別（幾何無襯線、grotesque、slab、mono display 等）。
   - **body 字體迴避 Inter**：Inter 是 2020-2023 SaaS 的預設臉，加入迴避清單；DNA 檔案裡的字體是「類別示意」，撞到迴避清單就換同類別的替代字體（如 Inter → Archivo / Instrument Sans / Schibsted Grotesk）。
   - 教訓來源：2026-08 健檢發現連續四站全是暖紙底＋襯線大標（Fraunces、Cormorant Garamond、DM Serif Display），並排看像同一家的三種皮膚，使用者原話「我們電商頁面好像被統一了」。
5. **記錄選取結果**：兩個 DNA 編號、各自 Family、混血規則寫入 `design-system/DECISIONS.md`
6. **選中的當下就訂位（強制，時機不對等於沒做）**：底色、display 字體、body 字體一決定，**立刻**跑：

   ```bash
   python scripts/design_history.py reserve \
     --brand "<品牌>" --category "<品類>" --project <專案路徑> \
     --primary-dna DNA-<##> --primary-family <X> \
     --secondary-dna DNA-<##> --secondary-family <Y> \
     --ui-framework <框架> \
     --bg-tone <warm-paper|cool-white|dark|tinted> --bg-hex "#xxxxxx" \
     --display "<Display 字體>" --body "<Body 字體>" \
     --primary-hex "#xxxxxx" --signature-fx "<tilt|magnetic|parallax|none>"
   ```

   這個動作把去重檢查與登記**綁在同一把檔案鎖裡**完成：違反第 3、4 條就直接拒絕並非零退出，通過才寫進去，狀態記成 `in_progress`。**印出來的 id 要記著**，後面兩步要用。
   - 站交付後：`python scripts/design_history.py commit --id <id> --maturity-score <分數>`
   - 站做不下去：`python scripts/design_history.py abandon --id <id> --reason "<原因>"`（不 abandon 的話，這組基因會佔位到 120 分鐘後才自動釋放）

   ⚠️ **不可以改回「站建成之後才回寫」。** 讀取與回寫之間隔著整個建站流程，
   兩個站平行建置時後開工的那支讀到的是舊資料，防重複會**安靜失效**：
   2026-08-04 實測，站二鎖定基因的時間比站一完工早 188 秒，兩站都選了暖紙底＋襯線大標。
   健檢另一項實證：此檔曾連續 4 站沒人回寫，防重複檢查形同虛設。
   訂位式登記把這兩種失效一起解掉，因為登記發生在「選中」而不是「完工」。

**混血分工（80/20 主從法則 — 整體風格由主 DNA 決定，副 DNA 只貢獻局部亮點）**：

| 設計要素 | 來源 | 說明 |
|---------|------|------|
| **整體調性與品牌感** | 主 DNA | 網站的第一印象、情緒、定位完全由主 DNA 決定 |
| **Header 結構** | 主 DNA | 導航架構、logo 位置、元素配置 |
| **Hero 版型** | 主 DNA | 首屏體驗不可混亂 |
| **Product Grid** | 主 DNA | 商品展示核心結構 |
| **色溫方向** | 主 DNA | 色彩體系必須統一 |
| **字體類別** | 主 DNA | Display + Body 字體配對 |
| **Footer 結構** | 主 DNA | 信任元素佈局 |
| **Hero 微互動/動效** | 副 DNA | 借鑒副 DNA 的特色動效（如 Lottie 動畫、parallax、hover 效果）|
| **1 個特色組件** | 副 DNA | 從副 DNA 借鑒一個獨特元素（如 Sniff Quiz、age gate、color-curated shop）|
| **成熟度特徵補充** | 副 DNA | 若主 DNA 的 Maturity Signals 不足 12 個，從副 DNA 補充 |

**禁止事項（避免四不像）**：
- ❌ 不可混合兩個 DNA 的色系（色彩必須完全來自主 DNA）
- ❌ 不可混合兩個 DNA 的字體（字體配對必須完全來自主 DNA）
- ❌ 不可用副 DNA 的 Header 或 Footer 結構覆蓋主 DNA
- ❌ 不可從副 DNA 借鑒超過 2 個元素（1 個動效 + 1 個特色組件）
- ❌ 如果兩個 DNA 風格衝突太大（如 Supreme 極簡 + Rifle Paper 插畫風），副 DNA 只貢獻成熟度特徵，不貢獻視覺元素

**風格衝突判斷**：以下 Family 組合視為「風格衝突」，副 DNA 只能貢獻成熟度特徵：
- E (Bold) + D (Artisan) → 衝突
- K (High Fashion) + L (Food) → 衝突
- B (Luxury) + E (Bold) → 衝突
- F (Asian Modern) + K (High Fashion) → 衝突

**組合數**：66 × 65 ÷ 2 = 2,145 種混血 × 6 框架 = **12,870 種獨特變化**

### 1.06 現代 UI 框架選取 (Modern UI Framework Selection)
**必須執行**：每次生成必須使用一個真實的現代 UI 組件庫。

**讀取** [modern-ui-frameworks.md](references/modern-ui-frameworks.md)

**執行流程**：
1. **查看 DNA-框架親和矩陣**：根據 Phase 1.05 選定的 DNA Family，找出 "Strong Fit" 框架
2. **從 Strong Fit 中隨機選取一個**（若 Strong Fit 只有 1 個，50% 機率選 OK Fit）
3. **記錄選取結果**到 `design-system/DECISIONS.md`

**框架決定以下工程要素**：
- Phase 2.1 的安裝指令（每個框架不同）
- 所有 UI 組件必須來自該框架（不可手寫按鈕、輸入框等基礎元件）
- 框架主題必須根據 DNA 色系自定義（不可使用預設主題）

### 1.07 結構隨機化 (Structural Variation)
**必須執行**：DNA 決定風格骨架後，本步驟決定「放哪些區塊、什麼順序、哪些頁、哪種組件排法」，讓結構層也每站不同，不只外觀不同。

**讀取** [structural-variation.md](references/structural-variation.md)

**執行流程**：
1. 生成隨機 `structural_seed`，寫入 `design-system/DECISIONS.md`
2. 用該 seed 選定：首頁區塊組成與順序（Hero/Footer 錨定，中間 5-8 個區塊）、分頁組合（5 個核心頁 + 依商品品類配對的 1-4 個選配頁）、5 組組件變體
3. **腳本強制（不再是人工比對）**：seed 選定的當下跑 `python scripts/design_history.py struct-reserve --brand <品牌> --project <路徑> --seed <seed> --sections <逗號分隔區塊 token> --pages <逗號分隔分頁組合>`——與近 8 站的區塊序列編輯距離 <3、或分頁組合 Jaccard ≥0.8 直接拒絕並非零退出，不再是「完全相同才重抽」那種弱判準。細節見 [uniqueness-guarantee.md](references/uniqueness-guarantee.md)
4. 記錄選定結果到 `design-system/DECISIONS.md`，並追加一筆到 `data/structural-history.json`

**輸出**：本步驟選出的分頁組合，就是 Phase 2 要實作的內容頁清單（非固定頁數，依品類與 seed 浮動 6-9 頁）；會員中心／搜尋頁仍照 [site-architecture.md](references/site-architecture.md) 既有規格加上。

> **與 15 個路由的關係**：本步驟浮動的只有內容頁。[site-architecture.md](references/site-architecture.md) 的 11 類必備頁面、展開後 15 個路由是**下限**（該文第一段：低於此標準視為失敗），這裡選出的品類選配頁是加在下限之上，不是拿來取代它。

### 1.1 商品主題選取 (隨機化深度)

> **數據來源**：`<商品資料目錄>`（呼叫端提供的絕對路徑，本 repo 不收錄實際位置）

**核心流程**：
1. **讀取分類池**：載入 `extracted_products.json`，取得所有商品分類（每個分類的 `id` 欄位，如 `## 1. 傳統風水護身類`）。
2. **排除已用分類**：讀 `data/design-history.json` 每筆既有的 `category` 欄位（`load_products.py` 已改讀這裡，不再是獨立的 `used_categories.json`——那個檔案2026-03 之後沒人更新過，兩套帳必然脫節。細節見 [uniqueness-guarantee.md](references/uniqueness-guarantee.md)）。
3. **隨機抽取一個分類**：從剩餘可用分類中隨機選取一個作為本次電商主題。
4. **提取該分類下的商品**：將該分類的 `items` 陣列寫入 `category_products.json`，作為本次電商網站的商品來源。
5. **記錄已用分類**：本次選取的分類 `id` 要出現在 Phase 1.05 那一步的 `design_history.py reserve --category "<選中的 id>"` 裡（不是另外寫檔）——這一步只確保有真的執行，不再重複寫入。

**輪替機制（Zero Repeat Policy）**：
- 每次抽取後，該分類不會再被抽中，直到**所有分類都被用完**。
- `design-history.json` 是永久紀錄不會清空：當已用分類數 ≥ `extracted_products.json` 的分類總數時，代表一輪跑完，直接進下一輪即可（等同原本「清空重置」的效果）。
- 若用戶未來更新 `extracted_products.json`（新增/刪除分類），系統會自動適應，因為是動態讀取比對。

**商品品牌化包裝**：
- `category_products.json` 中的商品名稱為中文原始名。代理人需依照 Phase 1.4 的品牌創意將商品名**轉譯為英文品牌化商品名**，用於 `mockData.ts`。
- 例：`聖木條` → `Sacred Palo Santo Sticks`、`白水晶柱` → `Clear Quartz Tower`。

**Fallback**：若以上檔案不可用，自行選取一個具有視覺張力的商品品類。

**識別情感**：[奢華精品 / 手工藝 / 自然有機 / 街頭潮流 / 機能運動 / 科技電競 / 極簡美學 / 復古文藝]

### 1.15 NotebookLM 智能設計決策 (Smart Decision Engine)

**執行條件**: 檢查環境變數 `NOTEBOOKLM_ENABLED`
- **`true`** (預設): 啟用 NotebookLM 智能決策（推薦）
- **`false`**: 跳過此步驟，使用傳統隨機設計

**必須執行**: 在生成設計系統前，先從 NotebookLM 獲取數據驅動的設計決策建議。

> ⚠️ **工具現況（2026-06）**：本機**未安裝 NotebookLM MCP**。下方 `notebook_query(...)` 為示意；實跑時改用 `/notebooklm` 技能查詢同一個 notebook_id，或在 `NOTEBOOKLM_ENABLED=false` 時整段跳過（已有 fallback，不影響主流程）。**不要呼叫不存在的 `mcp__notebooklm-mcp__*`。**

**執行流程**:

1. **載入查詢模板**:
   ```python
   # 讀取設計決策查詢模板
   template = read_file("templates/notebooklm_queries/design_decision.txt")
   ```

2. **格式化查詢**:
   ```python
   query = template.format(
       category_name=category['name'],           # 例: "Organic Skincare"
       brand_positioning=identified_emotion,     # 例: "Sustainable Lifestyle"
       target_audience="Eco-conscious millennials",
       price_range="Mid to Premium ($30-$100)"
   )
   ```

3. **查詢 NotebookLM**:
   ```python
   design_rules = notebook_query(  # 透過 /notebooklm 技能；MCP 未裝則跳過
       
       notebook_id="<notebook-id>",
       query=query
   )
   ```

4. **提取決策規則** (從回應中提取 JSON):
   ```json
   {
     "hero_pattern": "Split Hero",
     "colors": {
       "primary": {"h": 120, "s": 35, "l": 45},
       "secondary": {"h": 30, "s": 20, "l": 85},
       "accent": {"h": 25, "s": 70, "l": 50}
     },
     "typography": {
       "display": "Playfair Display",
       "body": "Inter"
     },
     "product_grid": "Hover-Swap",
     "benchmark_brands": ["Allbirds", "Everlane"]
   }
   ```

5. **Anti-Pattern 動態檢查**:
   ```python
   anti_patterns = notebook_query(  # 透過 /notebooklm 技能；MCP 未裝則跳過
       
       notebook_id="<notebook-id>",
       query=read_file("templates/notebooklm_queries/anti_patterns.txt").format(
           category_name=category['name'],
           brand_positioning=identified_emotion
       )
   )
   ```

6. **記錄決策到 `design-system/DECISIONS.md`**:
   ```markdown
   ## 🤖 NotebookLM 智能決策記錄

   ### 查詢時間
   2026-03-18 16:00:00

   ### 輸入參數
   - 商品分類: Organic Skincare
   - 品牌定位: Sustainable Lifestyle
   - 目標客群: Eco-conscious millennials

   ### 決策結果
   - Hero 設計: Split Hero (參考 Allbirds)
   - 主色: Forest Green (H:120, S:35%, L:45%)
   - 字體: Playfair Display + Inter
   - 產品網格: Hover-Swap

   ### 避免的 Anti-Patterns
   - ❌ Carousel Hero (參與度僅 2%)
   - ❌ Neon Colors (不符合永續品牌調性)
   - ❌ Dark Mode Default (不適合自然有機品類)

   ### 參考品牌
   - Allbirds (配色與布局)
   - Everlane (簡潔設計)
   - Patagonia (永續理念視覺化)
   ```

**關鍵優勢**:
- ✅ **有來源可循**: NotebookLM 的回覆會附上引用來源，決策理由可回查
- ✅ **品類精準**: 針對特定商品分類的最佳實踐
- ✅ **可追溯**: 清楚記錄決策理由
- ✅ **避免錯誤**: 動態 Anti-Pattern 檢查

### 1.16 Stitch AI 設計探索 (強烈推薦，解決同質化)

**執行邏輯**:
1. **優先嘗試使用 Stitch** - 先檢查 Stitch MCP 是否可用
2. **自動 Fallback** - 若 Stitch 不可用或連接失敗，自動跳過此步驟
3. **環境變數控制** - 可用 `STITCH_ENABLED=false` 強制跳過（不建議）

**為什麼要使用 Stitch?**
- ✅ **解決設計同質化** - 每次生成 3-5 個專業設計變體
- ✅ **提升設計品質** - 基於真實設計師作品，非純程式碼生成
- ✅ **增加多樣性** - 提供產線之外的第二個設計來源，變體不受本產線既有版型慣性影響
- ✅ **防止重複** - 自動追蹤設計歷史，避免產出相似網站

**何時跳過 Stitch?**
- Stitch MCP 未配置（自動跳過，不中斷）
- Stitch API 連接失敗（自動 Fallback）
- 用戶明確設置 `STITCH_ENABLED=false`（不建議）

**目的**: 利用 Google Stitch AI 生成多個專業設計變體，避免每次產出相似網站。

**執行步驟（代理人必須遵循）**:

```python
# Step 0: 嘗試使用 Stitch（強烈推薦）
try:
    # 1. 快速生成 3 個設計變體（不同風格）
design_prompts = [
    f"Modern {category} ecommerce, Apple minimalism, clean white space",
    f"Bold {category} store, Nike energy, dynamic asymmetric layout",
    f"Organic {category} shop, Allbirds natural, earth tones, soft shapes"
]

# 2. 使用 Stitch MCP 生成設計
stitch_project = mcp__StitchMCP__create_project(title=f"{category}-{timestamp}")

screens = []
for prompt in design_prompts:
    screen = mcp__StitchMCP__generate_screen_from_text(
        projectId=stitch_project['id'],
        prompt=prompt,
        deviceType="DESKTOP"
    )
    screens.append(screen)

# 3. 選擇最具獨特性的設計
# 比對設計歷史 (data/design-history.json)，選擇相似度最低的設計
selected_design = select_most_unique(screens, load_design_history())

# 4. 從 Stitch 提取配色與版型靈感
stitch_html = mcp__StitchMCP__get_screen(
    projectId=stitch_project['id'],
    screenId=selected_design['id']
)

design_inspiration = {
    "colors": extract_colors_from_html(stitch_html),
    "layout_type": identify_layout_pattern(stitch_html),
    "unique_elements": extract_innovative_components(stitch_html)
}

# 5. 記錄到 design-system/DECISIONS.md
# "本次設計參考 Stitch AI 生成的 {layout_type}，
#  主色為 {colors}"
```

**輸出**:
- `design-system/STITCH_INSPIRATION.md` - Stitch 設計參考
- `data/design-history.json` - 設計歷史（防重複）。這一筆在 Phase 1.05 選定基因時就已經用 `design_history.py reserve` 訂位了，這裡不重複追加

**Fallback**: 若 Stitch 不可用，自動跳過，不影響主流程。

### 1.2 🎨 UI-UX-PRO-MAX 設計系統生成 (Design System Generation)
**必須執行**：調用 UI-UX-PRO-MAX 技能生成專業設計系統，並在專案根目錄下生成 `design-system/MASTER.md`。

> **⚠️ 重要：UI-UX-PRO-MAX 是核心設計引擎**
>
> **方式一：使用 SlashCommand（推薦）**
> ```bash
> # 直接調用 ui-ux-pro-max 技能
> /ui-ux-pro-max "[分類] [情感] ecommerce" --design-system --persist -p "[Brand Name]"
> ```
>
> **方式二：直接執行腳本**
> ```bash
> # 確認當前目錄有 .agent/skills/ui-ux-pro-max/
> python .agent/skills/ui-ux-pro-max/scripts/design_system.py "[分類] [情感] ecommerce" --design-system --persist -p "[Brand Name]"
> ```
>
> **方式三：手動讀取 UI UX Pro Max 技能**
> ```python
> # 如果找不到腳本，讀取技能文件並手動生成設計系統
> skill_content = read_file(".agent/skills/ui-ux-pro-max/SKILL.md")
> # 根據技能指引手動建立設計系統
> ```

**檢查清單（執行前必須確認）**：
- [ ] 確認 `.agent/skills/ui-ux-pro-max/` 目錄存在
- [ ] 確認 `.agent/skills/ui-ux-pro-max/scripts/design_system.py` 或 `.agent/skills/ui-ux-pro-max/scripts/search.py` 存在
- [ ] 如果找不到腳本，改為讀取 SKILL.md 並手動生成

**設計自由度**：UI-UX-PRO-MAX 會根據品類和情感自動生成最適合的設計系統，包括色彩、字體、間距、版面等，代理人擁有完全的創意自由。

### 1.2.5 動效基線與美學增援 (Motion Baseline + Distinctiveness Boost)

**必須執行**：讀取 **[motion-system.md](references/motion-system.md)**，依主 DNA Family 選定動效強度層級（Tier 1-3），把選定層級的動效清單寫入 `design-system/DECISIONS.md`。動效引擎統一 `motion/react`，同站禁混搭第二套。

> ⚠️ 2026-08 視覺健檢實證教訓：舊動效清單（`archive/aesthetics-engines.md`）標了 DEPRECATED 後沒有東西接手，產線連續多站零動效、CSS 只剩框架出廠預設 transition。動效基線從此是**必經步驟**，不是加分項。

選用增援（加分項，缺了不中斷主流程）：
- **`/frontend-design`**（全域版）→ 在定 hero 版型與關鍵頁面風格時調用，避開千篇一律的「左文右圖 + 漸層字」長相。比內建 `.agent/skills/frontend-design` 那份新。
- **`/gsap-awwwards-website`** → 需要滾動敘事、複雜編排時**作為編排參考**調用；實作仍一律落在 `motion/react`，不因此引入第二套引擎。

### 1.3 設計決策記錄 (Design Decision Log)
在開始寫代碼前，**必須在 `design-system/DECISIONS.md` 中記錄決策鏈**：
```markdown
## 決策 #1：色系選擇
- 輸入：品類 = [Category], 情感 = [Emotion]
- NotebookLM 靈感：[Benchmark Brand] 的 [Specific Element]
- UI UX Pro Max：Palette #[N] ([Colors])
- Stitch AI 建議：[Design Variant Colors]
- Anti-Pattern 檢查：✅ 通過（未違反 #5~#10）
- 最終決策：[Primary] / [Secondary] / [Accent]

## 決策 #2：版型選擇
- Stitch AI 變體：[Generated Layout Patterns]
- 選用風格：[Layout Style]

## 決策 #3：字體選擇
- UI UX Pro Max 建議：[Typography System]
- Display Font：[Font Name]
- Body Font：[Font Name]
- 連續去重檢查：✅ display 與最近 3 站不同、body 非 Inter、底色系未連續第 3 次（見 Phase 1.05 第 4 條）
- 訂位編號：design-history id=[N]（`design_history.py reserve` 在選定當下回傳的，交付後要 commit）

## 決策 #4：動效層級
- 主 DNA Family：[X] → Tier [1/2/3]（見 motion-system.md）
- 本站動效清單：[列出將實作的項目]
- Easing 曲線：[進場曲線] / [微互動 spring 參數]
```

### 1.4 創意宣言 (Manifesto)
在開始寫代碼前，**必須輸出專屬於本站的創意宣言**：
- **DNA 混血**：`主 DNA-[##] [站名] (Family [X]) × 副 DNA-[##] [站名] (Family [Y])` — 說明主從關係和借鑒了什麼
- **UI 框架**：`[Framework Name]` — 說明使用哪個現代 UI 框架
- **風格名稱**：`[主DNA站名] × [副DNA站名] | [Framework]`
- **設計核心**：基於 [主DNA] 的結構骨架（80%），借鑒 [副DNA] 的 [具體元素]（20%），由 UI-UX-PRO-MAX 生成色系和字體
- **副 DNA 貢獻**：明確列出從副 DNA 借鑒的 1 個動效 + 1 個特色組件
- **成熟度目標**：列出計畫實作的 12+ 個成熟度特徵
- **UX 心理學應用**：列出本站使用的 3 個核心心理法則
- **關鍵字體/色系/Hero 版型**

---

## Phase 2：工程實作（11 類頁面完全實作藍圖，展開為 15 個路由）

### 2.1 環境初始化（框架感知）
```bash
# 建立專案目錄格式：ecommerce-sites/YYYYMMDD-brand（輸出到呼叫端指定的站台輸出目錄底下）
mkdir -p <站台輸出目錄>/$(date +%Y%m%d)-[brand] && cd $_
npm create vite@latest . -- --template react-ts

# 基礎依賴（所有專案通用）
# 動效引擎統一 motion（import 路徑 motion/react，見 references/motion-system.md）；不再裝舊套件名 framer-motion
npm install clsx react-router-dom lucide-react zustand react-hook-form react-helmet-async motion

# 根據 Phase 1.06 選定的框架安裝對應依賴：
# 若 shadcn/ui:
#   npm install -D tailwindcss@^3 postcss autoprefixer && npx tailwindcss init -p && npx shadcn@latest init
# 若 DaisyUI:
#   npm install -D tailwindcss@^3 postcss autoprefixer daisyui && npx tailwindcss init -p
# 若 Radix UI:
#   npm install @radix-ui/themes @radix-ui/react-dialog @radix-ui/react-dropdown-menu
# 若 Mantine:
#   npm install @mantine/core @mantine/hooks @mantine/form -D postcss postcss-preset-mantine
# 若 HeroUI（2025 年初由 NextUI 改名，舊套件 @nextui-org/* 已棄置，裝了就是死庫）:
#   npm install @heroui/react framer-motion -D tailwindcss@^3 postcss autoprefixer
#   （framer-motion 是 HeroUI 的 peer 依賴，僅供元件庫內部使用；站內自寫動效仍用 motion/react）
# 若 Aceternity:
#   npm install -D tailwindcss@^3 postcss autoprefixer && npx tailwindcss init -p
#   (then copy Aceternity components manually)
```

### 2.2 核心資產與數據 (100% 完整度)
1. **Types (`src/types/index.ts`)**: 嚴格遵循 **[woocommerce-api.md](references/woocommerce-api.md)** 的 Interface。
1.9 **部署設定檔（必做，不可省略）**：專案根目錄與 `dist/` 都要有 `vercel.json`：

```json
{
  "rewrites": [{ "source": "/(.*)", "destination": "/index.html" }]
}
```

> **沒有這個檔，部署上去只有首頁能開，其他頁全部 404。**
> 這是單頁應用的固定要求：所有網址都要交給首頁的程式去處理路由。
> 2026-08-04 兩個站因為漏掉這一步，上線後除了首頁全部打不開。
> **不要靠記憶，生成階段就寫進去。** 詳見 `PITFALLS.md` 第 14 條。

2. **Mock Data (`src/data/mockData.ts`)**: 商品數依模式決定，包含分類、描述、多圖。

   **商品數量的兩種模式**（開工前先確認是哪一種，不確定就問）：

   | 模式 | 商品數 | 什麼時候用 |
   |---|---|---|
   | **展示模式**（預設） | **6 到 10 個** | 給人看的、驗證產線的、還沒要賣的 |
   | 上架模式 | 12 個以上 | 真的要開賣、商品來源已確定 |

   > **鐵則：圖的品質優先於商品數量。**
   > 22 個商品配 22 張湊數的圖，比 8 個商品配 8 張像樣的圖差得多。
   > **如果圖產不出來，先減商品數，不要降圖的品質。**
   > 商品之後隨時可以自己新增，但一個看起來沒做完的站會直接毀掉第一印象。
3. **SafeImage (`src/components/common/SafeImage.tsx`)**: **必備件**，處理所有圖片載入錯誤，顯示帶有產品名的精美佔位塊。

### 2.3 狀態管理 (Zustand)
- `useCart`: 加入、移除、修改數量、計算 Tax/Shipping。
- `useAuth`: 模擬登入/註冊，持久化 Token。
- `useSearch`: 處理全局即時關鍵字過濾。

### 2.4 11 類頁面全覆蓋開發（展開為 15 個路由，不可跳過）
你必須依照以下路由結構完成所有頁面：
- **Layer A (Core)**: 
  - `/` (Home): 帶有 `generate-image` 產出的高品質 Banner。
  - `/shop`: 商品網格，支援分類 Filter 與 Sort。
  - `/product/:slug`: 詳情頁，含內容豐富的 Description (Rich Text)。
  - `/cart`: 側邊欄抽屜 (Drawer) + 獨立頁面。
  - `/checkout`: **三步驟實體功能** (Shipping -> Payment -> Success)。
  - `/search`: 獨立搜尋頁，含 Search Results & Not Found 狀態。
- **Layer B (Member)**:
  - `/account/login`, `/account/register`
  - `/account/orders`, `/account/profile` (遵循 **[member-zone.md](references/member-zone.md)**)
- **Layer C (Policy)**:
  - `/policies/*` (FAQ, Shipping, Returns, Privacy, About) - 內容必須根據品牌語氣生成真實段落。

### 2.5 成熟度特徵實作 (Maturity Signals Implementation)
**必須執行**：讀取 [maturity-signals.md](references/maturity-signals.md)

根據 Phase 1.05 選定的 DNA 的 Maturity Signals + 通用清單，實作 ≥ 12 個成熟度特徵。

**同時必須檢查「Forbidden AI Tells」清單**，確保無任何 AI 生成痕跡：
- ❌ 不可出現 "Welcome to [Brand]" 作為 Hero 標題
- ❌ 不可所有商品描述相同長度和結構
- ❌ 不可缺少 favicon
- ❌ 不可 Footer 只有連結（需要 newsletter、社群、付款圖示）
- ❌ 不可所有商品相同價格格式（混合 $29、$29.99、$30.00）
- ⚖️ 促銷/折扣商品：**只有在具備過去 30 天最低價基準時才可產生劃線原價或 `% OFF`**（見 [anti-patterns.md §L1](references/anti-patterns.md)）。Mock 資料站不具備基準 → **一律只顯示現價，不劃線**。價格層次靠品項間的真實價差與 Bundle 呈現，不靠假折扣。

### 2.55 動效基線實作 (Motion Baseline，不可跳過)
**必須執行**：依 Phase 1.2.5 選定的 Tier，實作 **[motion-system.md](references/motion-system.md)** 的動效清單。四項最低要求缺一即 FAIL：
1. 滾動進場（首頁 ≥ 4 區塊 `whileInView`，清單元素 stagger）
2. 有意圖的 hover（商品卡＝圖片縮放或第二圖 crossfade ＋ 位移或陰影；不是只變色）
3. 禁用預設 easing（一律指定曲線或 spring 參數，CSS 曲線註冊進 Tailwind config）
4. `<MotionConfig reducedMotion="user">` 包住 App 根部

**建置後自查**：grep 編譯產物必須出現非出廠預設的 `cubic-bezier`；瀏覽器實開滾動一輪，進場與 hover 肉眼可見。

### 2.6 UX 心理學實作清單
在實作每個頁面時，**必須檢查以下電商心理學要素**（詳見 **[ux-psychology-ecommerce.md](references/ux-psychology-ecommerce.md)**）：

| 頁面 | 必須實作的心理法則 |
|------|-------------------|
| Home | Von Restorff (CTA 唯一高亮) + Serial Position (首末 CTA) |
| Shop | Hick's Law (Filter ≤ 6) + Miller's Law (每行 ≤ 4 列) |
| Product | Anchoring Bias (⚖️ 有 30 天基準才劃線，否則用 Bundle/系列價差錨定) + Social Proof (真實評分，無資料用空狀態) + Scarcity (⚖️ 接真實庫存，否則只顯示 In/Out of Stock) |
| Cart | Zeigarnik (進度感) + Goal Gradient (免運門檻進度條) |
| Checkout | Tesler's Law (自動偵測) + Peak-End Rule (成功頁動畫) |
| Search | Postel's Law (容錯輸入) + Doherty Threshold (即時回饋) |

### 2.7 文案去 AI 味過濾 (Anti-AI Copy Pass) — 品牌文案質感最關鍵一關

> **為什麼最關鍵**：文字是 AI 第一露餡點，比版面更會洩底。所有 hero 標語、商品描述、About、FAQ、政策頁文案寫完後，**必須整批過一次去 AI 味**，不可裸交模型初稿。

**執行流程**：
1. **先用 `/generic-language-killer`** 掃整批英文文案，清掉 AI 通用語（self-sustaining、game changer、elevate your、unleash、in today's world… 這類空形容詞與陳腔）。
2. **再用 `/copywriting`** 重寫 hero 標語與商品描述，注入品牌觀點與具體畫面（對齊本站 DNA 的品牌聲音），取代「Welcome to / Shop Now」這種無記憶點文字。
3. **最後用 `/copy-editing`** 收尾，確保語氣一致、長短句有節奏、無重複句構。

**禁令（對齊 [site-quality-rubric.md](references/site-quality-rubric.md) §3 品牌文案 x2）**：
- ❌ 禁破折號黏兩個短句當節奏
- ❌ 禁「不是 A，而是 B」句型
- ❌ 禁假評論「首字母縮寫 + 美國城市州」格式（Elena M., Portland OR）→ 要真資料或不放
- ❌ 禁所有商品描述同長度同結構（混合長短與切入角度）

**深度增援（選用，內容要更有血肉時）**：
- `/avatar-extraction` → 先定義客群痛點，讓 About 與商品文案有真實觀點
- `/marketing-psychology`、`/objection-crusher` → FAQ 與商品頁回應真實異議，而非泛泛而談

> **驗收**：交付前的 rubric §3 若 < 4 分，回到本關重過，修到過為止。

---

## Phase 3：圖片與 SEO 強化

### 3.1 多層圖片生成系統 (Multi-tier Image Fallback)

**鐵律**：主要視覺、分類封面、關鍵產品不可使用 Placeholder。

**執行腳本**: `python scripts/generate_images_fallback.py`

#### 圖片生成策略（真圖優先，反指紋）

> **⚠️ 反 AI／反量產指紋鐵律**：Unsplash 圖庫圖可被反向圖搜，一搜就露出「模板站」指紋，是量產站最大破綻。site-quality-rubric 的正例全是真實／獨家圖。因此**生成獨家圖 > 真實產品圖 > 圖庫圖**。

| 優先級 | 方法 | 品質 | 備註 |
|--------|------|------|------|
| **Priority 1** | **獨家生成圖**（generate-image / nano-banana，或 `/ads-photoshoot` 商品圖） | ⭐⭐⭐⭐⭐ | **首選**，每站獨一無二，無法反向圖搜 |
| **Priority 2** | **真實產品圖**（客戶提供的實品圖／CDN 真品圖） | ⭐⭐⭐⭐⭐ | 有現成真品圖時直接用，最真 |
| Fallback 1 | Unsplash API | ⭐⭐⭐⭐ | 真圖管線都不可用時才用；**量產時每站換不同 query，禁止跨站共用同一張** |
| Fallback 2 | Placeholder.com | ⭐⭐⭐ | hero／分類封面／關鍵商品禁用，僅次要位置保底 |
| Fallback 3 | 本地漸變 | ⭐⭐ | 最終保底方案 |

> **執行邏輯**：先試 `/generate-image` 或 `/ads-photoshoot` 生成 hero 與分類封面；該品牌若有真品圖則優先採用；兩者皆不可用才退 `python scripts/generate_images_fallback.py` 走 Unsplash。詳見 [PITFALLS.md](PITFALLS.md) 方案 D。

#### 執行範例

1. **單張圖片生成**：
   ```bash
   python scripts/generate_images_fallback.py \
     --category "Sustainable Home" \
     --type "hero" \
     --output public/images/hero.png \
     --width 1920 --height 1080
   ```

2. **批次生成（推薦）**：
   ```bash
   # 建立配置檔案 image_config.json
   {
     "category": "Sustainable Home",
     "images": [
       {"type": "hero", "filename": "hero.png", "width": 1920, "height": 1080},
       {"type": "category1", "filename": "cat1.png", "width": 800, "height": 600},
       {"type": "category2", "filename": "cat2.png", "width": 800, "height": 600},
       {"type": "category3", "filename": "cat3.png", "width": 800, "height": 600}
     ]
   }

   # 執行批次生成
   python scripts/generate_images_fallback.py --batch image_config.json
   ```

#### 自動降級流程

```
1. 獨家生成圖（Priority 1）／真實產品圖（Priority 2）
   ✅ 首選，每站獨一無二

   ↓ 兩者皆不可用時

2. Unsplash（Fallback 1）
   查詢: "sustainable+eco+home"
   ✅ 每站換不同 query，禁止跨站共用同一張

   ↓ 如果失敗

3. Placeholder（Fallback 2）
   生成: "Sustainable Home - Hero"
   ⚠️ hero／分類封面／關鍵商品禁用，僅次要位置保底

   ↓ 如果失敗

4. 本地漸變（Fallback 3）
   ✅ 最終保底
```

> 這一段的順序與上方表格一致。`generate_images_fallback.py` 本身只涵蓋 Unsplash 之後的退路，
> Priority 1／2 由 `/generate-image`、`/ads-photoshoot` 或客戶提供的實品圖在呼叫此腳本前完成。

> **實作細節**: 見 [scripts/generate_images_fallback.py](scripts/generate_images_fallback.py)

### 3.2 SEO 與 Schema.org
- 每個頁面由 `react-helmet-async` 動態生成 Title/Meta。
- 商品詳情頁置入 `application/ld+json` 格式的 Product Schema。

---

## Phase 4：交付驗收（100% 覆蓋率測試）

> **品質目標**：確保 15 個路由 100% 可點擊、100% 無死圖、100% 邏輯連貫。

### 4.0 一鍵自動化測試（推薦）

**執行總編排腳本**: `python scripts/auto_test_and_fix.py`

此腳本會自動執行所有驗收流程：

```
Phase -1: Preflight Check        ✅
Phase  1: Build + Auto Fix        ✅ (自動修復 TypeScript 錯誤)
Phase  2: Image Generation        ✅ (多層備援)
Phase  3: Start Dev Server        ✅ (自動啟動 http://localhost:5173)
Phase  4: Quality Checklist       ✅ (電商品質檢查)
Phase  5: Generate Report         ✅ (AUTO_TEST_REPORT.json)
```

**執行時間**: 2-3 分鐘（粗估，未做正式計時；實際受站台規模與 build 重試次數影響）

**報告輸出**: `AUTO_TEST_REPORT.json`
- 包含所有階段的執行結果
- 標記關鍵失敗項目
- 提供詳細錯誤資訊

#### 手動執行模式（進階）

如需單獨執行某個階段：

### 4.1 Build 自動修復 Loop

**執行腳本**: `python scripts/auto_fix_build.py`

**自動修復能力**:
- ✅ TS2304: 缺少 import 聲明（自動添加 React, useState, Link 等）
- ✅ TS7006: 參數類型註解缺失（自動推斷 FormEvent）
- ✅ TS6133: 未使用變數（自動加 `_` 前綴）
- ✅ TS7010: 缺少返回類型（自動添加 `void`）
- ✅ TS2339: 屬性不存在（自動添加環境變數類型聲明）

**執行流程**:
```
1. 執行 npm run build
   ↓ 發現 5 個 TypeScript 錯誤
2. 自動修復 3 個錯誤
   ↓ 重新執行 build
3. 發現 2 個錯誤
   ↓ 自動修復 2 個錯誤
4. ✅ Build 成功
```

**最大迭代次數**: 5 次（防止無限循環）

> **若 TypeScript 錯誤無法自動修復，必須手動檢查並修正代碼。**

### 4.2 自動化電商品質檢查
執行腳本：`python scripts/ecommerce-checklist.py <project_path> --preview`

這支腳本就是本文開頭說的 **8 層品質門檻**，一次執行跑完八層：
建置 → P1 路由完整性 → P2 電商邏輯 → P3 圖片健康度 → P4 SEO/Schema → P5 反面樣式 → P6 安全基本項 → P7 UK/EU 合規。

**計分與否決是兩件事，別搞混**（實際行為見 `scripts/ecommerce-checklist.py` 的 `print_scorecard`）：
- **總分**：八層一起算，`通過層數 ÷ 未跳過層數 × 100`，75 分以上才算過。P7 也在分母與分子裡。
- **否決**：P7 另外標記為 `blocking`。它沒過就直接回傳失敗，**分數再高也一樣不得交付**。

以下列出其中三層的細節：

- **P1 Deep Scan**：會檢查物理文件 `src/pages/` 是否與路由定義對應。
- **P3 Asset Scan**：會檢查 `public/` 目錄，抓出所有死圖。
- **P7 UK/EU Compliance Gate**：抓無 30 天基準的劃線價／`% OFF`、假倒數、假庫存數字、假瀏覽人數、預設勾選加購。
  **渲染端掃 `src/`，資料端掃 `data/`、`public/`、`src/data/` 與根目錄 JSON**（商品資料裡帶值的 `compareAtPrice`／`salePrice` 才是源頭，只堵畫面沒用）。
  **這關是 blocking，不看總分**：只要有違規，即使總分 ≥ 75 也會回傳 exit code 1，不得交付。
  有真實依據時，把逐 SKU 的 30 天最低售價寫進專案的 `compliance/EVIDENCE.md`（格式與必填欄位見 anti-patterns.md §L1），通過驗證的 SKU 才會改為人工覆核；空殼檔不予豁免。

### 4.3 瀏覽器子代理深度測試 (Active Scanning)
**必須執行**：啟動伺服器後，呼叫 `browser_subagent` 執行以下任務：
1. **導航測試**：點擊 Header 的每個連結（Home, Shop, Account, Cart, Search），確保頁面顯示正確（無 404）。
2. **圖片掃描**：捲動首頁，確認所有 `SafeImage` 都渲染成功。
3. **商務流測試**：
   - 進入 Shop 頁面 -> 點擊一個產品 -> 進入產品詳情頁。
   - 點擊「Add to Cart」 -> 開啟購物車確認商品存在。
   - 點擊「Checkout」 -> 確保能進入結帳第一步。

**若子代理回報任何頁面無法載入或圖片崩潰，必須立即修復。**

### 4.4 視覺與性能審計
```bash
# 執行 Kit 的 UX 與 SEO 深度檢查
python .agent/skills/frontend-design/scripts/ux_audit.py <project_path>
python .agent/skills/seo-fundamentals/scripts/seo_checker.py <project_path>
```

### 4.5 最終驗證與自動預覽 (Visual Final Check)
**必須執行**：在交付前，自動啟動伺服器並使用 `browser_subagent` 進行 100% 覆蓋率掃描。

```bash
# 自動啟動伺服器 (Auto-start preview server)
python .agent/scripts/auto_preview.py start 5173
```

使用 `browser_subagent` 驗證（參見 4.3 條目）：
- [ ] 15 個路由是否 100% 可載入？
- [ ] 圖片是否 100% 無死圖？
- [ ] 購物車與結帳按鈕是否 100% 有響應？


### 4.6 品質計分卡 & 設計決策交付

> **交付前強制自評**：依 **[site-quality-rubric.md](references/site-quality-rubric.md)** 用 browser_subagent 截圖（首頁／商品詳情／結帳／行動版）逐維度打分。原創性、設計品質、品牌文案三個權重維度只要任一 < 4 分，或任何禁令出現，就回去修，修到過為止才可交付。

#### 4.6.2 🧬 DNA 忠實度檢查（2026-08 新增，交付驗收 A 區 11.6，FAIL 就不得交付）

> **要擋的事**：選了一個 DNA，做出來的東西卻不照它做，而且沒有任何東西會叫。
> 2026-08-04 實測：某站選了 DNA-44（條目寫「White/light neutral base」＋「Bold sans headings」），
> 實際交出暖紙底 #f5f3ee ＋ Newsreader 襯線標題。版面沒壞、字體有載入、驗收全綠。

```bash
npm run build                                    # 沒有編譯產物就沒東西可驗
python scripts/check_dna_fidelity.py <project_path>
```

腳本三邊對照：**編譯後 CSS 的實際底色與字體 ↔ `design-history.json` 登記的主 DNA ↔ `real-ecommerce-dna.md` 那個 DNA 條目的規格**。引不出來就 FAIL，會印出「規格說 X、實際是 Y」。
- 它自己會先造出故意違反 DNA 的假樣本做變異測試，抓不到就中止並宣告本次結果不算數。
- 讀不到底色、認不出字體類別、DNA 條目寫不清楚，**一律判 FAIL**：判不出來與做錯了，對交付的意義完全一樣。
- **由驗收角色跑，不是產出者自己跑。** FAIL 要回 Phase 1.05／設計階段重做，不是改 DNA 編號來遷就結果。

#### 4.6.5 🎨 美學直覺把關 (Taste Gate) — rubric 之後最後一道閘門

> **定位**：rubric 是「規則化評分」（量化每個維度給分），但 AI 套版味是規則抓不滿的。rubric 打完分數後，**必須再過一次設計品味裁決**。兩者互補、缺一不可：rubric 在前（先量化過關），taste skill 在後（最終美學直覺裁決）。

**調用技能**：全域版 **`/frontend-design`**（路徑 `~/.claude/skills/frontend-design/SKILL.md`，Anthropic 反通用 AI 美學版，比 `.agent/skills/frontend-design` 那份新）。其核心職責就是判斷並避開 generic AI aesthetics，正是「美學最終把關」最對口的技能。與 Phase 1.2.5 生成階段所用的同一支技能，前後呼應。

**執行流程**：
1. 沿用 §4.6 rubric 自評時 browser_subagent 截的**同一組圖**（首頁／商品詳情／結帳／行動版），不另截。
2. 把這幾張圖餵給 `/frontend-design`，請它以「這站看起來像不像 AI 套版、美學是否及格」為唯一問題做直覺裁決，逐張指出露餡點（generic 字體、紫漸層、左文右圖樣板、千篇一律的卡片、缺乏記憶點等）。
3. 取得「過 / 不過」判定與具體修改建議。

**過關條件（與 rubric 同等是 blocking gate）**：
- ✅ `/frontend-design` 判定「不像 AI 套版、美學及格」→ 通過，進入最終報告。
- ❌ 若判定「像 AI 套版 / 美學不及格」→ **回到設計階段（Phase 1.2 / 1.2.5）依其建議重做**，修完重跑 §4.6 rubric 與本 §4.6.5 taste gate，兩關都過才可交付。

> **關係總結**：`quality-scorecard`（產出計分卡）← `site-quality-rubric`（規則化評分，§4.6）← **`/frontend-design` taste gate（美學直覺裁決，§4.6.5，最後一道）**。三者依序把關，taste gate 是交付前的最終門檻。

最終報告必須包含：
1. **交付概覽**：品牌名稱、美學風格、**預覽網址 (http://localhost:5173)**。
2. **品質計分卡**（參考 **[quality-scorecard.md](references/quality-scorecard.md)** 模板）
3. **設計決策記錄**（`design-system/DECISIONS.md`）
4. **品牌 DNA 摘要**（上傳至 NotebookLM MEMORY）

### 4.7 ⏸️ 階段一完成 — 前端驗收暫停點

> **🔴 強制暫停：不得自動進入 Phase 5。**

Phase 4 全部通過後，向用戶輸出以下訊息：

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ 階段一完成：前端已通過所有品質門檻
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📋 品質計分卡：[見上方報告]
🌐 預覽網址：http://localhost:5173

請驗收前端。確認 OK 後，回覆以下任一指令進入下一階段：

  「繼續後端」→ 進入階段二（注入 WooCommerce 服務層）
  「生成部署包」→ 跳到階段三（生成 WP 部署包）
  「都做」→ 階段二 + 三全部執行

⚠️ 階段二會修改現有代碼（注入 Service 層），建議先確認前端無需調整。
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

**等待用戶明確確認後才繼續。不可擅自進入 Phase 5。**

---

## Phase 5：後端服務層注入（階段二）

> **前置條件**：用戶已驗收階段一前端，並明確指示「繼續後端」。
> **核心原則**：雙模式（Mock / Live）— `VITE_WOO_URL` 為空走 Mock，有值走 WooCommerce API。
> **參考規格**：**[service-layer-spec.md](references/service-layer-spec.md)**、**[cart-hybrid-spec.md](references/cart-hybrid-spec.md)**

### 5.0 後端注入前置檢查

```
檢查清單：
✅ 前端 build 通過（npm run build 無錯誤）
✅ 15 個路由正常運作
✅ 現有 Zustand stores 正常（useCartStore, useAuthStore）
✅ mockData.ts 符合 WooProduct interface
```

### 5.1 注入共用 API 層：`src/services/api.ts`

建立統一的 API 基礎層（詳見 [service-layer-spec.md](references/service-layer-spec.md)）：

- `isMockMode()` — 偵測 `VITE_WOO_URL` 是否存在
- `wooFetch(endpoint, options)` — 統一請求包裝器
  - Live 模式：自動加 base URL + Nonce + credentials
  - 401 處理：自動登出 + 重導登入頁
  - 429 處理：指數退避重試（最多 3 次）
  - 網路錯誤：graceful fallback
- `getNonce()` — 從 WP REST discovery 端點取得 Nonce
- `refreshNonce()` — Nonce 過期時自動重取

### 5.2 改寫 ProductService：`src/services/product.ts`

將現有直接讀取 mockData 的邏輯改為雙模式 Service：

| 方法 | Mock 模式 | Live 模式 |
|------|-----------|-----------|
| `getProducts(params)` | 從 mockData 篩選、分頁 | `GET /wc/v3/products?per_page=&page=&category=&search=&orderby=` |
| `getProduct(idOrSlug)` | mockData.find() | `GET /wc/v3/products/<id>` 或 `?slug=<slug>` |
| `getCategories()` | 從 mockData 提取唯一分類 | `GET /wc/v3/products/categories` |
| `getFeaturedProducts()` | mockData.filter(on_sale) | `GET /wc/v3/products?on_sale=true&per_page=8` |

**回傳型別統一使用 `WooProduct` interface**（來自 [woocommerce-api.md](references/woocommerce-api.md)）。

### 5.3 注入混合購物車：`src/services/cart.ts`

**這是最複雜的 Service**，詳見 **[cart-hybrid-spec.md](references/cart-hybrid-spec.md)**。

三種運作模式：

| 條件 | 儲存 | API |
|------|------|-----|
| Mock 模式（無 `VITE_WOO_URL`） | localStorage | 無 |
| Live 模式 + 未登入 | localStorage | 無 |
| Live 模式 + 已登入 | WooCommerce Store API | `/wc/store/v1/cart/*` |

**關鍵邏輯 — 登入後合併**：
1. 讀取 localStorage 購物車項目
2. 讀取 WC 遠端購物車（可能有上次的項目）
3. 逐一合併：遠端已有 → 取較大數量；遠端沒有 → POST add-item
4. 清空 localStorage
5. 合併失敗的項目保留在 localStorage，下次重試

**改寫 `useCartStore`**：
- 原本直接操作 Zustand state → 改為透過 CartService
- 保留所有現有 UI 行為（Cart Drawer、Cart Page）
- 新增 `mergeLocalToRemote()` action
- Header 購物車 icon badge 數字來源不變

### 5.4 強化 AuthService：`src/services/auth.ts`

在 [member-zone.md](references/member-zone.md) 現有規格基礎上強化：

- **新增**：`refreshToken()` — JWT 到期前自動刷新
- **新增**：Token 到期時間追蹤（解碼 JWT payload 的 exp）
- **新增**：登入成功後自動呼叫 `CartService.mergeLocalToRemote()`
- **新增**：登出時清除遠端購物車 session
- **保留**：Mock 模式帳號 `demo@example.com / demo1234`
- **保留**：`useAuth` Hook + `ProtectedRoute` 元件

### 5.5 注入 OrderService：`src/services/order.ts`

| 方法 | Mock 模式 | Live 模式 |
|------|-----------|-----------|
| `getOrders(page, perPage)` | mockOrders 分頁 | `GET /wc/v3/orders?customer=me&per_page=&page=` (Bearer Token) |
| `getOrder(id)` | mockOrders.find() | `GET /wc/v3/orders/<id>` (Bearer Token) |

需要認證，未登入時重導至登入頁。

### 5.6 注入 CheckoutService：`src/services/checkout.ts`

| 方法 | Mock 模式 | Live 模式 |
|------|-----------|-----------|
| `getPaymentMethods()` | `[{ id: "placeholder", title: "Payment Gateway (Coming Soon)" }]` | `GET /wc/store/v1/checkout` → `payment_methods` |
| `getShippingRates(address)` | 固定 flat rate $5.00 | `POST /wc/store/v1/cart/select-shipping-rate` |
| `submitOrder(payload)` | 假成功 + 假 order ID | `POST /wc/store/v1/checkout` |

**金流執行區塊**：標記為 `// TODO: Custom payment gateway integration point`
用戶自研金流完成後在此對接，前端無需其他改動。

### 5.7 改寫 Zustand Stores 串接 Service 層

將所有 Zustand store 改為透過 Service 層操作：

```
useProductStore → ProductService.getProducts() / getProduct() / ...
useCartStore    → CartService.addItem() / removeItem() / mergeLocalToRemote() / ...
useAuthStore    → AuthService.login() / register() / refreshToken() / ...
useOrderStore   → OrderService.getOrders() / getOrder()
useCheckoutStore→ CheckoutService.getPaymentMethods() / submitOrder() / ...
```

**UI 元件不直接呼叫 API**，一律透過 Store → Service → API。

### 5.8 注入環境變數範本：`.env.example`

```env
# ═══════════════════════════════════════════
# E-Commerce Configuration
# ═══════════════════════════════════════════

# WordPress / WooCommerce Backend URL
# Leave EMPTY for Mock mode (frontend-only demo)
# Fill in to connect to real WooCommerce backend
VITE_WOO_URL=

# ═══════════════════════════════════════════
# Backend-only (NEVER in frontend bundle)
# Used by scripts/sync-to-wp.mjs only
# ═══════════════════════════════════════════
WOO_CONSUMER_KEY=
WOO_CONSUMER_SECRET=
```

### 5.9 後端對接 QA

**必須驗證 Mock 模式全流程可跑**：

```bash
python scripts/validate_mock_flow.py <project_path>
```

驗證項目：
- [ ] 商品列表載入（ProductService Mock）
- [ ] 商品詳情頁載入
- [ ] 加入購物車 → 購物車 Badge 更新
- [ ] 購物車頁面顯示正確商品與數量
- [ ] 更新數量 / 移除商品
- [ ] Mock 登入（demo@example.com / demo1234）
- [ ] 登入後購物車合併（localStorage → 保持）
- [ ] 會員中心 / 訂單列表 / 個人資料
- [ ] 結帳流程（地址填寫 → 金流選擇 → 模擬成功）
- [ ] 登出後購物車回到 localStorage 模式
- [ ] `.env.example` 存在且格式正確
- [ ] `npm run build` 無錯誤

### 5.10 真連線驗證（接了後端才做，但接了就必做）

> 5.9 驗的是假資料模式，它從頭到尾沒有對真的後端發過一個請求。
> 連線壞掉的站也能通過 5.9，所以 5.9 全綠**不等於**接得通。

```bash
# 站要先跑起來（dev server 或把 dist 用靜態伺服器服務）
python scripts/validate_live_flow.py <project_path> --site-url http://localhost:5174
```

驗證項目：
- [ ] **金鑰沒有被編譯進 `dist/`**（掃 `ck_` `cs_` `consumer_key` `sk-` `ghp_` `AKIA` 私鑰區塊）
- [ ] **畫面上的商品真的來自後端**：腳本會把後端某個商品改名成一組隨機碼，
      確認那組碼出現在畫面上，再改回原名並確認它消失

兩項都自帶偵測能力測試：先造出應該被抓到的樣本，抓不到就中止並宣告結果不算數。

**什麼情況會失敗**：
- 金鑰出現在建置產物裡 → FAIL，且**不得交付**，這是會外洩客戶個資的等級
- 前端完全沒呼叫後端 → FAIL，腳本會直接指出「在用寫死的假資料」
- 有呼叫後端但畫面沒更新 → FAIL，代表讀取失敗後靜默退回假資料
- 沒裝 playwright 或找不到後端憑證 → FAIL，不會假裝通過

純展示站（沒跑 Phase 5）用 `--secrets-only` 只跑第一項。

**全部通過後輸出**：

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ 階段二完成：後端服務層已注入
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🔄 模式：Mock（前端獨立運作）
📋 Service 層：5/5 已注入
🛒 混合購物車：已就緒
🔐 JWT 認證：已就緒
💳 金流接口：已預留（待自研金流對接）
📦 .env.example：已生成

🚀 接上真實 WooCommerce：
   只需在 .env 填入 VITE_WOO_URL=https://your-wp-site.com

要繼續生成 WP 部署包嗎？回覆「生成部署包」進入階段三。
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## Phase 6：WordPress 部署包生成（階段三，可選）

> **前置條件**：用戶明確指示「生成部署包」。
> **目標**：生成一鍵部署 WP + WooCommerce 後端的完整包，租主機後跑一個腳本即可。
> **參考規格**：**[wp-plugin-pool.md](references/wp-plugin-pool.md)**

### 6.1 生成目錄結構

```
wp-deployment/
├── docker-compose.yml          ← WP + MySQL + phpMyAdmin (本地測試用)
├── setup.sh                    ← 一鍵安裝主腳本
├── wp-cli-setup.sh             ← WP 設定自動化
├── .env.wp.example             ← WP 環境變數範本
├── plugins/
│   ├── required.json           ← 必裝外掛清單
│   └── random-pool.json        ← 隨機外掛池定義
├── theme/
│   └── functions.php           ← CORS + REST API 自訂設定
├── scripts/
│   └── sync-to-wp.mjs          ← 商品批量上傳（從 mockData）
└── DEPLOYMENT.md               ← 部署完整指南
```

### 6.2 Docker Compose（本地測試）

生成 `docker-compose.yml`：
- WordPress (latest) on port 8080
- MySQL 8.0 with persistent volume
- phpMyAdmin on port 8081
- 共享 network
- `.env.wp.example` 包含所有需要的變數

### 6.3 必裝外掛 + 隨機外掛池

**必裝（每次都裝）**：
- WooCommerce（核心電商）
- Simple JWT Login（前端 JWT 認證）
- WooCommerce Blocks（Store API 支援）
- WP Mail SMTP（交易信件）
- Wordfence Security（基本安全）

**隨機外掛池**（詳見 [wp-plugin-pool.md](references/wp-plugin-pool.md)）：
從 8 個分類中隨機抽取 3-5 個外掛：
- SEO（抽 1）：Yoast / Rank Math / AIOSEO / SEO Framework / Squirrly
- 效能（抽 1）：WP Super Cache / W3 Total / LiteSpeed / WP Fastest / Autoptimize
- 表單（抽 0-1）：CF7 / WPForms / Forminator / Ninja Forms
- 社群（抽 0-1）：AddToAny / Social Warfare / Shareaholic
- 備份（抽 0-1）：UpdraftPlus / BackWPup / Duplicator
- 圖片優化（抽 0-1）：Smush / ShortPixel / Imagify / EWWW
- 多語（抽 0-1，機率 0.3）：Polylang / TranslatePress / GTranslate
- 雜項真實感（抽 1-2）：Akismet / CookieYes / MonsterInsights / Really Simple SSL / Classic Editor ...

**Seed 邏輯**：使用與 DNA 選取相同的 seeded random，記錄到 `design-history.json`。

### 6.4 CORS + REST API 設定

生成 `theme/functions.php`：
- 允許前端域名的 CORS（localhost:5173 + 正式域名）
- `Access-Control-Allow-Credentials: true`
- 允許 Headers：Content-Type, Nonce, Authorization
- 允許 Methods：GET, POST, PUT, DELETE, OPTIONS

### 6.5 商品同步腳本

生成 `scripts/sync-to-wp.mjs`（詳見 [woocommerce-api.md](references/woocommerce-api.md)）：
- 讀取前端的 `mockData.ts` 中的商品資料
- 批量建立 WooCommerce 分類
- 批量建立 WooCommerce 商品
- 圖片 URL 保持不變（Unsplash URLs 直接用）
- 輸出同步結果報告

### 6.6 部署指南 DEPLOYMENT.md

自動生成的部署文件，包含：

```markdown
# 部署指南

## 前置需求
- PHP 8.0+ 主機（或 Docker）
- MySQL 5.7+ / MariaDB 10.3+
- 至少 512MB RAM

## 本地測試（Docker）
1. cd wp-deployment
2. cp .env.wp.example .env.wp
3. docker-compose up -d
4. 等待 30 秒...
5. bash setup.sh

## 正式部署（主機）
1. 在主機安裝 WordPress
2. bash wp-cli-setup.sh
3. 在前端 .env 填入 VITE_WOO_URL=https://your-domain.com
4. node scripts/sync-to-wp.mjs
5. 完成！

## 已安裝的外掛
[自動列出必裝 + 隨機選取的外掛]

## 安全注意事項
- 修改預設管理員密碼
- 設定 Wordfence 防火牆
- 確認 CORS 只允許你的前端域名
```

### 6.7 階段三完成報告

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ 階段三完成：WP 部署包已生成
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📁 部署包位置：<project>/wp-deployment/
📋 必裝外掛：5 個
🎲 隨機外掛：[列出抽到的外掛]
📖 部署指南：wp-deployment/DEPLOYMENT.md

🚀 下一步：
1. 租用 PHP 主機（推薦：Cloudways / SiteGround / Linode）
2. 按 DEPLOYMENT.md 指南執行
3. 在前端 .env 填入 VITE_WOO_URL
4. 對接自研金流（待金流完成後）
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## 🔗 依賴技能與腳本

### 必需依賴 (🔴 Required)

| 技能/腳本 | 路徑 | 用途 | 調用時機 |
|----------|------|------|---------|
| **ui-ux-pro-max** | `.agent/skills/ui-ux-pro-max/` | 生成設計系統 | Phase 1.2 |
| **real-ecommerce-dna.md** | `references/real-ecommerce-dna.md` | 真實電商 DNA 模板庫 | Phase 1.05 |
| **modern-ui-frameworks.md** | `references/modern-ui-frameworks.md` | 現代 UI 框架指南 | Phase 1.06 |
| **structural-variation.md** | `references/structural-variation.md` | 結構隨機化（區塊/分頁/組件變體） | Phase 1.07 |
| **maturity-signals.md** | `references/maturity-signals.md` | 成熟度特徵清單 | Phase 2.5 |
| **generate-image** | `.agent/skills/generate-image/` | 生成 Hero/商品圖 | Phase 3.1 |
| **ecommerce-checklist.py** | `scripts/ecommerce-checklist.py` | 品質檢查 | Phase 4.2 |
| **service-layer-spec.md** | `references/service-layer-spec.md` | 後端 Service 層完整規格 | Phase 5.1-5.7 |
| **cart-hybrid-spec.md** | `references/cart-hybrid-spec.md` | 混合購物車詳細邏輯 | Phase 5.3 |

### 可選依賴 (🟡 Optional)

| 技能/工具 | 用途 | 調用時機 |
|----------|------|---------|
| **/notebooklm**（技能，非 MCP） | 美學研究 (標竿品牌分析)；MCP 未裝可跳過 | Phase 1.0 |
| **generic-language-killer** (全域) | 清 AI 通用語／陳腔 | Phase 2.7 |
| **copywriting** (全域) | 重寫 hero／商品文案注入品牌觀點 | Phase 2.7 |
| **copy-editing** (全域) | 文案語氣一致性收尾 | Phase 2.7 |
| **generate-image / ads-photoshoot** (全域) | 生成獨家圖／商品圖（反指紋） | Phase 3.1 |
| **frontend-design** (全域) | 反通用 AI 美學、hero 版型 | Phase 1.2.5 |
| **gsap-awwwards-website** (全域) | 滾動敘事編排參考（實作限 motion/react） | Phase 1.2.5 |
| **motion-system.md** | `references/motion-system.md` | 動效基線（Tier 分級＋四項最低要求） | Phase 1.2.5 / 2.55 |
| **avatar-extraction / marketing-psychology** (全域) | 客群痛點→文案深度 | Phase 2.7 |
| **browser_subagent** | 自動化瀏覽器測試 | Phase 4.3 |
| **frontend-design/scripts/ux_audit.py** | UX 審計 | Phase 4.4 |
| **seo-fundamentals/scripts/seo_checker.py** | SEO 檢查 | Phase 4.4 |
| **wp-plugin-pool.md** | `references/wp-plugin-pool.md` | WP 外掛池（必裝 + 隨機） | Phase 6.3 |
| **validate_mock_flow.py** | `scripts/validate_mock_flow.py` | Mock 全流程驗證 | Phase 5.9 |
| **validate_live_flow.py** | `scripts/validate_live_flow.py` | 真連線驗證＋前端金鑰外洩掃描 | Phase 5.10 |
| **inject_services.py** | `scripts/inject_services.py` | Service 層自動注入 | Phase 5.1-5.7 |
| **generate_wp_package.py** | `scripts/generate_wp_package.py` | WP 部署包生成 | Phase 6.1-6.6 |

### 數據來源 (🗄️ Data Source)

| 文件 | 路徑 | 用途 |
|------|------|------|
| `extracted_products.json` | `<商品資料目錄>` | 商品分類池 |
| `used_categories.json` | `<商品資料目錄>` | 已使用分類記錄 |
| `category_products.json` | `<商品資料目錄>` | 當前分類商品 |

---

## 技術標準參考 (References)

### 技術標準文件
- **[engineering-standards.md](references/engineering-standards.md)**: TypeScript & SafeImage 代碼標準
- **[site-architecture.md](references/site-architecture.md)**: 11 類頁面、15 個路由架構詳解
- **[member-zone.md](references/member-zone.md)**: 會員功能實作細節
- **[woocommerce-api.md](references/woocommerce-api.md)**: API 與數據結構標準
- **[seo-and-testing.md](references/seo-and-testing.md)**: SEO 植入指南

### 後端對接文件（Phase 5-6）
- **[service-layer-spec.md](references/service-layer-spec.md)**: 5 個 Service 完整規格（api/product/cart/auth/order/checkout）
- **[cart-hybrid-spec.md](references/cart-hybrid-spec.md)**: 混合購物車詳細邏輯（localStorage ↔ Store API 合併）
- **[wp-plugin-pool.md](references/wp-plugin-pool.md)**: WP 必裝外掛 + 隨機外掛池（避免模板感）

### UX 與品質文件
- **[motion-system.md](references/motion-system.md)**: 動效基線系統（Tier 分級、easing 規範、reduced-motion）
- **[ux-psychology-ecommerce.md](references/ux-psychology-ecommerce.md)**: UX 心理學電商應用指南
- **[anti-patterns.md](references/anti-patterns.md)**: 設計反模式防護清單
- **[security-checklist.md](references/security-checklist.md)**: 電商安全自檢清單
- **[quality-scorecard.md](references/quality-scorecard.md)**: 品質計分卡模板

### Antigravity Kit 深度知識（按需讀取）
- `.agent/skills/frontend-design/ux-psychology.md`: UX 心理學法則庫
- `.agent/skills/frontend-design/SKILL.md`: 前端設計系統（色彩/字體/版面/動畫原則）
- `.agent/skills/tailwind-patterns/SKILL.md`: Tailwind CSS v4 最佳實踐
- `.agent/skills/nextjs-react-expert/SKILL.md`: React & Next.js 效能優化
- `.agent/skills/seo-fundamentals/SKILL.md`: SEO 深度優化
- `.agent/skills/vulnerability-scanner/SKILL.md`: 安全掃描原則
- `.agent/skills/web-design-guidelines/SKILL.md`: Web 設計規範審計
