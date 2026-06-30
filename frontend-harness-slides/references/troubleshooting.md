# Troubleshooting

Use this when the harness or rendered deck behaves unexpectedly. The exact
commands depend on the chosen project stack.

## First Visual Baseline Fails

Many visual tools fail the first time because no approved baseline exists yet.
That is not automatically a bug. Inspect the generated screenshots, confirm they
match the intended deck, then accept them with the project's baseline update
command.

Do not accept a baseline just to make tests green. A bad baseline creates false
confidence forever.

## Text Shifts Between Machines

Most cross-machine text drift comes from fonts:

- local machine has a font that CI or another reviewer lacks
- screenshots run before web fonts finish loading
- platform font hinting differs by a few pixels

Prefer checked-in web fonts or a documented font installation path. For CJK
fonts, consider subsetting only when file size or offline rendering requires it.

## Direct Frame Link Opens The Wrong Slide

Check the stable frame address contract:

- the requested scene id exists in the registry
- the requested beat or frame index is within range
- the rendered stage exposes enough metadata for the test to confirm it landed
- redirects or route fallbacks are not stripping query/path state

The test should fail on mismatch instead of silently showing the first slide.

## Content Overflows Or Collapses

Build tools rarely catch rendered overflow. Inspect the stage geometry:

- content should live inside the fixed stage
- stage scaling should not change internal layout
- visible text and important images should have nonzero size
- decorative empty elements should be explicitly ignored by the audit

Dense source slides should usually be split into more scenes or meaningful beats
instead of shrinking text until it technically fits.

## Navigation Keys Do Not Work

First check focus. Text inputs, code editors, embedded demos, and custom widgets
may need to keep keyboard events. The deck should distinguish global navigation
from interactive regions so typing does not unexpectedly change slides and slide
navigation does not break when focus returns to the stage.

## Screenshots Are Flaky

Common causes:

- animation or spring motion has not settled
- clocks, random values, or live data change per run
- video, canvas, iframe, or web component content is not frozen
- fonts load after screenshot capture
- dev server overlays or hot reload UI appear in the frame

Add or repair frozen mode before widening visual thresholds. A high tolerance can
hide real regressions.

## Static Host Shows HTML For Missing Assets

If a missing font or image returns the app entry page, the host fallback is too
broad. Static asset directories should fail visibly on 404 instead of being
rewritten to HTML.
