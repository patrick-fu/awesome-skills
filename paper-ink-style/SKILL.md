---
name: paper-ink-style
description: >-
  Paper-and-pencil engineering-whiteboard visual system (pencil lines, marker
  highlights, sticky notes) with progressive beat and interactive motion. Use
  when creating or restyling HTML or UI surfaces in this style (工程白板,
  inkboard).
---

# Paper Ink Style

A paper-and-pencil engineering-whiteboard style guide that defaults to a
standalone single-file HTML deliverable — pencil-line cards, marker highlights,
sticky notes and tape, hand-annotated diagrams, and restrained paper-ink motion
working together in one self-contained page. The same hand transfers to slides
or native UI via the vocabulary in `references/02-components.md`;
`assets/base.css` is its Web instance. The skill is self-contained and
advisory: compose from the vocabulary, keep the hand, and close with the
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
   (canvas, card, note, tape, highlight, annotation, density, stage, motion)
   with its options and the content signals that suit each; set the dials per
   element, and let the known-good combinations serve as examples rather than
   presets.
2. When the page explains state changes, causal flow, before/after deltas, or
   step-by-step evolution, load the matching motion guide on demand from
   `references/motion/` (`css-beats.md` for zero-JS CSS beats;
   `interactive-stage.md` for continuous scrubbed `seek(t)` stages).
3. Build one self-contained HTML file by default (`references/05-web-instance.md`):
   inline `assets/base.css` in a `<style>` block, downscale and compress
   embedded media to fit its rendered viewport slot, and compose with
   `assets/snippets/`, `references/01-grammar.md`,
   `references/02-components.md`, and `references/04-practice.md`. Multi-file
   Web deliverables or other carriers (slides, native mobile or desktop UI) are
   secondary paths when requested or required by an existing project —
   reproduce the parameters in `references/02-components.md` in that platform's
   idiom.
4. Look at `assets/examples/` — one specimen at default dials, one with every
   dial turned — for the range of the hand; then compose your own page.
5. Before delivering, run the self-check at the end of
   `references/03-composition.md`.

## Where things live

- `references/` — 01 grammar, 02 vocabulary (tokens and roles), 03
  composition and self-check, 04 practice, 05 Web & single-file HTML guide.
- `references/motion/` — progressive motion guides (`css-beats.md` for pure-CSS
  paper-ink beats, `interactive-stage.md` for continuous `seek(t)` stages).
- `assets/base.css` — the Web instance of the vocabulary (v1.5.0).
- `assets/fonts/` — LXGW WenKai Lite subsets (SIL OFL) for the handwritten voice.
- `assets/snippets/`, `assets/examples/` — Web specimens; open them in a browser.
