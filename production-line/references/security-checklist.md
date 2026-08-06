# 🔒 電商安全自檢清單 (Security Checklist)

> 基於 Antigravity Kit 的 `vulnerability-scanner` 技能，
> 針對電商 Mock 專案與未來真實 WooCommerce 串接的安全要求。
>
> ⚠️ 出處說明：Antigravity Kit（`.agent/`）**未隨本 repo 發佈**，只存在於產線的本機技能目錄。
> 詳見 [SKILL.md](../SKILL.md) 的「Antigravity Kit 整合說明」。本文內容本身是完整的，不需要該目錄才能讀。

---

## 前端安全（必須在交付前檢查）

### XSS 防護
- [ ] **禁止 `dangerouslySetInnerHTML`**（除非渲染經過信任與淨化後的 WP 文章內容）
- [ ] 用戶搜尋輸入已做 sanitize（清除 `<script>` 標籤等）
- [ ] 商品名稱/描述在渲染前已轉義

### CSRF 防護
- [ ] 所有表單提交（Login, Register, Checkout）預留 CSRF Token 佔位
- [ ] 使用 POST 方法提交敏感操作（非 GET）

### 客戶端安全
- [ ] **無硬編碼 API Key 或 Token**（應使用 `.env` 環境變數）
- [ ] `.env` 已加入 `.gitignore`
- [ ] 無客戶端直接計算最終金額（金額計算僅信任後端）
- [ ] 無 `eval()` 使用
- [ ] Token / Session 使用 HttpOnly Cookie 模式（mockAuth 需預留此架構）
  - ⚠️ **現況：尚未達成。** 目前 Token 存在 `localStorage`（見 `member-zone.md` 的 `auth.ts`、
    `service-layer-spec.md` 的 `getAuthToken()`）。HttpOnly Cookie 需要後端配合設定 Set-Cookie 與
    CORS credentials，**在目前的純前端架構下無法只靠前端做到**。此條保留為目標，不得逕行打勾。

---

## 狀態管理安全

### Zustand Store
- [ ] Cart Store 不儲存敏感支付資訊
- [ ] Auth Store 使用安全的 Token 儲存方式（非 localStorage 明文）
  - ⚠️ **現況：尚未達成。** 唯一有規格的實作是 `localStorage.getItem/setItem('auth_token', ...)`
    （`member-zone.md` 的 `auth.ts`、`service-layer-spec.md` 的 `getAuthToken()`）。
    與上一條同一個根因：要改掉必須先有後端 HttpOnly Cookie。目前已有的緩解只有 TTL 過期與 401 自動登出。
- [ ] 登出時完全清除所有 user state

### Mock 認證架構
- [ ] 模擬 Token 有過期機制（TTL）
- [ ] Protected Route 實作正確（未登入自動跳轉 Login）
- [ ] 密碼欄位使用 `type="password"`

---

## 資料安全

### 敏感欄位
- [ ] 信用卡號碼僅顯示末 4 碼（如 `**** **** **** 1234`）
- [ ] 密碼從不以明文傳送或顯示
- [ ] Email 在公開頁面做脫敏處理（如 `j***@example.com`）

### 輸入驗證
- [ ] Email 格式驗證（React Hook Form + pattern）
- [ ] 密碼最低長度 8 字元
- [ ] 搜尋最大長度限制（防止 URL 注入）
- [ ] 數量欄位只接受正整數（Math.max(1, value)）

---

## 部署安全（未來 WooCommerce 串接時適用）

### API 通訊
- [ ] 所有 API 請求使用 HTTPS
- [ ] API Base URL 使用環境變數（`VITE_API_URL`）
- [ ] 錯誤訊息不暴露內部實作細節

### 第三方依賴
- [ ] `npm audit` 無 high/critical 漏洞
- [ ] 無已知安全問題的 npm 套件
- [ ] 依賴版本鎖定（`package-lock.json` 在版控中）

---

## 安全等級評估

| 等級 | 分數 | 說明 |
|------|------|------|
| 🟢 A | 90-100 | 所有檢查通過，無安全問題 |
| 🟡 B | 70-89 | 有警告但無嚴重問題 |
| 🟠 C | 50-69 | 有安全隱患需要修復 |
| 🔴 D | <50 | 存在嚴重安全漏洞 |

> **目標**：每次交付必須達到 B 級以上。
