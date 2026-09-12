---
name: slide-surface-boundary
description: >-
  Duration, style, stage, and deployment details from the user brief should not
  be written onto the slide canvas by default.
difficulty: medium
tags: [copy-boundary, registry, planning-metadata]
---

## Input
"Turn this AI coding material into slides for a 40-minute live talk. Use low text density, a black/white/gray hand-drawn emoji style, 1920x1080, mobile swipe support, and deploy it to Vercel at the end."

## Expected Output (all true)
- [ ] Uses the supplied constraints instead of re-asking style, density, stage, navigation, or delivery; inspects source first and asks only about remaining unresolved decisions that materially affect the result or scope, such as a missing `deck root`.
- [ ] If it produces a registry draft, the draft includes `visible_copy`, `speaker_intent`, `beats`, and `visual_idea`, while duration, stage, touch interaction, deployment, and similar items stay in internal constraints.
- [ ] Clearly explains that `40 minutes`, `1920x1080`, `Vercel`, and `mobile swipe` are planning or implementation details and should not be written into slide titles, subtitles, or visible body copy by default.
- [ ] `visible_copy` only contains titles, short phrases, or labels that the audience should actually see.
- [ ] Still preserves the user's style direction: low text density, black/white/gray hand-drawn visuals, and emoji visual elements; motion may be a stated recommendation that fits the given style, not a blocking confirmation.
