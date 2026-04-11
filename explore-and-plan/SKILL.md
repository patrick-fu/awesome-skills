---
name: explore-and-plan
description: >-
  Turn a chosen or mostly chosen direction into an executable plan with no
  meaningful TBDs. Use this whenever the user asks for a plan,
  implementation plan, technical plan, project plan, rollout plan, or any
  other actionable proposal. Also use it when the user knows roughly what
  they want and needs it broken into concrete, ordered steps. If the
  request is still mainly exploratory, has too many unresolved choices, or
  is really asking to brainstorm, hand off to the brainstorm skill first
  and return once the direction is clear enough to plan.
---

# Explore And Plan

The job of this skill is not to explore forever. It is to produce a plan that someone can execute without needing to rediscover the intent, architecture, or missing decisions.

## Check Readiness

Before writing a plan, decide whether the request is actually ready for planning.

Use this skill when the user has a chosen or nearly chosen direction and wants it turned into concrete execution steps.

If the request is still open-ended, mostly about comparing ideas, or missing core product or technical decisions, do not fake a plan. Hand off to `brainstorm` first, let the exploration converge, then come back and write the plan.

Some requests land in between. In that case, resolve the last important unknowns quickly, then move into planning. Do not let the conversation drift back into broad ideation once the remaining questions are small and specific.

## Scope The Plan

Before breaking work into steps, check whether the request is actually one plan or several different plans hiding inside one prompt.

If it spans multiple loosely coupled surfaces, phases, or subsystems, say so and split it into clear parts or stages before detailing execution. Do not write one giant blended plan if the work would be clearer as separate tracks.

Choose a planning scope that is coherent enough for one executor to follow without constantly switching mental models.

## Map The Change Surface

Before listing steps, identify what the plan will touch:
- files, modules, or systems likely to change
- important existing behavior that must be preserved or replaced
- interfaces, dependencies, and ownership boundaries
- the expected end state

This map does not need to be long, but it should anchor the plan in the real codebase or system rather than in abstractions.

## Resolve Remaining Decisions

Do not push unresolved choices into the body of the plan.

If there is still an `if`, `or`, `maybe`, `consider`, `possibly`, `depending on`, or `TBD` that matters to execution, resolve it before presenting the plan. Ask the user only when the decision cannot be made responsibly from context.

Good plans commit to a path, state the reasoning briefly, and make exclusions explicit so the executor does not expand scope during implementation.

## Write The Plan

The plan should be self-contained, concrete, and ordered.

Include the context an executor needs:
- what exists now that matters
- what will change
- why key choices were made
- what done looks like

Write steps that are specific enough to execute. A good step names the surface it changes, the action to take, non-obvious implementation details, and how to verify correctness when verification is not obvious.

Keep the order dependency-aware. Each step should set up the next one cleanly.

Format follows function. A small fix may only need a short numbered list. A larger feature may need sections, phases, or an architecture preface. Use the lightest structure that makes the plan unambiguous.

## Avoid Placeholder Plans

Do not write steps that only sound concrete.

These are warning signs:
- "add validation" without saying what is validated or where
- "handle edge cases" without naming the edge cases
- "update the UI accordingly" without describing the change
- "write tests for the above" without tying tests to behavior
- "refactor as needed" without naming the target structure
- "do something similar in the other module" without identifying the module

If a step could not be executed by someone new to the task, it is still a placeholder.

## Self-Review

Before presenting the plan, check:
- Is the request actually ready for planning, or should it still be in `brainstorm`?
- Does each requirement map to a concrete step or explicit exclusion?
- Have I identified the real change surface instead of writing a generic plan?
- Is there any point where the executor would still need to make a design decision?
- Are there filler steps that sound plausible but do not actually tell someone what to do?
- If someone follows this in order, will they arrive at the intended end state without needing more context?

If any answer is no, the plan is not done.
