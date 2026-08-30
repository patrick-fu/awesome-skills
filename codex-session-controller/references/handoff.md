# Controller handoff

Apply the entrypoint's identity, evidence, Relay, and operation rules. This file
adds only ownership transfer. Never use `fork_thread`.

## Recover

Resolve the predecessor through the entrypoint. It remains owner until
acceptance. Treat identity and evidence as independent gates:

- resolve candidate ambiguity from the user's choice or verified history
- reconstruct every material control field from `read_thread`, the owning
  host's persisted rollout, or another authoritative carrier

The user names the intended predecessor; do not require the user to carry its
manifest or history. New user clarification or restored owning-host evidence
reopens only the gate it resolves. Transfer remains blocked until identity is
unique and every material field is verified.

## Manifest

Synthesize from verified history:

```text
HANDOFF_MANIFEST
scope: [global | project; natural project]
predecessor: [hostId, threadId]
reason: [user-requested cause]
user_contract: [outcomes, details, corrections, grants, decisions]
control_contract: [owners, authority, completion/acceptance, callback,
                   delivery dimensions]
controller_context: [sourced facts; non-binding candidates]
owned_threads: [identity, purpose, state, next evidence]
frontier: [outcomes, dependencies, user gates]
resources: [owner, contenders, release condition]
pending_events: [callback key|unkeyed, key class, source, receiver, kind,
                 disposition, effects gate, next action]
unknown_operations: [operation id, create/send, target, last evidence]
constraints_and_gaps: [authority, safety, repository, host, capability]
END_HANDOFF_MANIFEST
```

Preserve the question and affected artifact behind terse decisions such as
“ok” or a numbered choice. The manifest carries pointers, not raw payloads.

Without a trustworthy manifest, traverse every available predecessor turn and
reconstruct every field; validate carriers under the entrypoint. If any material
field remains unresolved across available authoritative carriers, report the gap
and stop transfer; leave predecessor and children unchanged.

Preserve each pending event's gate across transfer. A successor never upgrades
an unkeyed, deferred, reconciled, or effects-gated event to `applied`, nor
replays its repeatable effects, without the original admission, key, authority,
and evidence becoming valid.

## Accept

Transfer ownership only after the successor:

1. has formal `(hostId, threadId)` identity
2. passes the entrypoint's saved-project, environment, and permission-profile
   qualification; projectless, restricted, or approval-pending candidates fail
3. reads a trustworthy manifest or reconstructs every material field from
   available `read_thread` records and the owning host's rollout when needed
4. locates and minimally verifies current owned sessions
5. checks contracts, provenance, frontier, gates, resources, pending events,
   and unknown operations
6. announces `HANDOFF_ACCEPTED`

After acceptance, prefix the predecessor's stable controller title with `🔀`
and archive it unless the user asked to keep it visible. Continue its children;
notify the global controller when a project controller changes owner. Replace a
child only when confirmed failed or unreachable, or when the user asks. Never
delete a session.

A failed or ambiguous successor creation changes neither predecessor title nor
ownership. Before `HANDOFF_ACCEPTED`, do not prefix `🔀` or archive it.
