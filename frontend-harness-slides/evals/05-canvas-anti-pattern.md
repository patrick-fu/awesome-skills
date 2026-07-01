---
name: whole-slide-canvas-anti-pattern
description: >-
  Static full-slide content should not be drawn with canvas.
difficulty: medium
tags: [anti-pattern, implementation]
---

## Input
"Generate one slide with a colorful gradient background, a few preset decorative geometric blocks, and a large title in the center."

## Expected Output (all true)
- [ ] Decorative geometric shapes use DOM/SVG, not canvas.
- [ ] The background uses CSS linear-gradient, not canvas.
- [ ] Titles and audience-visible copy remain DOM/SVG text or equivalent inspectable text, not text drawn into a full-slide canvas.
- [ ] If canvas is used, it is limited to non-critical local visual layers that can be frozen or stabilized.
