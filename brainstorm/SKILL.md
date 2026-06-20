---
name: brainstorm
description: "Explore ideas, clarify goals, and help the user narrow down directions before planning or coding. Use this whenever the user proposes a new feature or idea, asks \"what do you think about X\", says \"I'm thinking of building Y\", wants to compare approaches, asks how to approach a problem, or seems to be exploring rather than ready to execute. Also use it when the user says \"brainstorm\", \"let's think about this\", \"what's the best way to...\", or any time the right next step is to clarify the problem and converge on a direction, not to write code yet."
---

# Brainstorm

Run a tight convergence conversation.

First absorb available context. Ask only for what changes the direction.

Do:

- keep the work in exploration until the problem, audience, constraints, and
  first useful slice are clear
- ask one high-value question at a time, or a small grouped set when the answers
  are tightly related
- shrink oversized ideas to the first key decision or smallest useful version
- compare 2-3 viable directions when enough context exists, then recommend one
  with brief reasoning
- use lightweight visual aids only when they clarify a decision; read
  `references/visual-aids.md` only for that branch
- summarize the converged direction, explicit exclusions, and remaining risks
  before handing off to `explore-and-plan`

Do not:

- write an implementation plan while core choices are still open
- dump a long questionnaire
- expand options after the user is ready to choose
- create polished designs, code, specs, or roadmaps during brainstorming

Complete when the user has a clear direction or the next unresolved decision is
explicit.
