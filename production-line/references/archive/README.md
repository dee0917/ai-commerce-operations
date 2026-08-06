# archive/ 為什麼留著這些檔案

這裡放的是**已停用（DEPRECATED）的舊版規格**。它們被搬出 `references/` 是因為：
代理人執行時會逐檔讀取 `references/`，撞見停用檔一樣會讀、會照做，2026-08 健檢已實證這會害人。

| 檔案 | 停用原因 | 接手者 |
|------|---------|--------|
| `aesthetics-engines.md` | 九引擎體系已被 v11 DNA 混血體系取代 | 動效分級清單由 `../motion-system.md` 接手（對映 DNA Family）；美學骨架由 `../real-ecommerce-dna.md` 接手 |
| `aesthetic-variance-engine.md` | 同上，且其標竿品牌表已併入 DNA 檔案 | `../real-ecommerce-dna.md` |

**保留理由**：品牌標竿對照表與動效清單原文仍有查閱價值（motion-system.md 的分級清單即源於此），
且版本考古時需要對照。

**使用規則**：
- ❌ 執行產線流程時**不讀本資料夾**，一切以 `references/` 現行檔案為準。
- ❌ 不可把本資料夾的規格直接照做。
- ✅ 只在「查歷史脈絡、比對舊清單」時人工查閱。

- `prd-generation.md`：被 v11.0 的設計基因系統取代。原本還留在 `references/` 頂層，但它自己第一行就標了停用，執行時一樣會被讀到。
