---
name: codex-session-naming
description: >-
  Name user-visible top-level Codex App sessions, including controllers.
  Keep the main task stable, reflect meaningful progress, and check completion
  claims. Excludes chats and subagents.
---

# Codex Session Naming

Use this default headline for work tasks and controllers:

`<state> [tags] <mandate> · <focus>`

Keep the state emoji, one or two useful tags, and two-part structure. Write tag
content, the main task, and current focus in the user's preferred language,
preserving their names, IDs, and terminology. An explicit request for a different
format takes precedence.

For a global controller without a naming preference, use the localized form of
Global Controller as the main line. Use the project name for a project
controller; machine or project tags can distinguish known scopes. A stable
`YYYY-MM-DD` start date is a useful second part for an ongoing controller when
there is no current focus to highlight. These are recommendations, not fixed
strings or required dates.

## When

At entry, establish a headline from the available context or retain a suitable
existing one. As work progresses, normally update only the state and current
focus when they materially change. Routine tool calls need no title update.
Use the conversation to judge transitions; naming does not require a separate
confirmation step.

## Mandate

The **mandate** is the overall task this session is responsible for. Prefer a
stable main line through questions, temporary detours, experiments, and changes
of approach. Refine it when the user's clarification changes how the same task
should be described. Normally switch to a new main line when the previous task
is complete and the user moves to the next; a clear replacement or cancellation
can also change it.

For a controller, the mandate is its coordination responsibility. Routine checks
and child milestones do not end that responsibility. Use
`codex-session-controller` to determine its role, scope, and termination.

## Focus

The second part describes the current bottleneck, decision, or useful next step.
Choose what helps the user understand progress without turning the title into
an activity log. It describes existing work rather than adding a new approval
or acceptance requirement.

## Owner

Choose the state emoji from who acts next and the actual task state. Use this
vocabulary by default:

- `🏁` mandate completed
- `☑️` an agreed checkpoint reached and work parked
- `🔀` accepted successor owns unfinished work
- `🙋` user decision, authorization, or action
- `🕒` time, device, review, build, or external system
- `⛔` no valid path
- `⏸️` user pause
- `⏳` owned queue not started
- `🏃` Agent-owned active work; a self-explanatory action emoji may also fit

## Claim

For a completion, checkpoint, or handoff claim, read
[references/closure.md](references/closure.md). Judge the meaning of the claim
in any language, whether expressed with an emoji or words.

## Authority

Rename your own session; a controller may rename work sessions it owns.
The first bulk rename needs user authorization. Naming does not archive tasks
or change who owns them.
