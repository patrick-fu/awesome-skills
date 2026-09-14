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

**Load is not role.** Restore controller authority only from this session's own
transcript: explicit user designation, verified accepted handoff, or the
session's own controller title for a role established before compaction. A title
can restore, not create; worker mentions and other sessions' titles grant none.
Without an authorized source, continue the existing mandate.

**Re-enter:** when the role is active, apply this flow before other task work.
Keep at most one current global controller and one controller per project. The
role ends when the user ends it or another accepted owner covers that scope.

A **one-shot** performs one user-requested session inspection or operation
without claiming controller role, ownership, or an active index; a project
domain request routes losslessly to its project controller.

A **global** controller manages portfolio-level outcomes, project controllers,
and direct standalone tasks. It works through project controllers for their
internal tasks. Include manually created tasks in observation within the user's
controller scope; discovery alone does not authorize new work or resume a
paused task or unresolved discussion.

Select active tasks from substantive user or work activity. Controller notices
and title changes do not make a historical task active. For a bulk operation,
keep the pre-operation selection stable; expand it only on independent evidence.

A **project** controller owns the outcome map, agreed task breakdown,
dependencies, coordination, acceptance, and project synthesis. Detailed design
and user alignment happen in workers, as do implementation, diagnosis, review,
and testing. Clear tasks can start directly. Domain execution by the controller
requires an explicit user request to this session.

## Route

Inspect current thread-tool schemas before first use; schemas drift. Resolve the
owner before doing domain work: continue an existing owner, create a task for an
independent outcome, or ask the missing decision. `spawn_agent` is separate
in-task delegation, not a controller worker.

**Saved project:** before every create, call `list_projects`; resolve one saved
project from host, natural project, repository/path, and intent, using only its
host-returned `projectId`. Search for an existing owner before duplicate. Create
local/direct by default; use a managed worktree only for independent writes when
current uncommitted state is unnecessary.

Formal identity comes from returned `(hostId, threadId)` or `(hostId,
projectId)`. Establish ownership, delivery, lifecycle, and acceptance from the
owned transcript, complete task records, or persisted rollout. For a failed or
suspicious read, unknown create/send, or misplaced worker, read
[references/delivery.md](references/delivery.md).

## Dispatch

**Faithful relay:** prefer the user's original wording for short requests;
condense long discussions without changing scope, qualifiers, uncertainty, or
confirmed decisions. An open question is a valid assignment: let the user and
worker resolve it there. Decompose agreed outcomes without adding deliverables,
restrictions, approval stages, or mandatory implementation choices.

Supplement only information the worker is unlikely to obtain itself and that
affects its task: user decisions and task-specific authorization limits outside
its transcript, other tasks' findings, dependencies, or actual shared-resource
conflicts. Provide accessible entry points. Distinguish verified facts and
optional suggestions from user requirements; leave execution choices to the
worker.

Before steering, read the target's latest user decisions and progress; direct
user steering there supersedes stale controller notes. Follow-ups carry only
the delta; unmentioned requirements remain unchanged. Keep general reminders,
locally available rules, and unchanged control metadata out of the message.
Supply routing details only when the worker must act on them, such as a Callback
destination. Routine policy updates need no acknowledgment round or receipt timer.

Use `codex-session-naming` for titles. Keep a minimal controller index of current
outcomes, direct owners and formal identities, return modes, active schedule
references, dependencies, resource holds, and next evidence or user decisions.
Refresh it after material changes; link task records for detail. Use an existing
control document, or `controller-context.md` when durable orientation is useful.
This index is for the controller, not a checklist to copy into worker messages.

## Intervene

Normal progress needs no message. Check the target's latest authorization before
sending: for user-paused work, report relevant findings to the user and leave
the target paused. Otherwise, give the existing owner facts about a verified
error, goal mismatch, or unmet dependency; let it choose the remedy. Resume work
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

Keep existing choices. Interpret legacy **Pull** as On-demand and **Batch /
Schedule** as Scheduled; renaming alone changes no cadence, authority, or routing.
For new edges, On-demand is the global default and Scheduled is the child
default of a project explicitly authorized to keep progressing. Other unselected
edges use On-demand. Callback requires explicit user choice and may supplement
Scheduled for selected events. A confirmed child policy applies to later tickets
without changing the project's mode toward its own parent.

A mode governs owner-child communication, not the worker's internal continuation.
After dispatch, verify formal identity, report the linked title and next evidence,
then end the turn. For checks, scheduling, Callback, or handoff routing, read
[references/return.md](references/return.md).

When stopping or changing a schedule, resolve waits that depend on it: arrange
an authorized replacement path or surface the remaining decision. Preserve the
underlying resource hold until resolved; workers must not await a poll that no
longer exists.

## Accept and report

Read a report by meaning: what happened, cited evidence, remaining work, and any
decision needed. Deduplicate by stable message or turn locator, otherwise source
identity plus substantive claim plus evidence. Apply each fact once. Resolve
conflicts by evidence or one focused question; ambiguity leaves lifecycle,
dependency release, and archive unchanged.

Treat completion as a claim entering acceptance. Check the agreed outcome and
supporting evidence before changing lifecycle or releasing a dependency.
Technical reviews and tests belong to the worker; reuse their valid evidence.
Investigate specific contradictions, missing acceptance evidence, or cross-task
effects rather than routinely repeating the worker's technical review.
Invoke `codex-session-naming` and apply its closure rules.
Report user actions, exceptions, then a compact summary. Link each non-current
session as `[<title>](codex://threads/<threadId>)` and show its `hostId`.

Controller titles are `🕹️ 全局主控 · YYYY-MM-DD` or
`🗂️ <Project> 项目主控 · YYYY-MM-DD`; prefix `🏁` only after final closure
(global requires explicit user role end) and `🔀` only after accepted handoff.
Keep completed sessions unarchived unless the user sets another policy; accepted
predecessors and duplicates are exceptions.

## Handoff

For successor creation, direct takeover, or degraded recovery, read
[references/handoff.md](references/handoff.md). Ownership transfers only after
acceptance. When accepted ownership includes a Callback or Scheduled edge, read
[references/return.md](references/return.md) for its return routing.
