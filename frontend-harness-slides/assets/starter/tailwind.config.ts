import type { Config } from 'tailwindcss';

// Tokens map to CSS variables set by ThemeProvider, so slides use clean classes
// (bg-background, text-primary, font-display) instead of inline hex. Do not use the
// `/<alpha>` opacity modifier on these var-backed colors — it produces invalid CSS.
export default {
  content: ['./index.html', './src/**/*.{ts,tsx}'],
  theme: {
    extend: {
      colors: {
        background: 'var(--color-background)',
        text: 'var(--color-text)',
        primary: 'var(--color-primary)',
        border: 'var(--color-border)',
      },
      fontFamily: {
        display: 'var(--font-display)',
        body: 'var(--font-body)',
      },
    },
  },
  plugins: [],
} satisfies Config;
