# Follow-up mechanics

Read for a status check, Scheduled timer behavior, a mode change, or handoff
routing. Mode selection lives in [SKILL.md](../SKILL.md#follow-up-modes).

## Check

Rebuild the requested set from known identities, external task records if used,
and the host's thread-listing surface. A global inventory covers active threads
and standalone work within scope; read thread detail when a decision or blocker
needs evidence. Deeper reading does not change thread ownership.

Take one non-blocking snapshot pass using the current host adapter's status or
read tools, respecting any batch limits of the current schema. Use
[delivery recovery](delivery.md) for suspicious or failed reads. Report partial
coverage if missing threads or unresolved reads affect the answer, and continue
handling verified independent work.

Select active tasks from substantive user or work activity; title updates alone
do not reactivate historical work. Apply
[coordination and integration](../SKILL.md#coordinate-and-integrate) rules to
new results. Under **Poll**, complete the requested check and any authorized next
work, then wait for the user's next request.

## Scheduled

Use the host adapter's native scheduler for a coordinator-owned heartbeat. If
the host lacks native scheduling, report that limitation and remain on **Poll**.
Reuse an existing check when it covers the same scope; keep wakeup prompts
short and stable so each run re-reads live thread and context state rather than
relying on stale prompt text. Preserve the user's cadence, expiry, and
notification choices. State the cadence and stopping conditions when
establishing a schedule, and verify its saved target and settings before
claiming it is active.

Each wakeup runs one snapshot pass and handles authorized next work. Stay quiet
when nothing actionable changed under the agreed policy; report meaningful
state shifts, blockers, or decisions needed, then end the turn.

## Changes and stopping

Apply mode changes within the requested scope. Switching to **Poll** retires the
affected coordinator schedules while preserving worker assignments, unresolved
dependencies, and worker-internal waits. Canceling a task also retires its
dedicated follow-up schedules without disturbing valid parallel work.

Pause a schedule when only user action can unblock the remaining work; one
blocked branch can coexist with continued checks for another actionable branch.
Resource holds persist until direct evidence proves release.

## Handoff routing

Cross-thread follow-up is unidirectional, so child threads carry no upward return
addresses and **Poll** needs no rebind.

After [ownership acceptance](handoff.md#accept-responsibility), transfer
**Scheduled** checks only when the host supports retargeting the saved schedule;
otherwise the successor establishes the replacement and the predecessor retires
the old check. Preserve active/paused state, cadence, expiry, and pending waits;
keep one active check per purpose. Verify the saved recipient and settings
before retiring the predecessor.
