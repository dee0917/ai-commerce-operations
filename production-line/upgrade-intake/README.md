# 產線升級收件區（upgrade-intake）

回答一個問題：**外面每天冒出來的開源專案，哪一個真的該接進這條產線。**

不靠「看起來很強」決定。這裡的規矩是：**拿它對這條產線做一次實際的事，看結果有沒有發生。**
安裝成功、能 import、伺服器回 200，一律不算通過，程式碼層面直接擋掉。

---

## 兩關

| 關卡 | 檔案 | 做什麼 | 有沒有權力說「可以採用」 |
|---|---|---|---|
| 第一關 情報篩選 | `screen.py` | 只做機械判斷：相關性、去重、活躍度、查不查得到。不做品質判斷 | 沒有。只能刷掉，不能放行 |
| 第二關 實測驗證 | `verify.py` | 在沙箱裡真的裝、真的建置、真的開瀏覽器看畫面 | **有，而且只有這一關有** |

第二關的眼睛是 `render_check.mjs`：開真的瀏覽器，逐個元素讀 computed opacity 與 visibility，
算「實際畫得出來的元素數」與可見文字量。**不看回應碼**，因為頁面打得開不等於畫得出來。

---

## 怎麼跑

### 第一關

```bash
set DIGEST_REPO=<每日開源情報 repo 的路徑>
python screen.py                 只看最近 7 份情報
python screen.py --days 30       看最近 30 份
python screen.py --no-pull       不要更新情報 repo
```

`DIGEST_REPO` 沒設就直接失敗，不會安靜地跑出一份空清單。
結果寫進 `queue/pending.json`，那是候選清單，不是結論。

### 第二關

```bash
python verify.py --selftest-only                        只跑檢查器能力測試
python verify.py --recipe recipes/facebook__astryx.json 實測一個候選
python verify.py --recipe <recipe> --keep-sandbox       留下沙箱自己去看
```

每次實測**跑之前**會先做一次能力測試：拿一個空白頁與一個正常頁對照，
證明這支檢查器分得出「畫得出來」與「畫不出來」。分不出來就整份結果作廢，回傳碼 2。

沙箱建在系統暫存目錄底下（`ecom-upgrade-intake/<repo>`），每次重跑會先整個刪掉重建，
**不會污染這個 repo，也不會留在這裡**。

需要 Playwright。`render_check.mjs` 住的資料夾沒有 `node_modules`，
`verify.py` 會把全域 `node_modules` 指進 `NODE_PATH`；找不到就讓它照原樣報錯，不假裝沒事。

---

## 結論有三種，不是兩種

| 結論 | 意思 |
|---|---|
| `PASS` | 要它做的事真的發生了，證據齊全 |
| `FAIL` | 沒有發生，或中途出錯 |
| `INCONCLUSIVE` | 逾時、外部服務不可用、或過程中出現退回退路的跡象 |

`INCONCLUSIVE` **不准當成通過，也不記成失敗**，要重跑或改條件。
這一態是刻意設計的：把「不知道」硬塞進通過或失敗，是這條產線踩過的坑
（見 [`../PITFALLS.md`](../PITFALLS.md)「外部服務壞掉時安靜退回退路，然後回報成功」）。

判 `INCONCLUSIVE` 的訊號寫死在 `verify.py` 的 `FALLBACK_MARKERS`：
`falling back to`、`using placeholder`、`mock mode`、`ECONNREFUSED`、「退回」這類字樣一出現，
就算畫面看起來對，也不准判 `PASS`。

---

## 目錄裡有什麼

| 路徑 | 是什麼 |
|---|---|
| `screen.py` | 第一關。輸出 `queue/pending.json` |
| `verify.py` | 第二關。輸出 `verifications/<repo>/report.json` 與截圖 |
| `render_check.mjs` | 第二關的瀏覽器量測，由 `verify.py` 呼叫，不單獨跑 |
| `recipes/*.json` | 一個候選一份：怎麼裝、怎麼建置、怎麼起服務、要看到什麼才算數 |
| `recipes/blocks/<repo>/` | 要塞進沙箱的檔案，例如用候選框架寫的商品區樣本 |
| `templates/vite-react/` | 沙箱樣板：一個乾淨的 Vite + React 專案，給「裝一個套件來試」的候選用 |
| `templates/empty/` | 沙箱樣板：空的，給「自己 clone 整個專案下來驗」的候選用 |
| `verifications/<repo>/` | 實測留下的證據：`report.json` 與 `screenshot_*.png` |
| `queue/pending.json` | 第一關的候選清單。**本機執行資料，不進版控** |
| `queue/selftest.json` | 最近一次檢查器能力測試的結果。**每跑必覆蓋，不進版控** |

### recipe 長什麼樣

一份 recipe 就是「這次要對它做什麼事、做完要看到什麼」。沒有 `build` 也沒有畫面斷言的 recipe
會被 `validate_recipe()` 直接判為無效，拒絕執行，因為那種 recipe 只能證明「裝得起來」。

```json
{
  "repo": "vercel/commerce",
  "template": "empty",
  "replaces_or_adds": "SKILL.md Phase 2 的店面骨架。要回答的是：能不能直接拿它當商品列表與商品頁的起點。",
  "steps": [ { "name": "取得原始碼", "cmd": ["git", "clone", "..."], "timeout": 600 } ],
  "build": { "cmd": ["npm", "run", "build"], "cwd": "app", "timeout": 1200 },
  "serve": { "cmd": ["npm", "run", "start", "--", "-p", "{port}"], "ready_timeout": 120 },
  "expect": { "routes": ["/"], "min_visible_elements": 30, "min_body_text": 200, "no_console_error": true }
}
```

`replaces_or_adds` 是必填，而且要寫成「它取代或補上產線的哪一塊」。
答不出這一格，就代表還不知道它要解決什麼，不該花時間驗。

---

## 已經留在這裡的三份證據

| 候選 | 結論 | 為什麼留著 |
|---|---|---|
| `facebook__astryx` | `PASS` | 通過的樣子：建置退出碼 0、首頁 61 個可見元素、345 字、主控台無錯 |
| `vercel__commerce` | `FAIL` | 「打得開但畫不出來」的樣子：伺服器有回應，可見元素只有 21 個，低於門檻 30 |
| `_mutation__timeout` | `INCONCLUSIVE` | **變異測試**：故意設一個不可能完成的時限，證明關卡在逾時的時候會說「不知道」 |

第三份是刻意種的假候選，`recipes/_mutation_timeout.json` 不評估任何東西。
**它的用途是證明這套關卡有偵測能力**：哪天有人把三態改成兩態，它就會從 `INCONCLUSIVE` 變成 `PASS` 或 `FAIL`。
報告檔進版控就是為了這個對照，不是實測結果沒清乾淨。

---

## 誰會叫它

**工具與研發部門**（[`../../departments/07-tools-rd.md`](../../departments/07-tools-rd.md)）。
要接進產線的東西一律走這兩關，`SKILL.md` 與 `references/` 的規範不因為「這個專案很紅」而改。

⚠️ **目前是手動觸發，沒有任何排程會自動跑它。**

⚠️ **採用之後的回寫還沒做。** `screen.py` 的說明提到 `adopt.py` 會把結論寫回情報端的決策紀錄、
去重會讀 `LEDGER.jsonl`，**這兩個檔目前都還不存在**（`LEDGER.jsonl` 讀不到時去重那一道會直接跳過）。
也就是說，第二關驗完的結論現在得自己記，同一個專案有可能被情報端再推一次。
