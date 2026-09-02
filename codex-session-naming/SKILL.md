---
name: codex-session-naming
description: >-
  Apply the session title lifecycle to every user-visible top-level Codex App
  session. Write a stable sidebar headline at entry, rewrite it only when its
  mandate, gate, or owner makes it false, and audit closure claims.
  Excludes chats, subagents, and controller-role titles.
---

# Codex Session Naming

A user-visible top-level domain work session owes one **mandate**. The
session title is the **headline**:

`<state> [tags] <mandate> · <gate>`

Tags are at most two searchable scope or facet labels. Keep user phrasing,
IDs, and entities. Controller-role titles belong to
`codex-session-controller`.

## When

1. **Entry:** before the first response, write the headline from available
   evidence. With no usable mandate, use `🙋 新会话 · 等待目标`.
2. **Semantic transition:** before the response that ends a turn, rewrite
   only when the headline is false; if true, leave it. Judge from user
   intent, delivered or verified work, and actual blockers—not recency or
   runtime alone.
3. **Closure:** decide `🏁` and `☑️` under Claim.

## Mandate

The **mandate** is the final boundary this session still owes, not the
current action or method. An explicit user correction may **revise** that
same boundary. While the current boundary is still owed, new work is
evaluated under Gate, not as a new mandate. It ends only when **revoked**
(explicitly released), **discharged** (final closure passes), or
**transferred** (an accepted successor owns it). After it ends, a new
mandate starts only on evidence that this session now owes another final
boundary. With no new mandate, the closing headline keeps the old one.

## Gate

The **gate** is the mandate's one bottleneck: the hold or step that first
decides whether the mandate can advance. Keep it while it remains the
bottleneck; with no hold, use the decisive next step. Activity outside the
bottleneck does not enter the headline.

## Owner

The **owner** is who must take the next step through the chosen gate, and
selects the state. Completion and handoff override:

- `🏁` mandate discharged
- `☑️` checkpoint passed and parked
- `🔀` accepted successor owns unfinished work
- `🙋` user decision, authorization, or action
- `🕒` time, device, review, build, or external system
- `⛔` no valid path
- `⏸️` user pause
- `⏳` owned queue not started
- `🏃` Agent-owned active work; its working Agent may use one self-explanatory
  emoji for its current action. Fall back to `🏃`; all other states stay fixed.

Turns and tool calls are not checkpoints; ordinary progress belongs in the
transcript or report.

## Claim

`🏁` and `☑️` are claims that the mandate is discharged or parked, not that
a gate or the latest turn finished. Read
[references/closure.md](references/closure.md) before writing, accepting, or
challenging either one.

## Authority

Rename your own session; a controller may rename work sessions it owns.
The first bulk rename needs user authorization, and `🔀` needs an accepted
successor. Naming never archives or deletes.
