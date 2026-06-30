# Showcase Plan

The showcase should prove the core promise: an agent can keep changing an HTML
slide deck without quietly breaking unrelated frames.

This folder is intentionally a plan. Do not claim screenshots or demos exist
until they are generated and checked in.

## Demo Story

1. **Plan**: align content orientation, presentation format, duration, content
   mix, style, density, technology stack, and delivery target before building.
2. **Track context**: create/update an external context document with the
   decisions, narrative plan, registry, theme contract, verification, and
   delivery status.
3. **Preview style**: show three interactive real-slide previews in contrasting
   visual directions when the style is not already settled, with screenshots and
   a local server.
4. **First draft**: build a small multi-section deck in any suitable web stack.
5. **Insert a scene**: add a new scene without renaming existing stable ids.
6. **Tune animation**: change one meaningful beat and show that only intended
   visual frames change.
7. **Catch a bad edit**: intentionally create overflowing text or a collapsed
   element and show the audit failure.
8. **Fix and re-run**: repair the slide, rerun the project-specific gate, and
   show a green harness.
9. **Share**: deploy or record the checked deck, run production smoke when
   hosted, and avoid unrelated export machinery.

## Assets To Add Later

- `screenshots/`: README-safe PNGs or GIFs of the demo flow.
- `example-decks/`: one complete deck used to generate showcase screenshots.
- `diffs/`: selected visual diff images that demonstrate intended and
  unintended changes.

## Acceptance Criteria For A Real Showcase

- The example deck uses stable frame addresses, a registry, a fixed stage,
  frozen mode, keyboard/touch navigation, and structural/visual checks.
- The showcase includes a context document and selected theme contract for the
  non-trivial deck.
- The README or handoff note records the production URL or exported artifact
  when the demo is shipped.
- The project-specific final gate passes.
- Screenshots in this folder match committed baselines.
- README text explains the iteration problem before showing aesthetics.
- No image claims a feature that the example deck does not implement.
