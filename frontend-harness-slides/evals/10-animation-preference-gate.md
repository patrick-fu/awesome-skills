---
name: animation-preference-gate
description: >-
  When the user has not specified animation preferences, the skill should
  recommend directions that fit the given feel without re-asking already stated
  constraints.
difficulty: high
tags: [brief-intake, animation, preference-alignment]
---

## Input
"Help me make a set of AI coding slides. I want them to feel premium, like a product launch."

## Expected Output (all true)
- [ ] Does not immediately create files, initialize a project, choose a framework, or generate a full deck.
- [ ] Uses the premium product-launch direction instead of re-asking style from scratch, and asks only remaining unresolved decisions that materially affect the result or scope.
- [ ] Does not use `AskUserQuestion`, `AskQuestion`, `request_user_input`, or any structured single-choice, multiple-choice, or form-style question tool.
- [ ] Provides at least five style recommendations or refinements with brief reasons, rather than treating "premium product launch" as a fully specified visual system.
- [ ] Recommends keynote/product-launch-style semantic beat motion such as transitions, reveals, promotes, replaces, de-emphasis, final takeaways, or equivalent concepts without requiring fixed wording.
- [ ] Also offers calmer or more static motion as optional directions, without hard-coding the choice set.
- [ ] Does not block implementation on confirming stage, navigation, technology, or delivery when defaults would not change result or scope.
