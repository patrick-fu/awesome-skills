---
name: small-deck-boundary
description: >-
  When the user wants a small, one-off, low-iteration-risk deck, the skill
  should recommend a lightweight delivery instead of a harness-backed workflow.
difficulty: medium
tags: [trigger-boundary, decision]
---

## Input
"Create a 5-slide deck for a small team weekly sync. It only needs to be shown to five teammates."

## Expected Output (all true)
- [ ] Clearly recommends that a single HTML file is enough because the deck is small, one-off, and does not justify full engineering overhead.
- [ ] Also explains that the work can move into this skill later if the user needs multiple edit rounds, animation states, or visual regression checks.
- [ ] Does not proactively create a harness-backed project or introduce the full harness workflow.
