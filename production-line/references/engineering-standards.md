# 🏗️ Engineering Standards v4 (高可用實作標準)

本文件定義 `auto-ecommerce` 的工程底線。所有生成的專案必須強制遵循。

---

## 1. 圖片安全加固 (SafeImage Component)

為了徹底解決歷史對話中反覆出現的「死圖/斷圖」問題，所有顯示圖片的地方**嚴禁直接使用 `<img>`**，必須封裝以下組件：

```tsx
// src/components/common/SafeImage.tsx
import React, { useState } from 'react';

interface SafeImageProps extends React.ImgHTMLAttributes<HTMLImageElement> {
  fallback?: string;
}

/**
 * SafeImage Component
 * 1. 嘗試載入 primary source
 * 2. 失敗時顯示 fallback 圖片
 * 3. 若 fallback 也失敗，顯示帶有產品名稱的品牌佔位色塊
 */
export const SafeImage: React.FC<SafeImageProps> = ({ 
  src, 
  alt, 
  className,
  ...props 
}) => {
  const [error, setError] = useState(false);

  if (error || !src) {
    return (
      <div 
        className={`flex items-center justify-center bg-secondary/10 text-secondary/40 text-xs font-medium text-center p-4 select-none ${className}`}
        style={{ aspectRatio: '1/1' }}
      >
        <div className="flex flex-col items-center gap-2">
          <span className="opacity-50">[ {alt || 'Image'} ]</span>
        </div>
      </div>
    );
  }

  return (
    <img
      src={src}
      alt={alt}
      onError={() => {
        console.warn(`Image Load Failed: ${src}`);
        setError(true);
      }}
      className={className}
      loading="lazy"
      {...props}
    />
  );
};
```

---

## 2. 狀態管理標準 (Zustand)

禁止使用冗長且難以維護的 `Prop Drilling` 或複合 Context。統一使用 Zustand。

### 購物車邏輯規範 (必須包含以下功能)
- `items`: `CartItem[]`
- `addItem`: 新增商品（若已存在則增加數量）。
- `removeItem`: 徹底移除。
- `updateQuantity`: 增減數量（向下限制為 1）。
- `clearCart`: 結帳完成後清除。
- `subtotal`: 自動計算。

---

## 3. 表單與驗證 (React Hook Form)

所有輸入（搜尋、登入、結帳）必須包含基礎驗證：
- 必填欄位檢查。
- Email 格式驗證。
- 密碼長度驗證 (Min 8 characters)。
- **User Feedback**: 錯誤時紅字提示，按鈕 `disabled` 狀態。

---

## 4. 全球化 SEO 與無障礙 (a11y)

- **Helmet**: 每個頁面 `useEffect` 都要確保 title 變化（例如：`{ProductName} | {BrandName}`）。
- **Lighthouse Score**: 目標是 Accessibility 與 Best Practices 分數 > 90。
- **Interactive**: 所有 `button` 與 `a` 標籤必須具備強烈的 `:hover` 與 `:active` 視覺回饋。

---

## 5. 無 Placeholder 實作清單

交付前檢查以下邏輯是否為「真」：
- [ ] **搜尋 (Search)**: 輸入關鍵字後，商品清單能真實過濾。
- [ ] **結帳 (Checkout)**: 點擊進到第三步 Success 頁後，購物車內容已被清空，且產生一筆 Mock Order ID。
- [ ] **詳情 (Detail)**: 能根據 `slug` 正確匹配到資料庫中的商品，若匹配不到應引導回商店頁而非崩潰。
- [ ] **彈窗 (Toasts)**: 加入購物車、登入成功等操作必須有 UI 反饋 (例如 `alert` 或自訂 Toast)。
