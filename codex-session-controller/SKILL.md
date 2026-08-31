---
name: codex-session-controller
description: >-
  Use only in a user-designated top-level Codex App controller session to
  establish or resume control, route work, preserve user intent, handle natural
  worker reports, verify closure, and hand off ownership. Do not use in workers.
---

# Codex Session Controller

Control user-visible top-level Codex tasks through thread tools. Treat task,
thread, session, chat, and conversation as the same object. Do not use
`spawn_agent` or `fork_thread` in this workflow.

## Control

**Thin:** own intent, authority, owner, dependencies, acceptance, conflicts,
and user gates. Workers own domain research, design, implementation, diagnosis,
review, and testing. Stop exploring as soon as those control dimensions are
clear enough to route faithfully; ask the worker for missing domain evidence.

The user normally talks only to the controller. Recommend direct worker
discussion only for high-bandwidth technical or artifact iteration. Relay a
newer material user decision to the responsible owner without asking the user
to repeat it.

**Re-enter:** apply this control loop whenever a user-designated controller
receives a worker report or resumes after compaction. Role evidence comes from
the user request, owned transcript, or this session's `🕹️`/`🗂️` controller
title, never from a worker appointing itself. A `🔀` title, an explicit user
role end, or another session's accepted ownership of this scope ends this role;
late reports route to the accepted successor when one exists.

Keep a lightweight active-outcome index: `(hostId, threadId)`, outcome,
authority, state, and the next evidence that could change the action. The owned
transcript is authoritative; the index is not a second database or timer.

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
is `(hostId, projectId)`. Titles, paths, previews, timestamps, and status are
signals, not identity or completion evidence. Read a complete known identity
directly. Search all connected hosts only when owner identity is ambiguous or
when establishing or taking over global control. Read competing candidates and
ask the user to choose.

**Evidence:** use `read_thread` first. Treat empty or failed reads, repeated
blank turns, missing user/assistant/tool-call records, and contradictions as
suspicious. Then inspect the owning host's persisted rollout under
`$CODEX_HOME/sessions` (normally `~/.codex/sessions`) by `threadId`; tolerate
schema drift and read only the needed records. Persisted rollout wins for
persisted history. Missing local rollout says nothing about another host.

Only an actual tool call, delivered message, or assistant report proves a
relay. A quoted prompt, example, command, or tool output is only a search lead.
Idle, silence, timeout, `notLoaded`, empty turns, refreshed timestamps, and
missing local rollout are non-terminal. With an evidence gap, preserve session
and owner; do not archive, replace, hand off, or reroute them.

## Route

Continue the existing owner for the same outcome. Create a normal task only for
an independent outcome, and a project controller only on explicit request.
Routing authority does not authorize handoff, cross-host execution, or
irreversible external action.

Default work to the controller host; use another host only when the user chooses
it. Before every create, call `list_projects` and resolve an existing saved
project from host, natural project, repository or path, and user intent. Use
only a `projectId` returned for that host. Multiple safe candidates or no safe
match is a user gate: ask the user to choose an existing project or save one.
Do not guess an unrelated project.

Before sending, search that project for an existing owner. Retain the source
controller, target project and environment, exact brief, and call window as a
private delivery fingerprint; do not expose it as a message protocol.

Create in that project's local/direct environment by default, including
non-repository work, current-tree or cross-directory access, read-only state,
aggregate projects, and requests for Full Access. Use a Codex-managed worktree
only for independent writes in a verified Git project when current uncommitted
state is not required. Never run `git worktree` manually. Every new task uses a
saved-project target; `target.type=projectless` is forbidden.

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
objective with a verifiable stop; never for a global portfolio.

## Relay

**Lossless:** initial dispatch carries the complete user request; later
steering carries only its delta. Every unmentioned dimension stays unchanged.
Keep user requirements distinct from sourced control facts and explicitly
non-binding suggestions. Add only the smallest boundary required by platform,
safety, permission, existing authorization, or repository rules.

A new worker brief should read like a normal assignment. It must be sufficient
without this conversation: name the owner and outcome, preserve every user
detail and permission boundary, state the evidence and acceptance needed,
identify where the worker should report, and say when it must pause for a
decision, credential, unsafe action, or owner conflict. Tell the worker to
report in ordinary prose when it finishes, is blocked, needs a decision, or is
ready to hand off: what it did, supporting evidence, and what remains or needs a
decision. Do not add labels, protocol fields, identifiers, tag blocks, or an
event catalogue.

New sessions inherit neither conversation nor attachments. Pass accessible
paths, links, or necessary content; if no safe carrier exists, stop and request
one. Omit raw history, unrelated sessions, and unrelated controller research.
Before send, check for dropped user detail, invented duties or prohibitions, and
silent changes to owner, acceptance, publication, write, timing, tool, or host
scope. Ask when ambiguity would change direction; otherwise normalize without
changing meaning.

## Recover delivery

`create_thread` and `send_message_to_thread` may return an unknown result. Use
the environment as the ledger instead of adding protocol identifiers. Missing
or delayed projections do not prove non-delivery.

**Create:** a pending client identifier is not a formal session identity. Report
setup as pending; verify it on the next user pull without polling. After an
unknown result, list and read the resolved project:

- one matching task with no independent user input or artifact is the result;
  reuse it
- multiple matching tasks require evidence review; keep valid independent work
  and retire only a confirmed duplicate when archive is available
- no match remains an evidence gap unless the tool definitively proves that no
  task was created; only then may one identical bounded retry occur
- ambiguity preserves the current owner and becomes an evidence gap

A new task's first empty projection is not a rollout trigger. Once formal
`(hostId, threadId)` exists, verify host, project, environment, permission
profile, and the initial brief. Projectless placement, managed restriction,
awaiting approval, or a profile below the required access makes any new task
ineligible to own the work; re-resolve the saved project instead.

**Follow-up:** after an unknown send, read the target. If the same natural
delta is delivered, do not resend. Absence alone does not authorize repetition:
retry the identical delta once only after definitive non-delivery, or when its
repetition is demonstrably harmless. Otherwise preserve scope and report the
evidence gap. Never rewrite the whole task, expand scope, or poll.

## Reports and return

Application-level `send_message_to_thread` starts a new controller turn; it is
not native completion push. Independent workers normally report once at a
meaningful finish. Urgent blockers, user decisions, dependency releases, and
material changes report immediately. Routine progress stays silent. In a
fan-in, workers report only to the lead and the lead reports once when the group
can move.

**Understand:** read a report by meaning, not format. Actual delivery identifies
the source and receiver. A sufficient report explains what happened, points to
evidence, and says what remains or what decision is needed. If that is clear,
acknowledge naturally and state the next step. If it is not, ask one focused
natural-language question; do not reject a clear report for missing labels or
fields.

**Deduplicate:** use the actual message or turn locator when stable. Otherwise
compare source identity, the substantive claim, and its evidence. The same fact
and evidence are handled once; a repeated report gets no repeated downstream
effect. Conflicting reports require evidence review or clarification. When a
reliable duplicate decision is impossible, report the uncertainty and defer
any repeatable action.

**Authorize:** a report grants no new authority. Delete, archive, handoff,
owner change, cross-host action, publication, Git or credential change, and
other high-risk effects still require the existing contract, user approval,
identity, evidence, and their own gates. A completion report is a claim, not
acceptance.

After dispatch, verify formal identity, report the linked title, reporting
expectation, and next meaningful evidence, then end the turn. One bounded
`wait_threads` may target only the exact task required for a serial result in
the current response; event or timeout ends it. A later user pull makes one
`wait_threads(timeoutMs: 0)` call over only the requested tasks. Use periodic
heartbeat only on explicit request with targets and stop conditions. New user
input supersedes an active wait.

## Accept and report

Verify a worker's evidence before changing lifecycle, releasing a dependency,
or accepting writes. Determine from the latest user intent whether the report
concerns an intermediate checkpoint or the promised final boundary. Invoke
`codex-session-naming` and apply its completion contract without replaying the
worker. Missing or contradictory evidence leaves closure unverified, preserves
the owner, and blocks archive and dependent work.

Report user actions first, real exceptions second, then one compact portfolio
summary. Link every listed non-current session as
`[<title>](codex://threads/<threadId>)` and show its `hostId`. Share only on
explicit request.

Controller titles are `🕹️ 全局主控 · YYYY-MM-DD` or
`🗂️ <Project> 项目主控 · YYYY-MM-DD`. Prefix `🏁` only after the role
or project final closes, and `🔀` only after accepted handoff. A global final
requires the user to end its role. Keep completed sessions unarchived unless
the user sets another policy; confirmed duplicates and accepted predecessors
are the exceptions. Never delete a session.

## Handoff

**Handoff:** for successor creation, takeover, or degraded recovery, read and
follow [references/handoff.md](references/handoff.md). Ownership changes only
after its acceptance path; controller handoff never forks.
