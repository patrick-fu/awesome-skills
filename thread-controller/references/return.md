# Follow-up mechanics

Read for a status check, selected Scheduled or Callback behavior, a mode change,
a wrong-level report, or handoff routing. Mode selection lives in
[SKILL.md](../SKILL.md#follow-up-modes).

## Check

Rebuild the requested set from the index, known identities, and `list_threads`.
A global inventory normally covers its project owners and standalone tasks;
read ticket detail when the request or a specific decision needs it. A focused
request selects its relevant tasks. Deeper reading does not change ownership.

Take one snapshot pass with `wait_threads` (`timeoutMs: 0`), in batches allowed
by the current schema. Read additional records where a decision needs evidence;
use [delivery recovery](delivery.md) for suspicious or failed reads. Report
partial coverage if missing tasks or unresolved reads affect the answer, and
continue handling verified independent work.

Select active tasks from substantive user or work activity. Controller notices
and title changes do not reactivate historical work. For bulk operations, keep
the pre-operation selection stable and expand it only on independent evidence.

Apply the entrypoint's [coordination and integration](../SKILL.md#coordinate-and-integrate)
rules to new results. Complete the requested check and any authorized next work;
under Poll, further monitoring waits for the user's next request.

## Scheduled

Use `automation_update` for a controller-targeted heartbeat. Reuse a check that
covers the same work; keep changing targets and state in the index, with a short,
stable wakeup reminder to resume from it. Preserve the user's cadence, expiry,
and notification choices. State the cadence and stopping conditions when
establishing a new schedule, and verify its saved target and settings before
claiming it is active.

Each wakeup takes one check pass and handles authorized next work. Stay quiet
while the result is unchanged or non-actionable; notify on meaningful changes
under the agreed policy. Continue independent work, then end the turn while
awaiting the next check.

## Callback

Give the child its direct owner's destination and the user's selected events,
typically completion or a blocker requiring the owner. Apply the entrypoint's
acceptance and deduplication rules to each report. When the user selected both
Callback and Scheduled, preserve the agreed schedule alongside event reports.

If a ticket reports to a global controller, resolve its direct owner from current
task records and forward the report unchanged with a short address correction.
That owner handles acceptance and task decisions. Keep the report while an
uncertain destination is resolved.

## Changes and stopping

Apply changes within the selected scope. A switch to Poll retires the affected
controller-check schedules and callback instructions while preserving worker
assignments, unresolved dependencies, and unrelated or worker-internal follow-ups.
Cancellation also ends follow-ups for the canceled work; preserve valid parallel
assignments.

Pause a schedule when only user action can unblock its remaining work; one
blocked branch can coexist with continued checks for another actionable branch.
When a schedule stops, expires, or changes, resolve dependent waits: use an
authorized replacement path or surface the remaining decision, and tell affected
workers their current resumption path. Keep expired schedules inactive through
handoff. Resource holds persist until their actual release is established.

## Handoff routing

After [ownership acceptance](handoff.md#accept-responsibility), rebind Callback
destinations that named the predecessor. Forward late reports unchanged until
the new route is confirmed; the successor deduplicates and owns acceptance.
Transfer Scheduled checks only when the tool supports changing their target;
otherwise the successor establishes the replacement and the predecessor retires
the old check. Preserve active/paused state, cadence, expiry, and pending waits;
keep one active check per purpose. Verify the saved recipient and settings before
retiring the predecessor. Poll needs no rebind. A global handoff leaves
project-internal routes with their project owner.
