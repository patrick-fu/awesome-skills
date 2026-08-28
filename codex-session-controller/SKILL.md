---
name: codex-session-controller
description: >-
  Codex App-only control of top-level Codex sessions across projects and hosts,
  including global and project controllers, routing, monitoring, callbacks,
  closure, deduplication, and handoff. Depends on codex-session-naming for
  session titles; use when the user explicitly invokes this controller
  workflow.
disable-model-invocation: true
---

# Codex Session Controller

Treat Codex task, thread, session, chat, and conversation as the same
user-visible top-level object. Operate as a **thin control plane** through thread
tools: owned sessions do research, implementation, diagnosis, review, and
testing; the controller does only the small read-only checks needed for hosts,
projects, repositories, owners, and acceptance evidence. Never use `spawn_agent`
in this workflow.

## Own the control plan

Own the user's single entry point and control plan: recover the latest intent;
choose the outcome and owner; preserve scope and authorization; order
dependencies; define acceptance; detect conflicts; and synthesize evidence into
real user gates. Answer control questions from established facts. Delegate or
continue an owner when the answer needs new repository/external evidence,
sustained tools, technical design, implementation, diagnosis, or testing. Ask
the owner for a targeted evidence gap instead of reconstructing its work.

The user should normally talk only to the controller. Recommend opening a
worker directly only for a high-bandwidth technical or artifact discussion. A
newer direct user decision takes effect in the session that received it; if it
materially changes scope, priority, resources, acceptance, or a settled
decision, send that change back to the responsible controller and record it
there instead of asking the user to repeat it.

Keep only a lightweight active-outcome index: owner `(hostId, threadId)`,
outcome, authorization/scope version, state, and event-shaped next check. The
owned transcript remains authoritative; do not build a second database or
timer-based polling state machine.

## Resolve the invocation

Classify the user's natural-language intent before changing state:

- **One-shot:** inspect, create, continue, rename, archive, or take over without
  changing this session's role.
- **Global controller:** manage the portfolio when the user explicitly asks to
  establish a controller and names no narrower scope.
- **Project controller:** manage multiple outcomes inside an explicitly named
  project; a path or difficult one-off task alone is insufficient.
- **Successor:** replace a controller after explicit handoff or takeover.

The current session becomes the requested controller by default. Create a
separate controller only when the user asks for a new one or requests handoff.
Keep an established controller's scope stable: route an unrelated project to
the global controller; route a narrow request from the global controller to
its project owner.

One current global controller may coexist with one per project. Identify a
project from its name plus returned host/project, paths, preview, and recent
history; do not invent a scope registry. A project controller may run alone and
be discovered by a later global controller.

## Preflight capabilities

Search for and inspect the callable thread tools before relying on remembered
schemas. Controller behavior requires equivalents of:

```text
list_projects  list_threads  read_thread  send_message_to_thread
create_thread  set_thread_title
```

Use current callable schemas; availability and arguments drift across sessions.
For a missing required capability, explain the gap and use the evidence
fallback. Recommend a fresh controller only when no safe degraded path remains.
Treat `wait_threads`, archive, pin, and share as optional and state degradation.

## Establish session evidence

Use `read_thread` with its current callable schema as the primary transcript
interface for a known `(hostId, threadId)`. Treat an empty or failed read,
repeated blank turns, a returned history with no user, assistant, or tool-call
items, and contradictions with other evidence as suspicious projections.

For a suspicious projection, inspect the owning host's persisted rollout under
`$CODEX_HOME/sessions` (normally `~/.codex/sessions`). Locate by returned
`threadId`, verify against observed metadata, and inspect record types, roles,
turns, and completion evidence. Tolerate unknown records and schema drift; do
not assume fixed fields, offsets, or one schema. Read only needed evidence and
never copy raw transcripts into reports.

When the tool projection and persisted transcript disagree about what happened,
use the rollout as the authority for persisted history. A rollout absent from
the current machine says nothing about a session owned by another host; inspect
that host or report the evidence gap. Treat `idle`, `notLoaded`, a timeout, an
empty turn, a refreshed timestamp, missing local rollout, and silence as
non-terminal. Until evidence establishes a terminal or ownership state,
preserve the session and its owner: report the gap without stopping,
interrupting, archiving, replacing, handing off, or rerouting the session.

## Discover owners before acting

Use tool-returned `(hostId, threadId)` as the complete identity for every
non-current session. Titles, previews, paths, timestamps, and status labels are
discovery signals, not identities or terminal evidence.

Before establishing a global controller, search every connected host. Inspect
active, unarchived, pinned, and roughly 30 recent days where exposed; go older
only when the request requires it. Reuse or hand off a unique candidate; read
multiple candidates and ask the user to disambiguate.

For a project controller, search its natural name, saved project, host, paths,
title, preview, and recent turns. A unique match is the owner; multiple matches
require user disambiguation.

## Route work

Giving work to an established controller authorizes continuing an owner or
creating a normal task under this policy—not another controller, cross-host
execution, handoff, or irreversible external action without matching intent.

1. Continue the existing owner for clarification, correction, scope-preserving
   follow-up, or the next step of the same outcome.
2. Create a new task session for a genuinely independent outcome with no safe
   existing owner.
3. Create a project controller only when the user explicitly asks for ongoing
   project-level control.
4. Default normal work to the controller's current host. Before deduplication
   or creation, resolve the target saved project on its owning host from the
   returned project list, absolute path, and project identity. Use another host
   only when the user specifies it; never reuse a `projectId` across hosts.
5. For a Git repository, use a Codex-managed worktree for independent write
   work or historical-ref investigation. Use the saved project directly for
   read-only current-state work. Include the working tree only when the user
   explicitly requires uncommitted state. Neither controller nor child should
   run `git worktree` manually.

Keep model and reasoning settings inherited unless the user specifies them.
When naming or renaming an owned non-controller session, call the Skill tool
with `codex-session-naming`. Carry that lifecycle-title requirement into each
new normal task brief. If the Skill is unavailable, preserve the title and
report the degradation instead of duplicating its rules here.

## Make each operation recoverable

`create_thread` and `send_message_to_thread` do not provide an exactly-once
guarantee. Before either operation, generate a compact unique operation ID and
include it in the task or directive so it is preserved in rollout history:

```text
<controller_operation id="csc-..." source="hostId:threadId">
```

The operation ID correlates and deduplicates one logical create or send; it is
not authentication, authorization, or session identity. Generate a new ID for
each new logical operation. Reuse the same ID only while resolving or retrying
an unknown result from that operation.

Before create, resolve `(hostId, projectId)` and search that scope for an owner
and operation ID. A pending/client identifier is not formal identity; wait for
`(hostId, threadId)`, then immediately read or list it and verify host, project,
working directory or environment, and operation ID. After an unknown result or
timeout, search and read before retrying; no immediate response is not failure.

A duplicate requires matching operation ID, source controller, scope, and
target, with no independent user input, unique artifact, or valid running work.
Archive a confirmed duplicate when available; otherwise report it. Title or
prompt similarity is insufficient.

## Compile a clean task brief

New sessions inherit neither conversation nor attachments. Synthesize the
smallest safe, self-contained brief:

```text
Role and outcome:
[One owner and one concrete outcome.]

Location and identity:
[Target host/project, accessible absolute paths or URLs, source sessions.]

Known facts and evidence debt:
[Confirmed facts; historical claims that must be revalidated.]

Boundary:
[Read/write scope, authority, irreversible actions, excluded work.]

Deliverable and acceptance:
[Success outcome and observable user-facing validation criteria/context.]
[Procedural verification requirements and evidence.]
[Acceptance mode, validator, acceptor, evidence/decision reference, and gates.]

Callback and re-entry:
[Parent controller, operation/cohort IDs, callback policy, report events, and
the next-check trigger.]

Pause and report if:
[A required user decision is missing, or credentials, destructive action,
ownership conflict, or unresolvable ambiguity blocks progress.]
```

Include the operation ID and parent identity. Preserve paths, links,
constraints, decisions, and acceptance criteria; omit raw history, unrelated
sessions, speculation, and verbose orchestration. Derive success and acceptance
from the latest intent and carry the `codex-session-naming` closure contract.

When the global controller sends a directive to a project controller, label the
source, original intent, authorized boundary, and report event. A newer direct
user decision there wins; execute it and report material scope or decision
changes to the global controller.

## Coordinate without becoming the executor

A project controller owns internal routing. Notify its global controller only
for a user decision, cross-project resource conflict, hard blocker, project
completion, or handoff. Users may interact with it directly.

Run independent sessions concurrently only when dependencies and resources
allow. Derive capacity from the request, `AGENTS.md`, host, and exclusive
resources. For shared checkouts, devices, accounts, deployment environments,
and production, record owner, contenders, and release condition; send peer
identities only where needed.

Trust an owner by default and verify evidence proportional to risk. On visible
drift, ask it to correct before commissioning independent review. Separate
implementation, review, and integration when risk or repository rules require.

Use `/goal` only inside a project controller whose project has one durable
objective, a verifiable stopping condition, and an explicit user request such
as “continue until I need to intervene.” A global portfolio is not one goal.

## Dispatch and re-enter

Choose one wait mode at dispatch; ordinary background work defaults to the
first:

- **Dispatch-return:** verify formal identity; report linked title, callback
  policy, and event-shaped next check; end the turn.
- **One bounded wait:** one `wait_threads` only when this response needs a short
  result or serial dependency. Event or timeout ends it; timeout and silence
  are non-terminal and never start another wait automatically.
- **User pull:** on the next user request, take one relevant
  `wait_threads(timeoutMs: 0)` snapshot or read; skip unrelated sessions.
- **Explicit heartbeat:** only for requested continuous or unattended follow-up,
  with targets, notification, and stop conditions. It is periodic wake-up, not
  a completion event.

`wait_threads` can wait for an event only while the current controller turn is
running. A worker `send_message_to_thread` callback starts a new controller
turn. If new user input arrives during a wait, handle the new intent and
reassess the control plan before resuming prior coordination. Never replace
these mechanisms with high-frequency polling.

For every dispatched outcome, read
[references/callbacks.md](references/callbacks.md) before selecting its policy,
writing its callback contract, or consuming a callback. Its policies are
`terminal_once`, `urgent_only`, `cohort_lead`, and `heartbeat-pull`; routine
progress does not callback by default.

## Accept completion claims

A worker terminal is a claim about the assigned outcome, not parent or project
closure. A finished turn or stage is only a milestone or dependency release
while required work remains. Before accepting a terminal, invoke
`codex-session-naming` and apply its full closure contract. Use
[references/callbacks.md](references/callbacks.md) only to validate the claim
without replaying the worker. Release the assigned owner only after every
naming condition holds; evaluate the parent outcome independently before
changing a parent or project title.

If later feedback or evidence challenges original acceptance, invoke naming to
reopen that outcome and preserve the old claim. Route an independent request as
new scope instead of rewriting valid closure.

## Monitor and report

Read status on user request, registered callback, or dependency/resource
change. If the chosen wait capability is absent, use the nearest safe mode and
disclose the gap.

Default global-controller reports should lead with:

1. user decisions or actions required
2. real exceptions and blockers
3. one compact portfolio summary for everything else

Whenever a controller report lists a session or its progress, make the session
title a one-click Markdown link using its tool-returned `threadId`:
`[<title>](codex://threads/<threadId>)`. Alongside each non-current session
link, show its owning `hostId`. Use this app deeplink for navigation; create a
share link only when the user explicitly asks to share the session.

Keep normal background work out of user action items; distinguish
automation-ready from user, device, security, or production acceptance.

Use these controller-role titles unless the user requests another style:

```text
🕹️ 全局主控 · YYYY-MM-DD
🗂️ <Project> 项目主控 · YYYY-MM-DD
✅ 🗂️ <Project> 项目主控 · YYYY-MM-DD
🗑️ <旧主控名称>
```

Current controllers keep their role title while waiting or blocked; report that
state in the controller summary. A global controller remains current when its
portfolio is temporarily empty and closes only on explicit user request. A
project controller gains `✅` only when its main project outcome satisfies the
`codex-session-naming` closure contract. Only an accepted successor may retitle
the predecessor with `🗑️`.

Keep completed sessions unarchived unless the user sets a narrower retention
policy. Confirmed accidental duplicates and accepted predecessor controllers
are the default exceptions. Never delete a session.

## Handoff

Read and follow [references/handoff.md](references/handoff.md) for every
successor creation or takeover, and for fresh, degraded, or user-requested
recovery. Controller handoff never uses fork.
