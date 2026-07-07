---
name: soft-grilling-alignment
description: >-
  When a slide request is underspecified, the skill should use a focused
  grilling-style alignment before implementation without becoming adversarial or
  form-like.
difficulty: high
tags: [brief-intake, preference-alignment, soft-grilling]
---

## Input
"Make me an HTML slide deck from the notes in this repo. Make it look good."

## Expected Output (all true)
- [ ] Does not immediately create files, initialize a project, start a dev server, or build slides.
- [ ] Says it will inspect discoverable repo/source facts before asking generic questions, or reports the inferred facts if inspection has already happened.
- [ ] Challenges the vague brief by naming the highest-impact missing decision first, such as audience, outcome, content boundary, presentation mode, style, or delivery target.
- [ ] Provides a recommended answer with rationale and impact so the user can confirm or correct a concrete direction.
- [ ] Uses normal chat text only, without `AskUserQuestion`, `AskQuestion`, `request_user_input`, or any structured single-choice, multiple-choice, or form-style question tool.
- [ ] Does not dump a long unordered checklist of unrelated questions.
- [ ] May group related low-risk confirmations, but keeps the grouping ordered by decision dependency.
