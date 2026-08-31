# Controller handoff

Apply the entrypoint's identity, evidence, Relay, delivery recovery, and
saved-project rules. This file adds only ownership transfer. Never use
`fork_thread`.

**Actors:** in predecessor-led handoff, the predecessor creates or continues an
eligible successor, sends the verified transfer summary, and verifies the
successor's natural acceptance report. The initial brief or follow-up explicitly
designates that session as the controller successor so its role can be restored
without a reporting protocol. In direct takeover, the user's request makes the
current session the successor; it reconstructs the same facts itself. No other
session may appoint itself.

## Recover

Resolve the predecessor through the entrypoint. It remains owner until the
successor is accepted. Identity and evidence are independent gates: the user
may identify the intended predecessor, but its control state must come from
`read_thread`, the owning host's rollout, or another authoritative carrier. Do
not make the user reproduce its history.

From verified history, write a concise natural-language transfer summary. It
must preserve the controller's scope and identity; the latest user outcomes,
corrections, permissions, decisions, and acceptance expectations; every owned
session's formal identity, purpose, state, and next evidence; unfinished work,
dependencies, user gates, and resource ownership; reports still requiring
action; create or send attempts whose delivery is unresolved; and all known
constraints or evidence gaps. Preserve the question and affected artifact
behind terse decisions such as “ok” or a numbered choice. Point to detailed
evidence instead of copying raw transcripts.

When history is incomplete, traverse every available predecessor turn and the
owning-host rollout. If any material fact remains unresolved, report the gap and
stop; predecessor, children, titles, and ownership remain unchanged. Reports
whose evidence or authority was unresolved keep that gate after transfer and
their effects are never replayed merely because a successor exists.

## Accept

Transfer ownership only after the successor:

1. has formal `(hostId, threadId)` identity
2. passes saved-project, environment, and permission qualification;
   projectless, restricted, or approval-pending candidates fail
3. reads the verified transfer summary or reconstructs every material fact
4. locates and minimally verifies all current owned sessions
5. checks user intent, authority, unfinished work, gates, resources, pending
   reports, and unresolved delivery attempts
6. states in normal language that it accepts ownership and what remains next

Only that evidence-backed statement, delivered to and verified by the
predecessor or made after a user-authorized direct takeover, transfers
ownership. A creation result, handoff request, or unverified readiness report
does not. The predecessor then updates and archives itself; in a user-authorized
direct takeover, the successor does so after reconstructing the same evidence.
Prefix the predecessor's stable controller title with `🔀` and archive it unless
the user asked to keep it visible.
The successor sends each active owned session one natural routing update with
its formal `(hostId, threadId)` so later reports reach the new owner. Continue
those sessions; notify the global controller when a project controller
changes owner. Replace a child only when confirmed failed or unreachable, or
when the user asks. Never delete a session.
