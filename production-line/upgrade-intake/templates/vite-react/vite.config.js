import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

// 沙箱用的最小設定。base 用相對路徑，讓 dist 可以直接被靜態伺服器餵出來。
export default defineConfig({
  plugins: [react()],
  base: './',
  build: { outDir: 'dist' },
});
