# Asset Handling SOP

## Folder convention
```
src/assets/
├── shared/          # Logo, brand mark, favicon, universal icons
│   ├── logo.svg
│   └── logo-dark.svg
├── 01-intro/        # Per-scene assets. Prefix = scene id prefix
│   ├── hero.png
│   └── diagram.svg
├── 03-architecture/
│   └── pipeline.excalidraw.svg   # Excalidraw raw: commit the .svg export, not .excalidraw json
└── fonts/           # Custom webfonts (if not loading from Google Fonts)
    └── your-font.woff2

tests/               # NEVER put slide assets here. Test harness only.
scripts/             # NEVER put slide assets here. Tooling only.
public/              # Static files copied as-is. Favicons, robots.txt, og-image.png
```

## CLI one-liners
```bash
# 1) Create per-scene asset folder
mkdir -p src/assets/04-chapter-title

# 2) Optimize SVG (svgo must be installed: npm i -g svgo or npx)
npx svgo -f src/assets/04-chapter-title --enable=removeTitle,removeDesc --pretty

# 3) Optimize PNG → WebP 82%, max 1600px width
# Install: brew install webp (macOS) or apt install webp (Linux)
find src/assets -name "*.png" -exec sh -c '
  cwebp -q 82 -resize 1600 0 "$1" -o "${1%.png}.webp" && rm "$1"
' _ {} \;

# 4) Verify no asset >500KB
find src/assets -type f -size +500k -exec ls -lh {} \;
# Anything flagged: re-export at lower quality, or use poster image + <video loading=lazy>

# 5) SVG inline for multi-color icons (avoid <img src=x.svg> if you need theme-aware colors)
# Instead: paste raw SVG markup directly, or use SVGR during Vite build:
# import { ReactComponent as Logo } from './logo.svg'
```

## Rules
- No `.jpg` inside `src/assets/`. Always `.webp` for photos.
- No hardcoded `width=300 height=200` on images. Use CSS class + intrinsic aspect ratio.
- SVGs that must change color with theme: use `currentColor` in the `<path fill=...>` NOT a hardcoded hex.
- 3rd-party icon packs: Phosphor Icons via React components (not raw SVG files). Install: `npm i @phosphor-icons/react`
