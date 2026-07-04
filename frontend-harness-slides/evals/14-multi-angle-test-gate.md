---
name: multi-angle-test-gate
description: >-
  When an agent creates HTML slides, it must create a sufficient multi-angle
  test suite instead of satisfying the requirement with one shallow check.
difficulty: medium
tags: [testing, tdd, verification]
---

## Input
"Make an interactive HTML slide demo in React/Vite. Keep it direct."

## Expected Output (all true)
- [ ] Creates or proposes a runnable test setup as part of the slide work.
- [ ] Covers render and visible stage content.
- [ ] Covers frame addressing or route/state behavior when the chosen implementation has addressable states.
- [ ] Covers keyboard, click/touch, or navigator behavior.
- [ ] Covers interaction isolation when local interactive elements exist.
- [ ] Covers layout overflow, collapsed content, and console/runtime errors.
- [ ] Covers asset/font loading and build/export/deployment behavior when relevant.
- [ ] Does not satisfy the test requirement with one shallow happy-path case.
