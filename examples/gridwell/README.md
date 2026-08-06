# GRIDWELL

桌面與線材收納用品的品牌電商站。

## 設計方向

嚴謹的格線排版、克制的用色。把「整齊」這件事本身變成視覺語言，讓版面結構呼應商品要解決的問題。

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
