/** @type {import('tailwindcss').Config} */
export default {
    content: ["templates/**/*.{html,j2}", "styles/**/*.css"],
    theme: {
        extend: {},
    },
    plugins: [require("daisyui")],
};
