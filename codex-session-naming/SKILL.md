---
name: codex-session-naming
description: >-
  Maintain every user-visible top-level Codex App session title. Invoke before
  substantive work at task start and on goal, checkpoint, final, gate, owner,
  wait, block, pause, resume, takeover, handoff, or reopen transitions.
  Excludes chats, subagents, and controller roles.
---

# Codex Session Naming

## Title loop

1. **Authority:** rename self; controllers may rename owned sessions. First bulk
   rename needs user authorization; `🔀` needs an accepted successor. Naming
   never archives or deletes; controller-role titles follow
   `codex-session-controller`.
2. **Evidence:** infer goal, state, and gate from task evidence, not runtime status.
3. **Format:** `<state> [scope][facet] <main goal> · <current gate>`
4. **Lifecycle:** rename before substantive work, before continuing after every
   description trigger, and before the final response.

Rename only when meaning changes.

## State

Choose by next-step owner; completion and handoff override:

- `🏁` final contract passed
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

## Completion contracts

Derive the promised boundary from latest user intent, never thread hierarchy.
A checkpoint is an explicit intermediate deliverable; only the promised final
boundary may become `🏁`.

**Checkpoint:** require delivery, verification, outcome validation, defined
acceptance, and no checkpoint work. It never releases the final boundary.

**Final:** derive scope from user intent, corrections, promises, observable
criteria, and acceptance authority. Require all six: scope delivered; procedure
verified; outcome validated in context; acceptance satisfied; no
`required-to-close` or `external-user-gate`; owner released.

**Delivery audit:** in-scope dirty changes keep a versioned task open unless the
user accepts working-tree delivery. Lacking commit authority is an
`external-user-gate`. Push, review, release, or publication is required only by
user intent or an explicit repository delivery rule.

**Acceptance:** follow the authority agreed with the user and the nature of the
result. Objective work may close on reliable evidence; subjective, device,
production, external-system, or user-review outcomes wait for the required
decision or observation. Procedure, idle, silence, and unrelated messages do
not count.

**Remainder:** classify work as `required-to-close`, `external-user-gate`,
`independent-optional-follow-up`, or `out-of-scope`. Only the last two allow
`🏁`; if skipping it would defeat current success, it is required.

**Waiver:** require an explicit decision; record gate, scope, reference, and
residual risk. It changes intent but does not verify the gate or bypass safety,
permission, or policy.

**Challenge:** reopen when evidence disproves completion; independent requests
start new boundaries. Audit completion as a claim. Without evidence, say what
cannot yet be verified, preserve owner and title, and do not archive, replace,
or reroute.

## Stability

Keep titles sticky: at most two useful tags; preserve user phrasing, IDs,
entities, and main goal. Change the gate with its owner or meaning; replace the
goal only for an independent boundary.
