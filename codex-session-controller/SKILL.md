---
name: codex-session-controller
description: >-
  Codex App-only control of top-level Codex sessions across projects and hosts,
  including global and project controllers, routing, monitoring, deduplication,
  and handoff. Depends on codex-session-naming for session titles; use when the
  user explicitly invokes this controller workflow.
disable-model-invocation: true
---

# Codex Session Controller

Use this skill only when the user invokes it explicitly. Treat Codex task,
thread, session, chat, and conversation as the same user-visible top-level
object when the surrounding request makes that meaning clear.

Operate as a **thin control plane**. Manage top-level Codex sessions through
thread tools; leave research, implementation, diagnosis, review, testing, and
worker-level subagents to the owned sessions. A controller may perform only the
small read-only checks needed to resolve hosts, saved projects, repositories,
existing owners, and acceptance evidence. Do not use `spawn_agent` from a
controller workflow.

## Resolve the invocation

Classify the user's natural-language intent before changing state:

- **One-shot operation:** inspect, create, continue, rename, archive, or take
  over a session without changing the current session's role.
- **Global controller:** manage the user's Codex portfolio across connected
  hosts and projects. When the user explicitly asks to establish a controller
  but names no narrower scope, use this mode.
- **Project controller:** manage multiple outcomes inside one explicitly named
  project. A repository path or a difficult one-off task alone is not an
  instruction to create a project controller.
- **Successor:** replace an existing controller after an explicit handoff or
  takeover request.

The current session becomes the requested controller by default. Create a
separate controller only when the user asks for a new one or requests handoff.
Keep an established controller's scope stable: route an unrelated project back
to the global controller rather than silently widening a project controller;
route a narrow request from the global controller to its project owner rather
than shrinking the global controller.

One current global controller may coexist with one current controller for each
project. Keep project identity lightweight: use the project name together with
the returned host/project, paths, preview, and recent history. Do not invent a
separate scope registry. A project controller may run without a global
controller; a later global controller can discover and manage it.

## Preflight capabilities

Search for and inspect the callable thread tools before relying on remembered
schemas. Controller behavior requires equivalents of:

```text
list_projects
list_threads
read_thread
send_message_to_thread
create_thread
set_thread_title
```

If a required capability is missing, explain the gap and use the evidence
fallback below where it applies. Recommend a fresh controller session only
when no safe degraded path remains. Treat `wait_threads`, archive, pin, and
share as optional: state the degraded behavior when they are absent. Tool
availability and argument schemas can differ between old and new sessions, so
use the schema actually returned in the current session.

## Establish session evidence

Use `read_thread` with its current callable schema as the primary transcript
interface for a known `(hostId, threadId)`. Treat an empty or failed read,
repeated blank turns, a returned history with no user, assistant, or tool-call
items, and contradictions with other evidence as suspicious projections.

For a suspicious projection, inspect the persisted rollout on the owning host
under `$CODEX_HOME/sessions` (normally `~/.codex/sessions`). Locate candidates
with the tool-returned `threadId`, then verify the identity from the metadata
that actually exists. Inspect the observed record types, roles, turn boundaries,
and completion evidence; tolerate unknown records and do not assume fixed field
names, offsets, or one rollout schema. Read only the minimum evidence needed and
do not copy raw transcript content into controller reports.

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

Before establishing a global controller, search all connected hosts for current
global-controller candidates. Inspect active, unarchived, pinned, and roughly
the last 30 days of activity where the available tools expose those views;
search older history only when a project or user request requires it. A unique
current candidate should be reused or handed off. Read multiple candidates and
ask the user to disambiguate.

Before establishing a project controller, search by the project's natural name,
saved project, target host, relevant paths, title, preview, and recent turns. A
unique matching controller is the existing owner. Multiple plausible owners
require user disambiguation.

## Route work

Giving work to an established controller authorizes it to continue an existing
owner or create a normal task session under this routing policy. It does not
authorize a new controller, cross-host execution, handoff, or irreversible
external action unless the user also expresses that intent.

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

Before create, resolve the exact target `(hostId, projectId)` and search that
scope for an owner and for the operation ID. When creation returns only a
pending/client identifier, wait for the formal `(hostId, threadId)`. Once the
formal identity exists, immediately read or list the created session and verify
its host, project, working directory or environment, and operation ID. After an
unknown result or timeout, search and read again before retrying. Do not infer
failure from a missing immediate response.

Treat sessions as confirmed duplicates only when operation ID, source
controller, intended scope, and target match, and the extra session has no
independent user input, unique artifact, or valid work still running. Such a
duplicate may be archived when archive is available; otherwise report it.
Title or prompt similarity alone is never sufficient. Never delete a session.

## Compile a clean task brief

New sessions do not inherit the controller conversation or its attachments.
Synthesize the smallest self-contained brief that lets the owner start safely:

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
[Result, checks, evidence, and completion gates.]

Pause and report if:
[User decision, credentials, destructive action, ownership conflict, or
unresolvable ambiguity.]
```

Include the operation ID and parent controller identity. Preserve exact paths,
links, constraints, decisions, and acceptance criteria; omit the raw controller
history, unrelated sessions, speculative solutions, and verbose orchestration
instructions.

When the global controller sends a directive to a project controller, label the
source, original user intent, authorized boundary, and requested report event.
This keeps forwarded coordination distinct from a direct user decision. A
newer direct user decision in the project controller wins; execute it and send
the material scope or decision change back to the global controller.

## Coordinate without becoming the executor

A project controller owns internal task routing. Notify its global controller
only when it needs a user decision, encounters a cross-project resource
conflict or hard blocker, completes the project, or performs handoff. Users may
also interact with the project controller directly.

Run independent sessions concurrently only when dependencies and resources
allow it. Derive the concurrency budget from the user's request, applicable
`AGENTS.md`, host capacity, and exclusive resources rather than hard-coding a
job count. Record the owner, contenders, and release condition for shared
checkouts, devices, accounts, deployment environments, and production
resources. Send peer identities only to sessions that need them.

Trust an owned session by default and verify the minimum evidence needed for
the current risk. When it visibly drifts, ask the same owner to correct itself
before commissioning an independent review session. Separate implementation,
review, and integration owners when risk or repository rules require it.

Use `/goal` only inside a project controller whose project has one durable
objective, a verifiable stopping condition, and an explicit user request such
as “continue until I need to intervene.” A global portfolio is not one goal.

## Monitor and report

Do not poll continuously by default. Read status when the user asks, when a
dependency or resource boundary changes, or when continuous monitoring was
explicitly requested. Prefer event-driven `wait_threads` when available; when
it is absent, check meaningful checkpoints and disclose the monitoring gap.

Default global-controller reports should lead with:

1. user decisions or actions required
2. real exceptions and blockers
3. one compact portfolio summary for everything else

Whenever a controller report lists a session or its progress, make the session
title a one-click Markdown link using its tool-returned `threadId`:
`[<title>](codex://threads/<threadId>)`. Alongside each non-current session
link, show its owning `hostId` because `(hostId, threadId)` remains the complete
identity. Use this app deeplink for navigation; create a share link only when
the user explicitly asks to share the session.

Do not turn normal background work into user action items. Distinguish
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
project controller gains `✅` only after its project outcome and all required
human/device/production gates complete. Only an accepted successor may retitle
the predecessor with `🗑️`.

Keep completed sessions unarchived unless the user sets a narrower retention
policy. Confirmed accidental duplicates and accepted predecessor controllers
are the default exceptions. Never delete a session.

## Handoff

Read and follow [references/handoff.md](references/handoff.md) whenever the user
asks to create a successor, take over a controller, or recover one whose context,
tools, or runtime are no longer reliable. Controller handoff never uses fork.
