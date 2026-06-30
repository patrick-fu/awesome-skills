# Component Libraries

Use project conventions first. Do not introduce a library only because this skill
mentions a category.

## Decision Tree

| Need | Prefer | Avoid |
|---|---|---|
| Icons | The icon set already used by the project; otherwise a small tree-shakeable SVG icon library. | Font packs or whole icon fonts for a few symbols. |
| Charts | The lightest charting approach that renders readable labels and can be frozen for tests. | A heavy dashboard library when the deck only needs one static chart. |
| Code blocks | Build-time or pre-rendered syntax highlighting. | Runtime highlighters that block render or produce nondeterministic markup. |
| Diagrams | Text-to-SVG or checked-in static SVG when the diagram is stable. | Embedded whiteboard/canvas tools that produce nondeterministic screenshots. |
| Tables | Plain HTML tables or a headless table utility for dense data. | Full UI suites for a single static table. |

## Harness Notes

- Prefer DOM or SVG output for text, labels, and accessibility.
- Disable or freeze library animations during visual checks.
- Mask only genuinely nondeterministic regions; do not mask the main content the
  user needs to inspect.
- Keep generated IDs, timestamps, random colors, and live data out of visual
  baselines unless they are intentionally part of the slide.
