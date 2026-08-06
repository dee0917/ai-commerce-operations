/** @type {import('tailwindcss').Config} */
export default {
    content: ['./index.html', './src/**/*.{js,ts,jsx,tsx}'],
    theme: {
        extend: {
            colors: {
                brand: {
                    primary: '#FAF6F0',
                    secondary: '#1A1A1A',
                    accent: '#9E2A2B',
                },
            },
            fontFamily: {
                display: ['"Cormorant Garamond"', 'serif'],
                body: ['"Inter"', 'sans-serif'],
            },
        },
    },
    plugins: [],
};
