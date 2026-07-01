---
name: editable-key-events-not-swallowed
description: >-
  Generated navigation logic should not accidentally trigger slide navigation
  while editable or custom interactive areas are focused.
difficulty: high
tags: [bug-free, implementation]
---

## Input (code audit)
"Audit the generated deck's keyboard navigation event handling."

## Expected Output (all true)
- [ ] Global navigation checks editable, focusable, and custom interactive area guards before acting, or uses an equivalent event-routing mechanism.
- [ ] When an editable element is focused, Space/Arrow does not change the current scene or beat.
- [ ] When the Stage or slide surface is focused, Space/Arrow still advances navigation by one expected step.
- [ ] Repeated keydown does not accidentally skip multiple beats unless the project explicitly supports that behavior.
- [ ] If tap, touch, click, or pointer navigation is supported, one physical input does not advance multiple steps because duplicate events fire.
- [ ] Custom interactive areas have an explicit event isolation boundary, not only reliance on one framework's synthetic event bubbling.
