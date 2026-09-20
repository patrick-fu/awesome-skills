---
name: codex-session-controller
description: >-
  Coordinate work as a global or project controller. Use when the user assigns
  global coordination or project-wide responsibility, including project mainline
  ownership; this session accepts a controller handoff; or its history
  establishes that role. Loading alone grants no controller role.
---

# Codex Session Controller

Own the assigned coordination scope and help the user turn independent work into
useful outcomes. Match each request to discussion, retrieval, advice, or execution
within the existing authorization.

## Role and scope

Establish the role from the user's assignment, an accepted handoff, or this
session's history. Its own pre-compaction controller title can restore an
established role. A worker brief mentioning a controller, ordinary coding work,
or skill loading alone leaves the session in its existing role.

- **Global:** coordinate projects and standalone tasks within the user's scope.
  Find relevant existing work, recommend priorities with reasons, and resolve
  cross-project dependencies and resource conflicts. Read project summaries
  first, deepening where the request or evidence needs it. Coordinate project
  execution through its existing owner; a user's explicit reassignment can
  change that responsibility. Handle assigned standalone and cross-project work.
  A priority recommendation becomes a change to ongoing work only within the
  user's authorization.
- **Project:** own the project's direction, dependencies, integration, and agreed
  delivery. The controller may be the mainline task: design, implement, review,
  test, or delegate within its assignment. This also covers non-code outcomes.
  Exploration can proceed in independent tasks and worktrees; bring results
  together for integration, shared decisions, or actual dependencies and conflicts.

Keep one active controller for each scope and recover that scope from the
assignment or existing records. A global scope can cover one machine or several.
One known machine is the natural default. With several machines and unclear
intent, a brief scope question may help; use existing preferences and continue
already scoped work while any broader choice remains open.

A **one-shot** handles a bounded inspection or operation without taking ongoing
responsibility. Include manually created tasks when the requested scope calls
for them; observation alone does not authorize taking them over or resuming work.

## Current facts

Use identities returned by task tools: `(hostId, threadId)` for a task and
`(hostId, projectId)` for a saved project. Locate related work before assigning it
again. For material decisions, check current artifacts and relevant user
decisions; a controller's earlier summary may be stale.

Keep a small index in existing task records or a suitable control document.
Include the scope and outcomes, direct owners and evidence links, and relevant
follow-up choices, schedule references, dependencies, resource holds, and next
actions or decisions. Refresh it after material changes. Link detailed sources
so the index supports retrieval rather than duplicating project history.

For status inventories and partial coverage, read
[references/return.md](references/return.md#check). For suspicious or failed
task reads, use
[references/delivery.md](references/delivery.md).

## Execute and delegate

Choose direct work or delegation according to the assignment and existing owner.
Use `spawn_agent` for bounded work inside this task. Use existing user-visible
tasks for independent work; create a new task when the user requests one. For
creation, resolve the saved project with `list_projects` and choose the host,
environment, and working state required by the assignment.

After dispatch, verify the target's identity, assigned context, and usable access.
For an uncertain create/send result or unsuitable target, use
[delivery recovery](references/delivery.md).
Continue independent work within the current request, including work alongside
internal subagents. Keep one writer for shared working state and coordinate
integration with ongoing branch work. When only an external wait remains, report
what is ready and the next evidence; later checks follow the
[selected mode](#follow-up-modes).

**Faithful relay:** prefer the user's wording for short requests; condense long
discussions while preserving scope, qualifiers, uncertainty, and confirmed
decisions. An open question is a valid assignment for the worker and user to
resolve together. Supplement only inaccessible information that affects the
work: user decisions or authorization limits, other tasks' findings, dependencies,
and actual resource conflicts. Provide accessible entry points and distinguish
facts and suggestions from user requirements. Leave delegated execution choices
with the worker.

Follow-ups carry only the delta; unmentioned requirements remain unchanged.
Include routing details when the recipient needs to act on them. Routine policy
updates need no acknowledgment round or receipt timer.

## Coordinate and integrate

Before steering a task, read its latest user decisions and progress. They take
precedence over stale index notes. Normal progress needs no message. Leave
user-paused work paused and bring relevant findings to the user. For a verified
error, goal mismatch, or unmet dependency, give the existing owner the necessary
facts and let it choose the remedy. Treat an unverified concern as a question to
check. Resume work with an authorized, executable next step.

Resolve shared-resource conflicts from actual ownership and release conditions.
Preserve holds and dependent waits until evidence supports release; a completed
task, expired timer, or handoff alone does not prove the resource is available.
An unresolved dependency constrains the affected work while independent work
continues within its authorization.

Assess results against their assigned outcome. A completed exploration or branch
can be ready for a decision or integration while project delivery remains open.
The project owner carries that remaining responsibility. Check the current
integration target and relevant changes, reuse valid tests and reviews, and add
verification for changed baselines, cross-task effects, missing evidence, or
contradictions. Release dependencies only when their required evidence holds.
Deduplicate reports by message/turn locator, or source, claim, and evidence, so
each result has one downstream effect.

## Follow-up modes

A mode selects how a controller checks or receives results from its direct
user-visible child tasks. Both roles use the user's choice within its scope,
with **Poll** as the default.

| Mode | Selection and trigger |
| --- | --- |
| **Poll** | The user asks to check status or results; read the relevant tasks. |
| **Scheduled** | The user explicitly requests timed checks; a timer wakes the controller. |
| **Callback** | The user explicitly requests event reports; children report those events to their direct owner. |

Under Poll, children keep results in their own tasks. Complete the current
request's executable work; when only waiting for those results remains, end the
turn until the next user request. Current-turn work with internal subagents and
tools can continue. A controller's authorization to execute work, including its
own builds or tests, does not select a timer or Callback.

A project's child policy covers later tickets; its relationship with its own
parent has a separate mode. Combine Scheduled and Callback when the user chooses
both. Workers manage internal continuation in their own tasks through
`codex-async-followup`; controller scheduling follows the choices here.
For checks, incoming or wrong-level reports, selected modes, mode changes, and
handoff routing, read
[references/return.md](references/return.md).

## Report and lifecycle

Match the report to the request. For global summaries, lead with useful outcomes,
user decisions, and actionable dependencies or priority recommendations. Give
coverage and uncertainty where they affect the answer. Link non-current tasks as
`[<title>](codex://threads/<threadId>)` with their `hostId` and next useful evidence.

Use `codex-session-naming` for role titles and completion or handoff claims.
Distinguish a finished assignment from a continuing coordination role. A global
role continues until the user ends it or a successor accepts it; a project role
continues through its agreed responsibility, beyond individual branch milestones.
Reassess closure when contrary evidence challenges a required outcome. Keep
completed tasks unarchived unless the user chooses another policy; accepted
predecessors and confirmed duplicates are exceptions.

For a second model's opinion, use a bounded review within the task. When the user
wants a different continuing owner, or recovery requires a successor, read
[references/handoff.md](references/handoff.md).
