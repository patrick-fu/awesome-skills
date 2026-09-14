---
name: codex-session-naming
description: >-
  Apply the session title lifecycle to every user-visible top-level Codex App
  session. Keep a stable sidebar headline aligned with user intent,
  mandate, gate, and owner, and audit closure claims.
  Includes controllers; excludes chats and subagents.
---

# Codex Session Naming

A user-visible top-level session owes one **mandate**. Its title is a stable
**headline**. Honor the user's chosen name, language, and format. Otherwise,
choose a concise title in the conversation's language. A recommended work-task
format is:

`<state> [tags] <mandate> · <gate>`

Include only useful parts; tags, when useful, are at most two searchable scope
or facet labels. Keep user phrasing, IDs, and entities.
For a controller, prefer a stable scope-and-role headline, such as `MacBook 主控`
or `Billing Coordinator`.
With a fixed user-selected name, report changing status in the conversation.

## When

1. **Entry:** before the first response, preserve a suitable existing headline
   or write one from available evidence. With no usable mandate, describe that
   the task is awaiting a goal in the chosen language.
2. **Semantic transition:** before the response that ends a turn, rewrite
   when the user requests it or the headline is false; otherwise leave it.
   Judge from user intent, delivered or verified work, and actual blockers—not
   recency or runtime alone.
3. **Closure:** decide completion and checkpoint claims under Claim.

## Mandate

The **mandate** is the final boundary this session still owes, not the
current action or method. An explicit user correction may **revise** that
same boundary. While the current boundary is still owed, new work is
evaluated under Gate, not as a new mandate. It ends only when **revoked**
(explicitly released), **discharged** (final closure passes), or
**transferred** (an accepted successor owns it). After it ends, a new
mandate starts only on evidence that this session now owes another final
boundary. With no new mandate, the closing headline keeps the old one.

A controller's mandate is its ongoing coordination scope. Routine checks and
child milestones do not end that mandate. Role authorization, scope, and
termination conditions belong to `codex-session-controller`.

## Gate

The **gate** is the mandate's one bottleneck: the hold or step that first
decides whether the mandate can advance. Keep it while it remains the
bottleneck; with no hold, use the decisive next step. Activity outside the
bottleneck does not enter the headline.

## Owner

The **owner** is who must take the next step through the chosen gate, and
selects the state. These markers are optional; their meanings apply when used:

- `🏁` mandate discharged
- `☑️` checkpoint passed and parked
- `🔀` accepted successor owns unfinished work
- `🙋` user decision, authorization, or action
- `🕒` time, device, review, build, or external system
- `⛔` no valid path
- `⏸️` user pause
- `⏳` owned queue not started
- `🏃` Agent-owned active work; its working Agent may use one self-explanatory
  emoji for its current action. Fall back to `🏃`.

Turns and tool calls are not checkpoints; ordinary progress belongs in the
transcript or report.

## Claim

Completion or checkpoint wording, including `🏁` and `☑️`, claims that the
mandate is discharged or parked. Read [references/closure.md](references/closure.md)
before writing, accepting, or challenging such a claim, regardless of its
language or format.

## Authority

Rename your own session; a controller may rename work sessions it owns.
The first bulk rename needs user authorization. A handoff claim, including `🔀`,
needs an accepted successor. Naming never archives or deletes.
