---
name: codex-session-naming
description: >-
  Apply the title lifecycle to every user-visible top-level Codex App session.
  Establish its sidebar identity before the first response, maintain it when
  the goal, next gate, owner, or lifecycle meaning changes, and evaluate
  completion claims. Excludes chats, subagents, and controller-role titles.
---

# Codex Session Naming

Apply to user-visible top-level Codex App sessions, not chats, internal
subagents, or controller-role titles.

The title is the sidebar's whole view of a session: its state, its goal, and who
owes the next step. Rename when that view has become false.

## Authority

Rename your own session; a controller may rename sessions it owns. The first
bulk rename needs user authorization, and `🔀` needs an accepted successor.
Naming never archives or deletes. Controller-role titles follow
`codex-session-controller`.

## Events

Three events decide every rename; anything else leaves the title alone.

1. **Entry:** establish the sidebar identity before the first response from the
   available entry evidence: state, main goal, current gate. With no usable
   goal yet, title the session `🙋‍♂️ 新会话 · 等待目标`; the next transition
   replaces it.
2. **Semantic transition:** rename when the goal, the next gate, the owner of
   the next step, or the lifecycle state changes meaning, and check the title
   before the response that ends your turn. Infer meaning from task evidence:
   latest user intent, delivered work, verification, and blockers, not runtime
   status. A turn boundary or a tool call changes nothing by itself.
3. **Closure:** `🏁` and `☑️` are claims. Read
   [references/closure.md](references/closure.md) before choosing either state,
   and before accepting or challenging someone else's claim.

## Format

`<state> [scope][facet] <main goal> · <current gate>`

## State

Choose by next-step owner; completion and handoff override:

- `🏁` promised final boundary passed
- `☑️` checkpoint passed and parked
- `🔀` accepted successor owns unfinished work
- `🙋‍♂️` user decision, authorization, or action
- `🕒` time, device, review, build, or external system
- `⛔` no valid path
- `⏸️` user pause
- `⏳` owned queue not started
- `🏃‍♂️` Agent-owned active work; its working Agent may use one self-explanatory
  emoji for its current action. Fall back to `🏃‍♂️`; all other states stay fixed.

Turns and tool calls are not checkpoints. On the next gate, use its state; keep
prior checkpoints only in the suffix or report.

## Stability

Keep titles sticky: at most two useful tags; preserve user phrasing, IDs,
entities, and main goal. Change the gate with its owner or meaning; replace the
goal only for an independent boundary.
