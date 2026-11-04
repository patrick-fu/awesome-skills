---
name: paper-ink-style
description: >-
  Paper-and-pencil engineering-whiteboard visual style for HTML: rough
  pencil-line cards, marker-yellow highlights, sticky notes and tape,
  hand-annotated diagrams. Use when building or restyling HTML in this style
  (工程白板, inkboard).
---

# Paper Ink Style

My personal visual style for HTML — a paper-and-pencil engineering whiteboard.
One core (`assets/base.css`: tokens + components) plus six bounded extensions
that change density and surface, never the hand. Everything lives in this
directory; never fetch external fonts, pages, or docs.

## Workflow

1. Read `assets/base.css` and `references/01-grammar.md`; keep
   `references/04-anti-patterns.md` open while writing.
2. Pick the minimum extension set from the content signals in
   `references/03-composition.md`; read only those notes under
   `references/extensions/`.
3. Compose from `assets/snippets/` with parameters from
   `references/02-components.md`: link base.css, copy structure, replace
   content.
4. Run `python3 scripts/audit.py <page.html>` and
   `python3 scripts/render.py <page.html> <out-dir>`; iterate to PASS.
5. Pass `references/05-acceptance.md` gate 3 against
   `assets/examples/canonical-desktop.png`.

## Hard rules

- Link or inline `base.css` verbatim; never redefine `--pvl-*` tokens or
  reimplement components in page CSS. A new component goes into base.css with
  a version bump.
- >= 2 distinct hand-made markers per page, one on the first screen: scribble
  title, tape, sticky note, rough card, band highlight, pencil annotation.
  audit.py enforces this and prints the markers.
- One focal accent per screen; <= 1 highlight per card, <= 3 per section.
- Hover never expands or reveals layout; expand is a whole-card click with
  `aria-expanded`.
- Body >= 14px, mono >= 10.5px; `<html data-dense="true">` opts scan surfaces
  into 10.5-13px. No horizontal overflow at 390px.
- Ink `#2a2a2a` (paper `#202723`); no pure black, brand gradients, glossy
  shadows, decorative motion; emoji attach to nodes, never float in prose.
- Edit before layering: merge, compress, draw; secondary material goes behind
  a fold, whole-card expand, or the density toggle.

Identity invariants and the freedoms each extension may take live in
`references/01-grammar.md` and `references/extensions/`. Production corrections
enter `references/04-anti-patterns.md` first; the base.css header carries
the version and git history is the changelog.
