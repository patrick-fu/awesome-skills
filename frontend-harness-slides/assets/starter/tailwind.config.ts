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
      // P0-3 FIXED: effects tokens (border-radius/border-width/box-shadow) map to the
      // CSS variables ThemeProvider injects from theme.effects.* in themes.ts. Use
      // rounded-card / shadow-card / border-theme in components instead of hard-coded
      // Tailwind values so a theme swap changes every surface at once.
      //
      // DEFAULT alias + sm/lg/xl variants keep the same naming cadence as the built-in
      // Tailwind ladder; --slide-* fallback keeps older slide sets that predate effects
      // tokens running without visible regressions.
      borderRadius: {
        DEFAULT: 'var(--slide-radius, var(--effect-border-radius, 0.5rem))',
        sm: 'var(--effect-border-radius-sm, 0.375rem)',
        card: 'var(--effect-border-radius, 0.75rem)',
        lg: 'var(--effect-border-radius-lg, 1rem)',
        xl: 'var(--effect-border-radius-xl, 1.5rem)',
      },
      borderWidth: {
        theme: 'var(--effect-border-width, 1px)',
      },
      boxShadow: {
        DEFAULT: 'var(--slide-shadow, var(--effect-shadow, 0 1px 3px 0 rgb(0 0 0 / 0.1)))',
        sm: 'var(--effect-shadow-sm, 0 1px 2px 0 rgb(0 0 0 / 0.05))',
        card: 'var(--effect-shadow, 0 4px 20px rgba(0, 0, 0, 0.10))',
      },
    },
  },
  plugins: [],
} satisfies Config;
