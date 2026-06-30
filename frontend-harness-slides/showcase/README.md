# Showcase Plan

The showcase should prove the core promise: an agent can keep changing an HTML
slide deck without quietly breaking unrelated frames.

This folder is intentionally a plan in phase 1. Do not claim screenshots or demos
exist until they are generated and checked in.

## Demo Story

1. **First draft**: start with a small multi-section deck built from the starter.
2. **Insert a scene**: add a new scene in the registry without renaming existing
   files or changing existing snapshot names.
3. **Tune animation**: change one beat's animation and show that only intended
   visual snapshots change.
4. **Catch a bad edit**: intentionally create overflowing text or a collapsed
   element and show the auditor failure.
5. **Fix and re-run**: repair the slide, rerun `npm run test:full`, and show a
   green harness.
6. **Share**: deploy or record the checked deck without adding starter-only
   export machinery.

## Assets To Add Later

- `screenshots/`: README-safe PNGs or GIFs of the demo flow.
- `example-decks/`: one complete starter-based deck used to generate showcase
  screenshots.
- `diffs/`: selected Playwright diff images that demonstrate intended and
  unintended changes.

## Acceptance Criteria For A Real Showcase

- The example deck is generated from `assets/starter/`.
- `npm run build` and `npm run test:full` pass inside the example deck.
- Screenshots in this folder match committed baselines.
- README text explains the iteration problem before showing aesthetics.
- No image claims a feature that the starter does not implement.
