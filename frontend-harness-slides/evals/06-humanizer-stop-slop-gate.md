---
name: final-copy-quality-check
description: >-
  The final phase should include concrete slide-copy quality checks so vague,
  repetitive, or unsupported claims are not shipped.
difficulty: low
tags: [workflow, copy-quality]
---

## Input
"The content for all 15 slides is complete. We are now in the final delivery phase."

## Expected Output (all true)
- [ ] Checks vague adjectives, repeated wording, and unsupported claims.
- [ ] Checks whether each slide title can stand on its own.
- [ ] Checks whether speaker-led and reading-first slides use suitable copy density for their respective modes.
- [ ] Does not require calling an external humanizer or stop-slop tool; direct review against concrete quality standards is acceptable.
- [ ] If issues are found, fixes them or clearly reports the residual risk in the delivery notes instead of assuming the check passed.
