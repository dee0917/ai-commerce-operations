# Real Ecommerce DNA Library

> **Purpose:** Every generated site must be based on a REAL ecommerce site's structural DNA.
> Unlike abstract "archetypes," these are reverse-engineered from sites that have been
> live for 5+ years and process real transactions.

## How to Use

1. **Mandatory:** Agent MUST randomly select 1 DNA profile before any design work
2. **Enforce diversity:** Cannot reuse same profile or family within 5 consecutive generations
3. **Record selection** in `design-system/DECISIONS.md`

## Selection Rules

- Roll a random number 1-66 to select profile
- Check `data/design-history.json` — if same family used in last 5 generations, re-roll
- **Consecutive visual dedup (mandatory, added 2026-08):** also check the last 3 entries' `bg_tone`
  and `fonts.display` — same display font as any of the last 3, or the same background tone family
  appearing a 3rd consecutive time, forces a re-roll or font/palette substitution (full rule:
  SKILL.md Phase 1.05 item 4). Body font **Inter is on the avoid list**; fonts named in DNA profiles
  are category examples, not mandates — substitute within the same category when they hit the avoid list.
- **Write-back is mandatory:** after the site ships, append an entry (with `bg_tone`, `colors`, `fonts`)
  to `data/design-history.json`. Skipping the write-back silently disables every anti-repeat rule above.
- The selected DNA determines: layout skeleton, header style, product grid, color temperature, typography class, and "maturity signals"
- ⚖️ **Compliance override (UK/EU targets):** DNA profiles DESCRIBE real sites that own their own price history.
  Copy their *structure*, not their price claims. Any "% OFF" / sale hero / strikethrough / stock-count / countdown
  mentioned in a profile is reproduced ONLY if this project has the underlying evidence
  (see `anti-patterns.md` UK/EU section). Otherwise render the same slot without the claim.

---

## Family A: Clean DTC (Direct-to-Consumer)

### DNA-01: Allbirds Style
- **Header:** Sticky minimal bar, logo center, hamburger left, cart right. Announcement bar on top.
- **Hero:** Full-width lifestyle photo, text overlay bottom-left, single CTA
- **Product Grid:** 2-col mobile / 3-col desktop, generous gap, hover → second image swap
- **Color Temp:** Warm neutrals (cream, sand, sage green)
- **Typography:** Sans-serif geometric (e.g., GT America, DM Sans)
- **Maturity Signals:** "Free shipping over $X" bar, "Sustainability" badge, customer review count, "As seen in" press logos
- **Footer:** 4-column, newsletter signup, social icons, B-Corp badge

### DNA-02: Glossier Style
- **Header:** Thin top bar, minimal nav (3-4 items), search icon + cart icon
- **Hero:** Pastel gradient background, product photo floating, playful copy
- **Product Grid:** 3-col, rounded corners on cards, "Best Seller" tags
- **Color Temp:** Millennial pink, soft lavender, white
- **Typography:** Rounded sans-serif (e.g., Apercu, Nunito)
- **Maturity Signals:** UGC gallery ("The Community"), "Routine Quiz", bundle deals, review photos

### DNA-03: Everlane Style
- **Header:** Clean black bar, category dropdowns with photos
- **Hero:** Split — left: editorial copy with serif, right: studio product shot
- **Product Grid:** 4-col tight grid, minimal card (image + name + price only)
- **Color Temp:** Pure white + charcoal + one muted accent
- **Typography:** Classic sans (Helvetica Neue, Inter) + serif accent (Freight)
- **Maturity Signals:** "Transparent Pricing" breakdown, factory photos, "Choose What You Pay" sections

### DNA-04: Mejuri Style
- **Header:** Dual-row — top announcement, bottom nav with "New Arrivals" highlight
- **Hero:** Cinematic lifestyle photo, minimal text
- **Product Grid:** 2-col with large images, quick-add button on hover
- **Color Temp:** Warm gold, off-white, soft black
- **Typography:** Elegant sans (Cera Pro, Plus Jakarta Sans)
- **Maturity Signals:** "Engraving available", "14-day returns", Instagram feed integration

### DNA-05: Warby Parker Style
- **Header:** Logo left, centered nav, utility icons right
- **Hero:** Lifestyle carousel with real people wearing products
- **Product Grid:** 4-col, shadow on hover, "Virtual Try-On" badges
- **Color Temp:** Blue-grey + white + warm wood tones
- **Typography:** Geometric sans (Proxima Nova, Outfit)
- **Maturity Signals:** "Home Try-On" CTA, store locator, quiz ("Find Your Fit")

---

## Family B: Luxury & Editorial

### DNA-06: Aesop Style
- **Header:** Monochrome, wide letter-spacing, minimal items
- **Hero:** Full-bleed dark photography, white serif text overlay
- **Product Grid:** 1 or 2 col, tall images, ingredient focus
- **Color Temp:** Dark olive, amber, parchment, black
- **Typography:** Serif display (Suisse Works, Playfair Display) + sans body
- **Maturity Signals:** Long ingredient descriptions, "Our Stores" with interior photos, editorial articles

### DNA-07: Le Labo Style
- **Header:** Typewriter-style font, centered, underline hover
- **Hero:** Single product on neutral background, minimal copy
- **Product Grid:** 2-col, ample whitespace, product names in uppercase
- **Color Temp:** Kraft paper, black, white
- **Typography:** Monospace or condensed sans (Courier, IBM Plex Mono)
- **Maturity Signals:** "Complimentary samples", store finder, "Our Story" timeline

### DNA-08: Byredo Style
- **Header:** Ultra-minimal, logo only, slide-out menu
- **Hero:** Art-directed campaign image, no CTA button (image IS the CTA)
- **Product Grid:** Large single-column, editorial feel
- **Color Temp:** Black + white + one seasonal accent
- **Typography:** High-contrast serif/sans pair (Didot + Aktiv Grotesk)
- **Maturity Signals:** "Discovery Set", curated collections, artist collaborations

### DNA-09: COS / H&M Premium Style
- **Header:** Two-tier — category bar + utility bar
- **Hero:** Video or slow-zoom image, centered text
- **Product Grid:** 3-4 col, model shots, color swatch dots under cards
- **Color Temp:** Cool neutrals (grey, navy, stone)
- **Typography:** Clean geometric (Futura, Montserrat)
- **Maturity Signals:** Size guide, "Responsible collection" tag, member pricing

### DNA-10: Net-a-Porter Style
- **Header:** Black bar, editorial nav, "SALE" in red
- **Hero:** Magazine-style editorial with "Shop the Look"
- **Product Grid:** 3-col, designer name bold, wishlist heart icon
- **Color Temp:** Black + white + one luxury accent (gold or burgundy)
- **Typography:** Fashion serif (Didot, Baskerville) + clean sans body
- **Maturity Signals:** "Designer" filter, editorial content, "The Edit" section

---

## Family C: Modern Minimal

### DNA-11: MUJI Style
- **Header:** Logo + horizontal category text, no icons
- **Hero:** Clean product arrangement photo, sans-serif text block
- **Product Grid:** 4-col dense, tiny text, material-focused
- **Color Temp:** White, light wood, beige
- **Typography:** Japanese-inspired clean sans (Noto Sans, Zen Kaku Gothic)
- **Maturity Signals:** "Material story", "Found MUJI" curation, store pickup

### DNA-12: HAY Style
- **Header:** Colorful accent bar, playful nav
- **Hero:** Styled room scene, overlay text with background color block
- **Product Grid:** Mixed grid (2+1+3 pattern), color-category browsing
- **Color Temp:** Bold pastels (yellow, mint, coral)
- **Typography:** Rounded geometric (Circular, Sofia Pro)
- **Maturity Signals:** "Room inspiration", "Gift guide", designer attribution

### DNA-13: Apple Store Style
- **Header:** Slim grey bar, icon-based nav
- **Hero:** Large product render centered, gradient background, spec highlights
- **Product Grid:** 1-2 col, card-based with specs comparison
- **Color Temp:** Pure white/dark mode, blue accents
- **Typography:** SF Pro, system font stack
- **Maturity Signals:** "Compare models", "Trade-in", financing options, genius bar

### DNA-14: IKEA Style
- **Header:** Blue + yellow branding, search-prominent, location icon
- **Hero:** Room scene with hotspots (clickable items)
- **Product Grid:** 3-col, price prominent, rating stars, "Add to bag" visible
- **Color Temp:** White + blue + yellow accent
- **Typography:** Noto Sans / system sans
- **Maturity Signals:** "Check stock", delivery estimator, assembly info, room planner CTA

### DNA-15: Uniqlo Style
- **Header:** Red logo, clean horizontal nav, search bar visible
- **Hero:** Full-width model photo, seasonal collection name
- **Product Grid:** 4-col tight, color chips under each product
- **Color Temp:** White + red accent + neutral grey
- **Typography:** Clean sans (Helvetica, Roboto)
- **Maturity Signals:** "LifeWear" philosophy section, material innovation, weekly promotion

---

## Family D: Artisan & Handmade

### DNA-16: Etsy Seller Style
- **Header:** Shop name in handwritten font, banner image, shop rating
- **Hero:** Lifestyle flat-lay photo, "Handmade with love" tagline
- **Product Grid:** 3-col, slightly uneven card heights (masonry feel)
- **Color Temp:** Warm earth tones (terracotta, olive, cream)
- **Typography:** Hand-drawn display (Caveat, Sacramento) + clean body
- **Maturity Signals:** "5,000+ sales", maker bio, process photos, custom order button

### DNA-17: Schoolhouse Electric Style
- **Header:** Vintage-inspired logo, centered nav, utility bar
- **Hero:** Lifestyle interior photo, serif headline
- **Product Grid:** 3-col, tall product photos on white, material specs visible
- **Color Temp:** Cream, brass gold, forest green
- **Typography:** Slab serif (Rockwell, Zilla Slab) + sans body
- **Maturity Signals:** "Made in Portland", factory tour link, design stories, clearance section

### DNA-18: Rifle Paper Co. Style
- **Header:** Illustrated logo, floral accent elements
- **Hero:** Illustrated banner with hand-painted style
- **Product Grid:** 3-col, card with subtle border, category icons illustrated
- **Color Temp:** Rich jewel tones on cream (emerald, navy, burgundy, gold)
- **Typography:** Stylish serif (EB Garamond, Cormorant) + clean sans
- **Maturity Signals:** "New Collection" seasonal, gift wrapping option, collaboration badges

### DNA-19: Toast (UK) Style
- **Header:** Minimal serif, centered, linen texture background
- **Hero:** Atmospheric lifestyle photography, overlaid poetry/quote
- **Product Grid:** 2-col generous spacing, model shots in natural light
- **Color Temp:** Linen, stone, sage, indigo
- **Typography:** Literary serif (Freight Text, Lora) + thin sans
- **Maturity Signals:** Editorial journal, fabric care guide, "Stories" section

### DNA-20: Uncommon Goods Style
- **Header:** Teal brand color, gift-oriented nav ("Gifts For Him/Her")
- **Hero:** Curated gift collection grid
- **Product Grid:** 3-col, "Uncommon" badge, star rating, "Made by" artisan name
- **Color Temp:** Teal + warm neutrals + craft brown
- **Typography:** Friendly rounded (Quicksand, Comfortaa) + standard body
- **Maturity Signals:** "Handmade", "Eco-friendly" badges, gift personalizer, impact report

---

## Family E: Bold & Contemporary

### DNA-21: Nike Style
- **Header:** Black bar, bold nav, swoosh left
- **Hero:** Dynamic athlete photo, italic condensed headline, "Shop Now" button
- **Product Grid:** 3-col, hover → quick view, filter sidebar
- **Color Temp:** Black + white + one high-energy accent (volt, red)
- **Typography:** Condensed bold (Oswald, Barlow Condensed)
- **Maturity Signals:** "Member exclusive", launch calendar, "Just In", athlete stories

### DNA-22: Supreme Style
- **Header:** Box logo centered, minimal nav
- **Hero:** Lookbook photo, no text overlay
- **Product Grid:** 4-col tight, no hover effects, sold-out crossed
- **Color Temp:** White + red + black only
- **Typography:** Futura Heavy
- **Maturity Signals:** "Sold Out" culture, limited drops, no sales ever, sparse descriptions

### DNA-23: Patagonia Style
- **Header:** Mountain silhouette, action-sport nav categories
- **Hero:** Epic landscape with product-in-use
- **Product Grid:** 3-col, color chips, activity tags, "Fair Trade" badge
- **Color Temp:** Earth tones + alpine blue + sunset orange
- **Typography:** Sturdy sans (Trade Gothic, Public Sans)
- **Maturity Signals:** "Worn Wear" section, environmental activism, repair guide, donation tracker

### DNA-24: Stussy Style
- **Header:** Logo left, minimal text nav, shopping bag icon
- **Hero:** Street photo, oversized text overlay
- **Product Grid:** 2-col large, lookbook style
- **Color Temp:** Black/grey/cream with seasonal pops
- **Typography:** Hand-drawn + grotesque (Druk, ABC Diatype)
- **Maturity Signals:** Chapter stores, collaborations, "Archive" section

### DNA-25: Outdoor Voices Style
- **Header:** Colorful, playful logo, "Shop" + "Community" nav
- **Hero:** Group activity lifestyle photo, rounded CTA buttons
- **Product Grid:** 3-col, model diversity, color block backgrounds
- **Color Temp:** Tech color blocks (teal, coral, lavender, chartreuse)
- **Typography:** Rounded geometric (Circular, Poppins)
- **Maturity Signals:** "OV Trail Shop" (resale), community events, "The Recreationalist" blog

---

## Family F: Asian Modern

### DNA-26: Gentle Monster Style
- **Header:** Ultra-minimal, hidden nav (hamburger), logo center
- **Hero:** Avant-garde campaign imagery, art installation feel
- **Product Grid:** 2-col, large square images, minimal text
- **Color Temp:** High-contrast monochrome with one surreal accent
- **Typography:** Extended sans (Neue Haas Unica, Extended Grotesque)
- **Maturity Signals:** Store gallery (each store is an art space), campaign films, celeb collaborations

### DNA-27: Snow Peak Style
- **Header:** Japanese minimal, logo centered, nature-inspired
- **Hero:** Outdoor camping scene, product-in-context
- **Product Grid:** 3-col, clean cards, material callouts
- **Color Temp:** Titanium grey + canvas + earth brown
- **Typography:** Japanese-influenced sans (Noto Sans JP, Zen Kaku)
- **Maturity Signals:** "Field" lifestyle content, camping event calendar, member points

### DNA-28: Ader Error Style
- **Header:** Experimental typography, asymmetric layout
- **Hero:** Surreal fashion photography, text as graphic element
- **Product Grid:** Irregular grid, mixed orientations
- **Color Temp:** Electric blue + white + accidental pastels
- **Typography:** Experimental mono/sans (Space Mono, JetBrains Mono)
- **Maturity Signals:** "Ader Space" (retail gallery), error as branding, editorial magazine

### DNA-29: Niko And... Style
- **Header:** Mixed English/Japanese, lifestyle-first nav
- **Hero:** Cafe-meets-lifestyle photo, warm tone filter
- **Product Grid:** 3-col, mixed products (clothes, furniture, food)
- **Color Temp:** Warm café tones (latte, matcha, raw wood)
- **Typography:** Friendly rounded sans + serif accent
- **Maturity Signals:** Event space info, curated lifestyle articles, seasonal "market" features

### DNA-30: Sulwhasoo Style
- **Header:** Elegant serif, gold accent line, bilingual (KR/EN)
- **Hero:** Product with traditional Korean art motifs
- **Product Grid:** 2-col centered, ritual/routine-based grouping
- **Color Temp:** Deep burgundy + gold + rice paper cream
- **Typography:** Elegant serif (Cormorant, Nanum Myeongjo)
- **Maturity Signals:** Heritage story, ingredient provenance (ginseng garden), ritual builder, luxury samples

---

## Family G: Fragrance & Ritual

### DNA-31: D.S. & DURGA Style
- **Header:** Centered logo with flanking horizontal nav (Perfume / Candles / Skin). Cart icon with free-shipping threshold counter. Sticky lavender (#e6bfff) announcement ticker
- **Hero:** Full-width image + video asset, text overlay with product name + tagline, single CTA to featured product. No hard overlay — text floats with ample whitespace
- **Product Grid:** Horizontal carousel (not grid), multiple cards visible per viewport. Card: image → title → description → price (multiple sizes listed). Nav arrows for scrolling
- **Color Temp:** White/off-white base, lavender (#e6bfff) accent, near-black text, neutral gray (#e5e5e5) borders
- **Typography:** Adobe Caslon Pro serif (weights 400/700, normal + italic) — classic premium hierarchy
- **Maturity Signals:** "Sniff Quiz" interactive fragrance finder, 15% newsletter discount gate, $5 gift wrap with custom note, free shipping progress tracker, 5 physical retail locations (NYC×3, LA×2), Level Access accessibility badge
- **Footer:** 4-column: Info / Shop / Stores / Social. SMS opt-in + newsletter. Physical retail addresses

### DNA-32: Mihan Aromatics Style
- **Header:** Centered "Mihan Aromatics ™" logo (color inverts black/white per section). Nav: Shop All / Discover My Scent / Stockists. Announcement bar above. Account + cart icons right
- **Hero:** Minimal typography-emphasis, no large hero image. Focus on navigation into collections and product discovery pathways
- **Product Grid:** 4-col desktop / 2-col mobile, portrait aspect ratio 150% (tall cards), white backgrounds, image-forward. Clean minimal
- **Color Temp:** 11 color scheme variants — primary white+black, alternates include dark #000 bg, warm beige #ab8c52, sage green #aecfb8
- **Typography:** Inter sans-serif (weights 400-600), 16px base. Navigation: 13px uppercase, 0.05em letter-spacing
- **Maturity Signals:** 200+ country/currency selector with flags, "Discover My Scent" quiz, Instagram as primary social, Schema.org Organization + Store markup

### DNA-33: Aather Style
- **Header:** AATHER logo centered above navigation. Menu: Home / An Introduction / Making / Candle Care / Stories. Hover image previews on nav items. Full-screen mobile overlay nav
- **Hero:** Full-width background image with centered text "Light a candle to match the mood". CTA: "Shop Candles". Generous whitespace, dark text on light backgrounds
- **Product Grid:** 2-column desktop. Cards: image / name / scent notes / size & burn time / availability status. "Sold out" displayed prominently. Minimal hover effects
- **Color Temp:** White #ffffff base, warm gold #9B9174, warm gray #D5C2A8, off-white #EDEBE7
- **Typography:** "Gestura Text Thin" serif (weight 200) for headings, "Untitled Sans Light" (weight 200) for navigation. H1: 100px desktop
- **Maturity Signals:** Animated announcement marquee, color-coded section backgrounds per page, Instagram feed 6-image grid in footer, Spotify link (music/mood pairing brand identity)
- **Footer:** Multi-column: Shop / Info (FAQ, Contact, Press) / Social (Instagram, Spotify) / Currency selector. Newsletter signup

### DNA-34: Emma Lewisham Style
- **Header:** Logo left, account + cart icons right. Clean Shopify-based structure
- **Hero:** Luxury skincare photography, high-end clean beauty positioning
- **Product Grid:** CSS Grid/Flexbox responsive, Judge.me review widgets with star ratings on product cards
- **Color Temp:** Primary brand purple/violet #49369E, secondary lighter purple #524EB7, teal accent #108474, white background
- **Typography:** "Regola Pro" custom font for buttons/CTAs, system fonts for body, 32px heading size
- **Maturity Signals:** Judge.me review system, BOLD Product Upsell, Regios dynamic discount engine, floating contact form, NZ luxury clean beauty positioning, hCaptcha integration

---

## Family H: Botanical & Wellness

### DNA-35: SuperMush Style
- **Header:** Sticky nav, logo left-center. Primary: Shop / Science / Bundle & Save. Secondary tier: Gummies / Mints / Mouth Sprays. Announcement ticker with swiper above header
- **Hero:** Full-width centered text "Think. Move. Feel." Dual CTA: "Shop Gummies" + "Shop All". Product shot background, min-height 550px. Bold, energetic
- **Product Grid:** 6-column carousel. Cards: image / title / benefit tags (Power• Strength• Focus) / star ratings (4.8-5.0) / price with subscription discount
- **Color Temp:** Off-white #f5f4f1, bright yellow-lime #eaff00 accent, orange #ff632a, dark navy buttons
- **Typography:** "Founders" custom font (medium weight) for headings, standard sans for body. Short punchy descriptors
- **Maturity Signals:** Cart progress bar + free gift upsell system, subscription toggle with 25-40% discount, ambassador testimonial carousel with photos, ingredient showcase with icon graphics
- **Footer:** 5-column: Shop / Science / About / Community / Connect. Newsletter. Social: IG, FB, X, TikTok, YouTube

### DNA-36: Houseplant Style
- **Header:** Fixed nav, HOUSEPLANT logo left. Account icon right. Megamenu dropdown: Shop All / New Arrivals / Collaborations / Sale. Header BG: dark chocolate #321E1E when scrolled
- **Hero:** Carousel full-width images with text overlays. Promo hero slot (⚖️ original site runs "25% OFF SALE" — only reproduce a reduction claim with a 30-day baseline; otherwise use a non-price hero message). Bold typography CTAs
- **Product Grid:** 2-4 column responsive. Cards: image / title / star ratings / price / "Add to Cart". Quick-add with variant selectors
- **Color Temp:** Chocolate brown #321E1E primary dark, cream #F4F1E0 light, teal #0E7D81 accent, muted gray #676986, taupe border #BDB498
- **Typography:** Custom "Houseplant" serif typeface (weight 400), 17-20px+ headings, system sans fallback
- **Maturity Signals:** Free shipping progress bar, age-gate modal overlay, referral program, review/rating widgets, announcement bars + promo banners
- **Footer:** Social: IG, Twitter, FB. Brand: Shop / Story / Beverages. Customer: Contact / FAQs. Legal: Privacy / Terms / Data management

### DNA-37: Leif Style
- **Header:** Centered "LEIF" logo, sticky. Categories: New / Home / Table / Woman / Jewelry / Art / Paper / Sale. Multi-level dropdowns. Search + cart right; mobile drawer menu
- **Hero:** Carousel/slider full-width. Text overlays as clickable collection links ("shop by color — red", "vintage capsule"). Multiple sequential product showcase
- **Product Grid:** Responsive centered-text cards. Image-first, minimal borders. Desktop: 16px H / 40px V spacing
- **Color Temp:** Off-white RGB(253,253,251), muted gold/tan RGB(211,211,166) accent, dark navy RGB(18,18,18) variant
- **Typography:** "TributeOt" serif (1.5-1.6rem, line-height 1.8) for body, "SackersGothicStd" sans (weight 600) for headings
- **Maturity Signals:** Color-curated shop collections ("shop by color"), auto-rotating carousel, Instagram primary social, store locations listed

---

## Family I: Tech & Design Objects

### DNA-38: Nothing Style
- **Header:** Left-aligned "Nothing (R)" logo. Horizontal nav: Shop All / Phones / Audio / Watches / Accessories / CMF. Secondary tier: Support / Newsletter / Store / Languages
- **Hero:** Full-width product photography per category. Centered headlines ("It's metal now" / "Built different"). Bold product-centric CTA ("Pre-order" / "Discover")
- **Product Grid:** Carousel/section layout (not traditional grid). Single feature product per section with rounded corner cards
- **Color Temp:** White/off-white base, dark gray/black text. Minimal accent — product imagery carries all color. Signature: dot-matrix / transparent texture elements
- **Typography:** Modern clean sans-serif throughout. No ornamental typography; readability-first. Minimal hierarchy variation
- **Maturity Signals:** Widget placements reflecting product OS aesthetic, YouTube embed integration, geo-location store switcher, newsletter validation, comprehensive regional store links

### DNA-39: Symbol Audio Style
- **Header:** Logo with opacity control (fades into page). Hamburger mobile; desktop: Shop / Learn / Showroom / Contact. Expandable submenus
- **Hero:** Full-width image carousel. Repeating CTA: "Visit our NYC Showroom Today!" Centered text overlays on lifestyle photography
- **Product Grid:** Responsive cards: image / title / "from $XXX" pricing / color swatches / Bestseller or Exclusive badges. Multiple product photos per card
- **Color Temp:** Golden Yellow #efa807, pure white #fcf9f1, graphite black, USM beige #bfa27a, olive green #414c2a. Light/dark mode toggle
- **Typography:** Premium-craft aesthetic hierarchy via CSS classes (.h1mock, .normal). Semantic heading structure
- **Maturity Signals:** Light/dark mode theme toggle, color-coded finish swatches, "Bestseller" (red) and "Exclusive" (blue) badges, newsletter modal, physical NYC showroom emphasis

### DNA-40: OCTAEVO Style
- **Header:** Sticky fixed, logo left (~11em). Mobile hamburger (3-line → X transform). Desktop inline nav at 75em+ breakpoint
- **Hero:** 90vh mobile → 100vh desktop. Swiper carousel with animated text (opacity + translateY). Pagination dots customized per breakpoint
- **Product Grid:** Swiper carousel cards. Image cover-fit / title / price / color variant selector. Hover: 1.05x scale. Color variants filter via data attributes
- **Color Temp:** Warm off-white #f6f6ed, light blush #f8eeee, cream #fdfdf3, dark charcoal #313131 text, red accent #c53b2f. Extensive custom product color palette (black, navy, mint, gold, blush pink, purple)
- **Typography:** "Domaine" serif (2.1-3.7em responsive) for headings, "Moderat" sans (17px, line-height 1.47) for body
- **Maturity Signals:** Sticky product bar on PDP (scrolls with user, shows color/qty/price), animated cubic-bezier transitions, rotating promo banner, skip-to-content accessibility, hCaptcha, MailChimp newsletter with GDPR checkbox

### DNA-41: Varier Style
- **Header:** Fixed top nav, transparent on scroll. Logo left; centered: Our chairs / Why movement / Stories. Mobile hamburger below 900px
- **Hero:** Full-width video background with overlay. Headline bottom-left: "Rethink sitting". CTA: "Explore our chairs" — white text on dark BG
- **Product Grid:** Mobile horizontal scroll slideshow, desktop 3-4 column. Cards: 3:4 aspect ratio / name / material-color variant / stock status. Hover: background color transition
- **Color Temp:** White #ffffff light, #494949 dark mode default, green #4caf50 success, red #f44336 error, neutral #D9D9D9
- **Typography:** "Roobert" custom sans-serif throughout. Headings: 3rem-5.27vw responsive scaling. Body: 1rem, line-height 1.45
- **Maturity Signals:** Product illustrations showing curved wooden runners, "In stock" badges, Klarna payment integration, multi-currency (SEK, EUR, GBP, NOK, DKK)

---

## Family J: Craft & Maker

### DNA-42: Flying Papers Style
- **Header:** "MenuControlsNoBackground" — hides on small screens. Sticky/fixed with controlled z-index. Max-width 1197px centered
- **Hero:** Full-viewport sticky section (min-height 100vh). Center-aligned text. Decorative scaled elements. CTA buttons with "PopOut" shadow/depth offset style
- **Product Grid:** 2-col mobile (calc 50% - 0.25rem). 3px solid #1A1A1A borders. Pseudo-element shadow offset -3px/-3px. Hover: scale 0.92→0.94. Rounded corners 6px
- **Color Temp:** Cream #F9F5F2, muted purple #8584BD, bright yellow #f4ed36, coral #F8C1BA, sage #B5C995, dark green #375027, mauve #AC4F98
- **Typography:** "ObviouslyVariable" (weight 800, uppercase, variable stretch 100-800%) for headings. "DegularDisplay" (multiple weights) for body. "bergen_monoregular" for labels. H1: 58rem max
- **Maturity Signals:** Dotted shadow pattern via radial-gradient (8px polka dot), multiple sticky scroll sections, rotation animations on hover, masked text overflow, staggered z-index layering

### DNA-43: Makr Style
- **Header:** "MAKR" logo top-left. Horizontal nav: New Releases / Wallets / Bags and Totes. Secondary: About / Process / Stockists / Help. Cart icon with counter. Minimalist
- **Hero:** No traditional large hero — immediate category tile display with background images and centered text overlays. Modular, non-narrative layout
- **Product Grid:** 2-3 column desktop. White/off-white backgrounds. Cards: product photo / title / descriptive text / PRE-ORDER or NEW badge / price. Splide carousel
- **Color Temp:** White/off-white base, black text. Minimal accent colors; craft leather tones carried through product imagery
- **Typography:** Modern sans-serif. Hierarchy via size. Descriptive product naming (e.g., "Impossible Bottom Corners")
- **Maturity Signals:** Newsletter modal "10% Off First Purchase", craftsmanship language ("Taking an industrial approach to craft"), Studio Birdsall attribution, physical address (St. Augustine, Florida)

### DNA-44: Postevand Style
- **Header:** Left-aligned logo. Nav: Shop / Impact / 3% Pledge / Wholesale. Contact email + phone + Instagram handle in header. Shopping bag icon right. Mobile hamburger
- **Hero:** Full-width responsive background image (mobile + desktop variants). Text overlay. Primary CTA to product collections
- **Product Grid:** 3-column desktop. Cards: product image carousel (front/back variants) / title / price per unit. White backgrounds
- **Color Temp:** White/light neutral base, dark gray text. Natural product photography dominant. Clean sustainability minimalism
- **Typography:** "Nimbus Sans D OT" custom web font (weights 400/700). Bold sans headings, regular body
- **Maturity Signals:** Lifecycle assessment callouts (97% plant-based, 18% lower climate impact), component diagram showing carton construction, B Corp badge, "Always drink tap water" tagline, Smiley food report link

---

## Family K: High Fashion & Streetwear

### DNA-45: KidSuper World Style
- **Header:** Minimal fixed bar. Logo as text left-aligned. Only Cart(0) + Close X on right. Almost no nav chrome — extreme restraint
- **Hero:** Loading progress bar as intentional design element. Products presented through copy as art ("If you send me a better purse design I'll give you a $100 gift card"). Anti-commerce commerce
- **Product Grid:** Responsive 25+ item grid. Cards: image, title, price, color variants (Grape, Mint, Yellow, Orange), real-time stock indicators
- **Color Temp:** Monochromatic — product colors do the palette work. No strong brand hex
- **Typography:** Custom abcDiatypeMono (monospace) + neueHaasGroteskDisplay. Geometric, intentional, anti-fashion
- **Maturity Signals:** Basement Studio partnership credit, real-time inventory display, art-brand positioning, custom type license

### DNA-46: Maison Margiela Style
- **Header:** Dual-brand system: "Maison Margiela" and "MM6" as top-level selectors. Horizontal: Women, Men, Unisex, About Us. Logo centered; account + wishlist + bag right
- **Hero:** Carousel/slideshow. SS26 "Joy" campaign — high-production film imagery. "Discover more" CTA. No aggressive conversion language
- **Product Grid:** 4-column desktop. Cards: image, name, localized price (TWD), "Preorder" badge, brand label (MM6 vs Margiela), color swatches
- **Color Temp:** Black + white primary. Warm neutrals (camel, pink beige) from product imagery only. Zero decorative color
- **Typography:** Sans-serif dominant throughout (deliberately anti-traditional for luxury). Regular and bold weights
- **Maturity Signals:** Dual-brand navigation architecture, regional currency/language selector, Preorder state management, deep editorial integration, loyalty segmentation in newsletter

### DNA-47: Entire Studios Style
- **Header:** Centered hamburger. Logo centered. Right: search, currency selector (USD), bag counter. Top marquee cycling promos ("adidas x entire studios - selling fast"). Dark/light mode
- **Hero:** Video-first — not traditional hero but grid of clickable collection tiles, each with video poster (1.78:1 ratio). Multiple collection launches compete equally
- **Product Grid:** Carousel/showcase grouped by collection (SS26, AW25, Archive, Uniform, Adidas collab) rather than flat grid. Video per section
- **Color Temp:** Near-white CSS variable bg. Black text. Dark mode supported. Video/imagery carries all color
- **Typography:** System font stack (Segoe UI, Roboto, Helvetica) + custom WOFF2 via Next.js. Minimalist voice
- **Maturity Signals:** Next.js framework, Klaviyo email, dark mode OS preference detection, custom WOFF2 fonts, video-first strategy, major brand collab (adidas) as hero

### DNA-48: Berner Kühl Style
- **Header:** Horizontal, logo centered, cart top-right. Nav: Shop, Collections, Inventory, Information with category dropdowns (Outerwear, Shirting, Knitwear)
- **Hero:** Marquee carousel with large-scale product photography. Minimal text overlay. Photography-led, not copy-led. Editorial campaign content ("PRESS25 Campaign")
- **Product Grid:** 3-4 column flexible. Cards: item code, product title, image. Pricing implicit (not foregrounded). High-quality photography
- **Color Temp:** Off-white/cream bg, deep charcoal text. Zero decorative color. Copenhagen minimalism
- **Typography:** Clean sans-serif, bold headings, generous line-height. Luxury spacing conventions
- **Maturity Signals:** Geographic coordinates as brand identifier (55.6761° N, 12.5683° E Copenhagen), FOLD magazine editorial, "Inventory" nav (not "Shop"), slow-fashion positioning

### DNA-49: P.A.M. (Perks and Mini) Style
- **Header:** Fixed sticky 57px. P.A.M. mutation graphic logo left. Right: search, account, cart. Announcement carousel with ✦ separators. Hamburger mobile with expandable sections
- **Hero:** Full-width lifestyle photo (P.A.M. x George Cox campaign). Dual CTA: "Shop" + "Photos". Overlay text left at 50% width
- **Product Grid:** 4-col desktop / 2-col mobile. Cards: image (150% aspect ratio), title, AUD price, "Add to cart" on hover, "New" badge, sold-out/pre-order states
- **Color Temp:** White/Black base. Deep purple accent #64288c. Sale red #da0000. Success green #56ad6a. Earth tones in alternates. 11 total color schemes
- **Typography:** Helvetica/Arial system stack. 700 weight headings, 0.05em letter-spacing. Uppercase nav option. 15-50px heading scale
- **Maturity Signals:** 11 switchable color themes, 40+ brand A-Z partner organization, Klaviyo restock notifications, persistent cart drawer with free shipping threshold, lookbook "Shop the look", blog 3-column grid

### DNA-50: HARDCLO Style
- **Header:** Horizontal bar, logo left. Nav: SHOP dropdown (T-Shirts, Hard Classics, Headwear, Accessories, Hoodies, Shirts, Swimwear, Sales), About. Cart counter right
- **Hero:** Image carousel/gallery — 4+ lifestyle fashion shots. "Southern Realities" collection. Magazine-style editorial layout. No prominent text CTA
- **Product Grid:** WooCommerce-based. Variation swatches (30x30px squared buttons). Responsive grid. Cards: price, availability, variation options
- **Color Temp:** White/Black base. Charcoal #32373c buttons. Accent purple #9b51e0. Functional defaults
- **Typography:** CSS-variable font system. Button text 1.125em. Standard and bold weights
- **Maturity Signals:** Facebook Pixel + Google Analytics, WooCommerce variation swatches, Instagram/Facebook/Soundcloud social, physical store (Athens, Greece)

### DNA-51: Filling Pieces Style
- **Header:** Horizontal, logo far left. Mega-menu: Men, Women, Our World, Rewards. Subcategories: New Arrivals, Shoes, Clothing. Right: search, login, wishlist, bag
- **Hero:** Full-width banner. "Breaking Bread" headline, "Spring/Summer 2026" tagline. Dark bg, light text. CTA: "SHOP NOW"
- **Product Grid:** Card-based responsive. Featured: "Loafer Pepper Black" at €390. Cards: image, title, price, size/color options
- **Color Temp:** Forest green primary #005540. Black + White. Neutral grays. Signature green anchors brand without overwhelming
- **Typography:** Oswald + Cardo + Big Caslon mixed serif/sans for headlines. System fonts for body performance
- **Maturity Signals:** Loyalty rewards program, free shipping threshold (€150), Shopify Pay + Apple Pay + 3D Secure, mega-menu architecture

### DNA-52: Clyde Style
- **Header:** Sticky, CLYDE logo centered (150px desktop). Horizontal: Shop, Archive Sale, Everything, New Arrivals, Winter Favorites, categories (Scarves, Hats, Gloves, Bags). Account + cart + currency selector
- **Hero:** Announcement banner as primary hero: "Shop The Archive — one of a kind, samples, rare styles, previous season." Limited-time event framing
- **Product Grid:** CSS variable columns: 4 desktop, 3 medium, 2 small, 1 mobile. Cards: 120% aspect ratio images, sale badges, "Sold Out" indicators, pre-order labels
- **Color Temp:** White #ffffff bg, text #212121. Button cream #f5f2ec with black text. Gold accent #ab8c52. Warm and restrained
- **Typography:** Karla sans-serif throughout. Weights 400/500. 13px uppercase buttons. 16-46px heading scale
- **Maturity Signals:** 11 color schemes + transparent overlays, 70+ predefined swatch colors, archive sale as editorial event, handmade/small-batch positioning, currency selector

### DNA-53: Terminal 27 Style
- **Header:** Luxury retail navigation. Syndicat Grotesk typeface exclusively throughout visual identity
- **Hero:** Gallery/editorial alongside retail — concept store framing (gallery + café + boutique at Beverly Blvd, LA). Five-sense experience
- **Product Grid:** Shopify-based. Luxury + emerging designers (Rick Owens, Ottolinger, Maisie Wilen). AJAX filtering, lazy-loading, modal product popups
- **Color Temp:** Black/white neutrals. Typography does the visual identity work
- **Typography:** Syndicat Grotesk (edition.studio) — single-typeface brand system. Contrasting sizes, reversed type on images, numeral-forward compositions
- **Maturity Signals:** Bespoke identity with CTHDRL studio, custom editorial section, single-typeface discipline, physical concept store, Fonts In Use industry recognition

---

## Family L: Food & Beverage

### DNA-54: Mr. Pops Style
- **Header:** Minimal. mr.pops logo top-left. Centered menu toggle. Nav: Home, About Us, Catalog, Selling Points, FAQ, Contacts. Language switcher UA/EN
- **Hero:** Full-width immersive with Lottie animations. Cloud SVG graphics. CTA: "Flavours" to catalog. Narrative copy: "He'll win over even those completely indifferent to ice cream." Brand personality over conversion
- **Product Grid:** 2-4 column responsive. Cards: pastel product photography, flavor name, weight (80г), "New" badges, out-of-stock states. Whimsical
- **Color Temp:** Soft pastel product photography dominates. Light neutral backgrounds. Cloud graphics neutral. Product color variety does brand work
- **Typography:** Readable sans hierarchy. Conversational tone in copy
- **Maturity Signals:** Lottie animation integration, Google Form for B2B partnerships, regional delivery info, marquee scrolling values, cloud SVG system, narrative brand voice

### DNA-55: Fallen Grape Style
- **Header:** Sticky, logo left-center. Nav: Shop All, Shop Wine, Shop Merch, About Us. Right: Log in + Instagram + TikTok social links
- **Hero:** Full-width parallax banner (desktop + mobile variants). Organic butterfly and dragonfly SVG graphics. CTA: "SHOP ALL". Tagline: "It's natural"
- **Product Grid:** Swiper.js carousel — 1.2 slides mobile, 2 tablet, 3 desktop. Cards: image, title, price, unit pricing. Spacing 4-8px mobile, 8-20px desktop
- **Color Temp:** Warm brown #573d21, cream/beige #ece0d2, warm orange #efa164, light cream #f3f3f3. Earthy, warm, organic
- **Typography:** Romie (regular/bold) primary. Arial Narrow 700 for headings. 1.8rem mobile / 2rem desktop. 0.06rem letter-spacing
- **Maturity Signals:** Age verification modal, dual social (IG + TikTok) in header, animated SVG wildlife graphics, natural wine narrative, Santa Ynez CA sourcing story, unit pricing

### DNA-56: Misuko Style
- **Header:** Horizontal, logo left. Nav: "Our story," "Corporate," "Private label." Language switcher (EN/NL/FR) + Login + cart right
- **Hero:** Headline-led: "We design healthy, creative and trendy drinks." CTA: "Let's get in touch." Content-first, no full-bleed hero image
- **Product Grid:** 4-column desktop. Cards: 300×300px thumbnails, title, Euro price (€2.50-€12.90), ingredient description, "Add" CTA. Ingredient transparency card-level
- **Color Temp:** White/cream bg. Dark charcoal text. Earthy greens in product imagery. Subtle blues interactive
- **Typography:** Custom "Beausite" (BeausiteClassicWeb) 400/500 weights. Semantic H1-H3 hierarchy. Clean sans modernity
- **Maturity Signals:** Multi-language (EN/NL/FR), Grapify ERP integration, detailed service tier pricing, newsletter, social (IG/LinkedIn/FB)

---

## Family M: Design & Furniture

### DNA-57: LAK Gallery Style
- **Header:** Sticky horizontal flex. "LAK Gallery" text logo left. Right nav: 3 breakpoints (desktop >1440px / tablet icon / mobile hamburger). Cart "(0)" right. 30px padding. Light gray border #E5E5E5
- **Hero:** No traditional hero — jumps directly into alphabetically categorized product collections (Chairs, Table Lamps, Stools, Mirrors, Cabinets, Vases, Coffee Tables)
- **Product Grid:** Dual system: (1) Horizontal scroll carousels with hidden scrollbars (min-width 294px) for major categories; (2) 2-col desktop / 1-col mobile for others. Cards: 1:1 square, 30px padding, 1.05x hover scale (0.3s ease). Price in EUR, designer attribution
- **Color Temp:** White/black high-contrast. Light gray #E5E5E5 borders. Warm neutrals: Pampas #F1EDE8, Ecru #F9F7F0, Wood #F4F0E9
- **Typography:** NeueHaasGrotesk (woff2). Display: 154px desktop / 47px mobile, weight 400, letter-spacing -2px. Body: 25px / 19px at -0.5px tracking
- **Maturity Signals:** 20+ featured international designers with bio pages, multi-currency (EUR/USD/AUD/CAD/GBP/CHF), Sanity CDN imagery, Tinloof developer credit (known high-end Shopify agency)

### DNA-58: OMHU Copenhagen Style
- **Header:** Minimal modern, OMHU logo top-left. Responsive nav. Shopify-native backend
- **Hero:** "Elevating spaces with our iconic TEDDY sofa" — product-hero format with marquee piece as anchor
- **Product Grid:** Card-based with Trustpilot integration. Shopify collection layout with multiple color schemes (dark purple #5027BD through vibrant blue #2445EB)
- **Color Temp:** Warm off-white #FBFAF5. Vibrant blue CTA #2445EB. Black text. Light taupe #EFECEA. Warm gray borders #D0C9BD. Green confirmations #21A050
- **Typography:** "Syne" (500/600) for headings. "DM Sans" (400) for body. "Reenie Beanie" as decorative editorial accent. Capitalized buttons. 61-90% mobile ratio
- **Maturity Signals:** Trustpilot integration, Pandectes GDPR, hCaptcha, Klarna + Shop Pay, showrooms across Europe and USA, D2C model with influencer partnerships

### DNA-59: Vitra Style
- **Header:** Fixed 90px, white bg. Vitra logo centered-left. Horizontal: Products, Inspirations, Services, Professionals, Magazine, Campus, About Vitra. Search + cart right. "vitraFutura" custom font
- **Hero:** Full-width image teasers at 0.65:1 desktop ratio. Dark overlay (#101010 at 30%). White centered text. CTAs: "Discover more" / "Register for early access"
- **Product Grid:** Up to 6-column desktop. Square cards with image overlays. Hover: darkens + "Discover" in light blue #02BAF2 + 1.06x scale (0.5s cubic-bezier). 20px col gaps, 32-64px row gaps
- **Color Temp:** #333 text, #101010 headings, #FFF bg, #02BAF2 interactive blue, #D43E42 hover red
- **Typography:** "vitraFutura" / "vitraFuturaV2" (custom Futura), Arial fallback. Weights 300-600. Body 17px / 1.9 line-height. Headlines 30-50px. Button letter-spacing 2.1px
- **Maturity Signals:** Designer attribution (Eames, Nelson, Prouvé), "Vitra Professionals" dealer portal, client logos (Royal College of Art, Swatch, citizenM, On), CAD downloads, "Vitra Circle Stores" sustainability, Campus physical location, Magazine editorial, GSAP scroll animations, 70+ years heritage

### DNA-60: François-Joseph Graf Style
- **Header:** Minimal. Logo "François-Joseph Graf PARIS" centered. Language toggle (FR/EN) in footer. Portfolio-first hierarchy, no prominent nav bar
- **Hero:** Gallery-heavy — multiple high-res images (1002-1008px × 1368px) in horizontal slider (5000px width container). Not a single hero — panoramic scroll
- **Product Grid:** 3-column desktop portfolio (1-col mobile). 60px gaps. Absolute-positioned image stacks with Gatsby opacity transitions (0.25s linear)
- **Color Temp:** White #FFF, Black #000, Gray #999. High contrast, maximum whitespace
- **Typography:** "Sweet Sans Bold" custom. Uppercase site-wide. 13px base (10px mobile). Bold/700 throughout
- **Maturity Signals:** Physical address: 43 rue du Faubourg Saint Honoré, 75008 Paris. Phone number. Clientele includes Valentino Garavani. Versailles Palace credential. École des Beaux-Arts + École du Louvre pedigree

---

## Family N: Specialty & Multi-brand

### DNA-61: Riptype Style
- **Header:** Minimal left-aligned SVG logo ("RT" mark). Cart with count top-right. No traditional nav bar — navigation implicit through page structure
- **Hero:** Foundry statement ("Riptype is a type foundry by Ciarán Brandin and Nick Losacco") + featured release: "Office 2.0 is out now!" with star icon accent
- **Product Grid:** 4-typeface gallery using custom SVG previews — each card renders typeface name in its own face. Visual authenticity over photography
- **Color Temp:** White/light gray bg. Purple selection accent #9483ED. Minimal saturation
- **Typography:** Fluid responsive scaling (clamps 0.6667rem-0.875rem). Custom foundry typefaces on display
- **Maturity Signals:** Transparent 3-tier pricing ($50-$500/weight), comprehensive FAQ, email contact, active Instagram, professional licensing structure

### DNA-62: Brentano Fabrics Style
- **Header:** Sticky horizontal. Red wordmark logo left. Account links + showroom nav right. Hamburger mobile with slide-out overlay. Search icon overlay
- **Hero:** Full-width image carousel — Luminary and Terra collections. Lifestyle photography storytelling, no heavy overlay text. Images link to collections
- **Product Grid:** Category-based browsing: 7+ types (Upholstery, Wallcovering, Eco Fabrics, Vegan Leather). Standard card format
- **Color Temp:** Primary red #CA382B logo/hover. Black #000 nav bg. White #FFF content. Gray #6D7882 body text
- **Typography:** Bold headlines, subdued body. Professional readable hierarchy
- **Maturity Signals:** Founded 1990, 35+ years. Terra biodegradable collection. Textile Glossary, care guides, warranty docs. Careers + sustainability pages. Flickr + Pinterest + IG + FB + Twitter

### DNA-63: DECIEM Style
- **Header:** Two-tier sticky: utility bar (37px) with location/language + brand switcher showing The Ordinary, NIOD, LOOPHA, DECIEM logos horizontally. Main: logo, dropdowns, search, login, cart
- **Hero:** Full-width (357px mobile / 611px desktop). "• t h e a b n o r m a l l a b •" with spaced lettering. Rotating pastille element (15-20rem diameter) with spinning text. Animated arrow CTA
- **Product Grid:** 2-col desktop / 1-col mobile. No card borders/shadows. Left-aligned text. GSAP motion path animations — products animate along SVG paths on scroll
- **Color Temp:** White #FFF bg, near-black #121212 fg. Accent blue #334FB4. Stark and clinical
- **Typography:** "Assistant" (Google, 400-700) body/headings. "Geologica" in video. Base 10px (62.5%), body 1.5-1.6rem. Decorative 0.31em letter-spacing rotating text
- **Maturity Signals:** Estée Lauder ownership, Modern Slavery Act compliance, CAMH partnership, Veritree + 4ocean sustainability, renewable energy credits, accessibility page, "1 product sold every second"

### DNA-64: UY Studio Style
- **Header:** Centered logo. Dropdown: Fragrance Collection (U/S/X scents, Candles), Core Homewear, Gift Collection, Clothing, Journal, The Studio. Account + multi-currency (EUR/USD/JPY/GBP/CHF/SEK) top bar
- **Hero:** Large banner "BECOME MORE OF YOU". Aspirational lifestyle. Berlin club culture identity. Clean, dark aesthetic
- **Product Grid:** 4-column desktop. Cards: high-quality photography, brand attribution, product title ("U ROOM SPRAY"), Euro pricing (€59-€89). Structured JSON product data with inventory
- **Color Temp:** Black #000 buttons/text. White #FFF bg. Muted rose #D59392 accent. Off-white/gray neutrals
- **Typography:** Helvetica/Arial system stack. Capitalized button text with 10px letter-spacing. 15px base
- **Maturity Signals:** Shopify infra, GDPR cookie management, Weglot multilingual, Appikon back-in-stock waitlist, physical Berlin studio with hours, B2B inquiry, employment listings

### DNA-65: Nestig Style
- **Header:** Clean minimal, "Nestig" logo left. Shopify cart + customer account integration
- **Hero:** Shopify modular section-based. Performance-optimized. Warm, parental brand voice
- **Product Grid:** CSS variable grid (24px desktop / 12px mobile spacing). Zero border radius on cards. Flat, contemporary minimal card aesthetic
- **Color Temp:** Deep black #0A0A0A. Warm off-white #F9F5F2. Navy blue accent #173482. Warm taupe #D1B19B. Multiple color schemes
- **Typography:** Matter (400/500/600) primary. Gooper + Geneva secondary. All WOFF2 optimized. Warm, approachable
- **Maturity Signals:** 150+ named color swatch system ("Bluebell Gingham", "Dinosaur Island"), hCaptcha, zero-radius as deliberate design, performance-first loading, premium baby furniture with emotional naming

### DNA-66: Blok Studio Style
- **Header:** Fixed horizontal 130px. Logo (50x50px) left. Nav: Projects, About Us, Contact, Workshops, Jobs. Dark bg #0a0a0a with transparent overlay on load
- **Hero:** White bg with optional video layer at 20% opacity. Pink accent headline. German copy. CTA: "mehr über uns"
- **Product Grid:** Portfolio masonry 12-column system. Variable widths. Thumbnails with title + category on hover. 12 visible, "Load more" button. 1.15x hover scale
- **Color Temp:** Pink #f35973 / #f94852. Dark charcoal #0a0a0a. Warm beige hover #efb794. Off-white #f5f5f5. Muted gray #918788
- **Typography:** Apercu light/regular/bold. Custom blokstudio_iconfont. 15px body. Headlines bold, uppercase optional
- **Maturity Signals:** Custom icon font, full-screen hamburger with centered nav, video background with fade-in, masonry layout, German-language primary (Vienna market)
