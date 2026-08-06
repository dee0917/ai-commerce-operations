# Modern UI Framework Integration Guide

> **Purpose:** Each generated site MUST use a real UI component library instead of raw Tailwind.
> This ensures contemporary look, consistent components, and professional quality that
> raw CSS/Tailwind cannot achieve alone.

## Selection System

Each generation, randomly select ONE framework from the pool below.
Record selection in `design-system/DECISIONS.md`.

### Framework Pool (6 options)

| # | Framework | Vibe | Best For | Install |
|---|-----------|------|----------|---------|
| 1 | **shadcn/ui** | SaaS-modern, crisp | Clean DTC, Minimal | `npx shadcn@latest init` |
| 2 | **DaisyUI** | Themed variety (29 themes) | Artisan, Bold, Playful | `npm i daisyui` |
| 3 | **Radix UI + Tailwind** | Accessible, headless | Luxury, Editorial | `npm i @radix-ui/themes` |
| 4 | **Mantine** | Feature-rich, polished | Full-featured stores | `npm i @mantine/core @mantine/hooks` |
| 5 | **HeroUI** (前 NextUI) | iOS-inspired, smooth | Asian Modern, Minimal | `npm i @heroui/react framer-motion` |
| 6 | **Aceternity UI** | Motion-heavy, award-site feel | Bold, Contemporary | Copy components manually |

> ⚠️ **HeroUI 命名注意（2026-08 修正）**：HeroUI 於 2025 年初由 NextUI 改名，
> 舊套件 `@nextui-org/*` 已棄置，**安裝舊套件名會裝到死庫**。一律裝 `@heroui/react`，
> 並同裝 peer 依賴 `framer-motion`（僅供元件庫內部使用；站內自寫動效統一 `motion/react`，
> 見 `motion-system.md`）。

### Framework-DNA Affinity Matrix

When a DNA profile is selected, use this matrix to weight framework selection:

| DNA Family | Strong Fit | OK Fit | Avoid |
|------------|-----------|--------|-------|
| A: Clean DTC | shadcn/ui, Mantine | HeroUI | DaisyUI |
| B: Luxury | Radix UI, shadcn/ui | Mantine | DaisyUI |
| C: Modern Minimal | HeroUI, shadcn/ui | Radix UI | Aceternity |
| D: Artisan | DaisyUI, Mantine | Radix UI | HeroUI |
| E: Bold | Aceternity, DaisyUI | shadcn/ui | Radix UI |
| F: Asian Modern | HeroUI, Radix UI | Aceternity | DaisyUI |
| G: Fragrance & Ritual | Radix UI, shadcn/ui | Mantine | Aceternity |
| H: Botanical & Wellness | DaisyUI, Mantine | shadcn/ui | Radix UI |
| I: Tech & Design Objects | shadcn/ui, HeroUI | Aceternity | DaisyUI |
| J: Craft & Maker | DaisyUI, Radix UI | Mantine | HeroUI |
| K: High Fashion | Aceternity, shadcn/ui | HeroUI | DaisyUI |
| L: Food & Beverage | DaisyUI, Mantine | shadcn/ui | Aceternity |
| M: Design Furniture | Radix UI, shadcn/ui | Mantine | DaisyUI |
| N: Specialty & Multi-brand | Mantine, shadcn/ui | Radix UI | Aceternity |

### Mandatory Components from Framework

Regardless of which framework is chosen, these components MUST come from the framework (not hand-coded):

1. **Button** — all variants (primary, secondary, outline, ghost)
2. **Input / TextField** — with label, error state
3. **Select / Dropdown** — for filters, checkout
4. **Dialog / Modal** — for quick view, cart drawer
5. **Card** — for product cards
6. **Badge** — for "Sale", "New", "Sold Out"
7. **Toast / Notification** — for add-to-cart feedback
8. **Tabs** — for product details (Description / Specs / Reviews)
9. **Accordion** — for FAQ, mobile filters
10. **Skeleton** — for loading states (EVERY page must have skeleton)

### Anti-Patterns for Framework Usage

- Do NOT mix components from multiple frameworks
- Do NOT override framework styles with raw Tailwind to the point it's unrecognizable
- Do NOT use framework's default theme without customization (colors must match DNA)
- DO customize the framework's theme/config to match the selected DNA profile colors and fonts
