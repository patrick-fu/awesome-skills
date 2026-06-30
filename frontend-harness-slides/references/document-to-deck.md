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

## Heuristics

- A speaker-led technical talk often needs fewer words and more pacing beats than
  the source document suggests.
- A reading-first deck can carry more detail, but each page still needs a clear
  title and visible hierarchy.
- If one source section contains several claims, split it into multiple scenes
  instead of shrinking text.
- Preserve concrete numbers, names, and examples. Remove duplicated setup.

## Output Shape

Before building scenes, produce a registry draft:

```text
id: opening
title: Why this matters now
takeaway: The old workflow is no longer the bottleneck.
mode: speaker-led
source: paragraphs 1-4
```

Ask only the questions that materially change the deck direction.
