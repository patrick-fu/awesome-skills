# Fonts — open-source only, installed locally

Beautiful type without licensing risk. Never bundle commercial font files in the skill or the project; pull open-source faces from official sources and install them into the deck's own `public/fonts/`.

## Recommended open-source faces

**Sans / Display**
- *Syne* (bold, brutalist) — https://fonts.google.com/specimen/Syne
- *Cabinet Grotesk* (sharp, modern) — https://www.fontshare.com/fonts/cabinet-grotesk
- *Plus Jakarta Sans* (clean, professional) — https://fonts.google.com/specimen/Plus+Jakarta+Sans

**Serif / Editorial**
- *Cormorant Garamond* (high-contrast serif) — https://fonts.google.com/specimen/Cormorant+Garamond
- *Playfair Display* (editorial classic) — https://fonts.google.com/specimen/Playfair+Display

**Chinese / Handdrawn**
- *LXGW WenKai Lite* (霞鹜文楷 Lite, handdrawn/sketch) — https://github.com/lxgw/LxgwWenKai-Lite
- *Noto Serif SC* (思源宋体) — https://fonts.google.com/specimen/Noto+Serif+SC

Avoid the AI-slop defaults: Inter, Roboto, Arial, system-ui.

## Install locally (don't hotlink)

1. Download the `.woff2` / `.ttf` from the official source above.
2. Put the files in `public/fonts/`.
3. Declare `@font-face` in `index.css` pointing at the local files; reference the family in your `ThemeConfig` font tokens.

Local install buys two things: zero copyright liability, and a deck that renders identically offline (no dependence on a live font CDN mid-talk). For compiling a large CJK font to `woff2` in CI, see `deploy.md`.
