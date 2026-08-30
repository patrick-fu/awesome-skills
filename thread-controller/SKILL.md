---
name: codex-session-controller
description: >-
  Use one top-level Codex App session as a thin control plane for other
  top-level sessions: route work, preserve user intent, coordinate callbacks,
  verify closure, report progress, and hand off ownership.
disable-model-invocation: true
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
discussion only for high-bandwidth technical or artifact iteration. A newer
user decision applies where received; relay a material change to its controller
without asking the user to repeat it.

Keep a lightweight active-outcome index: `(hostId, threadId)`, outcome, scope or
authority, state, and event-shaped next check. The owned transcript is
authoritative; the index is not a second database or polling state machine.

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
directly. When identity or owner is ambiguous, or when establishing or taking
over global control, search active, unarchived, pinned, and recent sessions on
all connected hosts; go older only when required. For project work match the
natural project, host, returned project, paths, and transcript. Read competing
candidates and ask the user to choose.

**Evidence:** use `read_thread` first. Treat empty or failed reads, repeated
blank turns, missing user/assistant/tool-call records, and contradictions as
suspicious. Then inspect the owning host's persisted rollout under
`$CODEX_HOME/sessions` (normally `~/.codex/sessions`) by `threadId`; tolerate
schema drift and read only the needed records. Persisted rollout wins for
persisted history. Missing local rollout says nothing about another host.

Only an actual function call, delivered message, or assistant receipt proves a
relay event. A marker inside a prompt, example, command, or tool output is only
a search lead. Validate source, target, and event or operation identity.

Idle, silence, timeout, `notLoaded`, empty turns, refreshed timestamps, and
missing local rollout are non-terminal. With an evidence gap, preserve session
and owner; report the gap and stop lifecycle or ownership actions. Do not
archive, replace, hand off, or reroute them.

## Route

Continue the existing owner for the same outcome. Create a normal task only for
an independent outcome, and a project controller only on explicit request.
Giving work to a controller authorizes only this routing policy—not handoff,
cross-host execution, or irreversible external action.

Default work to the controller host. Resolve the saved project there before
dedupe or create; never reuse a `projectId` across hosts. Use another host only
when the user chooses it. For Git repositories, choose a Codex worktree for
independent writes or historical-ref investigation, and the saved project for
read-only current-state work. Include uncommitted state only on explicit ask;
do not run `git worktree` manually.

Create and follow-up inherit model and reasoning settings; pass `model` or
`thinking` only when the user changes it in that turn. A normal follow-up uses
only `threadId`, `hostId`, and `prompt`. Use `codex-session-naming` for owned
non-controller titles and carry that requirement into new tasks.

Coordinate independent work only when dependencies and exclusive resources
allow. Record each shared resource's owner, contenders, and release condition.
Trust owners by default; request targeted correction or evidence on drift, and
separate implementation, review, and integration only when risk or repository
rules require it. Project controllers keep ordinary events internal; they send
global control a separate callback only for a user gate, cross-project conflict,
hard blocker, portfolio-affecting material change, project final, or handoff.
That relay is a new `cb-*` Event, not a `csc-*` Operation. Use `/goal` only for
an explicit durable project objective with a verifiable stop; never for a
global portfolio.

## Relay

**Lossless relay:** initial dispatch carries the complete user contract;
steering carries only its delta. Every unmentioned dimension remains unchanged.
The same rule governs callback re-entry and handoff.

- **User contract:** authoritative outcomes, details, decisions, and
  constraints.
- **Control contract:** owner, authority, completion, acceptance, callback, and
  defined delivery dimensions (publication, write, timing, tools).
- **Controller context:** only execution-relevant sourced facts or evidence
  gaps; helpful inferences or candidates are explicitly **non-binding**.

Add only the smallest sourced platform, safety, permission, authorization, or
existing-contract boundary. Before send, check for dropped user detail,
invented duty or prohibition, and silent changes to owner, acceptance, or
delivery dimensions. Ask when ambiguity would change direction; otherwise
normalize without changing meaning. Omit unrelated controller exploration;
calling it non-binding does not make it relevant.

For a new task, send the smallest self-contained brief:

```text
User contract: [complete requested outcome, details, decisions, constraints]
Control: [source/target/operation; owner/outcome; completion_role; acceptance;
          user-defined delivery dimensions]
Context: [only execution-relevant facts/evidence gaps; helpful non-binding candidates]
Mandatory boundary: [source-labelled; omit when none]
Pause: [missing decision/credential; unauthorized destruction; owner conflict;
        direction-changing ambiguity]
```

Set `completion_role` to `checkpoint` or `final` from the promised boundary,
not thread hierarchy. Callback policy and its single receiver are mandatory;
omit other undefined dimensions rather than inventing them. New sessions
inherit neither conversation nor attachments: pass worker-accessible paths,
links, or necessary content; if no safe carrier exists, stop and request one.
Preserve acceptance criteria and parent identity; omit raw history and unrelated
sessions. A follow-up sends only the user delta, changed control dimensions,
and new non-binding context—never the whole brief again.

Carry only this worker-safe callback directive into a new task:

```text
Callback: [receiver; policy; originating operation; completion_role;
           policy-eligible terminal; task-relevant urgent events]
On a policy-eligible event, send CSC_CALLBACK/v1 with a unique cb id, source,
receiver, originating operation, kind, one-line summary, locatable evidence,
and only its event-specific fields. Set callback_skill=codex-session-controller;
only at send time, form the first line by prefixing its value with a dollar sign.
```

**Dispatch gate:** before `create_thread`, verify the final prompt contains zero
literal `$codex-session-controller`, no canonical callback block or exhaustive
event list, and no user requirement duplicated outside `User contract`. Keep
Control and Callback fields referential; repair transport text, never user text.

## Recover operations

Controller-issued `create_thread` and ordinary follow-up sends are
at-least-once. Wrap each new logical create or follow-up, including its exact
brief or delta, with:

```text
<controller_operation id="csc-..." source="hostId:threadId">
...
</controller_operation>
```

**Operation:** the ID correlates one controller create or ordinary follow-up;
it is not
authority or session identity. Generate a new ID for every new controller-side
effect. Reuse it only to resolve or retry the same unknown result with the same
payload. Every callback, including a controller's relay, is an **Event**: use a
new `cb-*`, do not wrap or mint a transport `csc-*`, and keep its `operation`
bound to that sender's originating dispatch. Only a distinct downstream create
or ordinary worker follow-up triggered by the callback gets a new Operation.

Before create, resolve `(hostId, projectId)` and search that scope for the owner
and operation. A pending/client ID is not identity: wait for formal
`(hostId, threadId)`, then verify host, project, environment, and operation.
A newly created task's first empty projection is not a rollout trigger; verify
its formal identity and operation first. After timeout or unknown delivery,
search and read before a bounded retry; silence is not failure. A duplicate
requires the same operation, source, scope, target, and payload with no
independent input, artifact, or valid work. Archive a confirmed duplicate when
available; otherwise report it.

## Callback and return

Callbacks are the default completion channel. They are application-level
`send_message_to_thread` follow-ups that start a new controller turn, not native
completion push. Every callback costs a re-entry and inherits operation
delivery ambiguity.

### Send

Choose one policy per outcome:

- `terminal_once`: one independently actionable or user-visible terminal
- `cohort_lead`: each worker's sole receiver is the lead; the lead sends one
  aggregate event when fan-in closes
- `urgent_only`: ordinary low-value terminals stay silent under context pressure
- `heartbeat-pull`: high-fan-in, low-urgency terminals wait for an explicit
  heartbeat or user pull; this policy starts neither a wait nor a heartbeat

Default independent work to `terminal_once` and one fan-in to `cohort_lead`.
Under every policy, `user_gate`, `hard_blocker`, `dependency_release`, and
`material_change` immediately notify the registered receiver. `routine_progress`
never sends. Register exactly one controller `(hostId, threadId)`; workers never
fan out the same fact. That receiver forwards a release to its consumer as a new
operation when needed.

**Event:** `cb-*` identifies one immutable semantic callback. `operation`
associates it with the originating dispatch; it is never the event ID. The
following wire is controller-bound only; never copy it into a worker's initial
prompt. Keep each field on one line and point to detail:

```text
$codex-session-controller
CSC_CALLBACK/v1
id=cb-... source=hostId:threadId controller=hostId:threadId operation=csc-...
kind=user_gate|hard_blocker|dependency_release|material_change|
     milestone|terminal
summary="one fact" evidence=[compact pointers] [request="action and target"]
[cohort=...] [gate="id/need/impact"] [change="from/to/impact"]
[completion_role=checkpoint|final outcome=succeeded|partial|failed|cancelled]
END_CSC_CALLBACK
```

Omit optional fields outside their named event. A milestone is `checkpoint`; a
terminal echoes its dispatched role. Only `succeeded` may support successful
closure. Detailed proof stays in the source transcript; the callback carries
locatable pointers. Pending explicit acceptance sends `user_gate`, not terminal.

**Delivery:** freeze the event and payload. Explicit tool success ends sending.
After an unknown result, read the controller for the event ID; if absent, retry
the same ID and payload a bounded number of times. Changed payload means a new
event and reconciliation request.

### Consume

**Latch:** every callback turn invokes this Skill, then validates version,
receiver, source, operation, registered policy, allowed kind, cohort,
completion role, and evidence carrier. A mismatch records `reconcile` with zero
downstream effects. The callback contract is incomplete unless its
controller-bound message starts with the literal `$codex-session-controller`
line. Unstructured “done” text is not a callback and triggers neither waiting
nor closure. Malformed or
identity-mismatched input has no side effect.

Deduplicate on `(source.hostId, source.threadId, id)`: apply it once; identical
retries are duplicates. A changed payload under the same ID requires
reconciliation with zero downstream effects. Record exactly one disposition—
`applied`, `duplicate`, `deferred`, `rejected`, or `reconcile`—in the ordinary
controller output, then return. Do not send acknowledgment traffic.

`request` asks for action; it grants no authority. Apply only the source event's
in-scope request, report when required, then return. A callback relay stays an
Event; a distinct create or ordinary worker follow-up requested after
consumption gets a new Operation. Look once at the same cohort with
`wait_threads(timeoutMs: 0)` only when registered fan-in may close, a dependency
or resource released, or the user asks for its summary. Never sweep the
portfolio, start another wait, or poll.

After dispatch, verify formal identity, report its linked title, policy, and
next event, then end the turn. One bounded `wait_threads` may target only the
exact task needed for a serial result in the current response; event or timeout
ends it. A later user pull makes one `wait_threads(timeoutMs: 0)` call over only
the tasks requested in that turn. Use periodic heartbeat only on explicit
request with targets, notification, and stop conditions. If callbacks are
unavailable, disclose the gap and use user pull or explicit heartbeat. New user
input supersedes an active wait and reopens the control plan.

## Accept and report

**Claim, not closure:** milestone and terminal events never close an outcome.
Invoke `codex-session-naming`, apply its completion contract without replaying
the worker, and render the resulting state. Reconcile a role mismatch; reopen
original scope on contrary evidence and route an independent new request
separately.

Read status only on user pull, valid callback, or registered dependency/resource
event. Report user actions first, real exceptions second, then one compact
portfolio summary. Link every listed non-current session as
`[<title>](codex://threads/<threadId>)` and show its `hostId`. Share only on
explicit request.

Controller titles are `🕹️ 全局主控 · YYYY-MM-DD` or
`🗂️ <Project> 项目主控 · YYYY-MM-DD`. Prefix `🏁` only after the role
or project final closes, and `🔀` only after accepted handoff. A global final
requires the user to end its role; a project final uses the naming contract.
Waiting and blockers stay in the report. Keep completed sessions unarchived
unless the user sets another policy; confirmed duplicates and accepted
predecessors are the exceptions. Never delete a session.

## Handoff

**Handoff:** for successor creation, takeover, or degraded recovery, read and
follow [references/handoff.md](references/handoff.md). Ownership changes only
after its acceptance protocol; controller handoff never forks.
