---
name: frozen-screenshot-determinism
description: >-
  Visual capture should place the frame into a deterministic frozen or snapshot
  state first.
difficulty: high
tags: [test, determinism]
---

## Input (code audit)
"Check the freeze logic for visual snapshot tests."

## Expected Output (all true)
- [ ] Enables frozen, snapshot, test mode, or an equivalent deterministic render mechanism before visual capture.
- [ ] Stops, fixes, or stabilizes visual-affecting state from CSS animation, transition, timer, clock, random values, SVG draw-lines, media/canvas/live widgets, and similar sources.
- [ ] Captures the settled end state for the requested scene/beat, not a mid-entry-animation state.
- [ ] Does not bind the mechanism to one specific test library, constant name, or function name.
- [ ] If CSS injection is used for freezing, it should not bluntly break legitimate animation timing that the project uses for phase control.
