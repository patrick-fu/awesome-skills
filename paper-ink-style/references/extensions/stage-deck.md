# Extension · stage-deck

Fixed stage, beat-driven reveal, one thesis per scene: the language aimed at a
projector.

**Load when** the output is a talk deck or any HTML that is presented rather
than scrolled — one idea per screen, revealed in beats, read from the back of a
room.
**Skip when** the reader scrolls and controls the pace; a long page should use
`surface-paper` (and `fold-deep` for evidence) instead of freezing one scene.

## What it may activate (complete allowlist)

- `<html data-stage>` (or any `data-stage` marker on the stage root) to declare
  a fixed-stage page; audit exempts it from fixed-width warnings because the
  stage is sized by design.
- True-white surface (the default; do **not** load `surface-paper` or
  `surface-dot` here) so the projector keeps contrast.
- Beat timing: the core motion primitives `.pvl-reveal` / `.pvl-reveal--stamp`
  driven by `--pvl-d` delays, so the argument unfolds step by step (card in,
  stamp, marker sweep). Reduced-motion must stay honoured — base.css already
  disables it; never re-add motion in page CSS.
- `.pvl-takeaway` lane at the bottom of each teaching beat, with
  `.pvl-highlight` on the key phrase only.
- `.pvl-sticker` on real nodes/roles and `.pvl-connector` between them, so the
  diagram carries the explanation.

## What it must never change

- Type gets *bigger*, never denser: a stage scene is the one place where
  `data-dense` is wrong.
- One thesis per scene, one focal accent per screen; a scene that needs a
  second accent needs a second scene.
- Motion reveals argument state only; no decorative animation.

## Out of scope by design

This skill supplies the visual language. Scene addressing, navigation, keyboard
handling and export (web / PDF / static) belong to the consumer — keep them
minimal (`?scene=&beat=` style addressing plus a frozen mode for rendering is
enough). If the deck needs an iteration harness, that is a separate concern
from this style.

## Markers it should leave on the page

Scribble on the scene title that carries the verdict, plus tape or a sticky
note where a scene needs a human aside. A deck of clean rectangles and yellow
blocks still reads as a template.
