# 線上運作中的電商站

這些站全部由同一條產線產出。這裡收的是**最新一輪、畫面最完整的成品**，
並排看的重點不是數量，是**沒有兩個站長得像同一個模板做的**。

每一張縮圖都可以點開對應的線上網址。

> **關於這些站的階段說明**
> 這條產線的合規檢查（含英國 DMCCA 的促銷標示規則）建立於 2026-07-31，
> 而清單中多數站建於 2026-03 到 06，**早於那道檢查**。
> 因此部分早期站的示範資料仍帶有促銷價欄位與樣板顧客評論，不符合現行標準。
> **這些是測試階段的產出，不是對外販售的商品頁**（沒有接金流、沒有開賣）。
> 現行檢查已納入產線，**2026-08-04 之後產出的站在建置時就會被擋下**，
> 要重跑驗證可以直接執行 `production-line/scripts/ecommerce-checklist.py <站的路徑>`。


<table width="100%">
<tr>
<td width="33%" align="center"><a href="https://sg-thirdstop.vercel.app"><img src="site-thumbnails/sg-thirdstop.png" width="100%" alt="THIRDSTOP"></a><br><b>THIRDSTOP</b><br>相機快拆板與腳架配件</td>
<td width="33%" align="center"><a href="https://sg-tensile.vercel.app"><img src="site-thumbnails/sg-tensile.png" width="100%" alt="TENSILE"></a><br><b>TENSILE</b><br>隨身工具與充電配件</td>
<td width="33%" align="center"><a href="https://sg-auraguard.vercel.app"><img src="site-thumbnails/sg-auraguard.png" width="100%" alt="AuraGuard"></a><br><b>AuraGuard</b><br>風水御守護身符</td>
</tr>
<tr>
<td width="33%" align="center"><a href="https://sg-inkandecho.vercel.app"><img src="site-thumbnails/sg-inkandecho.png" width="100%" alt="Ink &amp; Echo"></a><br><b>Ink &amp; Echo</b><br>精品文具</td>
<td width="33%" align="center"><a href="https://sg-streetcourt.vercel.app"><img src="site-thumbnails/sg-streetcourt.png" width="100%" alt="StreetCourt"></a><br><b>StreetCourt</b><br>都會籃球潮牌</td>
<td width="33%" align="center"><a href="https://sg-gridwell.vercel.app"><img src="site-thumbnails/sg-gridwell.png" width="100%" alt="Gridwell"></a><br><b>Gridwell</b><br>居家收納</td>
</tr>
<tr>
<td width="33%" align="center"><a href="https://sg-harmonia.vercel.app"><img src="site-thumbnails/sg-harmonia.png" width="100%" alt="HARMONIA"></a><br><b>HARMONIA</b><br>聲音療癒樂器</td>
<td width="33%" align="center"><a href="https://sg-prismaura.vercel.app"><img src="site-thumbnails/sg-prismaura.png" width="100%" alt="PrismAura"></a><br><b>PrismAura</b><br>水晶光雕</td>
<td width="33%" align="center"><a href="https://sg-auravibe.vercel.app"><img src="site-thumbnails/sg-auravibe.png" width="100%" alt="AuraVibe"></a><br><b>AuraVibe</b><br>風水擺件</td>
</tr>
<tr>
<td width="33%" align="center"><a href="https://sg-mossglobe.vercel.app"><img src="site-thumbnails/sg-mossglobe.png" width="100%" alt="Moss &amp; Globe"></a><br><b>Moss &amp; Globe</b><br>生態瓶苔蘚景</td>
<td width="33%" align="center"><a href="https://sg-kanso.vercel.app"><img src="site-thumbnails/sg-kanso.png" width="100%" alt="Kanso"></a><br><b>Kanso</b><br>居家收納整理</td>
<td width="33%"></td>
</tr>
</table>

---

## 為什麼牆上只有 11 個，清單上卻有更多

縮圖是**精選**，不是全收。收進牆上的條件，四項全部要滿足：

1. 首屏畫面完整，沒有破版、沒有元素被切掉、沒有載入骨架、沒有彈窗遮住
2. 首屏看得出明確的視覺個性（配色、字體、版面結構）
3. **首頁整頁沒有劃線原價**（以瀏覽器 computed style 掃描確認，非讀原始碼）。
   `production-line/PITFALLS.md` 規定示範資料的站不得使用劃線促銷寫法
4. 跟牆上其他張不撞臉；兩個站調性太接近時只留較好的那一個

沒進牆的站**沒有從清單刪掉**，網址一樣可以點開自己看。它們多數是較早期的產出，
或是首頁往下捲某處仍留有劃線原價。

---

## 完整清單

**清單收錄 35 個網址**：其中 33 個為 2026-08-03 以前的存量（下表），
另 2 個為 2026-08-04 最新一輪產出（見表後）。
**2026-08-05 以 HTTP 逐一實測，35 個全部回應 200，沒有失效的站。**

清單中打 ● 的，就是上面縮圖牆收錄的那 11 個。

| # | 品牌 | 品類與視覺方向 | 網址 |
|---|---|---|---|
| 1 | **Lumina Coffee** | 精品咖啡｜暖奶油＋襯線 | [sg-luminacoffee.vercel.app](https://sg-luminacoffee.vercel.app) |
| 2 | **NEXUS GEAR** | 3C 配件｜暗色航太＋電光藍 | [sg-nexusgear.vercel.app](https://sg-nexusgear.vercel.app) |
| 3 | **PrismAura** ● | 水晶光雕｜深藍＋虹彩紫 | [sg-prismaura.vercel.app](https://sg-prismaura.vercel.app) |
| 4 | **NatureGlow** | 植物護膚｜奶油植物綠 | [sg-natureglow.vercel.app](https://sg-natureglow.vercel.app) |
| 5 | **VANGUARD** | 戰術 EDC｜暗色＋橘＋軍事語氣 | [sg-vanguard.vercel.app](https://sg-vanguard.vercel.app) |
| 6 | **Gridwell** ● | 居家收納｜暗綠Japandi編輯風 | [sg-gridwell.vercel.app](https://sg-gridwell.vercel.app) |
| 7 | **Kintsugi & Clay** | 手作陶瓷｜wabi-sabi 暖陶 | [sg-kintsugi.vercel.app](https://sg-kintsugi.vercel.app) |
| 8 | **Sonic Silk** | 聲音療癒｜午夜靛＋紫襯線 | [sg-sonicsilk.vercel.app](https://sg-sonicsilk.vercel.app) |
| 9 | **Ink & Echo** ● | 精品文具｜奶油＋酒紅 concierge | [sg-inkandecho.vercel.app](https://sg-inkandecho.vercel.app) |
| 10 | **AuraVibe** ● | 風水招財｜暖色紅金玉 | [sg-auravibe.vercel.app](https://sg-auravibe.vercel.app) |
| 11 | **Lumière & Co.** | 芳療香氛｜暖奶油＋琥珀金 | [sg-lumiere.vercel.app](https://sg-lumiere.vercel.app) |
| 12 | **LUMINA Oracle** | 神諭占卜｜金＋午夜＋羊皮紙 | [sg-lumina-oracle.vercel.app](https://sg-lumina-oracle.vercel.app) |
| 13 | **Apothecary Archive** | 古董草藥｜暗紅＋羊皮古籍 | [sg-apothecary.vercel.app](https://sg-apothecary.vercel.app) |
| 14 | **Verdant Veda** | 阿育吠陀｜大地植物綠 | [sg-verdantveda.vercel.app](https://sg-verdantveda.vercel.app) |
| 15 | **QiBalance** | 風水能量水晶｜奶油米＋深棕 | [sg-qibalance.vercel.app](https://sg-qibalance.vercel.app) |
| 16 | **HARMONIA** ● | 聲音療癒樂器｜奶茶＋陶土 | [sg-harmonia.vercel.app](https://sg-harmonia.vercel.app) |
| 17 | **Kanso** ● | 居家收納整理｜侘寂奶油＋陶土 | [sg-kanso.vercel.app](https://sg-kanso.vercel.app) |
| 18 | **FRAMEKIT** | 攝影器材｜暖羊皮＋赭橘 | [sg-framekit.vercel.app](https://sg-framekit.vercel.app) |
| 19 | **AURAZEN** | 風水能量淨化｜奶油暖＋金 | [sg-aurazen.vercel.app](https://sg-aurazen.vercel.app) |
| 20 | **ordra** | 居家收納｜奶油＋午夜藍 | [sg-ordra.vercel.app](https://sg-ordra.vercel.app) |
| 21 | **TrailForge** | 超輕量露營戶外｜森林綠 | [sg-trailforge.vercel.app](https://sg-trailforge.vercel.app) |
| 22 | **GEM TERRA** | 寶石水晶礦石｜礦廊白＋森綠 | [sg-gemterra.vercel.app](https://sg-gemterra.vercel.app) |
| 23 | **TidyNest** | 電線桌面收納｜科技藍 | [sg-tidynest.vercel.app](https://sg-tidynest.vercel.app) |
| 24 | **SACRED GROVE** | 御守護身符｜靛藍＋朱紅＋金 | [sg-sacredgrove.vercel.app](https://sg-sacredgrove.vercel.app) |
| 25 | **DeskZenith** | 桌面美學｜暖胡桃＋黃銅 | [sg-deskzenith.vercel.app](https://sg-deskzenith.vercel.app) |
| 26 | **StreetCourt** ● | 都會籃球潮牌｜橘黑brutalist | [sg-streetcourt.vercel.app](https://sg-streetcourt.vercel.app) |
| 27 | **SONARA** | 聲音療癒頌缽｜深紫金 | [sg-sonara.vercel.app](https://sg-sonara.vercel.app) |
| 28 | **Moss & Globe** ● | 生態瓶苔蘚景｜暗綠植物 | [sg-mossglobe.vercel.app](https://sg-mossglobe.vercel.app) |
| 29 | **Aura & Ash** | 線香淨化鼠尾草｜奶油大地色 | [sg-auraash.vercel.app](https://sg-auraash.vercel.app) |
| 30 | **AuraGuard** ● | 風水御守護身｜暗色宮廷 | [sg-auraguard.vercel.app](https://sg-auraguard.vercel.app) |
| 31 | **Sacred Embers** | 線香淨化｜奶油綠 | [sg-sacredembers.vercel.app](https://sg-sacredembers.vercel.app) |
| 32 | **AuraPurify** | 香氛薰香｜奶油米+鼠尾草綠 | [sg-aurapurify.vercel.app](https://sg-aurapurify.vercel.app) |
| 33 | **ZenFlow** | 風水水晶飾品｜淺色五行 | [sg-zenflow.vercel.app](https://sg-zenflow.vercel.app) |

> 最新一輪產出的兩個站不在上表：
> [sg-thirdstop.vercel.app](https://sg-thirdstop.vercel.app) 與 [sg-tensile.vercel.app](https://sg-tensile.vercel.app)。
> 這兩個都在縮圖牆的第一排。

---

## 關於這份清單

**原始碼不是每個站都還在。** 早期產出的站，原始碼存放在後來汰換掉的儲存裝置上，
線上部署仍正常運作，但本機不再保有那些專案的檔案。
本機保有完整原始碼的是 23 個，其中 20 個有編譯好可直接部署的版本。

**本 repo 收錄 3 個完整範例**（含原始碼與編譯版），挑選標準是視覺方向差異最大。
只收 3 個是為了讓 repo 保持在可以下載、可以跑起來的大小。

**這些站尚未接金流、尚未開賣。** 它們是生產線的實際產出，
用來驗證能不能穩定做出可上線品質的店面。

**縮圖怎麼來的：** 2026-08-05 以 Playwright 於 1280×800 視窗擷取首屏，
等頁面載入穩定後拍攝，等比縮到寬 400px。縮圖沒有經過修圖或裁切美化。
