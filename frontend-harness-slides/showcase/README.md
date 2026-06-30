# Showcase Plan

The showcase should prove the core promise: an agent can keep changing an HTML
slide deck without quietly breaking unrelated frames.

This folder is intentionally a plan. Do not claim screenshots or demos exist
until they are generated and checked in.

## Demo Story

1. **First draft**: build a small multi-section deck in any suitable web stack.
2. **Insert a scene**: add a new scene without renaming existing stable ids.
3. **Tune animation**: change one meaningful beat and show that only intended
   visual frames change.
4. **Catch a bad edit**: intentionally create overflowing text or a collapsed
   element and show the audit failure.
5. **Fix and re-run**: repair the slide, rerun the project-specific gate, and
   show a green harness.
6. **Share**: deploy or record the checked deck without adding unrelated export
   machinery.

## Assets To Add Later

- `screenshots/`: README-safe PNGs or GIFs of the demo flow.
- `example-decks/`: one complete deck used to generate showcase screenshots.
- `diffs/`: selected visual diff images that demonstrate intended and
  unintended changes.

## Acceptance Criteria For A Real Showcase

- The example deck uses stable frame addresses, a registry, a fixed stage,
  frozen mode, and structural/visual checks.
- The project-specific final gate passes.
- Screenshots in this folder match committed baselines.
- README text explains the iteration problem before showing aesthetics.
- No image claims a feature that the example deck does not implement.
