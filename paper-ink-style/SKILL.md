---
name: paper-ink-style
description: >-
  Paper-and-pencil engineering-whiteboard visual style for HTML: rough
  pencil-line cards, marker-yellow highlights, sticky notes and tape,
  hand-annotated diagrams. Use when building or restyling HTML in this style
  (工程白板, inkboard).
---

# Paper Ink Style

A style guide, not a template and not a linter: a paper-and-pencil engineering
whiteboard where pencil-line cards, marker highlights, sticky notes and tape,
and hand-annotated diagrams lead a reader through a complex system. The
vocabulary lives in `assets/base.css`; the judgment lives here and in
`references/`. Nothing in this skill is a gate — read it as guidance and keep
the hand.

## The hand

- Pencil-line ink in three alphas, never pure black; shadows are small hard
  offsets or soft paper lifts.
- One focal marker accent per screen; the highlight sits on the phrase that
  carries the verdict.
- The handwritten face is the reading voice: titles, annotations and body all
  speak it. System sans appears only inside realistic device frames and on
  dense scan surfaces; mono speaks for precise objects (versions, files, logs).
- Titles are verdicts or questions; open with a TL;DR stamp card; diagrams carry
  the argument and prose carries verdicts, conditions, key facts; close each
  teaching beat with a takeaway lane.
- Leave hand-made marks on the page — scribble underline, tape, sticky note,
  rough card, band highlight, pencil annotation; two or more, one of them early,
  is what keeps a page from reading as a generic report.
- Emoji are semantic objects on nodes, roles, files, incidents; never floating
  in prose.

## Working with it

1. Look at the content first. `references/03-composition.md` lists each element
   (canvas, card, note, tape, highlight, annotation, density, stage) with its
   options and the content signals that suit each; pick per element, and let
   known-good combinations serve as examples rather than presets.
2. Deliver a single HTML file by default: inline `base.css` in a `<style>`
   block, embed the font subsets when their size is acceptable, otherwise let
   the system Kai fallbacks carry the handwritten voice. Split into multiple
   files only when the reader asks or the deliverable genuinely needs it.
3. Compose from the vocabulary: `references/02-components.md` for parameters,
   `assets/snippets/` as specimens — copy structure, replace content, keep the
   classes. `references/01-grammar.md` is how this style leads a reader; keep
   `references/04-anti-patterns.md` in mind while writing.
4. Before delivering, look at the page once more against the self-check at the
   end of `references/03-composition.md`. If you want eyes on it,
   `scripts/render.py <page.html> <out-dir>` screenshots 1440 and 390 widths.

## Where things live

- `assets/base.css` — the vocabulary: tokens and components (v1.3.0).
- `assets/snippets/`, `assets/examples/` (+ renders), `assets/fonts/` (LXGW
  WenKai Lite subsets, SIL OFL).
- `references/` — 01 grammar, 02 components, 03 composition and self-check,
  04 anti-patterns, 05 provenance.
- `scripts/render.py` — optional screenshots and a truthful 390px measure.
