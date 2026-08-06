# Typography Baseline（字體與版面鎖值）

> 本檔是產線鎖值，不是建議。每一條都有 FAIL 條件，任何一條 FAIL 就回去改，不得進入交付。
> 數字來源：2026-08 對五個受肯定站（gridwell、aurazen、vanguard、inkandecho、streetcourt）
> 的計算後樣式量測（metrics.json 全數值與五張全頁截圖）。這五組紀律先前不存在於任何技能文件，
> 只存在執行者的手感裡，換一個執行者就消失。本檔把它們鎖成可檢查的值。
> 載入時機：設計系統生成之前讀入。驗收時機：交付前用 Playwright 讀 computed style 逐條驗。

## 一、展示字型配額

**鎖什麼**
每站只准一個展示字型加一個內文字型。展示字型只准出現在 h1、h2、eyebrow、大型標語，
不准進按鈕、內文段落、表單、商品描述。
展示字型元素數佔全站文字元素總數的比例，上限 20%。

**實測依據（metrics.json 各站 fonts 欄位）**
- gridwell：DM Serif Display 12 個元素，DM Sans 148 個，佔比 7.5%
- aurazen：Cormorant Garamond 25 個，Inter 198 個，佔比 11.2%
- inkandecho：Noto Serif TC 15 個，Cormorant 74 個，佔比 16.9%
- streetcourt：Oswald 27 個，Inter 176 個，佔比 13.3%
- vanguard 是登記例外：IBM Plex Mono 152 個，Inter 327 個。mono 兼任數據標籤字體所以超額。
  這種兼用必須在決策檔申報，沒申報就照配額算。

**怎麼檢查（FAIL 條件）**
用 computed style 統計每個文字元素的 font-family，任一條成立即 FAIL：
- 展示字型出現在 button、input、內文段落或商品描述
- 展示字型元素數 ÷ 全站文字元素總數 > 20%，且決策檔沒有申報 mono 兼用例外

## 二、字級階層

**鎖什麼**
- h1 字級 ≥ 3.5 倍 body 字級
- h1 行高 ≤ 1.05 倍自身字級
- 字級 ≥ 48px 的標題，letter-spacing 必須小於 0

**實測依據（metrics.json 各站 h1、body 欄位）**
- 五站 body 全部 16px。h1：gridwell 60px（3.75 倍）、aurazen 72px、vanguard 96px、
  inkandecho 96px、streetcourt 128px（8 倍）。比值範圍 3.75 到 8 倍。
- h1 行高全部等於或小於字級：60/60、96/96、128/128、86.4/96。
- 大字負字距：gridwell h1 為 -1.5px，vanguard h1 為 -4.8px。

**怎麼檢查（FAIL 條件）**
讀 h1 與 body 的 computed style，任一條成立即 FAIL：
- h1 字級 ÷ body 字級 < 3.5
- h1 行高 ÷ h1 字級 > 1.05
- 任何字級 ≥ 48px 的標題 letter-spacing ≥ 0

## 三、eyebrow 是必要元素

**鎖什麼**
每個主區塊的標題上方必有一行 eyebrow 小標：字級 11 到 14px、全 uppercase、
letter-spacing ≥ 1.2px。

**實測依據（metrics.json 與五張全頁截圖）**
五站全有，無一例外：HOME ORGANIZATION（gridwell）、YOUR SANCTUARY（aurazen）、
VANGUARD MISSION CONTROL（vanguard）、EST. 2026 // STREET COURT（streetcourt）。
字級落在 11 到 14px。小型 uppercase 標籤正字距實測 1.2px 到 7px，
最寬的是 vanguard「VERIFIED OPERATIVES」，14px 字級配 7px 字距。

**怎麼檢查（FAIL 條件）**
逐一檢查主區塊，任一條成立即 FAIL：
- 任一主區塊的標題上方沒有 eyebrow
- eyebrow 不是 uppercase
- eyebrow 字級不在 11 到 14px 區間
- eyebrow letter-spacing < 1.2px

## 四、留白節奏

**鎖什麼**
- 區塊垂直 padding 只准從 {64px、80px、96px、128px} 選
- 同一站使用的相異值至多兩個
- 主容器 max-width 1280px
- 散文段落容器另縮到 768px 或 896px

**實測依據（metrics.json 各站 sections 與 maxWidths 欄位）**
- aurazen 96/96/128、inkandecho 128/128、vanguard 80/96/80/96、streetcourt 96/96/64，
  每站都只用一到兩個值，形成節奏
- 主容器 max-width 五站全部 1280px
- 散文段落縮到 896px 或 768px（aurazen、inkandecho、vanguard 的 maxWidths 欄位）

**怎麼檢查（FAIL 條件）**
收集全部 section 的 paddingTop 與 paddingBottom，任一條成立即 FAIL：
- 出現 {64、80、96、128} 以外的值，或出現小於 64px 的值
- 同站相異值超過兩個
- 主容器 max-width 不是 1280px
- 散文段落容器寬度超過 896px

## 五、圓角與圖比紀律

**鎖什麼**
- 全站至多一個非零圓角 token，寫進決策檔；圖片圓角一律 0
- 同一格線內所有商品圖同一長寬比；全站至多兩種長寬比；商品圖一律 object-fit: cover

**實測依據（metrics.json 各站 images 欄位）**
- 圓角：gridwell 全站唯一 token 8px（只用在卡容器，卡內圖片仍是 0px）；
  aurazen、vanguard、inkandecho、streetcourt 全站 0px。沒有一站混用多種圓角。
- 圖比：gridwell 商品格 239×208、aurazen 商品 302×302 正方加分類卡 292×389（3:4）、
  vanguard 全部 292×292、inkandecho 全部 296×296。同一格線內比例零混用，
  全站至多兩種（aurazen 的商品格與分類卡各自統一）。

**怎麼檢查（FAIL 條件）**
掃編譯產物的 border-radius 與圖片的 computed size，任一條成立即 FAIL：
- border-radius 相異值超過兩種（0 加單一 token 之外出現第三種）
- 任一圖片圓角不是 0
- 同一格線內出現第二種長寬比
- 全站長寬比超過兩種
- 商品圖不是 object-fit: cover

## 六、色彩與對比（2026-08-06 新增）

**鎖什麼**
- 內文文字對比度 ≥ 4.5:1，大字（≥24px 或 ≥19px 加粗）對比度 ≥ 3:1（WCAG AA）
- 全站色相桶（30° 一桶，共 12 桶）：主色＋中性＋強調色合計 ≤ 3 桶；> 4 桶即 FAIL
- 全站 unique box-shadow 值 ≤ 3 種

**依據**：WCAG AA 是國際通用最低標準，非本產線自訂；色相桶與陰影種類上限沿用
圓角/圖比紀律（本檔第五節）同一種思路——不是測出某個「業界常見值」，是把「品味上不能
花」翻成可驗的數字上限。這兩條先前只存在 anti-patterns.md 的紫色禁令這一個特例裡，
沒有推廣成通用鎖值，直到 amberflask 健檢發現全站色彩發散才補上。

**怎麼檢查（FAIL 條件）**
- Playwright 讀 computed `color`/`background-color`，套 WCAG 相對亮度公式算對比度：
  任一段落級文字 < 4.5:1，或任一大字 < 3:1 → FAIL
  （靜態掃描版先接在 `ecommerce-checklist.py` 的 `check_color_contrast`：只抓同一個
  CSS 規則區塊裡明寫的 color/background hex 配對，是近似值，不是完整的 computed-style
  稽核——那要 wcag-audit-patterns 技能配 Playwright 讀真正渲染後的樣式，目前產線還沒接，
  這裡先有一個會真的動的關卡，好過規則寫著沒人跑）
- 收集全站 computed `color`/`background-color`/`border-color`，濾掉中性色（近黑/近白/灰）
  後 30° 分桶去重計數：> 3 桶 → FAIL
- 收集全站 computed `box-shadow`，去重計數：> 3 種 → FAIL

## 七、首屏（2026-08-06 新增）

**鎖什麼**
- 首屏（viewport 1440×900 內）恰好一個 `<h1>`
- 首屏恰好一個「主 CTA」（視覺權重最高的那顆按鈕/連結）
- 首屏禁止：≥2 個同視覺權重的 CTA、自動輪播（autoplay carousel）、蓋住 CTA 的浮層
- 品牌名可見、至少一張品牌圖片可見

**依據**：這是把「電商首頁該有的最低限度清楚」翻成硬指標——多個同權重 CTA 讓使用者
不知道該點哪個，自動輪播的第 2/3 張永遠沒人看到卻仍佔首屏版面，都是轉換率已知的負面
模式（見 `page-cro`／`popup-cro` 相關技能的共識），不是本產線自創的美學偏好。

**怎麼檢查（FAIL 條件）**
- DOM 斷言：`document.querySelectorAll('h1')` 在首屏內數量 ≠ 1 → FAIL
- 「主 CTA 恰一個」與「CTA 視覺權重誰高」需要語意判斷，靜態掃描不可靠——這一項
  **明確不自動化**，留給 site-quality-rubric.md 人審／`/frontend-design` 截圖直覺裁決，
  不做假檢查冒充能自動
- 自動輪播偵測（可自動）：原始碼掃到 `swiper`/`embla`/`carousel` 關鍵字且鄰近出現
  `autoplay` → FAIL（已接進 `ecommerce-checklist.py` 的 `check_aesthetic_locks`）
- 品牌名／品牌圖片可見：沿用既有的 Image Health／Anti-Pattern Guard 檢查範圍，不重複造

---

相關檔案：`image-scene-spec.md`（商品圖場景鎖定，與本檔同時為生圖與排版的必要輸入）。
`uniqueness-guarantee.md`（去重維度總表，與本檔的美感鎖值共用同一顆色彩判準，互不重複）。
