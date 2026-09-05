# Controller handoff

Read this file for successor creation, direct takeover, or degraded recovery.
It adds only ownership transfer; identity, saved-project, delivery, and return
rules stay in their entrypoint or reference homes.

## Actors

In predecessor-led handoff, the predecessor creates or continues an eligible
successor with `create_thread` or formal `(hostId, threadId)`, sends the
verified transfer summary, and verifies the successor's acceptance report. The
brief explicitly designates the controller successor so its role can be restored
from history. In direct takeover, the user makes the current session the
successor; it reconstructs the same facts itself.

## Recover

The predecessor remains owner until acceptance. User identification and control
evidence are independent gates. Reconstruct history from `read_thread`, the
owning host's rollout, or another authoritative carrier. Write a concise natural
transfer summary preserving scope, role source, latest outcomes and corrections,
permissions, decisions, acceptance expectations, every owned session's formal
identity and return mode, unfinished work, dependencies, user gates, resource
ownership, actionable reports, unresolved create/send attempts, and evidence
gaps. Preserve the question behind a terse answer; link evidence instead of
copying transcripts.

If a material fact remains unresolved after available history and rollout, stop:
predecessor, children, titles, and ownership stay unchanged. A report with an
unresolved evidence or authority gate keeps that gate after transfer.

## Accept

Transfer ownership only after the successor:

1. has formal `(hostId, threadId)` identity
2. passes saved-project, environment, and permission qualification;
   projectless, restricted, or approval-pending candidates fail
3. reads the verified summary or reconstructs every material fact
4. locates and minimally verifies all current owned sessions
5. checks intent, authority, unfinished work, gates, resources, pending
   reports, and unresolved delivery attempts
6. states in normal language that it accepts ownership and what remains next

Only that evidence-backed statement, delivered to and verified by the
predecessor or made after user-authorized direct takeover, transfers ownership.
After acceptance, read [return routing](return.md) before changing report
destinations or retiring. Prefix the predecessor's stable controller title with
`🔀` and archive it when those rules permit retirement, unless the user asks to
keep it visible. Record the successor in the project task for the global
controller's next Pull; notify immediately only when the user has explicitly
switched that direct project→global edge to Callback. Retain history; replace a
child only when it is confirmed failed or unreachable or the user asks.
