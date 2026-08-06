# 07 技術選型與研發

**現況：運作中**

## 職責

兩件事。第一，找市場上新出現的工具與開源專案，評估值不值得用，決定要不要引進。第二，引進之後不能裝上就放著，要把它接進日常流程，變成真的有人在用的東西，並持續維護。

既是探路的人，也是確保裝了的東西真的有在運作的人。

## 實際產出

**產線本體從 v9.0 演進到 v11.1。** 紀錄在 [`production-line/VERSION_HISTORY.md`](../production-line/VERSION_HISTORY.md)。v11.0 最大的一刀是換掉舊的美學引擎，改用 66 個真實電商 DNA 加混血機制，並新增系統預檢與防重複檢查。每一版的變更與被取代的原因都寫在裡面，舊版不是消失，是標明「已被哪一版取代」。

**六種現代 UI 框架的選型規範。** [`production-line/references/modern-ui-frameworks.md`](../production-line/references/modern-ui-frameworks.md) 定義依商品定位選框架的規則。這份文件裡有一條是踩過坑才寫下來的：某個元件庫在 2025 年初改名，舊套件名已經棄置，裝了就是死庫。選型規範記的不只是選什麼，還有哪些不能再裝。

**外掛池。** [`production-line/references/wp-plugin-pool.md`](../production-line/references/wp-plugin-pool.md)，354 行。分成必裝清單與隨機池，依設計基因的雜湊值決定這個站裝哪幾支，讓每個站的後台組成也不一樣。

**一支自己寫的跨網域外掛。** [`production-line/backend/mu-plugins/`](../production-line/backend/mu-plugins/) 裡處理跨網域、讓前台要得到後端資料的那一支，是為了補現成方案沒有的那一段而寫的。同一個目錄下還有一支模擬付款外掛，那支屬於付款這一段，記在 [12 金流與財務](12-finance.md)。

**圖片備援目前只有第三層會執行。** [`generate_images_fallback.py`](../production-line/scripts/generate_images_fallback.py) 定義了三層退路，但實測下來：第一層未實作（原本是靜默 `return False` 的退路，已改成 `raise NotImplementedError`，不會偷偷放行）；第二層打的 `source.unsplash.com` 免費端點已下線，實測回傳 503（Heroku 錯誤頁，不會轉址）；因此真正會跑到的只有第三層，抓的是 `placehold.co`，而這個來源正好是 [site-quality-rubric.md](../production-line/references/site-quality-rubric.md) 自己列為「很 AI」的反例。要恢復多層備援，得接 Unsplash 正式 API。退路本身有設計立場，寫在 [`generate_catalog_plates.py`](../production-line/scripts/generate_catalog_plates.py) 的開頭：退路不知道商品長什麼樣，所以退路不該假裝畫商品，它該做的是把已知為真的規格資料排版成一張型錄規格卡。這個立場目前只有第三層在實踐。

**系統預檢。** [`preflight_check.py`](../production-line/scripts/preflight_check.py) 在開始生成前先驗依賴與資料來源都在，不在就不要開始。

## 用什麼在做

**引進的東西要接進流程才算數。** 選型規範不是清單，是生成流程裡的一個步驟；外掛池不是推薦，是自動選取；備援理論上該是失敗時自動走的路，但圖片這條目前只有最後一層真的在走，前兩層一個沒做、一個端點已死。

**汰換要留下理由。** 版本歷史記的是「什麼被什麼取代、為什麼」，不是只有新版功能。

**退路的產出品質要撐得住。** 這條寫在 `PITFALLS.md` 第七節：如果退路產出的東西一看就是半成品，那它不是退路，是一個延後爆炸的失敗。

## 現在卡在哪

**產線有多份副本，同步腳本是先刪再複製。** 從比較舊的那一份跑同步，會把比較新的目標整個蓋掉。已經發生過，改好的規則不見了、檔案退回幾週前的版本。做法已經寫下來（指定正本、同步前比版本、同步前備份），但目前靠人記得，沒有自動擋。

**外部服務失效會安靜退回退路，然後回報成功。** 同一天發生兩次，兩個不同的子系統：生圖端回 401 之後退回線稿，商店後端查詢回 401 之後退回內建假商品。兩次都回報成功，兩次都沒人當場發現。原則已經定了（走退路一定要說），偵測還沒自動化。

**單獨拿這個資料夾跑不起整條產線。** [`production-line/README.md`](../production-line/README.md) 已經寫明：部分步驟依賴本 repo 之外的元件，包含圖片生成與商品資料來源。這代表這條產線目前不是一個可以獨立交付的東西。

**認證狀態沒有定期健檢。** 上面兩次 401 都是事後才知道的。而且公開端點回 200 不代表金鑰有效，要打需要認證的端點才算數，這一點目前沒有排程在跑。
