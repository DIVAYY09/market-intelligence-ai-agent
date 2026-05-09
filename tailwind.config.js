/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  darkMode: 'class',
  theme: {
    extend: {
      colors: {
        'retro-light': '#F4F0EB',
        'retro-dark': '#121212',
        'retro-gray': '#888888',
      }
    },
  },
  plugins: [],
}
