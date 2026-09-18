# Controller handoff

Read this file for successor creation, direct takeover, or degraded recovery.

## Actors

In predecessor-led handoff, the predecessor creates or continues an eligible
successor with `create_thread` or formal `(hostId, threadId)`, sends the
verified transfer summary, and verifies the successor's acceptance report. The
brief explicitly designates the controller successor so its role can be restored
from history. In direct takeover, the user makes the current session the
successor; it reconstructs the same facts itself.

## Recover

The predecessor remains owner until acceptance. Reconstruct history from
`read_thread`, the owning host's rollout, or another authoritative carrier.
Select tasks using the [check procedure](return.md#check). Build the transfer
summary from the [control index](../SKILL.md#route), adding
the role source, authorization limits, and unresolved delivery or evidence gaps.
Reconcile recent user steering in workers before carrying old controller
assumptions forward. Preserve the question behind a terse answer; link evidence
instead of copying transcripts.
Notify only tasks whose next action or return path changes; routine transfer
needs no broadcast to every historical task.

If a material fact remains unresolved after available history and rollout, stop:
predecessor, children, titles, and ownership stay unchanged. A report with an
unresolved evidence or authority gate keeps that gate after transfer.

## Accept

Transfer ownership only after the successor:

1. has formal `(hostId, threadId)` identity
2. matches the assigned host/project and has the access required for its role
3. verifies the transfer summary against current directly owned tasks and
   resolves material gaps
4. states in normal language that it accepts ownership and what remains next

Only that evidence-backed statement, delivered to and verified by the
predecessor or made after user-authorized direct takeover, transfers ownership.
After acceptance, read [return routing](return.md) before changing report
destinations or retiring. Use `codex-session-naming` for the predecessor's
outgoing handoff and the successor's continuing role. Archive the predecessor
when routing permits retirement, unless the user asks
to keep it visible. Record the successor in the project task for the global
controller's next check under its selected mode; notify immediately only when the
user has explicitly selected Callback on that direct project→global edge.
Retain history; replace a child only when it is confirmed failed or unreachable
or the user asks.
