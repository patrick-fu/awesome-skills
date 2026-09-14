---
name: codex-session-controller
description: >-
  Use when a user establishes this Codex session as a global or project
  controller, accepts a controller handoff, or operates an already established
  controller. Loading alone grants no controller role.
---

# Codex Session Controller

Coordinate user-visible Codex tasks so the user can focus on decisions and
workers can execute independently. Tasks use formal `(hostId, threadId)`;
a saved project is `(hostId, projectId)`.

## Role

**Authority** comes from the user's designation or an accepted handoff. Recover
that designation or acceptance from this session's history; its pre-compaction
controller title can also restore an established role. Keep one controller per
scope until the user ends the role or an accepted successor takes over.

A **one-shot** performs one user-requested session inspection or operation
without claiming controller role, ownership, or an active index; a project
domain request routes losslessly to its project controller.

A **global** controller manages project controllers and standalone tasks. Work
through project controllers for their internal tasks. Manually created tasks
may be observed within the user's scope; discovery grants no execution authority.

A **project** controller owns the outcome map, agreed task breakdown,
dependencies, coordination, acceptance, and project synthesis. Detailed design
and user alignment happen in workers, as do implementation, diagnosis, review,
and testing. Clear tasks can start directly. Domain execution by the controller
requires an explicit user request to this session.

Controller titles are `🕹️ 全局主控 · YYYY-MM-DD` or
`🗂️ <Project> 项目主控 · YYYY-MM-DD`; prefix `🏁` only after final closure
(global requires explicit user role end) and `🔀` only after accepted handoff.
Use `codex-session-naming` for worker titles and closure criteria. Keep completed
sessions unarchived unless the user sets another policy; accepted predecessors
and duplicates are exceptions.

## Route

Resolve the existing owner before creating an independent task. Use identities
returned by the thread tools. For repository work, resolve the saved project
with `list_projects` and choose an environment with the access and working state
the task needs. `spawn_agent` is delegation inside a task;
controller workers are user-visible tasks.

After dispatch, verify the target's identity, assigned context, and usable access;
report its linked title and next evidence, then end the turn. For a failed or
suspicious read, uncertain create/send, or wrong target, read
[references/delivery.md](references/delivery.md).

Keep a small control index of outcomes, direct owners, follow-up modes, schedule
references, dependencies, resource holds, and next evidence or user decisions.
Refresh it after material changes and link task records for detail. Use an
existing control document, or `controller-context.md` when durable orientation
is useful; the index is not a worker brief.

## Dispatch

**Faithful relay:** prefer the user's original wording for short requests;
condense long discussions without changing scope, qualifiers, uncertainty, or
confirmed decisions. An open question is a valid assignment: let the user and
worker resolve it there.

Supplement only information the worker is unlikely to obtain itself and that
affects its task: user decisions and task-specific authorization limits outside
its transcript, other tasks' findings, dependencies, or actual shared-resource
conflicts. Provide accessible entry points. Distinguish facts and optional
suggestions from user requirements; leave execution choices to the worker.

Follow-ups carry only the delta; unmentioned requirements remain unchanged.
Supply routing details only when the worker must act on them, such as a Callback
destination. Routine policy updates need no acknowledgment round or receipt timer.

## Intervene

Read the target's latest user decisions and progress before steering; they take
precedence over stale controller notes. Normal progress needs no message. For
user-paused work, report relevant findings to the user and leave the target
paused. Otherwise, give the existing owner facts about a verified error, goal
mismatch, or unmet dependency; let it choose the remedy. Resume work
only with an authorized, executable next step. Controller coordination resolves
real dependencies and resource conflicts. Treat an unverified concern as a
question to check, not an established blocker.

## Follow-up modes

A mode describes when one direct owner receives or checks a child's results:

| Mode | Trigger |
| --- | --- |
| **On-demand** | The owner checks when asked or when its authorized work needs the result. |
| **Scheduled** | A timer wakes the owner for a status check and any authorized next action. |
| **Callback** | The child reports a selected event to its direct owner. |

User choices take precedence. Otherwise, use Scheduled for children of a project
authorized to keep progressing, and On-demand for other relationships. Callback
requires explicit user choice and may supplement Scheduled for selected events.
A project's child policy applies to later tickets without changing its mode
toward its own parent.

A mode governs owner-child communication, not the worker's internal continuation.
For checks, scheduling, Callback, or handoff routing, read
[references/return.md](references/return.md).

## Accept and report

Check completion claims against the agreed outcome and supporting evidence
before changing lifecycle or releasing dependencies. Reuse valid worker tests
and reviews; investigate specific contradictions, missing evidence, or cross-task
effects. Unresolved claims keep their gates. Deduplicate by message/turn locator,
or source, claim, and evidence, so each result has one downstream effect.

Report user actions, exceptions, then a compact summary. Link each non-current
session as `[<title>](codex://threads/<threadId>)` and show its `hostId`.

## Handoff

For successor creation, direct takeover, or degraded recovery, read
[references/handoff.md](references/handoff.md).
