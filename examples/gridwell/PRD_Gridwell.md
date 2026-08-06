# PRD: Gridwell

## Brand Identity
- **Brand Name**: Gridwell
- **Tagline**: Organization meets visual harmony.
- **USP (Unique Selling Proposition)**: Premium, perfectly proportioned storage solutions that bring clarity to your everyday life through a refined bento-grid aesthetic.

## Target Audience
- **Primary**: Minimalist professionals, 25-45, valuing neatness, high-quality material, and aesthetic living spaces.
- **Device Preference**: Mobile-first
- **Emotional Trigger**: Peace of mind, aesthetic satisfaction, control and order (Curing FOMO on disorganization).

## Aesthetic Specification (美學規格鎖定)

> ⚠️ **這一節是初版規格，站在生成後又做過一次視覺改版，實際跑的值與初版不同。**
> 以下欄位已對齊 `src/` 與 `dist/` 的實際產出，括號內附初版寫法與查證位置，供版本考古用。
> 站的原始碼不在本輪改動範圍，這裡只修正文件與實際不符的部分。

- **Base Seed**: Bento Grid Box (便當盒網格 / Apple 風格)
- **Mutated Style Name**: Zen Structure Grid
- **Primary Colors**（實際值，見 [`tailwind.config.js`](tailwind.config.js) `theme.extend.colors.brand`）:
  #F5F5F0 (冷調米白，頁面底), #EDEEE8 (卡片面), #1B2E22 (深林綠近黑，主文字), #3D6B4F (森林綠，唯一強調色 / CTA), #8FA598 (次要文字)。
  （初版寫的是 #F9FAFB / #FFFFFF / #111827 / #0EA5E9 Sky Blue，全站查無，已作廢。）
- **Font Stack**（實際值，見 [`tailwind.config.js`](tailwind.config.js) 與 [`index.html`](index.html) 的 Google Fonts 連結）:
  'DM Serif Display', serif (標題 / display) / 'DM Sans', sans-serif (內文 / UI)
  - 初版寫的是 `'Inter' (Headers) / 'Roboto' (Body)`，那組**違反** [`quality/site-rubric.md`](../../quality/site-rubric.md)
    維度一「主視覺字體禁用 Inter / Roboto / Arial / 系統預設字當識別，Inter 只能當內文」。
  - **實際產出沒有違規**：`src/`、`index.html`、`tailwind.config.js`、`dist/assets/*.css`、`dist/assets/*.js`
    全數 grep 過，Inter 與 Roboto 一次都沒出現；`dist` CSS 內僅有的 font-family 宣告是
    `"DM Serif Display",serif`、`DM Sans,sans-serif` 與 `inherit`。是**規格書落後於實作**，不是站有問題。
- **Layout Grid**: Heavy reliance on CSS Grid (`grid-cols-2 md:grid-cols-4`, `gap-4` or `gap-6`)；卡片圓角實際用 `rounded-2xl`（16px，見 `src/index.css` 的 `.bento-card`），初版寫的 `rounded-3xl` 未採用。
- **Navbar Position**: Sticky Top with Frosted Glass (`sticky top-0 z-50 bg-brand-light/80 backdrop-blur-md`，初版寫 `bg-white/70`)。
- **Hero Section Style**: Asymmetric Bento Layout: A massive feature card on the left (text + CTA) and 2-3 smaller product visuals on the right, all perfectly padded.

## Content Specs (文案規格)
- **Product Count (Mock)**: 10 件商品
  1. Silicone Cable Organizer Tie (數據線收納綁帶) - $20.10
  2. Heavy Duty Vacuum Storage Bag (真空壓縮袋) - $27.00
  3. Matte Tinplate Organizer Box (馬口鐵收納盒) - $27.30
  4. Minimalist Mesh Zipper Pouch (網格拉鍊袋) - $22.80
  5. Bluetooth Smart Label Maker (標籤機) - $24.70
  6. Premium Leather Passport Holder (護照夾) - $22.30
  7. Transparent Coin Sorting Tube (硬幣收納筒) - $20.30
  8. Compact Travel Jewelry Case (旅行首飾盒) - $21.50
  9. Hard Shell Glasses Case (眼鏡收納盒) - $18.60
  10. Water-resistant Cosmetic Bag (防水化妝包) - $29.20
- **Hero CTA Text**: Explore the Grid
- **Section Headlines**: 
  - The Art of Organization
  - Travel Essentials
  - Daily Storage Solutions
  - Why Choose Gridwell

## Technical Constraints (技術約束)
- **Animation Style**: Smooth and subtle micro-interactions (`hover:-translate-y-1 hover:shadow-lg transition-all duration-300`). No exaggerated animations.
- **Image Strategy**: `https://image.pollinations.ai/prompt/minimalist_{product_name_no_spaces}_product_shot_on_soft_gray_background_studio_lighting?width=800&height=800&nologo=true`
- **SEO Priority Page**: `/product/[id]`
