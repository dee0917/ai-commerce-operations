# 🎬 動效基線系統 (Motion Baseline System)

> **地位：必須執行，不是加分項。** 本檔接手原 `aesthetics-engines.md`（已歸檔至 `archive/`）的分級動效清單，
> 對映到 v11 的 DNA Family 體系。沒有動效的站一眼就是半成品，2026-08 視覺健檢實證：
> 缺了這層之後，產出站的 CSS 只剩框架出廠預設 transition，全站零滾動進場。

## 一、動效引擎：統一使用 `motion/react`

```bash
npm install motion
# import { motion, AnimatePresence, MotionConfig } from 'motion/react'
```

**選擇理由（已定案，不要每站重新辯論）：**
1. `cart-hybrid-spec.md` 的購物車與結帳互動規格已採用 `motion/react`，全站同一套引擎。
2. 本產線是 React 專案，聲明式 `whileInView` / `whileHover` / `AnimatePresence` 與元件模型天然契合。
3. `prefers-reduced-motion` 一行搞定（`<MotionConfig reducedMotion="user">`）。

**禁止事項：**
- ❌ 同一個站禁止混搭第二套動效引擎（例如再引入 gsap）。要滾動敘事就用 `motion/react` 的
  `useScroll` + `useTransform`，不要為單一效果多拉一套函式庫。
- ❌ 舊套件名 `framer-motion` 不再用於新站，一律裝 `motion`、從 `motion/react` import。
- ❌ HeroUI 站的元件庫 peer 依賴 `framer-motion` 由框架安裝指令帶入，僅供元件庫內部使用；
  站內自寫動效仍統一 `motion/react` 寫法。

## 二、四項最低要求（缺一即 FAIL，驗收會抓）

| # | 要求 | 實作規格 |
|---|------|---------|
| 1 | **滾動進場** | 首頁至少 4 個區塊、內頁至少 2 個區塊使用 `whileInView`（淡入 + 12-24px 位移，`viewport={{ once: true, margin: '-80px' }}`）。清單類元素（商品卡、USP、FAQ）要 stagger（每項延遲 0.05-0.09s）。 |
| 2 | **有意圖的 hover** | 商品卡 hover 不可只變色：至少「圖片縮放 1.03-1.06 或第二圖 crossfade」+「卡片位移或陰影變化」二選二。CTA hover 要有背景填充、位移或圖示滑動其中一種。 |
| 3 | **禁用預設 easing** | 禁 `ease`、`linear`、`ease-in-out` 出廠值。一律指定曲線：進場用 `[0.22, 1, 0.36, 1]`（out-quint 類）或 `[0.16, 1, 0.3, 1]`（out-expo 類）；微互動用 spring（`stiffness 260-400, damping 22-32`）。CSS transition 同理，在 Tailwind config `transitionTimingFunction` 註冊具名曲線後使用，不寫裸 `duration-150` 配預設曲線。 |
| 4 | **尊重 reduced-motion** | App 根部包 `<MotionConfig reducedMotion="user">`；自寫 CSS keyframes 一律包在 `@media (prefers-reduced-motion: no-preference)` 內。 |

**時長紀律**：微互動 150-250ms、進場 400-700ms、大型轉場 ≤ 900ms。超過 1s 的動畫要有敘事理由。

## 三、動效強度分級（承接原分級清單，對映 DNA Family）

依 Phase 1.05 選定的**主 DNA Family** 決定強度層級。成熟電商不堆動效：奢華／自然有機宜少，潮牌／科技可多。

### Tier 1 節制（Family B Luxury / D Artisan / G Fragrance / H Botanical / J Craft / L Food）
必做（承原 Essentials／Vintage Artsy／Quiet Luxury 清單）：
1. Hero 淡入 + 上移（fadeInUp）
2. 商品卡片滾動進場（stagger）
3. CTA hover 背景填充過渡
4. 圖片 hover 濾鏡或緩慢縮放（如 grayscale→color、scale 1.03，帶阻尼感曲線）
5. （Luxury 選配）標題逐字／逐行浮現、慢速滾動視差

### Tier 2 標準（Family A Clean DTC / C Modern Minimal / F Asian Modern / M Design Furniture / N Specialty）
Tier 1 全部，加（承原 Modern Brand／Modern SaaS 清單）：
6. 標題逐行或逐字浮現（span 拆分 + stagger）
7. 無限跑馬燈（marquee，公告列或品牌列）
8. 卡片 hover 位移 + 陰影升起（hover lift）
9. 商品第二圖 crossfade 或 quick-add 滑入

### Tier 3 張揚（Family E Bold / I Tech & Design Objects / K High Fashion）
Tier 2 全部，加（承原 Interaction Pro／Tech Impact 清單，依品牌選 2-3 項，不全上）：
10. 按鈕磁吸效果（pointer 追蹤位移）
11. Hero 視差（`useScroll` + `useTransform`，scrub 式）
12. 1px 邊框光束或霓虹光效過渡
13. 大型自訂游標／游標吸附（確保觸控裝置 fallback）
14. 聲納脈衝、毛玻璃面板滑出

> 原九引擎中的 WebGL／Three.js／液態轉場等重型項目不在電商產線基線內；
> 需要時另立專案評估，不趁建站順手加。

## 四、驗收方式（建置後必查，見 Phase 2 動效基線實作）

1. `npm run build` 後 grep 編譯產物：CSS 或 JS 內必須出現**非出廠預設**的 `cubic-bezier` 曲線。
2. 用瀏覽器實開頁面滾動一輪：進場動效肉眼可見；截圖前後對比不可完全相同。
3. hover 商品卡與 CTA：必須有位移／縮放／陰影變化，不是只有變色。
4. 模擬 `prefers-reduced-motion: reduce`：頁面內容完整可用、無大位移動畫。
