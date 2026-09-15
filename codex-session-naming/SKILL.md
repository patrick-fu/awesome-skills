---
name: codex-session-naming
description: >-
  Name user-visible top-level Codex App sessions, including controllers.
  Keep work titles aligned with progress and controller titles recognizable
  by role. Check completion claims. Excludes chats and subagents.
---

# Codex Session Naming

Choose the headline for the session's established role. Ordinary work titles
show progress; controller titles keep the coordination role recognizable.
Localize wording to the user's preferred language and preserve their names,
IDs, and terminology. A supplied name normally becomes the main line within
the appropriate format; an explicit request for a different format takes
precedence.

## Work tasks

Use this default headline:

`<state> [tags] <mandate> · <focus>`

Keep the state emoji, one or two useful scope or facet tags, and two-part
structure. The **mandate** is the overall task this session is responsible for.
Prefer a stable main line through questions, temporary detours, experiments,
and changes of approach. Refine it when the user's clarification changes how
the same task should be described. Normally switch to a new main line when the
previous task is complete and the user moves to the next; a clear replacement
or cancellation can also change it.

The **focus** describes the current bottleneck, decision, or useful next step.
Choose what helps the user understand progress without turning the title into
an activity log or adding a new approval or acceptance requirement.

## Controllers

Use `codex-session-controller` to determine whether this session has an
established global or project role, its scope, and when that responsibility
ends. Apply these role-specific defaults:

| Role | Recommended headline |
| --- | --- |
| Global | `🕹️ <scope or global controller name> · YYYY-MM-DD` |
| Project | `🗂️ <project controller name> · YYYY-MM-DD` |

Without a naming preference, use a localized Global Controller name, such as
`全局主控` or `Global Controller`; for a project, include its name and controller
role. User-supplied names such as `Mac mini 主控` or `MacBook Coordinator` fit
in the same role format. Known scope can distinguish controllers without
forcing a particular language or a literal role name.

Keep the role emoji and main line through routine checks, waits, and child
milestones. Prefer a stable `YYYY-MM-DD` start date for the second part, using
the existing controller date or known session start date. If unavailable,
omitting the date is reasonable. Ongoing work belongs in progress reports;
these titles normally retain the date instead of switching to a worker focus.

For final role completion, prefix the role title with `🏁`. After transferring
its role to an accepted successor, the outgoing controller prefixes its title
with `🔀`; the receiving controller keeps its normal role headline. Use Claim
below. Completed workers alone do not end an ongoing controller role.

## When

At entry, establish a headline from the available context or retain a suitable
existing one. During ongoing work, normally update work titles for meaningful
state or focus changes, and controller titles for role, scope, or lifecycle
changes. Routine tool calls need no title update. Use the conversation to judge
transitions; naming does not require a separate confirmation step.

## Owner

For work titles, choose the state emoji from who acts next and the actual task
state. Use this vocabulary by default:

- `🏁` mandate completed
- `☑️` an agreed checkpoint reached and work parked
- `🔀` this session handed its unfinished work to an accepted successor
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
