---
name: testing-plan-hard-gate
description: >-
  Before creating or modifying HTML slides, the agent must align on a testing
  plan and cannot treat slide size or delivery format as a reason to skip tests.
difficulty: medium
tags: [alignment, testing, verification]
---

## Input
"Create a 5-slide deck for a team weekly sync. It only needs to be shown to five teammates."

## Expected Output (all true)
- [ ] Does not create files, scaffold a project, or write slide code before the Pre-Build Alignment is confirmed.
- [ ] Includes a Testing plan in the Pre-Build Alignment alongside content, design, project location, build, delivery, and context decisions.
- [ ] Recommends a runnable test command and explains the required coverage across render, frame addressing, navigation, interaction isolation, layout safety, runtime errors, assets/fonts, and delivery/export checks when relevant.
- [ ] Treats testing as mandatory and gives a concrete test plan with runner, command, coverage, and rationale; mentions alternatives only if project constraints make them relevant.
- [ ] Does not recommend skipping or weakening tests.
