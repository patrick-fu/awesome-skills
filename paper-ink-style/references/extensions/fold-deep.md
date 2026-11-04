# Extension · fold-deep

Deep-evidence layer behind a dashed fold: the argument stays clean, the complete
facts stay one click away.

**Load when** the page carries evidence that a reader must be able to reach but
that would crowd the argument — experiment matrices, raw logs, request/response
dumps, full parameter tables, long citation lists.
**Skip when** there is no real secondary layer. A fold that only hides
un-edited mess is anti-pattern #4.

## What it may activate (complete allowlist)

- `.pvl-fold` (`<details>`) with its `summary`: 2px dashed
  `--pvl-pencil-light` border, radius 11px, background `rgba(255,255,255,.55)`,
  display-face 14px bold summary, ▸ / ▾ marker in `--pvl-path`.
- The core reading-layer primitives `.pvl-tech-only` plus
  `<html data-density="tech">` for a page-wide technical layer (events,
  processes, logs, experiment conditions) when the split is systematic rather
  than per-block.
- `.pvl-expand` + `aria-expanded` for whole-card expansion when the deep layer
  belongs to one card rather than to the page.
- Inside a fold, mono is the default voice for evidence: `.pvl-mono`, exact
  versions, timestamps, identifiers.

## What it must never change

- Fold is a `<details>`/click affordance; hover never opens it, and motion is
  not required.
- The summary label states what is inside ("实验矩阵与原始日志"), never
  "更多"/"详情".
- Editing comes before layering: merge duplicates, compress sentences, draw the
  relations, then fold what is genuinely secondary.

## Markers it should leave on the page

The fold is a supporting layer, so it does not carry the identity by itself —
the page around it still needs >= 2 hand-made markers (scribble title, tape,
sticky note, rough card, band highlight, pencil annotation).
