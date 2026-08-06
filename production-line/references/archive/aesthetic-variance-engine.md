<!-- DEPRECATED: Replaced by DNA system in v11.0 -->
# 🎨 Aesthetic Variance Engine v3 (美學靈感引擎 - NotebookLM 增強版)

本引擎的目的是為你的設計注入獨特的個性與靈魂。在生成設計系統後，**必須先查詢 NotebookLM (ID: <notebook-id>)** 獲取特定品牌靈感，再與 UI UX Pro Max 的科學配色/字體結合。

---

## 📋 標竿品牌與美學對應 (Brand Benchmarks)

當你抽樣到某種風格時，請參考以下標竿品牌的前端基因：

| 美學風格 | 標竿品牌 (Reference) | 核心前端基因 |
|------------|------------|------------|
| 極簡禪意 | **Apple / Blue Bottle** | 巨大字體排印、透明磨砂質感、極度流暢的微互動 |
| 自然有機 | **Allbirds / Aesop** | 大地色系 (Pantone 11-4201)、手寫字體點綴、紙張質感背景 |
| 動能競技 | **Nike** | 動態文字 (Kinetic Typography)、高對比強烈色塊、3D 產品展示 |
| 玩味美學 | **Glossier / Frank Body** | 柔和粉色調、大量社交證明 (UGC)、俏皮的鼠標互動 |
| 奢華雜誌 | **Mejuri / Haus** | 非對稱排版、高品質攝影、優雅襯線字配極細邊框 |
| 實用日常 | **Everlane / MUJI** | 透明定價 UI、資訊模組化、極致清晰的網格 |

---

## 🎲 The 12 Aesthetic Archetypes（美學原型）

### 1. Minimalist Zen（極簡禪意）
- **核心哲學**：無邊界的留白、透過巨大的字體排印引導視覺。
- **視覺特徵**：單色系統為主，刻意不對齊邊緣的非對稱留白，大量空白。**[Apple 基因]**

### 2. Neo-Brutalism（新粗曠主義）
- **核心哲學**：大膽黑邊、死黑陰影、高對比度。
- **視覺特徵**：粗黑框 (`border-4 border-black`)，卡片具有偏移的純黑陰影。

### 3. Bento Grid Box (便當盒網格)
- **核心哲學**：資訊結構化，所有內容塞進完美對齊的圓角卡片。
- **視覺特徵**：淺灰背景，圓角卡片包含產品、影片與公告，**[Bento Hero 佈局]**。

### 4. Editorial Magazine（時尚雜誌排版）
- **核心哲學**：像閱讀實體高級時尚雜誌，依賴多欄文字佈局。
- **視覺特徵**：優雅的襯線字體大標題，不對稱多欄設計，圖片刻意打破文字流。

### 5. Organic Modern（有機現代主義）
- **核心哲學**：柔和、圓潤、非幾何形狀、流體感。
- **視覺特徵**：不規則 Blob 遮罩，紙張細微紋理，低飽和度暖色調。**[Allbirds 基因]**

### 6. E-commerce Brutalism（實用電商粗曠主義）
- **核心哲學**：資訊極端密集，功能第一主義。
- **視覺特徵**：嚴謹 1px 黑線拉表格，無圓角，System UI 字體。

### 7. Typographic Swiss（瑞士字體排版學）
- **核心哲學**：結構優先於裝飾，巨大的文字主導畫面。
- **視覺特徵**：超大無襯線標題文字 (`text-[10vw]`)，嚴謹的網格對齊。

### 8. Boutique Print（精品印刷質感）
- **核心哲學**：手工印刷溫度感，留白是奢侈的表現。
- **視覺特徵**：奶白底色，手寫感裝飾線條，極大的字母間距。

### 9. Market Stall（市集日常感）
- **核心哲學**：溫暖、親切、充滿生命力與色彩。
- **視覺特徵**：暖色系，手寫字體，卡片帶有輕微旋轉。

### 10. Catalog Grid（實用型錄體）
- **核心哲學**：像 MUJI，簡潔、實用。
- **視覺特徵**：純白底色，清晰的分割線，高密度商品排版。

### 11. Kinetic Athlete (動能競技) —— [NEW]
- **核心哲學**：力量感、速度感、攻擊性的視覺排版。
- **視覺特徵**：傾斜字體 (Italic/Condensed Bold)、縮放動畫、高飽和色彩點綴。**[Nike 基因]**

### 12. Liquid Glass (高光玻璃擬物) —— [NEW]
- **核心哲學**：科技與奢華的平衡，透過透明度建立層次。
- **視覺特徵**：磨砂玻璃效果 (`backdrop-blur-xl`)、Mesh 漸層背景、極細像素邊框。**[Apple 2026 基因]**

---

## 🧬 結構與互動突變 (NotebookLM Fusion Mutators)

針對 Phase 1.3，請從以下從頂級品牌中擷取的「突變因子」中選擇：

### A. 佈局變異 (Layout Mutators)
1. **The Asymmetric Overlay**: 圖片與文字重疊，使用 Z-index 創造空間深度（參考 Patagonia）。
2. **Floating Pill Nav**: 移除頂部 Navbar，改為底部懸浮膠囊選單，提升手機操作便利性。
3. **Bento Hero Grid**: 英雄區由 4-5 個不同比例的小方塊組成，分別展示大圖、影片、購買按鈕。
4. **Cinematic Full-Width**: 移除所有框線，讓商品圖片撐滿整個視窗，文字半透明浮動。

### B. 互動變異 (Interaction Mutators)
1. **Magnetic Cursor**: 鼠標移近按鈕時，按鈕會產生磁吸回饋。
2. **Sequential Scroll Reveal**: 商品卡片隨滾動順序以 0.1s 間隔逐一淡入。
3. **Liquid Hover**: 按鈕或卡片在 Hover 時產生類似流質的變形效果。
4. **Haptic Scroll**: 當滾動到頁面底部或特定卡片時，UI 產生輕微的反彈與擠壓感。

### C. 配色變異 (Color Mutators)
1. **Nature Distilled**: 使用 Pantone 11-4201 Cloud Dancer 配低對比木質、石色。
2. **Hyperreal High-Contrast**: 極致的黑 (#0a0a0a) 搭配單一高亮色 (驚嘆紅、電網藍)。
3. **Pastel Softness**: 使用莫蘭迪色系，營造溫柔、無害、具社群感的美學（參考 Glossier）。

---

## 🔬 AI 執行規則：創意宣言 (Manifesto)

在生成代碼前，你必須在「創意宣言」中回報：
1. **基底靈感**：我今天選擇了 [Archetype 1-12] 作為基底。
2. **標竿參考**：我將融合 [Apple/Nike/Allbirds...] 的 [具體前端特徵，如：Kinetic Typography]。
3. **突變因子**：我加入了 [Mutator A/B/C] 確保其獨特性。
4. **最終風格命名**：例如 `[Nike Kinetic] x [Bento Grid] High-Performance Fusion`。
