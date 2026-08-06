# Site Blueprint（建站藍圖：動手前先鎖定內容與鎖值）

> 本檔是硬性流程規格：任何一個站在寫下第一行程式碼之前，必須先產出一份
> 「本站藍圖」檔（存為站目錄根部的 `site-blueprint.md`），把商品、文案、
> 圖像場景、設計鎖值全部定案。藍圖不存在或五層有缺，不得進入工程實作。
>
> 這個機制在 PRD 時代被驗證過有效：AuraZen 成品的 h1、主按鈕、創辦人語錄
> 逐字等於 PRD（PRD_AuraZen.md:53-61）；Gridwell 十件商品的名稱與價格逐項
> 存活到成品（PRD_Gridwell.md:24-33）。v11 廢除 PRD 時，這一層沒有東西接手。
> 2026-08-04 的兩個站（20260804-thirdstop、20260804-tensile）站目錄裡
> 找不到任何一份內容規格檔，成品的每一個字都是寫程式途中臨場想的，
> 交付後想驗「字對不對、價格對不對」，連比對的基準都不存在。本檔把這一層救回來。
>
> ⚠️ **出處說明**：`PRD_Gridwell.md` 收錄在 `examples/gridwell/`，行號可以直接對照。
> **`PRD_AuraZen.md` 未收錄於本 repo**，下文引用它的行號是留給原始檔的索引，在這個 repo 裡查不到。

## 與現行 DNA 系統的關係（先讀這段）

兩者不衝突，是先後關係：

- **DNA 系統決定「長什麼調性」**。`real-ecommerce-dna.md` 的骨架選取、
  `design-system/DECISIONS.md` 的四項決策、創意宣言，回答的是：版型骨架、
  色溫、字體類別、動效層級。它給的是類別與方向，例如「Sans-serif geometric」。
- **藍圖決定「具體是什麼內容與哪些鎖值」**。這個站賣哪十件商品、各多少錢、
  每個區塊的標題逐字是什麼、商品圖共用哪一組場景、圓角釘在哪個值。
  它給的是實值與合約，例如「內文字型 DM Sans 16px，全站不准偏離」。

順序固定：**先選 DNA，產出決策檔與創意宣言；再依 DNA 產出本站藍圖；
然後照藍圖實作；交付前跑藍圖第五層的查核表。**
DNA 是輪盤，保證每站不重複；藍圖是合約，保證成品跟規格對得起來。
少了前者每站長一樣，少了後者成品無從稽核。

與另外兩份產線鎖值檔的分工：`image-scene-spec.md` 與 `typography-baseline.md`
定義的是**全產線通用**的欄位、合法範圍與 FAIL 條件；藍圖是**本站專屬**的一份
實例文件，第三層與第四層直接引用那兩份的規則，填入本站的具體值。

## 產生時機與硬性門檻

- 產生時機：Phase 1 全部完成（DNA 選定、DECISIONS.md、創意宣言）之後，
  Phase 2 工程實作動工之前。
- 存放位置：站目錄根部 `site-blueprint.md`，與 `design-system/DECISIONS.md` 並存。
- 硬性門檻，任一條成立即中止，不得動工：
  - 站目錄裡沒有藍圖檔
  - 五層任何一層缺漏或留白
  - 第一層任何一件商品沒有價格，或價格是佔位符
  - 第四層任何一個鎖值落在 `typography-baseline.md` 的合法範圍之外
- 實作期間藍圖唯讀。發現藍圖有錯，先改藍圖再改程式，兩邊同步，
  不准只改程式讓成品悄悄偏離規格。

---

## 第一層：商品清單

**填什麼**：每一件商品的名稱、價格、一句描述、所屬分類。四欄全必填。
**價格必須是實際數字，不是佔位符**。商品數依品類骨架決定（常態 8 到 12 件）。

**為什麼不先定會出事**：Gridwell 十件商品的名稱與價格先寫進規格，成品逐項
存活，交付後可以逐字對規格稽核（PRD_Gridwell.md:24-33）。2026-08-04 的
thirdstop 與 tensile 沒有這一層：商品名與價格是各頁面寫到時才發明的，
同一件商品在列表頁與詳情頁引用兩次就有機會出現兩個價格，而且因為沒有
基準可比，這種錯誤發生了也沒有人抓得到。

## 第二層：每個區塊的標題與主要文案

**填什麼**：首頁每一個區塊的標題（含 eyebrow 小標）、hero 的 h1 與主按鈕
文字、品牌故事段落；有創辦人語錄、社會證明、FAQ 的站，逐字寫進這一層。
**成品的字必須逐字從這裡來，不是邊做邊想**。實作時只准複製貼上，
不准現場改寫；想改字就回來改藍圖。

**為什麼不先定會出事**：AuraZen 成品的 h1、主按鈕「Shop the Collection」、
創辦人語錄，逐字等於規格（PRD_AuraZen.md:53-61），代表整站敘事在動工前
就被完整看過一遍。2026-08-04 的兩個站沒有這一層：每個區塊的文案是寫到
該區塊時臨場想的，沒有任何時刻有人把全站的字放在同一頁檢視過，
敘事斷裂與填充式空話（filler copy）就是這樣進站的；改版時也沒有唯一
事實來源，改哪句、漏哪句全憑運氣。

## 第三層：圖像場景規格

**填什麼**：依 `references/image-scene-spec.md` 的必填欄位，填出本站的
photography_type、background、lighting、mood_keywords、shared_prompt_suffix。
欄位定義、品牌色必綁規則（mood_keywords 至少含一個品牌色 hex）與 FAIL
條件以該檔為準，本層不重複定義，只負責在生圖之前把本站的值填好。

**為什麼不先定會出事**：見 `image-scene-spec.md` 開頭的完整證據鏈：
Gridwell 全部商品圖 prompt 共用同一個場景尾碼（PRD_Gridwell.md:43），
AuraZen 鎖攝影類型與情緒關鍵字且直接引用品牌色（PRD_AuraZen.md:75-80），
所以整站商品圖像同一個攝影師拍的、圖與版面同一色。這一層不先定，
每張圖各自發明場景，商品格一眼看出是東拼西湊的素材站。

## 第四層：設計鎖值

**填什麼**：本站選定的具體值，一旦寫進藍圖，全站不准偏離：

| 鎖值 | 說明 |
|------|------|
| 底色 | 全站基底色 hex |
| 展示字型 | 只准用於 h1、h2、eyebrow、大型標語 |
| 內文字型 | 全站內文、按鈕、表單 |
| 圓角 token | 全站唯一非零圓角值；圖片一律 0 |
| 圖片長寬比 | 商品格統一一種；全站至多兩種 |
| 區塊留白值 | 從 {64、80、96、128} 擇一或擇二 |

各項的合法範圍、配額與 FAIL 條件以 `references/typography-baseline.md`
為準（展示字型配額、字級階層、eyebrow、留白節奏、圓角與圖比五節）。
藍圖的責任是在動工前把「範圍」收斂成「單一值」並寫死。

**為什麼不先定會出事**：鎖值不在動工前釘死，就會在實作途中漂移：寫到第
五個區塊時換一種留白、第七個組件時多一種圓角，成品每區各長各的。
gridwell 成品全站只有一個圓角 token（8px，只用在卡容器，圖片全是 0）、
aurazen 留白只用 96 與 128 兩個值（typography-baseline.md 實測依據），
這種紀律是先釘後守的結果，不是邊做邊收斂得出來的。2026-08-04 的兩個站
沒有這一層，交付後想驗「有沒有漂移」，同樣連基準都沒有。

## 第五層：查核表

**填什麼**：交付前逐項打勾的檢查清單，每一項對應前四層的一個承諾，
且每一項寫明**怎麼驗**（用什麼指令、看什麼輸出），不是憑印象打勾：

1. 商品稽核：成品每一頁出現的商品名與價格，與第一層逐字一致。
   驗法：對 build 產物逐一 grep 第一層的每個商品名與價格字串。
2. 文案稽核：h1、主按鈕、各區塊標題、品牌故事逐字出現在成品。
   驗法：對 build 產物逐一 grep 第二層的每個鎖定字串。
3. 圖像稽核：所有商品圖 prompt 以 shared_prompt_suffix 結尾；
   抽任三張商品圖並排，光線與背景一致（image-scene-spec.md FAIL 條件）。
4. 鎖值稽核：用 Playwright 讀 computed style，逐條對第四層與
   typography-baseline.md 的 FAIL 條件（字型配額、圓角、留白、圖比）。

**為什麼不先定會出事**：AuraZen 的規格末尾就附了交付前必看查核表
（PRD_AuraZen.md:84-91），規格才有牙齒。沒有查核表，前四層只是願望清單：
2026-08-04 的兩個站連規格都沒有，更沒有查核，第一個看到成品問題的人
變成收件者。查核表把「交付即終審」改成「交付前終審」。

---

## 藍圖模板（每站複製一份填寫）

```markdown
# Site Blueprint: [Brand Name]
> 依據：DNA-[##] × DNA-[##]（見 design-system/DECISIONS.md 與創意宣言）

## 1. 商品清單
| # | 商品名稱 | 價格 | 一句描述 | 分類 |
|---|----------|------|----------|------|
| 1 | [名稱] | $[實際數字] | [一句] | [分類] |

## 2. 區塊標題與主要文案
- Hero h1：[逐字]
- Hero 主按鈕：[逐字]
- 區塊清單（依序）：
  - [eyebrow 逐字] / [區塊標題逐字] / [該區主文案逐字]
- 品牌故事段落：[逐字]
- 創辦人語錄（如有）：[逐字]
- 社會證明（如有）：[逐字]

## 3. 圖像場景（欄位定義見 references/image-scene-spec.md）
photography_type：[值]
background：[值]
lighting：[值]
mood_keywords：[值，至少含一個品牌色 hex]
shared_prompt_suffix：[值]

## 4. 設計鎖值（合法範圍見 references/typography-baseline.md）
- 底色：[#HEX]
- 展示字型：[名稱]（限 h1、h2、eyebrow、大型標語）
- 內文字型：[名稱]
- 圓角 token：[值]（圖片一律 0）
- 圖片長寬比：[值]（object-fit: cover）
- 區塊留白值：[從 64、80、96、128 擇一或擇二]

## 5. 交付前查核表
- [ ] 商品稽核：grep build 產物，第 1 層每個商品名與價格逐字命中
- [ ] 文案稽核：grep build 產物，第 2 層每個鎖定字串逐字命中
- [ ] 圖像稽核：全部 prompt 含 shared_prompt_suffix；抽三圖並排一致
- [ ] 鎖值稽核：computed style 過 typography-baseline.md 全部 FAIL 條件
```

---

## 完整範例（Gridwell 實例改寫）

商品名稱、價格、區塊標題、主按鈕、色票取自 PRD_Gridwell.md 的實際內容；
一句描述與分類是依本規格的欄位要求對真實商品名補寫的示範；字型、圓角、
字級取 2026-08 成品量測值（typography-baseline.md 實測依據；原規格寫
Inter 與 Roboto，成品實際採 DM 組合，且內文 Inter 現列迴避名單，
故以量測值為準）。

```markdown
# Site Blueprint: Gridwell
> 依據：Bento Grid Box 骨架，變異風格 Zen Structure Grid（見 DECISIONS.md）

## 1. 商品清單
| #  | 商品名稱 | 價格 | 一句描述 | 分類 |
|----|----------|------|----------|------|
| 1  | Silicone Cable Organizer Tie | $20.10 | Reusable ties that keep every cable coiled and labeled | Daily Storage |
| 2  | Heavy Duty Vacuum Storage Bag | $27.00 | Compress off-season bedding to a quarter of its size | Daily Storage |
| 3  | Matte Tinplate Organizer Box | $27.30 | A stackable matte tin for desktop clutter | Daily Storage |
| 4  | Minimalist Mesh Zipper Pouch | $22.80 | See-through mesh pouch for chargers and small kit | Travel Essentials |
| 5  | Bluetooth Smart Label Maker | $24.70 | Prints crisp labels straight from your phone | Daily Storage |
| 6  | Premium Leather Passport Holder | $22.30 | Full-grain leather cover with card slots | Travel Essentials |
| 7  | Transparent Coin Sorting Tube | $20.30 | Sorts coins by denomination at a glance | Daily Storage |
| 8  | Compact Travel Jewelry Case | $21.50 | Keeps rings and chains untangled in transit | Travel Essentials |
| 9  | Hard Shell Glasses Case | $18.60 | Crush-proof shell with microfiber lining | Travel Essentials |
| 10 | Water-resistant Cosmetic Bag | $29.20 | Wipe-clean interior for spill-prone bottles | Travel Essentials |

## 2. 區塊標題與主要文案
- Hero h1：Organization meets visual harmony.
- Hero 主按鈕：Explore the Grid
- 區塊清單（依序）：
  - HOME ORGANIZATION / The Art of Organization / 主打商品 bento 格
  - ON THE MOVE / Travel Essentials / Travel 分類商品格
  - EVERY DRAWER, SORTED / Daily Storage Solutions / Daily 分類商品格
  - OUR PROMISE / Why Choose Gridwell / 品牌故事段落
- 品牌故事段落（依原規格 tagline 與 USP 改寫的示範）：
  We make premium, perfectly proportioned storage that brings clarity to
  everyday life. Every Gridwell piece follows one refined bento-grid idea:
  a place for everything, and calm in every corner.

## 3. 圖像場景（欄位定義見 references/image-scene-spec.md）
photography_type：minimalist studio product photography
background：soft gray seamless background
lighting：studio lighting
mood_keywords：Zen Structure Grid, off-white #F9FAFB tones, clean order
shared_prompt_suffix：minimalist_product_shot_on_soft_gray_background_studio_lighting
（尾碼逐字取自 PRD_Gridwell.md:43；mood_keywords 綁品牌色 #F9FAFB 是依
image-scene-spec.md 必綁規則補上的示範，該規則源自 PRD_AuraZen.md:79）

## 4. 設計鎖值（合法範圍見 references/typography-baseline.md）
- 底色：#F9FAFB（卡片 #FFFFFF，主文字 #111827，強調 #0EA5E9）
- 展示字型：DM Serif Display（限 h1、h2、eyebrow、大型標語）
- 內文字型：DM Sans（h1 60px，body 16px，比值 3.75）
- 圓角 token：8px，只用於卡容器（圖片一律 0）
- 圖片長寬比：1:1（object-fit: cover）
- 區塊留白值：96 與 64（示範選值，從允許集合擇二）

## 5. 交付前查核表
- [ ] 商品稽核：grep build 產物，十件商品名與十個價格逐字命中，
      列表頁與詳情頁價格一致
- [ ] 文案稽核：h1、Explore the Grid、四個區塊標題、品牌故事逐字命中
- [ ] 圖像稽核：十件商品的 prompt 全部以共用尾碼結尾；抽三圖並排，
      同為亮灰棚拍窗光
- [ ] 鎖值稽核：computed style 只出現 0 與 8px 兩種圓角、留白只有
      96 與 64、DM Serif Display 未進按鈕與內文
```

---

相關檔案：`image-scene-spec.md`（第三層的欄位定義與 FAIL 條件）、
`typography-baseline.md`（第四層的合法範圍與 FAIL 條件）。
