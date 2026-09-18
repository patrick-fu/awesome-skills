---
name: codex-session-controller
description: >-
  Use when a user establishes this Codex session as a global or project
  controller, accepts a controller handoff, or history identifies an
  established controller role. Loading alone grants no controller role.
---

# Codex Session Controller

Coordinate user-visible Codex tasks so the user can focus on decisions and
workers can execute independently. Tasks use formal `(hostId, threadId)`;
a saved project is `(hostId, projectId)`.

## Role

Determine this session's role from the user's designation, an accepted handoff,
or its own history. Its pre-compaction controller title can help restore a
previously established role. A worker's mention of a controller or skill loading
alone does not assign that role; continue the existing mandate when no
controller role is established.

There are two controller roles. A **global** controller coordinates project
controllers and standalone tasks within the user's chosen scope. Work through
project controllers for their internal tasks. A **project** controller owns the
project's outcomes, agreed task breakdown, dependencies, coordination, acceptance,
and synthesis. Workers handle detailed design, user alignment, implementation,
diagnosis, review, and testing. Domain execution by the controller requires the
user to ask this session to do it.

Keep one active controller per scope and recover that scope from the assignment
or control index. A global scope may cover one machine or several. With only
one known machine, it is the natural default. When multiple machines are evident
and intent is unclear, a brief question about all machines versus the current
one can help. Use existing user preferences to judge whether to ask; an explicit
global or machine-specific choice needs no repeated question. Continue already
scoped work while any broader choice remains open.

A **one-shot** performs a bounded user-requested inspection or operation without
adopting ongoing controller responsibility. Route project work through its
existing project controller. Manually created tasks can be observed within the
requested scope; discovery alone does not authorize execution.

Use `codex-session-naming` for both controller and worker titles. A global role
continues until the user ends it or an accepted successor takes over; a project
outcome ends through acceptance. Keep completed sessions unarchived unless the
user chooses another policy; accepted predecessors and duplicates are exceptions.

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

Keep a small control index of scope, outcomes, direct owners, follow-up modes,
schedule references, dependencies, resource holds, and next evidence or user decisions.
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

A follow-up mode defines how a controller checks or receives a direct child's
results. For both global and project controllers, use the user's chosen mode
within its scope, with Poll as the default.

| Mode | Selection and trigger |
| --- | --- |
| **Poll** | The user asks to check status or results; the controller reads the relevant child tasks. |
| **Scheduled** | The user explicitly requests timed checks; a timer wakes the controller. |
| **Callback** | The user explicitly requests event reports; the child reports those events to its direct owner. |

Under Poll, children keep results in their own tasks. Handle each user request
within its scope: dispatch or inspect work, coordinate authorized next steps,
report, and end the turn.

Keep each choice within its assigned owner-child scope. A project's child policy
covers later tickets; its relationship with its own parent has a separate mode.
Combine Scheduled and Callback when the user requests both.

Workers manage their internal continuation in their own tasks, using
`codex-async-followup` for asynchronous waits. For controller checks, scheduling,
Callback, or handoff routing, read [references/return.md](references/return.md).

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
