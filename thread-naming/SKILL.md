---
name: codex-session-naming
description: >-
  Maintain titles for top-level Codex App tasks at entry, meaningful state
  changes, and turn wrap-up, including controllers. Excludes ChatGPT chats
  and subagents.
---

# Codex Session Naming

Localize to the user's language; preserve names, IDs, and terminology. Use a
supplied name as the main line; explicit format requests override defaults.

## When

At entry, meaningful state changes, and wrap-up, compare the title with the
task or established role: keep it while accurate; otherwise update it. Reuse
guidance in context. Routine tools need no update; naming needs no confirmation.

## Work tasks

`<state> [tags] <mandate> · <focus>`

Keep the state emoji, 1–2 useful scope/facet tags, and two parts.

- **Mandate — stable:** overall responsibility. Preserve through questions,
  detours, experiments, and approach changes; refine for user clarification.
  Replace for a new task after completion, or clear replacement/cancellation.
- **Focus — current:** bottleneck, decision, or useful next step. Show progress
  without an activity log or invented approval/acceptance requirement.

## Controllers

Use `codex-session-controller` to determine the established role, scope, and lifecycle.

- Global: `🕹️ <scope or controller name> · YYYY-MM-DD`
- Project: `🗂️ <project controller name> · YYYY-MM-DD`

Default to a localized controller name (`全局主控`; include the project name
for projects). Preserve user-supplied names; known scope can identify the role.

**Identity — stable:** retain role emoji, main line, and start date through
routine checks, waits, and child milestones. Reuse the existing controller date
or known session start date; omit if unknown. Report ongoing progress separately.
Change titles for role, scope, or lifecycle changes; finished workers alone
do not end the controller role.

**Exit:** prefix the role title with `🏁` for final role completion, `🔀` for an
outgoing transfer accepted by a successor. Receiving controllers keep normal
role titles. Apply Claim below.

## Owner

For workers, choose by who acts next and actual task state:

- `🏁` mandate completed
- `☑️` agreed checkpoint reached; work parked
- `🔀` unfinished work handed to an accepted successor
- `🙋` user decision, authorization, or action
- `🕒` time, device, review, build, or external system
- `⛔` no valid path
- `⏸️` user pause
- `⏳` owned queue not started
- `🏃` Agent-owned active work; a self-explanatory action emoji also fits

## Claim

For completion, checkpoint, or handoff claims (including others'), read
[references/closure.md](references/closure.md). Evaluate meaning in any language,
including words and emoji.

## Authority

Rename your own session; controllers may rename owned workers. First bulk
rename needs user authorization. Naming does not archive or transfer ownership.
