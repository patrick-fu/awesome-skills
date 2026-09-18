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

Select active tasks from substantive user or work activity. Controller notices
and title changes do not make a historical task active. For a bulk operation,
keep the pre-operation selection stable; expand it only on independent evidence.

Process new evidence through its owner under the entrypoint's intervention and
acceptance rules. Under Poll, return the assessment after this pass.

## Scheduled

Use `automation_update` for an owner-targeted heartbeat. Reuse an existing check
that covers the same work. Keep targets and current state in the controller
index; the wakeup prompt is a short, stable reminder to resume from that state.
Retain the user's cadence, expiry, and notification choices. For a new schedule,
state the cadence and stopping conditions when establishing it.

Each wakeup takes one check pass. Stay quiet while the result is unchanged or
non-actionable; notify on meaningful changes under the agreed policy. Continue
independent work, then end the turn while awaiting the next check.

Pause a schedule when only user action can unblock its work. When a schedule
stops or changes, resolve waits that depend on it: arrange an
authorized replacement path or surface the remaining decision. Preserve resource
holds until resolved and update affected workers with the current resumption
path. Verify the saved schedule and target before claiming it is active.

## Callback

Use the user's selected events, typically completion or a blocker requiring the
owner. Provide the child with that destination and those triggers.

Process each report through the entrypoint's acceptance and deduplication rules.
When the user has selected both Callback and Scheduled, keep the agreed check
schedule alongside event reports.

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
purpose. Poll needs no rebind. A global handoff leaves project-internal
routes with their project controller.
