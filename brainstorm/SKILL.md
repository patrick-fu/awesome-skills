---
name: brainstorm
description: >
  Explore ideas, clarify goals, and help the user narrow down directions before planning or coding.
  Use this whenever the user proposes a new feature or idea, asks "what do you think about X",
  says "I'm thinking of building Y", wants to compare approaches, asks how to approach a problem,
  or seems to be exploring rather than ready to execute. Also use it when the user says
  "brainstorm", "let's think about this", "what's the best way to...", or any time the right
  next step is to clarify the problem and converge on a direction, not to write code yet.
---

# Brainstorm

Before anything else, ask. Don't jump to solutions or implementation.

The goal is to draw out what the user actually means, uncover what they have not said yet, and help them converge on a direction. Think of this as Socratic dialogue with momentum: use questions to guide the thinking, but do not leave the user wandering in options forever.

## Start With Context

Before asking, absorb the context that already exists in the conversation, codebase, docs, and project state. Do not ask for information you can already infer or look up directly.

## Guide The Conversation

First figure out where the user is: still exploring, partly narrowed down, or close to a decision.

If the problem is too large, shrink it to the first key subproblem before going deeper. A good brainstorm usually moves one important decision at a time, not five in parallel.

Prefer low-friction questions. Good defaults are:
- binary or multiple-choice questions
- priority questions
- constraint checks
- edge-case probes

Do not dump a long list of questions up front. Ask the single most useful next question, then adapt based on the answer.

## Help Converge

Do not just expand the option space. Once the picture is clear enough, organize the discussion into 2-3 plausible directions and recommend one. Explain the recommendation briefly so the user can react to the reasoning, not just the conclusion.

If the user's answer is vague, go deeper. If the important decisions are already clear, stop probing and move the discussion toward a choice.

Useful prompts to keep in mind:
- What is the real goal behind this?
- What constraints or failure cases change the answer?
- What assumption might be wrong?
- Is there a simpler version worth choosing first?
- What decision still needs to be made before planning?

## Optional Visual Aids

When a problem is easier to understand visually than through text alone, propose lightweight visual aids. Only enter this branch after the user agrees.

Visual aids should help the user understand or compare one key decision at a time. They are for clarification and convergence, not for polished implementation. If you need more guidance, read `references/visual-aids.md`.

## Know When To Hand Off

Do not slide into implementation while the direction is still unclear.

Once the core direction, constraints, and exclusions are clear, summarize what you understand and hand off naturally to `explore-and-plan` so the chosen direction can become an executable plan.
