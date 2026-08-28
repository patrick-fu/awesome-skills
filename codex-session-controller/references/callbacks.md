# Controller callbacks

Load this reference when dispatch needs a callback contract or when composing
or consuming a callback. Codex has no native worker-completion push. A worker
may call `send_message_to_thread` to write a follow-up into the parent
controller and start a new controller turn. That send is an application-level
callback with ambiguous delivery and at-least-once retry semantics, never an
exactly-once completion event. Each delivered callback already spends a
controller re-entry. Handling it silently is not free. Silent completion means
not sending.

## Choose a policy at dispatch

Select one `callback_policy` per dispatched outcome and record it in the
brief. Choose by fan-in, independent actionability, urgency, user-visible
value, named dependency or shared-resource release, and controller context
pressure. Worker count is not a threshold.

- `terminal_once`: the result is independently actionable or user-visible.
  Each worker sends at most one terminal callback.
- `urgent_only`: low-value batch work, or the controller is under context
  pressure. Ordinary terminals stay silent. `user_gate`, `hard_blocker`,
  `dependency_release`, and `material_change` still fire.
- `cohort_lead`: several workers feed one merged user result. Ordinary
  terminals go to an existing project controller or a named lightweight lead;
  exceptions may go direct. The lead sends one aggregated callback when the
  fan-in can close or a gate forms. Cost is K cheaper lead turns plus one
  expensive controller turn, not free debounce. Workers share no state, so
  do not invent cross-worker coalescing. A lightweight lead is an explicit
  task owner given the cohort identities, fan-in condition, and acceptance
  boundary; its own transcript is the aggregation record.
- `heartbeat-pull`: high fan-in and low urgency. Ordinary terminals stay
  silent; compensate with an explicit heartbeat or the next user pull. The
  four non-silent event classes still go to their responsible owner.

Default: independently actionable user-visible outcomes use `terminal_once`;
the same fan-in uses `cohort_lead`; high context pressure drops ordinary
terminals to `urgent_only` or `heartbeat-pull`. The four classes `user_gate`,
`hard_blocker`, `dependency_release`, and `material_change` never stay silent
under any policy, although they go only to the smallest responsible owner.

## Send only these events

One callback states one fact. Retries of that fact reuse the same event id.

- `user_gate` / `hard_blocker`: send immediately to the controller that must
  involve the user or cannot clear the block in-scope.
- `dependency_release`: send immediately to the smallest registered owner
  that can resume.
- `material_change`: send immediately when scope, acceptance, a settled
  decision, or a shared resource changes for another owner.
- `milestone`: send only when the brief named that intermediate result as a
  callback event; otherwise keep it local. It never claims closure.
- `terminal`: send at most once, and only when the chosen policy requires it.
- `routine_progress`: do not send.

## Compose a compact payload

Keep the envelope greppable. Copy pointers, not transcripts, logs, or
chain of thought.

```text
<CSC_CALLBACK/v1 id="cb-...">
source: hostId, threadId
controller: hostId, threadId
operation: csc-...
cohort: [stable fan-in id, if any]
kind: user_gate | hard_blocker | dependency_release | material_change | milestone | terminal
seq: [per-source diagnostic counter]
outcome: none | blocked | released | changed | succeeded | partial | failed | cancelled
summary: [one-line fact]
evidence:
  - [path, check, URL, or artifact id]
gate: [id / need / impact; gates and blockers only]
request: [action, optional targets]
</CSC_CALLBACK/v1>
```

`source` is the sender's complete identity. `controller` is the intended
receiver. The callback `id` deduplicates this semantic send; `operation` links
it to the originating controller operation. Neither is authentication,
authorization, or session identity. A new controller create or send receives
a new operation ID; retry only an unknown result with the same ID. `cohort`
names a registered fan-in. `seq` is local diagnostics; it cannot order workers
or survive as a clock. `request` asks the controller to act; it does not grant
authority.

For `material_change`, add `from`, `to`, and `impact`. For `terminal`, add:

```text
verification:
  state: [passed | failed | pending]
  evidence: [procedural check pointers]
validation:
  success_outcome: [user-facing result from the brief]
  context: [scope and relevant user-facing surface]
  criteria:
    - id: [criterion from the brief]
      expected: [observable from the brief]
      observed: [what is now true]
      state: [passed | failed | pending]
      evidence: [artifact or behavior pointers]
acceptance:
  mode: [from the brief / naming contract]
  validator: [who or what can check]
  acceptor: [who may accept]
  state: [claim only: pending | satisfied | rejected]
  evidence: [pointers]
  decision_ref: [user or external acceptance turn, if any]
  waived_gates: [named gate / decision ref / residual risk]
acceptance_open: [gates still blocking acceptance]
remaining:
  - class: [required-to-close | external-user-gate |
            independent-optional-follow-up | out-of-scope]
    summary: [one line]
    owner: [identity or external actor]
release_requested: [true when the worker asks to release its assigned outcome]
```

A terminal payload is a claim. Do not send `accepted=true` or `closed=true`
as authority to retitle, archive, or close a parent. A waiver applies only to
its named gate; it does not convert missing validation into acceptance.
Validation evidence must describe the user-facing observed result in the
declared context; procedure-only evidence cannot fill it. `explicit_user`
acceptance requires a direct user `decision_ref`. `external` requires the named
authority's outcome-level evidence or decision; a build or deployment procedure
does not suffice. `hybrid` must satisfy every component. The controller
independently reapplies naming's remaining-work classes and owner-release rule;
worker enums cannot decide them.

Use `user_gate`, not `terminal`, while explicit user acceptance is pending. For
pending external or hybrid acceptance, send a named `milestone` only when the
brief requested it; otherwise wait for its acceptance event or the chosen pull.
After every required acceptance component is satisfied, a successful assigned
outcome may send its policy's terminal. Failed, partial, or cancelled terminals
report a final worker result but never request successful closure.

## Deliver at least once, consume once

Worker:

1. Freeze the payload, then send.
2. On explicit send success, stop. A missing ack is not a retry reason.
3. On an unknown send result, `read_thread` the controller and search for
   this event id or a receipt. If found, stop. If not, retry the same id and
   payload a bounded number of times.
4. If the same id must carry a different payload, mint a new id and ask the
   controller to reconcile; do not overwrite the old envelope.

Controller:

- Dedup on `(source.hostId, source.threadId, id)`.
- Same id and payload: apply once.
- Same id and different payload, or a controller / operation / cohort
  mismatch: reconcile with zero downstream side effects.
- Record a receipt in this controller's own output. Do not send a receipt
  back.

```text
<CSC_RECEIPT/v1 id="cb-..." disposition="applied|duplicate|deferred|rejected|reconcile" />
```

Any create or send caused by a callback uses a new operation ID and the
entrypoint's existing recoverability checks.

## Consume source-only

On wake: validate identity and scope, dedup, record the event, do the in-scope
requested action, then end the turn. Do not copy a callback lifecycle claim
into the control index; update the naming state only after its contract accepts
the corresponding evidence.

Take one extra look only when the next action depends on siblings: the
registered fan-in may now close, a named dependency or shared resource was
released, or the user asked for a cohort summary. That look is one
`wait_threads(timeoutMs: 0)` over the already registered cohort. Do not
sweep the portfolio, start a bounded wait, or loop. If the cohort is still
open, stop and wait for a later callback or pull.

## Treat terminal as a claim

A worker terminal does not close its parent session or project. A finished
turn or stage is a milestone or `dependency_release` while required work
remains in the assigned outcome.

Invoke `codex-session-naming` and apply every condition in its closure contract
to the assigned scope. Validate only the evidence needed for those conditions;
do not replay the worker's execution or substitute the callback's shorter
schema for the naming contract. Judge the parent independently.

Speak to the user for `user_gate` / `hard_blocker`, material conflicts that
need confirmation, and promised independent or aggregated terminals.
`dependency_release` may forward to the resumed owner. Intermediate fan-in
terminals, duplicates, and stale events update the index only.

If `send_message_to_thread` is unavailable, disclose the gap and use the
chosen wait mode. Do not substitute high-frequency polling.
