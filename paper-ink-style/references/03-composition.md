# Composition: one core, pluggable extensions

There is no menu of styles here. The **core** is always on: base.css tokens and
components, and the grammar and identity invariants in `01-grammar.md`. An **extension** is a bounded subset of those same components plus
an explicit allowlist of overrides, loaded only when the content asks for it.
Two pages that load different extensions must still look like the same hand.

Extensions are documentation-level modules, not extra stylesheets. Everything
they activate already lives in `assets/base.css`; an extension tells you *when*
to reach for it and *how far* you may go.

## Step 1 — read the content, then pick the minimum set

| Signal in the content | Extension | File |
|---|---|---|
| read for minutes, evidence-heavy, long scroll | warm paper surface | `extensions/surface-paper.md` |
| explaining what a user sees on a real screen | device frame + pencil annotation | `extensions/device-real.md` |
| scene-by-scene walkthrough, notebook canvas | dotted paper | `extensions/surface-dot.md` |
| revisited daily, action-first, 6–12 stable tiles | board tiles + dense scan type + lime marker | `extensions/card-board.md` |
| secondary evidence that would crowd the argument | dashed fold / tech layer | `extensions/fold-deep.md` |
| projected, one thesis per beat, revealed in steps | fixed stage + beat motion | `extensions/stage-deck.md` |

Conflicts: `surface-paper` and `surface-dot` both set `--pvl-surface` — pick
one. `stage-deck` keeps true white and never takes `data-dense`.
Everything else composes freely (`surface-paper` + `card-board`,
`surface-dot` + `device-real`, `surface-paper` + `fold-deep`, …).

## Step 2 — density is a dial, not a mode

Roughly, per screen: 1 thesis (stage) · 1 scene (walkthrough) · 3–5 cards
(report) · 6–12 stable tiles (workbench). Only one switch is declared:
`<html data-dense="true">`, which lowers the sans floor to 10.5–13px for scan
surfaces and in-device system UI. Continuous reading prose stays >= 14px
everywhere; nothing ever goes below 10.5px.

## Step 3 — hold the identity, whatever you composed

- Load the fewest extensions that serve the content. Every extension you add
  is surface area for drift.
- **>= 2 distinct hand-made markers must appear on the page**, and at least one
  of them on the first screen: scribble title, tape, sticky note, rough card,
  band highlight, pencil annotation. `audit.py` fails a page that has fewer.
  Stickers and plain yellow highlights do not count toward this number — they
  are core, not craft.
- Titles stay verdicts, the TL;DR callout stays first, diagrams still carry the
  explanation, and each teaching beat still ends in a takeaway lane.

## Known-good compositions (examples, not a closed set)

- **Report / mechanism explainer** — `surface-paper` + `fold-deep`; clean or
  alt-rough cards, band highlight on the verdict, warm tape, anchors for long
  scroll, technical layer behind the density toggle, evidence in mono. Length is
  fine; crowding is not — merge related facts into one card.
- **Experience walkthrough** — `surface-dot` + `device-real`; narrow column,
  one scene at a time, real UI inside the frame in system sans, pencil
  annotation cards and pen-blue arrows outside. Verified 2026-11-03.
- **Workbench / ops dashboard** — `surface-paper` + `card-board` (+ `fold-deep`
  for deep rows); `data-dense="true"`, board tiles, lime marker, pastel tags
  from the semantic kit, whole-card expand with remembered state.
  `[correction: whole-card click, no hover]` Verified 2026-11-03.
- **Talk deck** — `stage-deck` alone; true white, beat reveal via `--pvl-d`,
  takeaway lane on key beats, stickers on real nodes.

## Inventing a new combination

Allowed and expected — the four recipes above are field-tested starting points,
not a taxonomy. Before shipping a new combination, check it the way you would
check any page: strip the content down to boxes and lines, then ask whether it
still looks like the same hand (pencil line, one focal accent, three type
voices, >= 2 hand-made markers). If a new need recurs, the component goes into
`base.css` and the recipe gets written up as an extension note — never as page
CSS.
