# PRD: AuraGuard

## Brand Identity & Story
- **Brand Name**: AuraGuard
- **Tagline**: Protect your energy.
- **USP**: Authentic, hand-crafted feng shui talismans designed for modern life.
- **Brand Lore (Brand Manifesto)**:
  For centuries, our ancestors have understood the delicate flow of energy that surrounds us. AuraGuard was born from a deep respect for these ancient traditions and a desire to bring their protective power into the modern world. We source the finest materials and work with skilled artisans to create talismans that are not only powerful but also beautiful.
  In an increasingly chaotic world, maintaining personal equilibrium is more important than ever. We believe that everyone deserves a sanctuary, a shield against negativity. Our talismans are designed to be that shield, empowering you to navigate life with confidence and peace of mind.
  We are committed to authenticity and quality. Every piece is crafted with intention and blessed to ensure its effectiveness. With AuraGuard, you're not just buying an object; you're investing in your well-being and embracing a legacy of protection.
- **Founder's Persona**: Master Lin, a third-generation Feng Shui practitioner who seeks to bridge ancient wisdom and modern aesthetics.

## Target Audience
- **Primary**: Professionals seeking spiritual balance and protection, 25-45.
- **Device Preference**: Mobile-first
- **Emotional Trigger**: Peace of mind, empowerment, and refined aesthetic.

## Layout Preset（品類骨架）
- **Preset Name**: Artisan
- **Layer B Pages**: About + Contact
- **Home Extra Sections**: Brand Story + Craftsmanship
- **理由**: Feng Shui talismans require deep storytelling and emphasis on the craft/blessing process, fitting the Artisan preset.

## Aesthetic Specification & Layout Direction
- **Base Engine**: Boutique Print
- **Mutated Style Name**: Imperial Scroll Heritage
- **Layout Direction**: Magazine
- **Primary Colors**: #FAF6F0 (Rice Paper Off-White), #9E2A2B (Cinnabar Red), #1A1A1A (Ink Black)
- **Font Stack**: 'Cormorant Garamond', serif / 'Inter', sans-serif
- **Navbar Style**: Float Pill
- **Hero Grid Concept**: Split-ImageLeft

## Content Scenarios (The Brand Script)
- **Product Count (Mock)**: 12 件商品（含英文商品名稱 ×12）
- **Section Headlines**:
  - Unveil Your Guardians
  - The Sacred Craft
  - A Legacy of Protection
  - Master Lin's Vision
  - Curated Energies
  - Connect with Us
- **Hero CTA Text**: Discover Your Guard
- **Founder's Note**: "Protection is not about building walls, but about cultivating an inner light that no shadow can breach. Let our talismans be your constant reminder of that light." — Master Lin
- **FAQ Scenarios**: 
    1. Orders: How long does it take to process an order? (1-3 days)
    2. Orders: Can I modify my order after placing it? (Within 24 hours)
    3. Shipping: Do you ship internationally? (Yes, worldwide)
    4. Shipping: How are the talismans packaged? (Safely in custom boxes)
    5. Returns: Can I return a talisman? (Within 30 days if unused)
    6. Returns: Who covers return shipping? (Customer, unless defective)
    7. Philosophy: Are the talismans blessed? (Yes, by Master Lin)
    8. Philosophy: How do I choose the right talisman? (Follow your intuition and read the descriptions)
- **Social Proof**: **不提供文案，此區塊待有真實素材再啟用。**
  - 本 PRD 原本在這裡列了三則「英文姓名縮寫 + 職稱」格式的樣板評論。那個格式是明文禁令：
    [`quality/site-rubric.md`](../../quality/site-rubric.md) 維度三「禁假評論」、
    [`production-line/references/anti-patterns.md`](../../production-line/references/anti-patterns.md) L4
    「評價、推薦、媒體背書不得虛構（DMCCA 明文禁止假評價）」。三則已移除。
  - 那三則從未進到站上（`src/` 與 `dist/` 皆查無），但**規格書留著就等於指示下一個站再生一次**，所以從源頭刪掉。
  - 現行做法：要嘛接真實評論資料，要嘛做出「尚無評價」的空狀態。**不得補寫替代評論。**

## Technical Constraints（技術約束）
- **Animation Style**: Scroll Fade-Up Only
- **Hero Layout**: Split-ImageLeft
- **Image Strategy**:
  - **Photography Type**: artisan lifestyle photography
  - **Background Style**: soft linen and traditional wooden table
  - **Photo Mood Keywords**: Imperial Scroll Heritage aesthetic, #FAF6F0 #9E2A2B #1A1A1A tones, traditional feng shui talisman, golden hour lighting, zen minimalism
  - **Unsplash Hero Keyword**: traditional chinese architecture, wooden temple, golden hour
  - **Hero Banner Concept**: a serene setting with tea and a talisman on a wooden table, flooded with morning light
- **SEO Priority Page**: /product/[slug]
- **WooCommerce Mode**: Mock Mode

### 🛑 Engineer 交付前必看查核表 (Must-Build Checklist)
- [ ] **核心 API 實作**: `src/services/api.ts`
- [ ] **會員專區 (Auth)**: 建立 `src/services/auth.ts` 與全域狀態 `src/hooks/useAuth.ts`，並實作 Login/Register/Dashboard 等會員頁面。
- [ ] **購物車與體驗**: 實作 CartDrawer 動畫與商品卡片 Hover 功能。
- [ ] **PRD 指定頁面**: PRD 骨架要求的所有 Layer B 與 Layer C 政策頁。
- [ ] **圖片使用 Unsplash**: `mockData.ts` 所有`images[]` 使用 `buildUnsplashUrl()` 並搬入品類高相關關鍵字（禁止通用詞）。
- [ ] **Hero Banner 排版**: 照 PRD 的 `heroLayout` 欄位實作指定的排版方案，禁止產出平庸的置中排版。
