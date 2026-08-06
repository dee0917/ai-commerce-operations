import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vite.dev/config/
export default defineConfig(({ command }) => ({
  base: './',
  plugins: [react()],
  // The dist/ here is checked in as a demo people open straight from disk, so a
  // production build must never bake in a backend that only exists on one
  // developer's machine. Forcing this empty makes services/api.ts take the bundled
  // mock-data path and makes checkout return a simulated success. It wins over any
  // local .env.local, which is what previously leaked http://localhost:8088 into
  // the shipped bundle. `npm run dev` is untouched and still reads .env.local.
  ...(command === 'build'
    ? { define: { 'import.meta.env.VITE_WOO_URL': '""' } }
    : {}),
}))
