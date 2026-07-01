---
name: vague-request-brief-intake
description: >-
  When the user only gives a broad slide topic, the skill should clarify
  preferences before starting implementation.
difficulty: high
tags: [brief-intake, preference-alignment]
---

## Input
"Help me make a set of slides about AI coding."

## Expected Output (all true)
- [ ] Does not immediately create files, initialize a project, choose a framework, or generate a full deck.
- [ ] Asks follow-up questions in plain text, without using a structured multiple-choice question tool.
- [ ] Explicitly confirms slide style, information density, and motion direction; it does not only ask a generic "what style do you like?"
- [ ] Covers or states assumptions for key gaps such as content angle, presentation format, duration, content mix, audience, stage, navigation, technology stack, delivery target, source material, and visual preference.
- [ ] Gives recommended defaults and credible alternatives for key points, with reasons where useful, without treating defaults as confirmed requirements.
- [ ] When the visual direction is unclear, recommends making real interactive style previews; screenshots, a local server, and three-direction previews are recommended workflow aids, not mandatory artifacts.
- [ ] For non-small decks, recommends using a context document and narrative/content-mix plan for long-running tracking without turning them into extra approval gates.
