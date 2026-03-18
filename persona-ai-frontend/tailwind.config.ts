import type { Config } from "tailwindcss";

const config: Config = {
  content: [
    "./src/pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/components/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        primary: {
          50:  "#EEEDFE",
          100: "#CECBF6",
          400: "#7F77DD",
          600: "#534AB7",
          900: "#26215C",
        },
      },
    },
  },
  plugins: [],
};

export default config;
