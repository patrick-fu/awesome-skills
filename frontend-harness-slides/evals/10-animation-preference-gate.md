---
name: animation-preference-gate
description: >-
  When the user has not specified animation preferences, the skill should
  recommend directions without adopting one unilaterally.
difficulty: high
tags: [brief-intake, animation, preference-alignment]
---

## Input
"Help me make a set of AI coding slides. I want them to feel premium, like a product launch."

## Expected Output (all true)
- [ ] Does not immediately create files, initialize a project, choose a framework, or generate a full deck.
- [ ] Even when the user asks for a premium product-launch feel, still confirms key intake points in plain text: style, density, motion, stage, navigation, technology, delivery, and related choices.
- [ ] Recommends keynote/product-launch-style semantic beat motion such as transitions, reveals, promotes, replaces, de-emphasis, final takeaways, or equivalent concepts without requiring fixed wording.
- [ ] Also offers calmer or more static motion as optional directions, without hard-coding the choice set.
- [ ] Does not treat recommended motion as a final implementation requirement before the user confirms it.
