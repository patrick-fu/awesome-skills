# Return modes

Read this file only when selecting or switching Callback/Batch, receiving one of
those reports, handling a wrong-level report, or applying handoff return
routing. Pull's complete path stays in the entrypoint.

## Callback

Use Callback only for the user-selected edges that can immediately advance a
short dependency chain. A meaningful completion or control event wakes the
direct owner. The owner verifies evidence and acceptance, then may dispatch the
next step to the same frontier. The receiver is the formal identity named in the
worker brief—never a higher controller.

## Batch

Use Batch only when the user explicitly selected it for a wide fan-in. One
heartbeat covers one cohort and makes one status snapshot per run. Set targets,
fixed cadence, a TTL or run cap, stop conditions, and automatic pause. Ordinary
completion and progress wait for the snapshot. An immediate control event may
interrupt only when the confirmed Batch choice includes that exception; state
that boundary in the user-visible setup. A user gate, failure, full completion,
or material change appears at the agreed return point rather than silently
becoming Pull.

## Wrong level

If a ticket report reaches a global controller, do not accept it or act on its
contents. Identify the direct owner from the sender's brief or authoritative
task records. When verified, forward the report unchanged to that owner with a
short address correction. When the owner cannot be verified, ask the sender to
resend from its own records; global state remains unchanged.

## Handoff routing

After [controller handoff](handoff.md) verifies ownership acceptance, route by
each edge's selected mode. Callback edges whose predecessor is the direct return
target use
**Rebind → Drain → Retire**: send a short delta changing only the report
destination to the successor; before confirmation, forward late callbacks
unchanged for successor deduplication and take no acceptance or state action.
Pause a Batch heartbeat and let the successor rebuild one cohort heartbeat on
demand. Pull edges need no rebind;
retirement waits for callback routing or Batch pause confirmation. A global
handoff never touches tickets inside a project.
