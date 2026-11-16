# Coordinator handoff

Read when handing off coordinator ownership, taking over directly, or relaying
a degraded coordinator session across harnesses or models. Keep a second
opinion inside the existing thread; transfer ownership only when a new continuing
coordinator is needed.

## Establish the assignment

In predecessor-led handoff, continue an eligible successor by formal host thread
or external task identity, or launch one when the user requests a fresh thread.
Send a concise transfer summary naming the scope so the successor can recover
its responsibilities from host thread lists and persisted context records. In
direct takeover, the user designates the current session and it recovers those
facts itself.

The predecessor remains owner until acceptance. Coordinate writers of shared
working state so preparation does not produce competing execution.

## Recover current facts

Start with host thread lists, external task ledgers if present, linked
artifacts, and recent user decisions. Verify facts that affect the transfer
against current sources using [status check](return.md#check) and
[delivery recovery](delivery.md) when reads are incomplete or suspicious. Valid
current evidence settles the transfer without replaying full history or
repeating completed technical verification.

An unresolved gap in identity, access, or authority keeps the predecessor in
charge and the affected ownership, title, and routing unchanged. Existing
resource holds and dependencies stay active until evidence proves release.

## Accept responsibility

Once the successor holds the formal identity, assigned scope, usable access, and
verified understanding of remaining responsibilities, it states clearly what it
is taking over and what remains next. In user-authorized direct takeover, that
evidence-backed acceptance establishes the transfer.

After acceptance, apply [handoff routing](return.md#handoff-routing) for any
active Scheduled checks. Preserve existing running threads; replace a worker
only on confirmed failure, unreachability, or user request.

Update the outgoing predecessor's handoff marker (`🔀`) and the successor's
coordinator title (`🕹️ <scope>` via `thread-naming` or the host title tool).
Archive or retire the predecessor once Scheduled check transfers are verified,
unless the user prefers it kept visible. Retain history.
