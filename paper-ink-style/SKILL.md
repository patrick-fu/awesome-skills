---
name: paper-ink-style
description: >-
  Paper-and-pencil engineering-whiteboard visual style: rough pencil-line
  cards, marker-yellow highlights, sticky notes and tape, hand-annotated
  diagrams. Use when applying this personal style to any UI surface
  (工程白板, inkboard).
---

# Paper Ink Style

A style guide for any carrier: the same hand works in HTML, in slides, in
native mobile or desktop UI — pencil-line cards, marker highlights, sticky
notes and tape, diagrams that carry the argument. The platform-neutral
vocabulary (values and roles) lives in `references/02-components.md`;
`assets/base.css` is the worked Web instance of it. The skill is self-contained
and advisory: compose from the vocabulary, keep the hand, and close with the
self-check at the end of `references/03-composition.md`.

## The hand

- Pencil-line ink in three alphas (`#2a2a2a` on white, `#202723` on paper);
  shadows are small hard offsets or soft paper lifts.
- One focal marker accent per screen; the highlight sits on the phrase that
  carries the verdict.
- The handwritten face is the reading voice: titles, annotations and body all
  speak it. A neutral system sans appears only inside realistic device frames
  and on dense scan surfaces; mono speaks for precise objects (versions,
  files, logs).
- Titles are verdicts or questions; open with a TL;DR stamp card; diagrams carry
  the argument and prose carries verdicts, conditions, key facts; close each
  teaching beat with a takeaway lane.
- Leave hand-made marks on the page — scribble underline, tape, sticky note,
  rough card, band highlight, pencil annotation; two or more, one of them early,
  is what keeps a page from reading as a generic report.
- Emoji attach to nodes, roles, files, tools, incidents.

## Working with it

1. Look at the content first. `references/03-composition.md` lists each element
   (canvas, card, note, tape, highlight, annotation, density, stage) with its
   options and the content signals that suit each; set the dials per element,
   and let the known-good combinations serve as examples rather than presets.
2. Compose from the vocabulary: parameters and roles in
   `references/02-components.md`, grammar in `references/01-grammar.md`, the
   practice in `references/04-practice.md`. On the Web,
   `assets/base.css` plus `assets/snippets/` are the worked instance and its
   specimens (`references/05-web-instance.md`); on any other carrier reproduce
   the parameters in that platform's idiom. On the Web, one HTML file is the
   default deliverable.
3. Look at `assets/examples/` — four specimens set to different dials — for
   the range of the hand; then compose your own page.
4. Before delivering, run the self-check at the end of
   `references/03-composition.md`.

## Where things live

- `references/` — 01 grammar, 02 vocabulary (platform-neutral), 03 composition
  and self-check, 04 practice, 05 web instance.
- `assets/base.css` — the Web instance of the vocabulary (v1.3.0).
- `assets/fonts/` — LXGW WenKai Lite subsets (SIL OFL) for the handwritten voice.
- `assets/snippets/`, `assets/examples/` (+ renders) — Web specimens.
