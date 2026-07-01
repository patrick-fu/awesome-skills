---
name: stage-no-responsive-breakpoints
description: >-
  Generated Stage internals should not depend on viewport-responsive
  breakpoints.
difficulty: medium
tags: [anti-pattern, implementation]
---

## Input (code snippet context)
"Create one slide with text on the left and an app screenshot on the right: the left side has three bullet lines (title, subtitle, and explanation), the right side has a 16:9 phone mockup, and the whole slide is 1920x1080."

## Expected Output (all true)
- [ ] Stage-internal content layout does not rely on viewport/container breakpoints or equivalent utility breakpoints for reflow.
- [ ] The Stage shell may respond to the viewport for whole-stage scaling, but it does not change the slide's internal composition semantics.
- [ ] Uses fixed stage coordinates, stage-relative fixed-ratio layout, or an equivalent fixed-stage design system.
- [ ] Stage, scene, and beat elements expose stable attributes, roles, or equivalent selectors for auditability.
