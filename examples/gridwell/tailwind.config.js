/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      fontFamily: {
        // DM Sans for body/UI
        sans: ['"DM Sans"', 'sans-serif'],
        // DM Serif Display for hero headline only
        display: ['"DM Serif Display"', 'serif'],
      },
      colors: {
        brand: {
          light: '#F5F5F0',    // cool off-white (not warm cream/beige)
          dark: '#1B2E22',     // deep forest near-black
          accent: '#3D6B4F',   // muted forest green, single accent
          muted: '#8FA598',    // desaturated green for secondary text
          surface: '#EDEEE8',  // card surface, slightly distinct from page bg
        }
      },
    },
  },
  plugins: [],
}
