# PRD: VANGUARD GEAR

## Brand Identity
- **Brand Name**: VANGUARD GEAR
- **Tagline**: Master Your Everyday Mission.
- **USP**: Precision-engineered EDC kits curated for the modern minimalist explorer, combining aerospace-grade materials with tactical efficiency.

## Target Audience
- **Primary**: Tech-savvy professionals and outdoor enthusiasts, 25-45, who value durability, industrial design, and tactical preparedness.
- **Device Preference**: Mobile-first (Optimized for Bento Grid scaling)
- **Emotional Trigger**: Functional Confidence; The satisfaction of a perfectly organized and ready-for-anything gear setup.

## Layout Preset（品類骨架）
- **Preset Name**: Sports & Active
- **Layer B Pages**: Size Guide, FAQ
- **Home Extra Sections**: Gear Highlight, Review Strip
  - ⚠️ **Review Strip 的內容不得由 PRD 或工程師編造。** 只有兩種合法做法：接真實評論資料，
    或做出「尚無評價」的空狀態。捏造的評論、評論者身分、星等與評論數是明文禁令
    （[`quality/site-rubric.md`](../../quality/site-rubric.md) 維度三「禁假評論」、
    [`production-line/references/anti-patterns.md`](../../production-line/references/anti-patterns.md) L4，
    英國 DMCCA 明文禁止假評價）。骨架有這個版位不等於可以填假料，**沒有真實素材就整段省略**。
  - ⚠️ **已知未修**：本站現行 `src/pages/Home.tsx` 的 Review Strip 就違反了上面這條
    （三則捏造評論＋五星＋「Verified Operatives」標題），且已進到 `dist/`。修正需重新打包，不在文件修訂的範圍內。
- **理由**: EDC products are functional tools that require technical specifications and "setup" context similar to high-performance outdoor gear.

## Aesthetic Specification（美學規格）
- **Base Engine**: Bento Grid Box
- **Mutated Style Name**: Vanguard Obsidian Grid
- **Primary Colors**: 
  - #121212 (Obsidian Matte - Primary Background)
  - #FF3D00 (Vanguard Red/Orange - Technical Accents & CTA)
  - #334155 (Industrial Slate - Secondary accents for containers)
  - Selected for a "stealth tech" look with high-visibility tactical highlights.
- **Font Stack**: IBM Plex Mono (Headers & Data) / Inter (Body Text)
- **Layout Grid**: Uniform Bento Grids with variable col-spans (Tailwind grid-cols-4)
- **Navbar Position**: Sticky Top (Functional Access)
- **Hero Section Style**: Centered Split (Product Visual vs Technical Specs)

## Content Specs（文案規格）
- **Product Count (Mock)**: 12 件商品
  1. Titanium Carabiner "Apex"
  2. Carbon Fiber Slim Wallet "Cipher"
  3. Bolt Action Tactical Pen "Stinger"
  4. Aerospace Grade Keychain Light "Lumen"
  5. Modular Key Organizer "Axis"
  6. Precision CNC Tweezers "Needle"
  7. Multi-Tool Card "Void"
  8. EDC Tech Pouch "Cell"
  9. Anodized Aluminum Pry Bar "Lever"
  10. Ceramic Folding Blade "Razor"
  11. Magnetic Bit Driver Set "Torque"
  12. Titanium Pill Canister "Secure"
- **Categories (Mock)**: Core Essentials, Technical Carry, Precision Tools
- **Hero CTA Text**: ELEVATE YOUR KIT
- **Section Headlines**: 
  - BATTLE-READY ESSENTIALS
  - THE OBSIDIAN COLLECTION
  - PROVEN IN THE FIELD
  - JOIN THE VANGUARD

## Technical Constraints（技術約束）
- **Animation Style**: Element Hover Lift (Y-axis translate); Smooth Scroll Fade-Up.
- **Image Strategy**:
  - **Photography Type**: Technical product macro / Industrial flat lay
  - **Background Style**: Dark slate texture / Anodized aluminum surface / Blueprint overlay
  - **Photo Mood Keywords**: tactical, titanium, high-tech, precision, shadows, stealth
  - **Hero Banner Concept**: Overhead professional flat-lay of a perfectly organized EDC tray on a technical schematic drawing, harsh side-lighting creating long shadows.
- **SEO Priority Page**: /product/[slug]
- **WooCommerce Mode**: Mock Mode (default)
