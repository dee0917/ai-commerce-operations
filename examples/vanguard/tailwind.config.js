/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        vanguard: {
          obsidian: '#121212',
          red: '#FF3D00',
          slate: '#334155',
          industrial: '#1E293B',
          gray: {
            900: '#0F172A',
            800: '#1E293B',
            700: '#334155',
            400: '#94A3B8',
          }
        }
      },
      fontFamily: {
        mono: ['IBM Plex Mono', 'monospace'],
        sans: ['Inter', 'sans-serif'],
      },
      boxShadow: {
        'bento': '0 4px 20px -2px rgba(0, 0, 0, 0.5)',
        'tactical': '0 0 15px rgba(255, 61, 0, 0.2)',
      }
    },
  },
  plugins: [],
}
