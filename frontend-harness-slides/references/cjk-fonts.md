# CJK Fonts

Use this when a deck contains Chinese, Japanese, or Korean text. Keep the decision
simple unless the project needs reproducible visual baselines across machines.

## Three Levels

### 1. Local presentation first

Use a system font stack such as:

```css
font-family: -apple-system, BlinkMacSystemFont, "PingFang SC", "Noto Sans CJK SC", sans-serif;
```

This is fastest and often enough for a local talk. It may drift across machines
or CI because different systems render different fallback fonts.

### 2. Reproducible baseline

Bundle a webfont under `public/fonts/` and reference it with `@font-face`. This
reduces cross-machine drift and is preferred when visual baselines must be shared
or run in CI.

### 3. Large CJK deck

Do not commit a full 10-20MB CJK font package by default. Subset the glyphs used
by the deck and aim for small WOFF2 files. Use this only when the project needs
stable CI or handoff rendering and the extra setup is worth it.

## Practical Guidance

- Check package size and available weights before adding a font package.
- Keep display, body, and mono decisions separate.
- If visual snapshots show text-edge drift across machines, suspect fonts before
  raising screenshot thresholds.
- If you choose system fonts, state that the baseline is local-environment
  dependent.
