import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vite.dev/config/
export default defineConfig(({ command }) => ({
  base: './',
  plugins: [react()],
  // The dist/ here is checked in as a demo people open straight from disk, so a
  // production build must never bake in a backend that only exists on one
  // developer's machine. Forcing this empty makes services/api.ts take the bundled
  // mock-data path. It wins over any local .env.local.
  // `npm run dev` is untouched and still reads .env.local.
  ...(command === 'build'
    ? { define: { 'import.meta.env.VITE_WOO_URL': '""' } }
    : {}),
}))
