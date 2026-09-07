---
name: codex-session-controller
description: >-
  Use when a user establishes this Codex session as a global or project
  controller, accepts a controller handoff, or operates an already established
  controller. Loading alone grants no controller role.
---

# Codex Session Controller

Control user-visible Codex tasks through thread tools. Workers and successors
are separate tasks identified by formal `(hostId, threadId)`; a saved project is
`(hostId, projectId)`.

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
direct standalone tasks, but not project-internal tickets. Every direct child
edge defaults to Pull. Inventory takes one bounded snapshot of those children,
without ticket detail unless the user asks.

A **project** controller owns one project's outcome map, backlog, frontier,
dependencies, concurrency and resource limits, acceptance, next dispatch, and
project synthesis. It may do light control work. Domain research,
implementation, diagnosis, review, testing, and artifact iteration belong to
workers; direct execution requires an explicit user request to this session.

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

**Lossless:** the initial brief carries the complete user request; steering
carries only its delta. Every unmentioned dimension remains unchanged. State the
outcome, user details, permission and host boundary, acceptance evidence,
decisions that pause work, and the direct owner's formal identity as the report
destination. Keep the brief self-contained and distinguish requirements from
non-binding suggestions. Give the worker accessible paths, links, or content.

Invoke `codex-session-naming` to establish a worker title; the brief carries the
outcome, not a naming protocol. Maintain a minimal active index. When durable
orientation is useful across re-entry, Pull, or handoff, externalize the active
control context in an existing controller document, or a small
`controller-context.md` scoped to that controller and host. Keep the current
outcome, active frontier, and each relevant direct edge's formal identity,
direct owner, return mode, and decisive evidence or gate. Refresh the current picture
after material control changes. Task records remain the evidence for
acceptance, permissions, and detail. Prefer natural language or a small table.
A Batch cohort may group edges; no other hierarchy is inferred.

## Return

Return belongs to one direct owner→child edge. Workers report only to their
direct owner; a report never leapfrogs to a grandparent. Before dispatch, choose
one mode for that edge:

- **Pull** is the default for every unselected edge and global→project,
  switchable only by explicit user choice. It is dispatch-and-return: verify
  formal identity, report the linked title and next evidence, then end without
  `wait_threads`, callback, or schedule. For inventory, rebuild the named or
  directly owned set from the index, known identities, and `list_threads`; take
  one snapshot pass in `wait_threads` batches of at most eight, report links,
  hosts, and one-line states, then end.
- **Callback** and **Batch** require the user to choose directly or to confirm
  after the controller explains effects on response speed, interruption, token
  use, and latency. Echo an explicit user choice and use it without asking
  again. Work shape alone never upgrades a mode.

Mode changes only return behavior; scope, owner, authority, and acceptance stay
unchanged. A project controller→ticket edge may be Callback when the user chose
that default for active work; project→global stays Pull unless the user
explicitly switches that edge. Pull keeps blocker/final/handoff state in the
project task until global pull. For Callback/Batch mechanics, wrong-level
reports, or handoff return routing, read [references/return.md](references/return.md).

When establishing a project controller, recommend and obtain one confirmation
for its child default return policy; **Callback-first** suits an active
frontier. That confirmed policy supplies the return mode for later ticket edges
without asking per worker. If unconfirmed, each edge remains Pull.

## Accept and report

Read a report by meaning: what happened, cited evidence, remaining work, and any
decision needed. Deduplicate by stable message or turn locator, otherwise source
identity plus substantive claim plus evidence. Apply each fact once. Resolve
conflicts by evidence or one focused question; ambiguity leaves lifecycle,
dependency release, and archive unchanged.

Treat completion as a claim entering acceptance. Verify evidence before
changing lifecycle, releasing a dependency, or accepting writes. Invoke
`codex-session-naming`, apply its closure rules, and do not replay the worker.
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
acceptance. When accepted ownership includes a Callback or Batch edge, read
[references/return.md](references/return.md) for its return routing.
