---
name: thread-controller
description: >-
  Coordinate threads, schedules, and cross-project work from Home or an
  explicitly invoked coordinator session.
disable-model-invocation: true
---

# Thread Controller

Coordinate work across projects, machines, and parallel top-level threads from
an explicitly invoked coordinator session (such as `Home` or a dedicated duty
thread). Match each request to inspection, routing, advice, or bounded
execution within the user's authorization.

## Role and scope

This skill is user-invoked (`$thread-controller`) and does not replace ordinary
project threads. Within a single project, normal threads work directly against
the project's repository or shared context store (`work-context` /
`life-context`) and use in-thread delegation without loading a controller
skill.

Keep one active coordinator per scope and recover that scope from the user's
assignment, the current session's pre-compaction coordinator title, or persisted
records. Skill loading alone grants no coordination authority over unrelated
projects or machines.

- **Scope:** cover the environments and projects assigned (defaulting to the
  current environment when local intent is clear; ask one brief question only
  when multiple reachable environments create real ambiguity, while continuing
  already scoped work).
- **Responsibilities:** discover existing threads and context records before
  dispatching duplicate work, recommend priorities with reasons, route follow-ups
  to existing owners when appropriate, resolve cross-project dependencies and
  shared-resource conflicts, and synthesize concise global status.
- **One-shot vs. ongoing:** a one-shot check answers a bounded question without
  claiming ongoing ownership. Include manually created user threads in status
  inventories when the scope calls for them; observation alone does not
  authorize taking them over or steering them.

## Host adapters and references

Read **only the single adapter matching the current host** when performing
host-specific dispatch, inspection, scheduling, evidence recovery, or linking:

- T3 Code: [references/adapters/t3-code.md](references/adapters/t3-code.md)
- Codex App: [references/adapters/codex-app.md](references/adapters/codex-app.md)
- Standalone CLI or single-thread harness (Claude Code, Codex CLI, Antigravity): [references/adapters/standalone-harness.md](references/adapters/standalone-harness.md)

Consult these references on demand:

- Status checks, scheduling, and handoff routing: [references/return.md](references/return.md)
- Suspicious, blank, or uncertain reads and deliveries: [references/delivery.md](references/delivery.md)
- Completion, checkpoint, settle, and archive decisions: [references/closure.md](references/closure.md)
- Coordinator succession or anti-compaction relay: [references/handoff.md](references/handoff.md)

## Current facts and workspace boundary

Use formal host identities returned by the active environment:
environment/host, project/repository, thread or delegate ID, and workspace or
task record path. Locate existing threads and context entries before launching
new ones. For material decisions, read current artifacts and latest user
steering rather than relying on stale summaries.

Keep durable project state in the project's own external context store or task
ledger (following its locking and single-writer rules), and rely on host thread
histories for live execution tracking. Keep a dedicated `Home` directory
strictly read-only (only its instructions and local git anchor): write temporary
scratch to `$TMPDIR`, and route durable project updates through the owning
project thread or context repo rather than maintaining a second ledger inside
`Home`.

## Execute and delegate

Choose the execution surface by assignment, existing owner, and host
capability:

1. **In-thread helper (`delegate_task` / native subagent):** bounded helper
   research, multi-model analysis, review, or verification kept under this
   session's ownership. Follow the runtime's async notification contract; never
   poll `task_status` or sleep.
2. **Existing or new top-level thread:** independent ongoing project work or
   explicit user-requested threads, routed to an existing owner when one already
   holds that branch or scope, or launched in the resolved environment, project,
   and working state.

**Capability probe and routing:** inspect available environments, providers,
models, options, and scheduler support via the host adapter before
cross-harness dispatch. Report unavailable providers or capabilities clearly
instead of silently substituting.

**Single writer and context coordination:** keep one writer per shared branch,
worktree, or physical resource hold. Parallel threads within the same project
coordinate through the project's external context ledger, branches, and explicit
resource locks rather than inter-thread callback messages.

**Anti-compaction relay:** when a coordinator or worker thread degrades from
repeated compaction or context saturation, hand remaining scope to a clean
thread (or reset via `freshContext: true` where supported) grounded in
persisted external records and artifacts rather than forcing endless compaction.

**Faithful relay:** condense long discussions while preserving scope,
qualifiers, uncertainty, and confirmed decisions; send concise deltas on
follow-ups; leave execution choices with the worker. After dispatch, verify the
target's identity, assigned context, and usable access; use
[delivery recovery](references/delivery.md) for uncertain results or unsuitable
targets.

## Coordinate and integrate

Before steering a task, read its latest user decisions and progress. Normal
progress needs no interruption; leave user-paused work paused and surface
relevant findings to the user. For a verified error, goal mismatch, or unmet
dependency, give the existing owner the concrete facts and let it choose the
remedy.

Preserve resource holds and dependent waits until direct evidence proves
release; a completed turn or expired timer alone does not prove availability.
Verify claims against actual branch state, tests, or artifacts, and
deduplicate findings by message/turn locator or `(source, claim, evidence)`.

## Follow-up modes

Cross-thread follow-up is strictly **unidirectional** (coordinator-owned).
**Never instruct child threads to send upward callback or completion messages
back to the coordinator.** Child threads finish, record outcomes in their own
thread or external context store, and stop.

Use only two modes, with **Poll** as the default:

| Mode | Selection and trigger |
| --- | --- |
| **Poll** | Default. Inspect relevant threads on user request via the host adapter. |
| **Scheduled** | User explicitly requests timed checks; a parent-owned timer wakes the coordinator. |

Under **Poll**, complete the current request's executable work; when only
external waits remain, report what is ready and end the turn until the next user
request. Waiting on the coordinator's own authorized operation does not
authorize creating a timer. If the host lacks native timers, keep **Poll** and
report that limitation explicitly rather than simulating background checks.

Workers manage internal waits inside their own threads via the host's native
continuation tools; coordinator scheduling governs only cross-thread checks.
For status checks, timer management, and handoff routing, read
[references/return.md](references/return.md).

## Report, titles, and lifecycle

Lead global summaries with useful outcomes, user decisions needed,
dependencies, and priority recommendations. State coverage gaps or unresolved
reads explicitly. Cite non-current threads using the host adapter's canonical
link format alongside environment provenance and next useful evidence.

**Titles:** apply `thread-naming` if available, keeping coordinator role
headlines visible (`🕹️ <scope>`, prefix `🔀` on outgoing handoff or `🏁` on
closure; use `☑️` for checkpoints and `🙋`/`⛔`/`🕒` for waits), updating only
when role or state changes.

For completion, checkpoint, settle, or archive decisions, use
[references/closure.md](references/closure.md). Settle verified completed
child threads where the host supports it (`t3_thread_organize`) while keeping
history recoverable; archive only accepted predecessors or confirmed
duplicates. When a new continuing coordinator is needed, read
[references/handoff.md](references/handoff.md).
