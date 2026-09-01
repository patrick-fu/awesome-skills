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
2. **Semantic transition:** check and update the title before the response that
   ends your turn whenever the state, mainline goal, or active gate changes
   meaning. The latest user message does not automatically change the main
   goal. Infer meaning from durable promises, delivered work, verification,
   and blockers rather than raw runtime status or turn boundaries.
3. **Closure:** `🏁` and `☑️` are claims evaluated against the durable main
   goal boundary. Side work or the latest user message cannot narrow this
   boundary unless a main-goal replacement condition is satisfied. Read
   [references/closure.md](references/closure.md) before choosing either state,
   and before accepting or challenging someone else's claim.

## Format

`<state> [scope][facet] <main goal> · <current gate>`

## State

Choose by the controlling gate owner on the durable main goal, including an
unresolved blocker; completion and handoff override:

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

## Mainline stability

Keep titles sticky: at most two useful tags; preserve user phrasing, IDs,
entities, and length stability.

### Main goal vs transient gate

The **main goal** is the session's durable anchor—the promised outcome and final
boundary the session still owes and will return to complete.

The **current gate** (suffix `· <gate>`) reflects the active transient branch,
milestone, waiting condition, or blocker. Prioritize an unresolved mainline
blocker or wait; show an active side branch or action only when no controlling
mainline blocker is waiting.

- **Branches never replace the main goal:** temporary investigations, side
  questions, log checks, diagnostics, explanations, status queries, evidence
  gathering, review, or external waits attach only as the `· <gate>` suffix.
  The leading state always follows the controlling gate owner on the durable
  mainline; concurrent side work never overrides a blocking wait or blocker.
  When the branch resolves, the suffix returns to the mainline's next gate.
- **Suffix hysteresis:** keep the current gate stable until it is resolved, its
  owner or substantive meaning changes, or a higher-priority blocker emerges.
  Do not jitter the suffix across turns or multiple concurrent branches.
- **Ephemeral branches:** brief side queries or actions that do not change the
  controlling owner, substantive gate, or sidebar identity leave the title
  unchanged.
- **Single active gate:** when multiple subtasks or branches arise, show only
  the single gate that best explains the immediate next action or blocker. Never
  stack history in the title.

### Replacing the main goal

Replace the main goal only when concrete evidence proves the durable outcome has
changed:

1. The user explicitly abandons, cancels, or pivots away from the previous goal.
2. The promised final boundary was closed with `🏁`, and work begins on a new
   independent deliverable.
3. Proven lifecycle transfer: after an accepted handoff or takeover, the session
   genuinely owns a different independent outcome.

To distinguish same-mainline evolution from an independent new goal, check the
promised boundary, owner, success criteria, and whether the session must still
return to the original outcome. Conversational markers (such as "by the way",
"also", or "first check") are evidence of intent, not rigid keyword rules.
