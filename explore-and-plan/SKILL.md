---
name: explore-and-plan
description: "Turn a chosen or mostly chosen direction into an executable plan with no meaningful TBDs. Use this whenever the user asks for a plan, implementation plan, technical plan, project plan, rollout plan, or any other actionable proposal. Also use it when the user knows roughly what they want and needs it broken into concrete, ordered steps. If the request is still mainly exploratory, has too many unresolved choices, or is really asking to brainstorm, hand off to the brainstorm skill first and return once the direction is clear enough to plan."
---

# Explore And Plan

Produce an executable plan, not more exploration.

Gate first:

- if the direction is still open-ended, hand off to `brainstorm`
- if only small decisions remain, resolve them quickly and continue
- if execution depends on user judgment, ask before planning

Before writing steps, name:

- the goal and explicit non-goals
- the change surface: files, modules, systems, contracts, owners, or workflows
- important existing behavior to preserve or replace
- the acceptance condition

Then write the plan:

- split broad work into coherent tracks or phases
- order steps by dependency
- make each step concrete enough for a new executor
- tie verification to the behavior or surface it proves
- commit to decisions; do not bury meaningful `if`, `maybe`, `consider`,
  `possibly`, or `TBD` inside the plan

Reject placeholder steps such as "handle edge cases", "update UI accordingly",
"write tests", or "refactor as needed" unless they name the exact cases,
surfaces, behaviors, and verification.

Complete when the plan can be executed without rediscovering intent or making a
new design decision.
