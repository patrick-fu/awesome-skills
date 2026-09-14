# Follow-up mechanics

Read for a status check, scheduling, Callback, wrong-level report, or handoff
routing. Mode definitions and defaults stay in [SKILL.md](../SKILL.md).

## Check

Rebuild the requested or directly owned set from the index, known identities,
and `list_threads`. Match the requested depth; global checks normally read
project summaries and standalone tasks, leaving ticket detail to project owners.
Take one snapshot pass with `wait_threads` (`timeoutMs: 0`),
in batches allowed by the current schema. Read task history where a decision
needs more evidence. A missing task or failed read remains unresolved; report
partial coverage when it affects the answer.

Process new evidence and continue work already authorized through its owner.
Healthy progress needs no steering. Under On-demand, return the requested
assessment after this pass; it establishes no ongoing monitoring.

## Scheduled

Use `automation_update` for an owner-targeted heartbeat. Reuse an existing check
that covers the same work. Keep targets and current state in the controller
index; the wakeup prompt is a short, stable reminder to resume from that state.
Retain the user's cadence, expiry, and notification choices. For a new schedule,
state the cadence and stopping conditions when establishing it.

Each wakeup takes one check pass. Stay quiet while the result is unchanged or
non-actionable; notify on meaningful changes under the agreed policy. Continue
independent work, then end the turn while awaiting the next check. A worker
handles an uncovered internal wait through `codex-async-followup` in its own task.

Pause checks that can no longer advance work, preserving the reason and the
condition for resumption. Apply the entrypoint's dependent-wait rule when a
schedule stops or changes. Verify the saved schedule and target before claiming
it is active; a failed update does not establish a future check.

## Callback

Use the user's selected events, typically completion or a blocker requiring the
owner. Provide the child with that destination and those triggers. The direct
owner checks the report, accepts supported results, and continues authorized
work. Normal progress remains in the child unless selected for reporting.

When Callback supplements Scheduled, apply the same evidence once regardless
of which path delivers it first. A callback leaves the schedule in place unless
its stopping condition or the user changes it. Avoid acknowledgment exchanges
when no recipient action changes.

## Wrong level

If a ticket report reaches a global controller, identify its direct owner from
authoritative task records and forward it unchanged with a short address
correction. Leave acceptance and task decisions to that owner. If the owner is
unresolved, preserve the report and resolve its destination before forwarding.

## Handoff routing

After [handoff](handoff.md) verifies ownership acceptance, rebind Callback
destinations that named the predecessor. Forward late reports unchanged until
the new route is confirmed; the successor deduplicates them and owns acceptance.
Transfer Scheduled checks only when the tool supports the target change;
otherwise the successor establishes the replacement and the predecessor retires
the old check. Verify the saved recipient, active/paused state, cadence, expiry,
and pending waits before retiring the predecessor, with one active check per
purpose. On-demand needs no rebind. A global handoff leaves project-internal
routes with their project controller.
