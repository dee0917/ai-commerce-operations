<!-- DEPRECATED: Replaced by DNA system in v11.0 -->
# 技術與美學引擎選項定義

本文件定義了 9 種等級與風格的美學引擎，供技能執行時隨機抽取。

## A. Essentials (基礎動態版)

- **技術棧**: HTML5, CSS3, Vanilla JS, Tailwind CSS
- **特色動效**: CSS Animations 滾動進場、CSS transition hover 特效
- **游標**: 預設系統游標
- **紋理**: Global Grain 雜訊背景（CSS `background-image` 疊加 noise PNG）
- **適用場景**: 極速加載、輕量級品牌頁

### 必須實現的動效清單
1. Hero 區塊淡入 + 上移 (`fadeInUp`)
2. 商品卡片滾動進場 (IntersectionObserver + CSS class toggle)
3. CTA 按鈕 hover 背景填充過渡
4. 無限跑馬燈 (`@keyframes marquee`)

---

## B. Modern Brand (現代品牌版)

- **技術棧**: Tailwind CSS, GSAP (核心), Iconify-icon (CDN)
- **特色動效**: 按鈕磁吸效果 (Magnetic Pull)、逐字浮現動畫 (SplitText)、1px 邊框光束
- **游標**: 自訂圓形追蹤游標 + `mix-blend-mode: difference`
- **紋理**: Global Grain + 微弱漸層光暈

### 必須實現的動效清單
1. 自訂滑鼠游標 (GSAP `quickTo` 跟隨)
2. Hero 標題逐字浮現 (GSAP SplitText 或手動 span 拆分)
3. 按鈕磁吸效果 (mousemove 計算偏移量)
4. 1px 邊框光束動畫 (CSS `background: linear-gradient` 動態位移)
5. 商品卡片 GSAP ScrollTrigger 進場

---

## C. Interaction Pro (高階互動版)

- **技術棧**: Tailwind CSS, GSAP (ScrollTrigger), Anime.js (或純 CSS 替代)
- **特色動效**: 手電筒光暈、無限跑馬燈、聲納脈衝、Glassmorphism 毛玻璃排版
- **游標**: 手電筒光暈跟隨 (radial-gradient 圓形)
- **紋理**: Global Grain + 多層毛玻璃面板

### 必須實現的動效清單
1. 手電筒光暈游標 (GSAP 跟隨 + `radial-gradient` + `mix-blend-mode: screen`)
2. 聲納脈衝 (CSS `@keyframes sonarPulse` scale + opacity)
3. 無限跑馬燈 (`@keyframes marquee` 向左無限滾動)
4. Hero 視差 (GSAP ScrollTrigger `scrub: true`)
5. 商品 overlay 毛玻璃面板 (`backdrop-filter: blur(16px)` + 半透明)
6. 購物車側邊欄 Glassmorphism 滑出

---

## D. WebGL Visualist (WebGL 視覺版)

- **技術棧**: Tailwind CSS, Three.js / Curtains.js, GSAP
- **特色動效**: 全螢幕圖片 4 欄位切片下拉、液態轉場 (Liquid Wipe)、流體互動
- **游標**: 自訂圓形追蹤 + 圖片懸停扭曲效果
- **紋理**: Global Grain + 全域高品質噪點 (Noise Texture shader)

### 必須實現的動效清單
1. Three.js Canvas 背景粒子場或流體
2. 圖片切片過渡 (4-column clip-path 下拉動畫)
3. 液態轉場 (GLSL displacement shader)
4. 全螢幕噪點紋理 (Three.js ShaderMaterial)
5. GSAP ScrollTrigger 整合 WebGL 場景更新

---

## E. Awwwards Extreme (極致電影感版) 🚀

- **技術棧**: Tailwind CSS, Advanced Three.js, Shaders (GLSL), Physics Engine
- **特色動效**: 4 垂直欄位錯位捲動 (Staggered Scroll)、動態模糊尾跡 (Motion Blur)、視覺回彈
- **游標**: 大型自訂圓環游標 + 文字吸附 + 圖片預覽
- **紋理**: 全域高品質噪點 + 電影級色彩分級 (Color Grading)

### 必須實現的動效清單
1. 4 垂直欄位錯位捲動 (各欄不同速度的 GSAP ScrollTrigger)
2. 動態模糊尾跡 (CSS `filter: blur()` 或 shader post-processing)
3. 視覺回彈彈性動畫 (GSAP `elastic.out` 或 physics engine)
4. 大型自訂游標 (跟隨 + hover 狀態切換 + 吸附文字放大)
5. Three.js 全螢幕背景場景
6. 電影級色彩分級 (CSS `filter` 或 GLSL fragment shader)

---

## F. 專業清新 SaaS 版 (Modern SaaS)

- **技術棧**: Tailwind CSS, GSAP, CSS Animations
- **視覺氛圍**: 清新、專業、現代感。使用柔和光暈與微粒子裝飾。
- **色彩與排版**: 明亮背景 (`#F8FAFC`), 品牌色點綴。使用大留白與柔和陰影。
- **游標**: 預設游標或細緻幾何游標
- **紋理**: 留白為主，無明顯噪點

### 必須實現的動效清單
1. Hero 漸層 SVG 遮罩 + 緩慢浮動的抽象幾何圖形
2. 優雅的元件淡入動畫 (Fade & Slide UP)
3. 卡片懸停輕微位移 (Hover Tilt / 3D旋轉)

---

## G. 高端暗黑奢華版 (Quiet Luxury)

- **技術棧**: Tailwind CSS, GSAP
- **視覺氛圍**: 尊榮、神祕、極致質感。參考頂級精品或飯店風格。
- **色彩與排版**: 暗黑色調 (`#0D0D12`), 襯線體 (Serif) 與無襯線體混搭，創造強烈對比與層次。
- **游標**: 自訂游標特效 (`mix-blend-mode: difference` 融合效果)
- **紋理**: 深色大理石紋理 (Dark Marble) + 金屬色流光 (Gold/Champagne) 遮罩

### 必須實現的動效清單
1. Hero 大理石與流光效果遮罩過渡
2. 細膩的標題逐字浮現動畫 (SplitText / 字元錯位淡入)
3. 電影感慢速滾動視差

---

## H. 科技未來衝擊版 (Tech Impact)

- **技術棧**: Tailwind CSS, GSAP, WebGL / Three.js
- **視覺氛圍**: 前衛、炫酷、數位感。具備強烈的視覺震撼力。
- **色彩與排版**: 超高對比、霓虹發光效果 (Neon Glows)、深邃純黑背景。
- **游標**: 幾何準星或拖曳光跡游標
- **紋理**: 網格線條 (Grid) 或電路板感背景

### 必須實現的動效清單
1. Hero 區塊配置 WebGL 粒子系統或 3D 抽象物件，且隨滑鼠追蹤互動
2. 按鈕物理磁吸效果 (Magnetic Pull)
3. 1px 邊框動態光束動畫 (Border Beam) 與卡片霓虹光效過渡

---

## I. 復古文藝質感版 (Vintage Artsy)

- **技術棧**: Tailwind CSS, GSAP, CSS Filters
- **視覺氛圍**: 溫暖、人文、具備厚重的故事感。
- **色彩與排版**: 暖奶油色 (`#F5F0E8`), 深勃艮第紅或亞麻色。強調非對稱網格排版 (Asymmetric Grid)。
- **游標**: 書法筆觸或經典 Serif 文字游標
- **紋理**: 暖色調紙張紋理背景 + 具備膠卷感的顆粒 (Grain) 噪點

### 必須實現的動效清單
1. 平滑的捲動進場動畫，帶有稍具阻尼感的 ease 特效
2. 圖片懸停濾鏡切換 (Sepia/Grayscale → Color)
3. Hero 區域紙張與膠卷噪點結合的底圖處理

---

## 通用規範 (所有選項共用)

| 項目 | 規範 |
|------|------|
| 圖片來源 | Unsplash 真實高清，嚴禁佔位符 |
| 圖標 | SVG inline 或 Emoji |
| 字體 | 按照美學引擎分配適合的 Google Fonts |
| 適配 | RWD 手機 / 平板 / 桌機完美適配 |
| UI/UX | 確保閱讀對比度，提供有質感的留白 |
