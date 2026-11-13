# Web instance & single-file HTML

A standalone single-file `.html` page is the default deliverable.
`assets/base.css` is the worked Web instance of the vocabulary in
`02-components.md`, providing every token and component as CSS custom
properties and classes.

- **Self-contained by default**: inline `assets/base.css` in a `<style>`
  block, keep scripts and inline SVGs in the same file, and compose page rules
  with the existing `--pvl-*` tokens. Split into separate files or integrate
  into an existing stylesheet only when the reader asks or the host codebase
  needs it. A new reusable component joins `base.css` with a version bump.
- **Handwritten fonts**: embed the subsets from `assets/fonts/` (SIL OFL) as
  `data:font/woff2;base64,...` URIs when their size (~1.1 MB encoded) fits the
  delivery context, or drop the relative `url("fonts/...")` `@font-face` rules
  so `--pvl-font-display` falls back cleanly to system Kai
  (`"Kaiti SC","STKaiti",cursive`) with no broken local requests.
- **Screenshots**: any headless browser works. Measure the real 390px layout
  (an iframe probe or devtools device mode): macOS headless Chrome clamps
  windows to >= 500px, so a direct 390px screenshot reports the clamped width.
- **Specimens**: `assets/snippets/` and `assets/examples/` are Web specimens:
  look at them for the hand; copy structure and classes, replace content. On
  other carriers reproduce the parameters from `02-components.md` in that
  platform's idiom.
