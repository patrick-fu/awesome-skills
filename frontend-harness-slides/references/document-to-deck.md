# Document To Deck

Use this when the source material is a long article, memo, PRD, transcript,
report, or outline. Do not paste sections onto slides one by one. First rebuild
the story.

## Minimal Process

1. Extract the core claim, audience, and desired outcome.
2. Identify 3 to 5 sections that create a narrative arc.
3. Decide whether the deck is speaker-led, reading-first, or hybrid.
4. Estimate slide count from delivery context, not source length.
5. Convert each section into scene titles and one takeaway per scene.
6. Put dense evidence, examples, or scripts outside the slide surface unless the
   deck is explicitly reading-first.

For non-trivial decks, do not start scene implementation before producing a
registry draft. This is a planning gate, not a polished deliverable.

## Heuristics

- A speaker-led technical talk often needs fewer words and more pacing beats than
  the source document suggests.
- A reading-first deck can carry more detail, but each page still needs a clear
  title and visible hierarchy.
- If one source section contains several claims, split it into multiple scenes
  instead of shrinking text.
- Preserve concrete numbers, names, and examples. Remove duplicated setup.

## Output Shape

Before building scenes, produce a registry draft with separate visible copy,
speaker intent, and internal constraints:

```text
id: opening
title: Why this matters now
visible_copy: The old workflow is no longer the bottleneck.
speaker_intent: Explain that the audience's pain is coordination, not typing.
beats: 3
visual_idea: robot, keyboard, and microphone converge into one workflow
mode: speaker-led
source: paragraphs 1-4
internal_constraints: 40-minute talk, low text density, 1920x1080 stage
```

`visible_copy` is the text intended for the audience on the slide surface. Keep
planning metadata out of it. Duration, audience, density, style, stage size,
deployment target, navigation, implementation notes, and review instructions are
internal constraints unless the user explicitly asks to show them.

Ask only the questions that materially change the deck direction.
