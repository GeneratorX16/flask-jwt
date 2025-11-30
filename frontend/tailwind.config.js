/** @type {import('tailwindcss').Config} */
module.exports = {
  theme: {
    extend: {
      animation: {
        // Define a custom animation for slower spinning
        slowSpin: "spin 2s linear infinite",
      },
    },
  },
  plugins: [],
};