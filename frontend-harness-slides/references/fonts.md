# Fonts

Choose type as part of the deck's visual direction, not as an afterthought. The
font should match the chosen style, cover the deck's languages, and render
reliably in the final handoff.

Do not bundle commercial font files inside this skill. In a deck project, prefer
the user's own licensed font files when they provide them and the license allows
web embedding/deployment. If the user does not provide fonts, use open-source
faces from official sources.

## Rules

- Match fonts to the style preset or custom reference instead of defaulting to a
  generic web stack.
- For Chinese, Japanese, or Korean text, choose a font family with real CJK
  coverage for that language. Do not use Times New Roman, Helvetica, or another
  Latin-only face as the primary font for CJK content.
- Bundle delivery-critical fonts with the deck and load them with local
  `@font-face`. Do not depend on remote font CDNs for a live talk or final
  deployment.
- Keep display, body, and mono choices separate; a playful display font may not
  work for dense body text.
- Check package size and subset large CJK fonts when the deployed deck needs
  stable rendering without shipping unnecessary megabytes.

## Recommended open-source faces

**Sans / Display**
- *Syne* (bold, brutalist) — https://fonts.google.com/specimen/Syne
- *Cabinet Grotesk* (sharp, modern) — https://www.fontshare.com/fonts/cabinet-grotesk
- *Plus Jakarta Sans* (clean, professional) — https://fonts.google.com/specimen/Plus+Jakarta+Sans

**Serif / Editorial**
- *Cormorant Garamond* (high-contrast serif) — https://fonts.google.com/specimen/Cormorant+Garamond
- *Playfair Display* (editorial classic) — https://fonts.google.com/specimen/Playfair+Display

**Chinese / Handdrawn**
- *LXGW WenKai* (霞鹜文楷, handwritten/warm CJK) — https://github.com/lxgw/LxgwWenKai
- *LXGW WenKai Lite* (霞鹜文楷 Lite, lighter handdrawn/sketch option) — https://github.com/lxgw/LxgwWenKai-Lite
- *Ma Shan Zheng* (马善政体, expressive Chinese display) — https://fontsource.org/fonts/ma-shan-zheng
- *ZCOOL KuaiLe* (站酷快乐体, playful Chinese display) — https://fontsource.org/fonts/zcool-kuaile
- *Noto Serif SC* (思源宋体) — https://fonts.google.com/specimen/Noto+Serif+SC

Avoid the AI-slop defaults: Inter, Roboto, Arial, system-ui.

## Install locally

1. Download the `.woff2` / `.ttf` from the official source above.
2. Put the files in `public/fonts/`.
3. Declare `@font-face` in `index.css` pointing at the local files; reference the family in your `ThemeConfig` font tokens.

Local install gives the deck stable offline and deployed rendering. It does not
solve licensing by itself; confirm the user-owned font license or use
open-source fonts whose license permits the intended use. For compiling or
subsetting a large CJK font to `woff2` in CI, see `deploy.md`.
