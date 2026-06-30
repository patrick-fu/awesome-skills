# Deploy

Use this when the user wants a live URL, a shareable build, or a static handoff
after the deck frames have already been checked.

## Live URL

The deck routes on `?scene=<id>&beat=<n>`. On static hosting, a deep link or
manual refresh can 404 unless the host rewrites app routes to `index.html`.
Do not rewrite known static-asset paths, or a broken `/assets/font.ttf` can
resolve to HTML and fail as a font.

The starter includes a conservative `vercel.json`:

```json
{
  "cleanUrls": true,
  "trailingSlash": false,
  "headers": [
    { "source": "/fonts/(.*)", "headers": [{ "key": "Cache-Control", "value": "public, max-age=31536000, immutable" }] },
    { "source": "/assets/(.*)", "headers": [{ "key": "Cache-Control", "value": "public, max-age=31536000, immutable" }] }
  ],
  "rewrites": [
    { "source": "/((?!assets|fonts|_next|favicon\\.ico|sitemap\\.xml).*)", "destination": "/index.html" }
  ]
}
```

Typical deployment flow:

```bash
npm run test:full
npm run build
npx vercel --prod
```

If using another static host, preserve the same idea: immutable asset caching,
SPA fallback for deck routes, and no fallback for static asset directories.

## Optional PDF Handoff

The starter intentionally does not bundle a PDF exporter. If the user explicitly
needs PDF, choose the simplest project-specific path after `npm run test:full`
passes:

- Browser print/export is enough for simple decks.
- A temporary Playwright script can be created inside the project when the deck
  needs precise stage captures.
- A hosted URL plus manual export may be preferable when the user wants to review
  the live deck first.

Whatever path is chosen, inspect the output before delivery. Check font loading,
page count, clipped content, and whether animated beats collapse to the intended
static frame.

## CJK Font Size

If the deck uses a heavy CJK font, format conversion alone is not enough to get
it under budget. `ttf2woff2` changes the container; it does not subset glyphs.
For a large CJK TTF, a converted WOFF2 can still be many megabytes.

Use a subsetter only when stable CI or handoff rendering is worth the extra step:

```bash
glyphhanger ./dist/index.html --subset=./public/fonts/NotoSansSC.ttf --formats=woff2 --LATIN
pyftsubset public/fonts/NotoSansSC.ttf \
  --text-file=content/used-chars.txt \
  --flavor=woff2 \
  --output-file=public/fonts/NotoSansSC.subset.woff2
```

See `references/cjk-fonts.md` for the lighter decision tree.

## CI

The starter ships a GitHub Actions workflow as an optional harness gate. It
installs dependencies, installs Playwright Chromium, runs `npm run test:full`,
and uploads Playwright artifacts on failure.
