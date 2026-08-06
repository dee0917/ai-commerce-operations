# VANGUARD

隨身裝備與工具的品牌電商站。

## 設計方向

深色底、等寬字體、橘色作為單一強調色。走機能與戰術感，資訊密度高，強調規格與用途。

跟同一條產線產出的其他站刻意走完全相反的方向：那些站用留白營造質感，這個站用密度營造專業感。

## 怎麼看

```bash
cd dist
python -m http.server 8000
```

開 `http://localhost:8000`。截圖在 [`../screenshots/`](../screenshots/)。

## 怎麼改

```bash
npm install
npm run dev
```

React 19 + TypeScript + Vite + Tailwind CSS 3。商品資料寫在程式碼裡，不需要資料庫或任何金鑰。
