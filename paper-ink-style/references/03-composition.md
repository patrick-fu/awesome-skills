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
- **alt radius** (`.pvl-card--alt`) — neighbour variation so cards don't clone.

## Sticky note

- Translucent tints (`--pink/--blue/--green`) sit well on true white.
- Opaque tints (`--mint/--sky/--rose`) survive warm paper.
- No note is fine; a note is a human aside, not a layout slot.

## Tape

- Beige on white, warm (`--warm`) on paper, or none. Tape attaches a card to
  the canvas; one or two per page is plenty.

## Highlight

- **yellow block** (default) — the verdict phrase.
- **band** (`--band`) — underline-band emphasis inside long prose on paper.
- **lime** (`--lime`, on `.pvl-highlight`) — board tiles; it replaces yellow on
  that surface, never joins it. One focal accent per screen either way.

## Annotation

- None by default.
- Pencil annotation cards (`.pvl-annot`) plus pen-blue arrows when a realistic
  device frame (`.pvl-device`) is on the page: real UI inside in system sans,
  the hand outside explaining it.

## Density and stage

- Normal reading by default; the handwritten face carries the body.
- `<html data-dense="true">` for scan surfaces (workbench tiles, in-device
  rows): body voice switches to system sans and the sans floor drops to
  10.5–13px. Continuous prose elsewhere stays >= 14px; nothing below 10.5px.
- Scrolling page by default; a fixed stage with beat reveals (`--pvl-d`) when
  the page is presented rather than read. Stage pages keep true white and never
  go dense.

## Known-good combinations (examples, not presets)

- **Report / mechanism explainer** — paper canvas, clean or alt-rough cards,
  band highlight, warm tape, dashed fold (`.pvl-fold`) for deep evidence,
  technical layer behind the density toggle.
- **Experience walkthrough** — dotted canvas, device frame with pencil
  annotation outside, one scene at a time.
- **Workbench / ops dashboard** — paper canvas, board tiles, dense scan type,
  lime marker, pastel tags from the semantic kit, whole-card expand with
  remembered state.
- **Talk deck** — true white, fixed stage, beat reveals, takeaway lane on key
  beats, stickers on real nodes.

New combinations are welcome: set the dials the content asks for and check the
hand below.

## Self-check before delivering

Look at the page once, as a reader would:

- Can you name the current question and the verdict at a glance?
- Are the main relations drawn rather than described?
- One focal accent on this screen? Two or more hand-made marks on the page,
  one of them early?
- Does the body read in the handwritten voice, with sans only where real UI or
  scan density lives?
- At 390px: nothing overflows sideways, grids collapse, notes stay inside?
- Does it feel right? Open the specimens in `assets/examples/` and compare the hand.
