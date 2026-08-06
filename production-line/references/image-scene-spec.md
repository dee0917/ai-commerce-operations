# Image Scene Spec（商品圖場景規格）

> 一個站的商品圖看起來像同一個攝影師拍的，靠的就是這份規格。
> 這個機制原本存在於 PRD 時代：PRD_Gridwell.md:43 讓所有商品圖 prompt 共用尾碼
> `product_shot_on_soft_gray_background_studio_lighting`；PRD_AuraZen.md:75-80
> 鎖攝影類型與情緒關鍵字，且情緒關鍵字直接引用品牌色 Sand #E7D8C6。
> v11 廢除 PRD 時這一層被一起丟掉，沒有東西接手。本檔把它救回來，成為獨立的必要輸入。
>
> ⚠️ **出處說明**：`PRD_Gridwell.md` 收錄在 `examples/gridwell/`，行號可以直接對照。
> **`PRD_AuraZen.md` 未收錄於本 repo**（AuraZen 站本身也沒收），下文引用它的行號是留給原始檔的索引，
> 在這個 repo 裡查不到。要看得到的實例，一律以 Gridwell 的引用為準。

## 產生時機與硬性門檻

- 在品牌識別與配色定案之後、任何生圖動作之前，先產生本規格，存在站目錄。
- **缺這份規格不准生圖**：生圖腳本與 generate-image prompt 啟動前必須先讀到本檔，
  讀不到就中止，不得先生再補。
- 全站所有商品圖 prompt 一律拼接 shared_prompt_suffix，一張都不准例外。

## 必填欄位

| 欄位 | 說明 | 實際出處 |
|------|------|----------|
| photography_type | 攝影類型，全站商品圖共用一種 | PRD_AuraZen.md:77「Artisan lifestyle photography」 |
| background | 背景描述，全站商品圖共用 | PRD_AuraZen.md:78「Minimalist Zen interior with soft textures」；PRD_Gridwell.md:43「soft_gray_background」 |
| lighting | 光線描述，全站商品圖共用 | PRD_Gridwell.md:43「studio_lighting」；PRD_AuraZen.md:79「soft morning light, linear shadows」 |
| mood_keywords | 情緒關鍵字，**必須至少含一個品牌色 hex** | PRD_AuraZen.md:79「Digital Satori, Sand #E7D8C6 tones, Zen atmosphere」 |
| shared_prompt_suffix | 全部商品圖 prompt 共用的尾碼，由上面四欄串成 | PRD_Gridwell.md:43「product_shot_on_soft_gray_background_studio_lighting」 |

選填欄位：hero_keyword（PRD_AuraZen.md:79）、hero_banner_concept（PRD_AuraZen.md:80）。

## 為什麼必須綁品牌色

商品圖本身要帶著站的配色，圖文才是一體。2026-08 五站量測（metrics.json 與全頁截圖）：
- gridwell 商品圖全部是亮灰攝影棚窗光，來源就是共用尾碼裡的 soft_gray_background
- inkandecho 商品圖全部是深色木桌燭光古物場景
- vanguard 商品圖全部是黑石板暗調棚拍
- aurazen 成品配色第三名的沙金 rgb(231,216,198)，就是 PRD 情緒關鍵字裡的 Sand #E7D8C6，
  出現 43 次，圖與版面同一色

## 每商品圖庫下限（鐵律，2026-08-06 新增）

- 每個商品必須擁有**專屬於它自己的圖庫，至少 3 張**：不同角度／特寫／顏色
  （建議組成：主圖＋細節特寫＋情境或第二角度），全部拼接同一 shared_prompt_suffix。
- **嚴禁跨商品混用**：任何一張圖只屬於一個商品；兩個商品出現同一圖片 URL 即 FAIL。
- 圖庫直接餵前端動效：商品卡 hover 第二圖 crossfade 取第 2 張，詳情頁 gallery 取全部。
- 來源：2026-08 thirdstop（單圖沿用 8 次）、tensile（單圖沿用 4 次）健檢破口——
  同一張商品圖被不同商品或同商品不同角度反覆借用，是「圖片健康」檢查抓不到的另一種缺陷
  （檔案本身沒壞、路徑存在，只是同一張圖被重複使用）。
  已接進 `ecommerce-checklist.py` 的 `check_product_image_count`（blocking，掃 mockData.ts
  每個商品的 `images` 陣列）。

## 檢查（FAIL 條件）

任一條成立即 FAIL：
- 生圖啟動時本檔不存在，或任一必填欄位空白：中止生圖
- mood_keywords 裡沒有任何品牌色 hex
- 任一商品圖 prompt 沒有拼接 shared_prompt_suffix
- 成品驗收時抽任三張商品圖並排，光線或背景明顯不一致
- 任一商品專屬圖少於 3 張
- 任兩商品出現相同圖片 URL

## 完整範例（AuraZen 實例改寫）

以下欄位值全部取自 PRD_AuraZen.md:31-80 的實際內容，
shared_prompt_suffix 依 PRD_Gridwell.md:43 的尾碼格式把欄位串起來：

```yaml
brand: AuraZen
photography_type: Artisan lifestyle photography
background: Minimalist Zen interior with soft textures
lighting: soft morning light, linear shadows
mood_keywords: Digital Satori, Sand #E7D8C6 tones, Zen atmosphere
shared_prompt_suffix: artisan_lifestyle_product_shot_in_minimalist_zen_interior_soft_morning_light_sand_E7D8C6_tones
hero_keyword: minimalist zen interior, soft morning light
hero_banner_concept: A serene corner with a crystal pillar and a singing bowl on a low wooden table, morning light
```

套用示範：商品「Cinnabar Meditation Beads」（PRD_AuraZen.md:44）的生圖 prompt 為
`cinnabar_meditation_beads_artisan_lifestyle_product_shot_in_minimalist_zen_interior_soft_morning_light_sand_E7D8C6_tones`。
全站十二件商品共用同一尾碼，只換商品名。

---

相關檔案：`typography-baseline.md`（字體與版面鎖值，與本檔同為交付前的硬性檢查）。
