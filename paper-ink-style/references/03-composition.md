# Composition: options per element

One hand, many dials. Each element below lists its options and the content
signals that suit each; pick per element instead of reaching for a bundled
preset. The known-good combinations at the end are examples of the dials set
well, not templates to apply.

## Canvas

- **true white** (default) — projected pages, short crisp explainers, anything
  that should feel like a whiteboard under bright light.
- **warm paper** (`data-surface="paper"`) — reading that lasts minutes: long
  reports, mechanism explainers, incident records; also ops surfaces revisited
  daily, where white glares.
- **dotted paper** (`data-surface="dot"`) — scene-by-scene walkthroughs and
  annotated tours, where the canvas should feel like a notebook page.
- Paper and dot both set the surface tokens: choose one per page.

## Card

- **rough** (`.pvl-card`, default) — the argument unit; irregular pencil radius.
- **clean** (`.pvl-card--clean`) — report blocks on paper, where the rough
  radius would fight long prose.
- **board** (`.pvl-card--board`) — tiles on surfaces that are used rather than
  read: workbenches, queues, dashboards.
- **alt radius** (`.pvl-card--alt`) — neighbour variation: adjacent cards keep their own shape.

## Sticky note

- Translucent tints (`--pink/--blue/--green`) sit well on true white.
- Opaque tints (`--mint/--sky/--rose`) survive warm paper.
- A note is a human aside; skip it when the page has no aside.

## Tape

- Beige on white, warm (`--warm`) on paper, or none. Tape attaches a card to
  the canvas; one or two per page is plenty.

## Highlight

- **yellow block** (default) — the verdict phrase.
- **band** (`--band`) — underline-band emphasis inside long prose on paper.
- **lime** (`--lime`, on `.pvl-highlight`) — board tiles, where it is the
  focal accent in place of yellow. One focal accent per screen either way.

## Annotation

- None by default.
- Pencil annotation cards (`.pvl-annot`) plus pen-blue arrows when a realistic
  device frame (`.pvl-device`) is on the page: real UI inside in system sans,
  the hand outside explaining it.

## Illustrations

- Standard diagrams and emoji stickers by default (zero JS).
- Optional clumsy MS Paint pixel doodles (`.pvl-doodle`, copied on demand from
  `assets/snippets/scribble-canvas.html`) inside a card when a conceptual
  metaphor, incident cartoon, or humorous character makes the point faster than
  another box diagram. Keep page prose and card chrome clean so the rough
  doodle reads as intentional contrast.

## Density and stage

- Normal reading by default; the handwritten face carries the body.
- `<html data-dense="true">` for scan surfaces (workbench tiles, in-device
  rows): body voice switches to system sans and the sans floor drops to
  10.5–13px. Continuous prose elsewhere stays >= 14px; 10.5px is the floor
  everywhere.
- Scrolling page by default; a fixed stage with beat reveals (`--pvl-d`) when
  the page is presented rather than read. Stage pages stay true white at
  reading-large type.

## Motion (Progressive Routing)

Whenever a page explains **state changes, causal flow, before/after comparison,
or step-by-step evolution**, bring the whiteboard alive with the matching motion
tier below instead of stopping at static walls of 3-column `.pvl-flow` boxes.
Load only the reference file the chosen tier needs:

| Content signal | Motion dial | Load on demand |
| --- | --- | --- |
| Static reference note, checklist, or calm prose with no state progression | `still` (zero JS, no beat animations) | None needed |
| Step-by-step argument unfolding, verdict sweep, label/state swap, directional flow, or native expandable evidence folds | `beat-css` (pure CSS, zero JS via `base.css` v1.4.0) | [motion/css-beats.md](motion/css-beats.md) |
| Queues, backpressure, cache eviction, before/after numeric deltas, layered event history, or scrubbed X-Ray annotation comparison | `scrubbed-25d` (stateless `seek(t)` lab via `assets/snippets/motion-stage.html`) | [motion/interactive-stage.md](motion/interactive-stage.md) |

Stay strictly inside the hand-drawn paper-ink whiteboard aesthetic across every
tier—never introduce dark neon, glassmorphism, or SVG Gooey.

## Known-good combinations (examples, not presets)

- **Report / mechanism explainer** — paper canvas, clean or alt-rough cards,
  band highlight, warm tape, dashed fold (`.pvl-fold`) for deep evidence,
  `beat-css` or `scrubbed-25d` for the core mechanism, technical layer behind
  the density toggle.
- **Experience walkthrough** — dotted canvas, device frame with pencil
  annotation outside, one scene at a time.
- **Workbench / ops dashboard** — paper canvas, board tiles, dense scan type,
  lime marker, pastel tags from the semantic kit, whole-card expand with
  remembered state.
- **Talk deck** — true white, fixed stage, `beat-css` reveals, takeaway lane on
  key beats, stickers on real nodes.

New combinations are welcome: set the dials the content asks for and check the
hand below.

## Self-check before delivering

Look at the page once, as a reader would:

- Can you name the current question and the verdict at a glance?
- Are the main relations drawn (or evolved in place) rather than buried in prose?
- One focal accent on this screen? Two or more hand-made marks on the page,
  one of them early?
- Does the body read in the handwritten voice, with sans only where real UI or
  scan density lives?
- At 390px: everything fits — grids collapse, tables scroll inside their
  card, notes stay inside, and `.pvl-camera` resets to identity with zero
  horizontal overflow?
- Under `prefers-reduced-motion: reduce`: animations/transitions disable
  cleanly and the page remains legible as a settled frame?
- Does it feel right? Open the specimens in `assets/examples/` and compare the hand.
