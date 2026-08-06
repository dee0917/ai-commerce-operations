# AURAGUARD

開運與能量飾品的品牌電商站。

## 設計方向

溫潤的米白基調、襯線標題字、大幅實物攝影。整體走精品編輯風，用留白與攝影撐起質感，而不是靠裝飾元素。

商品本身有文化脈絡，所以視覺刻意收斂，讓實物照片說話。

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
