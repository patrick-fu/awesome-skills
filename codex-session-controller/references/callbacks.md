# Controller callbacks

Load this reference before choosing a callback policy, writing its contract, or
consuming a callback. Codex has no native worker-completion push. A worker can
use `send_message_to_thread` to write a follow-up that starts a controller turn,
but delivery is ambiguous and never exactly-once. Every delivered callback
spends a re-entry; silent completion means not sending one.

## Choose one policy at dispatch

Record one `callback_policy` per outcome. Choose by fan-in, independent
actionability, urgency, user-visible value, dependency or shared-resource
release, and controller context pressure—not a fixed worker count.

- `terminal_once`: each independently actionable or user-visible result sends
  at most one terminal callback.
- `urgent_only`: ordinary terminals for low-value batches or a pressured
  controller stay silent.
- `cohort_lead`: ordinary terminals for one merged result go to an existing
  project controller or explicit lightweight lead; exceptions may go direct.
  The lead owns cohort identities, fan-in and acceptance boundaries in its
  transcript, then sends one aggregate callback when fan-in closes or a gate
  forms. This costs lead turns plus one controller turn; workers share no state.
- `heartbeat-pull`: ordinary terminals for high fan-in, low-urgency work stay
  silent; an explicit heartbeat or the next user pull compensates.

Default independent outcomes to `terminal_once`, one fan-in to `cohort_lead`,
and pressured controllers to `urgent_only` or `heartbeat-pull`. Under every
policy, `user_gate`, `hard_blocker`, `dependency_release`, and
`material_change` go immediately to the smallest responsible owner.

## Send only meaningful events

One callback states one fact; retries reuse its event id.

- `user_gate` / `hard_blocker`: user involvement or an in-scope impasse.
- `dependency_release`: the smallest registered owner can resume.
- `material_change`: scope, acceptance, a settled decision, or a shared
  resource changes for another owner.
- `milestone`: only an intermediate result named by the brief; never closure.
- `terminal`: at most once when policy requires it.
- `routine_progress`: never send.

## Use the wire schema

Copy pointers, not transcripts, logs, secrets, or chain of thought.

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

`source` is the sender's complete identity; `controller` is the intended
receiver. `id` deduplicates this semantic send, while `operation` associates it
with the originating controller operation. Neither grants authority or replaces
session identity. `cohort` names a registered fan-in. `seq` is diagnostic, not
a cross-worker clock. `request` asks for action; it does not authorize it.

Add `from`, `to`, and `impact` to `material_change`. Add this projection to
`terminal`:

```text
verification:
  state: [passed | failed | pending]
  evidence: [procedural check pointers]
validation:
  success_outcome: [user-facing result from the brief]
  context: [scope and user-facing surface]
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
release_requested: [true when worker asks to release its assigned outcome]
```

Every terminal field is a worker claim. Never use `accepted=true` or
`closed=true` to retitle, archive, or close any outcome. Invoke
`codex-session-naming`: the controller independently checks remaining work and
owner release, and callback enums cannot close an assigned or parent outcome.
A waiver covers only its named gate and cannot replace missing validation.
User-facing validation cannot use procedure-only evidence; `explicit_user`
needs a direct user `decision_ref`, `external` needs named-authority outcome
evidence or decision, and `hybrid` needs every component. While acceptance is
pending, do not send `terminal`: send `user_gate` for explicit user acceptance,
or a named `milestone` for external/hybrid only when requested. Failed,
partial, or cancelled terminals never request successful closure.

## Deliver ambiguously, consume once

Worker:

1. Freeze the payload, then send.
2. Explicit success ends delivery; a missing acknowledgment is not a retry
   reason.
3. After an unknown result, `read_thread` the controller for the event id or a
   receipt. If absent, retry the same id and payload a bounded number of times.
4. Changed payloads use a new id and request reconciliation.

Controller:

- Deduplicate on `(source.hostId, source.threadId, id)` and apply an identical
  retry once.
- Reconcile a changed payload or controller, operation, or cohort mismatch with
  zero downstream side effects.
- Record the receipt in the controller output; do not send it back.

```text
<CSC_RECEIPT/v1 id="cb-..." disposition="applied|duplicate|deferred|rejected|reconcile" />
```

Any callback-triggered create or send uses a new operation ID and the
entrypoint's recoverability checks.

## Consume source-only

On wake, validate identity and scope, deduplicate, record the event, perform the
in-scope request, then end the turn. Update naming state only after its closure
contract accepts the evidence; never copy a callback lifecycle claim into the
control index or replay the worker's execution.

Take one extra look only when registered fan-in may close, a named dependency
or shared resource was released, or the user requested a cohort summary. Use
one `wait_threads(timeoutMs: 0)` over that cohort. Do not sweep the portfolio,
start a bounded wait, loop, or poll. If the cohort remains open, wait for a
later callback or pull.

Speak to the user for gates, hard blockers, conflicts needing confirmation, and
promised independent or aggregate terminals. Forward a dependency release to
its consumer; intermediate fan-in terminals, duplicates, and stale events only
update the index. If `send_message_to_thread` is unavailable, disclose the gap
and use the chosen wait mode.
