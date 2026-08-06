# 獨一無二保證機制（Uniqueness Guarantee）

> 單一權威頁。去重規則以前散在 SKILL.md Phase 1.05／1.07／1.1 三處，各自維護容易脫節
> （2026-08 的三個破口——DNA-50 撞紫色禁令、structural-history.json 是 `[]`、
> used_categories.json 停在 3 月——三個都是「規則寫在一處、真相在另一處」造成的）。
> 這份文件是「哪些維度、怎麼判、門檻多少」的唯一出處；SKILL.md 只留一行指路。

## 為什麼要做這件事：不只是美觀

> Dee 原話（2026-08-06 拍板時）：
> 「這件事要在已經開跑建了很多電商網站後就會有用，目的是防止我們網站五個內有重複，
> **就會被抓到是重複性網站**」

這是平台風控考量，不是單純的設計潔癖。同一批帳號底下的電商站如果視覺與結構高度相似，
容易被平台判定為同一批量產的「洗版站」而連坐處置。**5 代之內不重複**這個數字，
對應的是風控視窗，不是美感偏好——這也是為什麼下面的門檻要寫死、要能自動驗，
不能只靠人「看起來還行」。

---

## 一、去重維度總表

| 維度 | 判定方式 | 視窗 | 自動化 | 誰在管 |
|---|---|---|---|---|
| DNA family | 不得與近期相同 | 近 5 筆 | ✅ | `design_history.py plan --pool` 抽前剔除 |
| 底色系 bg_tone（4 類） | 近期出現 ≥2 次即禁 | 近 3 筆 | ✅ | `design_history.py reserve`（既有） |
| display 字體＋範式 | 不得與近期相同；同一「襯線大標」範式連續 2 次後第 3 次強制換類別 | 近 3 筆 | ✅ | `design_history.py reserve`（既有） |
| **主色 hue 桶（12 桶 ×30°）** | hex→HSL 桶號，不得與近期同桶 | 近 3 筆 | ✅ | `design_history.py reserve --primary-hex`（新） |
| **紫色主色** | hue 240°／270° 桶永遠禁用，不看歷史（anti-patterns.md #5） | 不看視窗 | ✅ | `dna-index.json` 抽前剔除 ＋ reserve 二次擋 |
| **區塊序列** | section token 序列 Levenshtein 編輯距離 <3 視為太像 | 近 8 站 | ✅ | `design_history.py struct-reserve`（新） |
| **分頁組合** | 頁面集合 Jaccard ≥0.8 視為太像 | 近 8 站 | ✅ | `design_history.py struct-reserve`（新） |
| **商品品類** | 不得與已用過的重複，用完全部品類才重新輪替 | 全歷史 | ✅ | 讀 `design-history.json` 的 `category` 欄位（新，見下方「品類去重改讀哪裡」） |
| **站內圖片** | md5 完全重複／pHash 距離 ≤8 = FAIL | 站內＋跨近站 | ✅ | `check_site_distance.py`（新） |
| **主色 ΔE2000** | 與近站主色距離 <20 且 bg_tone 同類 = FAIL | 近站（由驗收官指定幾站） | ✅ | `check_site_distance.py`（新） |
| **簽名動效組合** | reserve 時登記 `--signature-fx`，近 3 筆不建議重複 | 近 3 筆 | 🟡 登記制，不強制擋（動效組合從代碼反推不可靠，只能靠登記） | `design_history.py reserve --signature-fx`（新） |
| 整體氣質像不像 | — | — | ❌ 只能人看 | site-quality-rubric.md／`/frontend-design` 截圖直覺裁決 |

---

## 二、抽前過濾（先過濾池子再抽，不是抽完再檢查）

舊做法：SKILL.md 原文「生成 1-66 隨機數」→ 抽完才發現撞禁令
（2026-08 實證：DNA-50 抽中後才發現主色 `#9b51e0` 落在紫色禁令，白做一輪）。

新做法：
```bash
python scripts/design_history.py plan --pool
```
這個指令讀 `data/dna-index.json`（66 個 DNA 的機器可讀索引，從 `real-ecommerce-dna.md`
一次性抽出）＋ 目前的 `design-history.json`，做**三重交集剔除**：
1. 剔除近 5 筆（含 in_progress）的 primary family
2. 剔除主色命中紫色 hue 桶的 DNA（不看歷史，永遠剔除）
3. 剔除 display 字體與近 3 筆撞名、或連續 2 次以上撞同一個「襯線大標」範式的 DNA

只准從印出來的清單裡抽。池子空了會非零退出（`--force` 才能強行沿用，且要在
`--note` 寫明理由）。`reserve` 指令本身也會重跑一次這個過濾——就算有人跳過
`plan --pool` 直接呼叫 `reserve`，抽到池外一樣會被擋（`--primary-dna` 不在池內 → REJECTED）。

**dna-index.json 資料品質誠實標註**：66 筆裡有 25 筆能從 `real-ecommerce-dna.md` 抓到明確 hex
（`data_quality: "full"` 或 `"partial"`），其餘 35 筆只有文字描述色調（如 "cream, sand, sage
green"），沒有 hex 可算 hue 桶——這些筆的 `hue_bucket` 是 `null`，**null 不代表「安全」，
代表「這個判準判不出來」**。只有 family 判準對全部 66 筆都可靠（family 來自章節標題，不是
從散文解析）。

---

## 三、開工前強制查驗（訂位制的牙齒）

登記（reserve）只是「有沒有寫進去」，`verify` 才是「開工前有沒有人真的查」：
```bash
python scripts/design_history.py verify --project <站的路徑> [--decisions <DECISIONS.md 路徑>]
```
Phase 2 開工前跑，查無本站的訂位紀錄 → 非零退出、建站中止。給 `--decisions` 時會額外比對
`primary_dna`／`bg_tone`／`display` 三項有沒有真的寫進 DECISIONS.md（避免訂位登記了但文件
沒同步，兩邊各說各話）。

---

## 四、「證明兩站不像」的可跑檢查：check_site_distance.py

`design_history.py` 管的是「登記了什麼設計基因」——產出者自己回報的意圖。
`check_site_distance.py` 管的是「實際生出來的站真的不像」，讀編譯後的產物（CSS／HTML／
圖片），不看自報欄位。**這支由驗收官跑，不是產出者自己跑**（沿用 check_dna_fidelity.py
的分工原則）。

```bash
python scripts/check_site_distance.py check --site ./sites/newsite \
  --compare ./sites/prev1 --compare ./sites/prev2 --compare ./sites/prev3
```

五個 FAIL 硬指標：

| # | 指標 | 門檻 | 抓得到什麼 |
|---|---|---|---|
| 1 | 主色 ΔE2000 | <20 且站級 bg_tone 同類 = FAIL | 主色候選已濾掉中性色（近黑/近白/灰），避免「兩站文字都用近黑色」誤判 |
| 2 | 字體集合 | display 完全相同 = FAIL；Jaccard >0.5 = WARN | 換皮但字體沒換 |
| 3 | 區塊序列 | Levenshtein 編輯距離 <3 = FAIL | 骨架複製，內容換了皮 |
| 4 | 站內圖片 | md5 完全重複 = FAIL | 同商品多角度用同一張圖交差（2026-08 thirdstop×8／tensile×4 破口） |
| 5 | 跨站圖片 | pHash 距離 ≤8 = FAIL | 同圖改壓縮／裁切，md5 抓不到 |

依賴狀況（實測，寫在腳本檔頭）：Pillow 12.2.0 可用；`imagehash`／`colormath` **不可用**
（環境沒裝）→ pHash 與 ΔE2000 改用純 Python／numpy 手刻實作（不是簡化版，是同一套標準演算法
自己刻），已用已知數值組與造假樣本驗證過（`selftest` 子指令）。

**誠實標註**：這支抓得到「複製與換皮」，抓不到「品味上像同一個人做的」——那層留給人審
（site-quality-rubric.md／`/frontend-design`），不假裝可自動。CSS 抽色與抓字體是靜態正則
掃描，不是讀 computed style（那要 Playwright，見下方美感鎖值一節），抓不到跨檔繼承或
Tailwind 動態 class 算出來的顏色。

---

## 五、品類去重改讀哪裡（廢除 used_categories.json）

`used_categories.json` 是獨立檔，2026-03 之後沒人更新過（停擺整整半年），跟
`design-history.json` 兩套帳必然脫節——今天的破口就是證據。

**改法**：`load_products.py` 不再讀寫 `used_categories.json`，改直接讀
`data/design-history.json` 每一筆既有的 `category` 欄位（排除 `abandoned`）。單一真相，
不會有第二個檔案可以脫節。

⚠️ **已知落差**：`design-history.json` 舊的 8 筆 `category` 存的是英文品牌化分類
（如 `"Talisman"`），不是 `extracted_products.json` 的中文原始 `id`
（如 `"## 1. 傳統風水護身類"`）——兩邊字串對不上，**舊筆天生比不中**。這跟原本
`used_categories.json` 停在 3 月是同一種「事實上沒在擋」，不是新引入的退步。往後
`reserve --category` 要填 `load_products.py` 選中的那個 `id` 原始字串（不要填翻譯過的
英文名），比對才會真的生效。

---

## 六、結構訂位併入同一支腳本（不造第二把鎖）

`structural-history.json` 過去是空殼（`[]`），Phase 1.07 第 3 步原本要求「人工比對」，
等於沒人做。改法是照 `design_history.py` 的訂位制重做，**併入同一支腳本當子指令**，
不另造第二套鎖：

```bash
python scripts/design_history.py struct-plan          # 看近 8 站的結構指紋
python scripts/design_history.py struct-reserve \
  --brand "<品牌>" --project <路徑> --seed <structural_seed> \
  --sections hero,usp,grid,testimonial,faq,footer \
  --pages home,shop,product,cart,checkout
```
`commit`／`abandon` 直接沿用既有子指令，指到 `--history <structural-history.json 路徑>`
即可（同一把鎖管所有「選定即登記」）。

---

## 七、美感鎖值（色彩／對比／首屏）與去重維度的關係

色彩對比度、hue 桶數量上限、box-shadow 種類上限、首屏 h1/CTA 這些「美輪美奐的下限」
與本文件的「獨一無二」是兩個不同目的（前者是品質下限，後者是防撞臉），但共用同一顆
色彩判準（hue 桶 30° 分桶、ΔE2000/對比度公式）。鎖值細節寫在
`typography-baseline.md`「六、色彩與對比」「七、首屏」兩章，不在這裡重複，避免兩份文件
同時維護同一組數字、遲早對不上。

---

## 八、為什麼各腳本不共用同一個色彩/距離工具模組

`design_history.py`、`check_site_distance.py`、`ecommerce-checklist.py` 三支各自
獨立複製了一份 hue 桶／編輯距離的小函式（10-20 行），沒有抽成共用模組。這是刻意的：
三支是各自獨立可執行的 CLI，拆共用模組會讓其中任一支單獨測試/單獨呼叫時多一層 import
依賴（相對路徑、`sys.path` 处理），對這種量級的函式不划算。函式簽名與行為刻意保持一致，
改動一處時要記得三處一起改——這是目前的已知維護成本，不是遺漏。
