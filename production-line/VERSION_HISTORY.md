# 技能版本歷史 (Version History)

> 此 repo 只收錄當前版本的完整內容。下文提到的 `versions/` 舊版存檔與部分交付文件未一併收錄，版本演進的紀錄以本文為準。

## 檔案架構說明

本專案採用 **單一活動技能檔案** 架構：

- **`SKILL.md`** - 唯一會被 Claude Code 讀取的技能檔案（活動版本）
- **`versions/`** - 歷史版本存檔目錄（未隨本 repo 收錄，見上方說明）

## 版本演進

### v11.1 (Current) - 2026-08-04

**檔案**: `SKILL.md`

**這次改的是規範與驗收，不是產線骨架。** 以下每一條都有實證來源。

**變更**:
- 動效基線接回主線：新增 [references/motion-system.md](references/motion-system.md)，接手已歸檔的 `aesthetics-engines.md`。Phase 1.2.5 依 DNA Family 選 Tier，Phase 2.55 四項最低要求（滾動進場、有意圖的 hover、禁用預設 easing、`reducedMotion="user"`）缺一即 FAIL。起因：舊清單標了 DEPRECATED 之後沒有東西接手，產線連續多站零動效
- 連續視覺去重（強制）：`design-history.json` 加入 `bg_tone` 欄位，Phase 1.05 比對最近 3 筆的 `bg_tone` 與 `fonts.display`，撞到就重抽；建站後回寫歷史改成強制項。起因：連續四站都是暖紙底加襯線大標，並排看像同一家的三種皮膚
- 部署設定檔列為必做：Phase 1.9 要求專案根目錄與 `dist/` 都放 `vercel.json`。起因：2026-08-04 兩個站漏掉這一步，上線後除了首頁全部打不開
- 商品圖三層退路：[scripts/generate_images_fallback.py](scripts/generate_images_fallback.py)，生成工具不可用時退 Unsplash，再不行退佔位圖，不讓缺圖擋住整條線
- 驗收腳本補齊：[scripts/validate_live_flow.py](scripts/validate_live_flow.py) 做真連線驗證與前端金鑰外洩掃描，`check_visible.mjs` 檢查畫面實際畫得出來。起因：回應碼只證明伺服器有回東西，不證明前端跑得起來
- 停用檔案改成搬走而不是標註：停用的規範移到 `references/archive/`，因為代理人會逐檔讀 `references/`，撞見標了停用的檔一樣會照做
- 規範內部口徑統一：「11 頁」全面改寫成「11 類必備頁面，展開為 15 個路由」，與 README 和 site-architecture.md 對齊

---

### v11.0 - 2026-03-25
**檔案**: `SKILL.md`
**變更**:
- ✅ 66 個真實電商 DNA 模板（取代舊美學引擎系統）
- ✅ DNA 混血系統：主 DNA (80% 骨架) × 副 DNA (20% 靈感)，組合數 66×65÷2 × 6 個 UI 框架 = 12,870 種
- ✅ 現代 UI 框架選擇（shadcn/DaisyUI/Radix 等 6 種）
- ✅ design-history.json v3.0 schema（含 crossbreeding 紀錄）
- ✅ Phase -1 系統預檢（preflight_check.py）
- ✅ 防重複機制：檢查最近 5 次 DNA Family 使用紀錄

**特色**:
- DNA 混血取代舊 Aesthetic Variance Engine
- 結構、風格、框架三個維度都納入防重複檢查
- 成熟度評分系統（maturity_score）

---

### v10.0 - 2026-03-19
**檔案**: `SKILL.md.v10`（存檔為歷史參考）。v9 系列的最後穩定版，內容為：Antigravity Kit 完整整合、NotebookLM 設計決策查詢、`ui-ux-pro-max` 設計系統技能、11 頁完整實作、7 層品質門檻，以及從 v9.1 延續的 Stitch AI 可選整合。
**狀態**: 已被 v11.0 的 DNA 系統取代。

---

### v9.1 - 2026-03-19
**檔案**: `SKILL.md`。新增 Stitch MCP 工具支援（`allowed-tools` 加入 `mcp__stitch__*`）與 Phase 1.16 可選的 Stitch AI 設計探索步驟，並開始把每次的設計選擇寫進設計歷史檔以供比對。
**整合方式**: 最小化變更、可選啟用；Stitch 不可用時自動 fallback 回原有流程，向後相容。

---

### v9.0 - 2026-03-18
**檔案**: `versions/SKILL.md.backup`。第一個整合 Antigravity Kit（`.agent/` 目錄下的代理、領域技能、工作流與腳本套件）的版本。
**內容**: NotebookLM 設計決策查詢、`ui-ux-pro-max` 設計系統技能、11 頁完整實作、7 層品質門檻。

---

## 版本比較

> **兩處口徑差異先講清楚，免得誤讀：**
> - **頁面數**：v9-v10 當時的寫法是「11 頁」，v11.1 起統一改稱「11 類必備頁面，展開為 15 個路由」。指的是同一組頁面，只是口徑統一，不是頁數變了。
> - **品質門檻層數**：v9-v10 是 7 層；目前 `scripts/ecommerce-checklist.py` 實跑 8 層，多出來的是 UK/EU 合規閘門。**這一層是在哪一個版本加進來的，現存紀錄查不到**（本 repo 的 git 歷史從已含 8 層的狀態開始），所以下表不標它的版本，也不回填猜測值。

| 功能 | v9.0 | v9.1 | v10.0 | v11.0 | v11.1 (Current) |
|------|------|------|-------|-------|-----------------|
| NotebookLM 設計決策查詢 | ✅ | ✅ | ✅ | ✅ | ✅ |
| `ui-ux-pro-max` 設計系統技能 | ✅ | ✅ | ✅ | ✅ | ✅ |
| Stitch 整合 | ❌ | ⚡ 可選 | ⚡ 可選 | ⚡ 可選 | ⚡ 可選 |
| 防重複的實際規則 | 無 | 記錄設計歷史供比對 | 記錄設計歷史供比對 | 主 DNA Family 不得與最近 5 站相同 | 再加：display 字體不得與最近 3 站任一站相同、同一底色系不得連續第 3 次，且在選定當下就鎖定（`design_history.py reserve`） |
| 動效基線 | ❌ | ❌ | ❌ | ❌ | ✅ 必做 |
| 66 DNA 模板 | ❌ | ❌ | ❌ | ✅ | ✅ |
| 現代 UI 框架 | ❌ | ❌ | ❌ | ✅ (6 種) | ✅ (6 種) |

> 「防重複的實際規則」一列寫的是**程式實際會擋下什麼**，不是評分。
> v11.0 的規則見 [SKILL.md](SKILL.md) Phase 1.05 第 3 點與 [references/real-ecommerce-dna.md](references/real-ecommerce-dna.md)；
> v11.1 的比對窗口與判定條件見 [scripts/design_history.py](scripts/design_history.py)（`RECENT_WINDOW`、`dedup_violations`）。

---

## 使用指南

### 啟用 Stitch 功能 (v9.1)

1. **環境變數設定**
   ```bash
   # 在專案根目錄創建 .env
   STITCH_ENABLED=true
   STITCH_API_KEY=your_api_key
   ```

2. **執行時自動判斷**
   - 若 `STITCH_ENABLED=true`，執行 Phase 1.16
   - 若 `STITCH_ENABLED=false` 或未設定，跳過 Stitch 步驟

3. **無縫 Fallback**
   - Stitch 連接失敗不影響主流程
   - 自動回退到原有設計系統

---

## 變更日誌

### 2026-08-04
- 發布 v11.1：動效基線、連續視覺去重、部署設定檔、商品圖退路、真連線驗收腳本
- 停用的規範檔從 `references/` 移進 `references/archive/`
- 頁面數口徑統一為「11 類必備頁面，展開為 15 個路由」

### 2026-03-19
- 創建 v9.1，加入 Stitch 可選整合
- 整理版本檔案到 `versions/` 目錄
- 創建此版本歷史文件

### 2026-03-18
- 完成 v9.0：整合 Antigravity Kit（`.agent/` 代理與技能套件）
- 創建初始備份

---

## 相關文件

- [主技能檔案](SKILL.md) - 當前活動版本
