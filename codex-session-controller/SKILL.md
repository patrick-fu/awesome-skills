---
name: codex-session-controller
description: >-
  Use in a user-designated top-level Codex App controller session to establish
  or resume control, route work, preserve user intent, handle natural worker
  reports, verify closure, and hand off ownership.
---

# Codex Session Controller

Control user-visible top-level Codex tasks through thread tools. Treat task,
thread, session, chat, and conversation as the same object. Controlled workers
and successors are user-visible top-level tasks created with `create_thread` or
continued by formal `(hostId, threadId)` identity.

## Control

**Thin:** own intent, authority, owner, dependencies, acceptance, conflicts,
and user gates. Workers own domain research, design, implementation, diagnosis,
review, and testing. Stop exploring as soon as those control dimensions are
clear enough to route faithfully; ask the worker for missing domain evidence.
The controller runs this control loop; each worker executes and reports its
assigned outcome.

The user normally talks only to the controller. Recommend direct worker
discussion only for high-bandwidth technical or artifact iteration. Relay a
newer material user decision to the responsible owner without asking the user
to repeat it.

**Re-enter:** apply this control loop whenever a user-designated controller
receives a worker report or resumes after compaction. Role evidence comes from
the user request, owned transcript, or this session's `🕹️`/`🗂️` controller
title. A `🔀` title, an explicit user role end, or another session's accepted
ownership of this scope ends this role;
late reports route to the accepted successor when one exists.

Keep a lightweight active-outcome index: `(hostId, threadId)`, outcome,
authority, state, and the next evidence that could change the action. The owned
transcript is authoritative; the index is its lightweight view.

Classify each invocation before changing state:

- **one-shot:** inspect or operate on sessions without changing this role
- **global:** explicitly requested portfolio control
- **project:** explicitly requested multi-outcome control for one named project
- **successor:** explicit takeover or handoff

The current session assumes the requested role unless the user asks for a new
one. Keep at most one current global controller and one per project. Route
unrelated work to the global controller and narrow work to its project owner.

## Resolve

Inspect current thread-tool schemas before use; schemas drift. Core operations
are `list_projects`, `list_threads`, `read_thread`, `create_thread`,
`send_message_to_thread`, and `set_thread_title`. `wait_threads`, archive, pin,
and share are optional; disclose degradation and use the nearest safe path.

**Identity:** a non-current session is `(hostId, threadId)` and a saved project
is `(hostId, projectId)`. Establish identity and completion from complete task
records; use titles, paths, previews, timestamps, and status to locate
candidates. Read a known identity directly. Search all connected hosts when
owner identity is ambiguous or when establishing or taking over global control.
Read competing candidates and ask the user to choose.

**Evidence:** use `read_thread` first. Treat empty or failed reads, repeated
blank turns, missing user/assistant/tool-call records, and contradictions as
suspicious. Then inspect the owning host's persisted rollout under
`$CODEX_HOME/sessions` (normally `~/.codex/sessions`) by `threadId`; tolerate
schema drift and read only the needed records. Persisted rollout wins for
persisted history; query it on the owning host.

Only an actual tool call, delivered message, or assistant report proves a
relay. A quoted prompt, example, command, or tool output is only a search lead.
Idle, silence, timeout, `notLoaded`, empty turns, refreshed timestamps, and
missing local rollout leave state unresolved. An evidence gap preserves the
session, owner, lifecycle, and routing.

## Route

Continue the existing owner for the same outcome. Create a normal task only for
an independent outcome, and a project controller only on explicit request.
Handoff, cross-host execution, and irreversible external action retain their
specific authority gates.

Default work to the controller host; use another host only when the user chooses
it. Before every create, call `list_projects` and resolve an existing saved
project from host, natural project, repository or path, and user intent. Use
only a `projectId` returned for that host. Multiple safe candidates or no safe
match is a user gate: ask the user to choose an existing project or save one.

Before sending, search that project for an existing owner. Retain the source
controller, target project and environment, exact brief, and the before/after
task set as internal delivery evidence.

Create in that project's local/direct environment by default, including
non-repository work, current-tree or cross-directory access, read-only state,
aggregate projects, and requests for Full Access. Use a Codex-managed worktree
only for independent writes in a verified Git project when current uncommitted
state is not required. Let Codex create managed worktrees. Every new task uses
an existing saved-project target.

Create and follow-up inherit model and reasoning settings unless the user
changes them in that turn. A normal follow-up uses only `threadId`, `hostId`,
and natural-language `prompt`. Use `codex-session-naming` for owned
non-controller titles and carry that requirement into new tasks.

Coordinate independent work only when dependencies and exclusive resources
allow. Track each shared resource's owner and release condition. Project
controllers keep ordinary reports internal; they notify global control only for
a user gate, cross-project conflict, hard blocker, portfolio-affecting change,
project final, or handoff. For fan-in, workers report to one lead and the lead
sends one consolidated report. Use `/goal` only for an explicit durable project
objective with a verifiable stop.

## Relay

**Lossless:** initial dispatch carries the complete user request; later
steering carries only its delta. Every unmentioned dimension stays unchanged.
Keep user requirements distinct from sourced control facts and explicitly
non-binding suggestions. Add only the smallest boundary required by platform,
safety, permission, existing authorization, or repository rules.

A new worker brief reads like a normal assignment and stands on its own. State
the outcome, user details, permission boundary, evidence and acceptance needed,
reporting destination, and decisions or access that require a pause. Ask for a
concise report at meaningful completion, hard blocker, or user decision: actual
result, evidence, remaining work, and the impact of each choice.

Give a new session the accessible paths, links, or content it needs. If these
cannot carry the work safely, request a suitable carrier. **Fidelity:** compare
the brief with the user request so every detail remains traceable and owner,
acceptance, publication, write, timing, tool, and host scope stay unchanged.
Ask when ambiguity would change direction; otherwise normalize meaning.

## Recover delivery

`create_thread` and `send_message_to_thread` may return an unknown result. Use
the environment, actual messages, and formal task records as the delivery
ledger. Treat delivery as uncertain until that evidence resolves it.

**Create:** formal identity begins at `(hostId, threadId)`. While client setup is
pending, report that state and verify it on the next user pull. After an unknown
result, list and read the resolved project:

- one matching task that has only the dispatched work is the result; reuse it
- multiple matching tasks require evidence review; keep valid independent work
  and retire only a confirmed duplicate when archive is available
- a definitive non-creation result permits one identical bounded retry
- no match or an incomplete projection keeps delivery unresolved
- unresolved delivery preserves the current owner; a retry requires explicit
  tool evidence that creation did not occur

After formal identity exists, verify host, saved project, environment,
permission profile, and initial brief. Inspect rollout when the resulting task
projection is suspicious. Ownership begins after the task satisfies those
qualifications and its access meets the assignment; otherwise re-resolve the
saved project.

**Follow-up:** after an unknown send, read the target and classify delivery.
Delivered work ends recovery. Definitive non-delivery or a demonstrably harmless
repeat permits one identical retry. An absent message remains unresolved until
delivery evidence settles it; the original scope, owner, and evidence gap stay
unchanged.

## Reports and return

Application-level `send_message_to_thread` starts a new controller turn.
Independent workers report once at meaningful completion. Urgent blockers,
user decisions, dependency releases, and material changes report immediately.
In a fan-in, workers report to the lead and the lead reports when the group can
move.

**Understand:** read a report by meaning. Actual delivery identifies the source
and receiver. A sufficient report explains what happened, points to evidence,
and says what remains or what decision is needed. Acknowledge clear reports and
state the next step; ask one focused question for material gaps.

**Deduplicate:** use the actual message or turn locator when stable. Otherwise
compare source identity, substantive claim, and evidence. Apply each fact and
evidence pair once. Conflicting reports require evidence review or
clarification. Ambiguous repetition keeps repeatable action pending.

**Authorize:** authority continues to come from the existing contract, user
approval, identity, evidence, and action-specific gates. Apply these before
archive, handoff, owner change, cross-host action, publication, Git or
credential change. Treat a completion report as a claim entering acceptance.

After dispatch, verify formal identity, report the linked title, reporting
expectation, and next meaningful evidence, then end the turn. One bounded
`wait_threads` may target only the exact task required for a serial result in
the current response; the first result or timeout ends it. A later user pull
makes one `wait_threads(timeoutMs: 0)` call over only the requested tasks. Use
periodic heartbeat only on explicit request with targets and stop conditions.
New user input supersedes an active wait.

## Accept and report

Verify a worker's evidence before changing lifecycle, releasing a dependency,
or accepting writes. Determine from the latest user intent whether the report
concerns an intermediate checkpoint or the promised final boundary. Invoke
`codex-session-naming` and apply its completion contract without replaying the
worker. Closure advances when the evidence resolves the claim; until then the
owner, archive state, and dependent work stay unchanged.

Report user actions first, real exceptions second, then one compact portfolio
summary. Link every listed non-current session as
`[<title>](codex://threads/<threadId>)` and show its `hostId`. Share only on
explicit request.

Controller titles are `🕹️ 全局主控 · YYYY-MM-DD` or
`🗂️ <Project> 项目主控 · YYYY-MM-DD`. Prefix `🏁` only after the role
or project final closes, and `🔀` only after accepted handoff. A global final
requires the user to end its role. Keep completed sessions unarchived unless
the user sets another policy; confirmed duplicates and accepted predecessors
are the exceptions. Archive is the terminal visibility action; retain session
history.

## Handoff

**Handoff:** for successor creation, takeover, or degraded recovery, read and
follow [references/handoff.md](references/handoff.md). Ownership changes only
after its acceptance path.
