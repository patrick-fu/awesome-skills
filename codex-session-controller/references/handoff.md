# Controller handoff

Use rollout and `read_thread` history as the source of truth. Do not maintain a
periodic checkpoint, registry file, or controller database. A handoff manifest
is an on-demand transfer aid that the successor can reconstruct and verify.

## Entry paths

- No current controller: establish one and inventory the relevant scope.
- Old controller initiates: create a successor after the user's explicit
  request, then remain owner until acceptance.
- New session takes over: search for or read the specified predecessor; the
  current session becomes successor unless the user asks to create another.

Search every connected host for global-controller candidates. For a project
controller, use the natural project identity and recent history. Read multiple
candidates and ask the user to disambiguate rather than choosing by title or
recency alone.

## Normal transfer

When the predecessor is readable, synthesize this compact manifest from its
current history:

```text
HANDOFF_MANIFEST
controller_scope: global | project
project: [natural project name, if applicable]
predecessor: [hostId, threadId]
handoff_reason: [context, capability, runtime, user-requested, other]
owned_threads:
  - [hostId, threadId, purpose, current state, next evidence]
frontier:
  - [current outcomes and dependency gates]
settled_decisions:
  - [decision, evidence/artifact, affected scope]
pending_user:
  - [decision or action and why it blocks]
resources:
  - [resource, owner, contenders, release condition]
unknown_operations:
  - [operation ID, create/send, target, last evidence]
constraints:
  - [authority, safety, repository, host, or product boundaries]
capability_gaps:
  - [missing tool/schema and current degradation]
END_HANDOFF_MANIFEST
```

Include accepted and rejected decisions, because terse replies such as “ok,”
“continue,” or numbered choices are not recoverable without the question and
affected artifact. Keep long logs, command output, and raw reasoning out of the
manifest; the successor can reopen them when a specific item needs proof.

## Recovery from history

When no trustworthy manifest exists, traverse all available predecessor turns
or its rollout. Extract:

- user goals, corrections, decisions, grants, and direction changes
- create/send/read operations and operation IDs
- owned `(hostId, threadId)` pairs and title/state changes
- accepted results, remaining gates, and user actions
- resource ownership and conflicts
- timeouts, unknown results, failures, and capability gaps

Scan the complete history, but place only the structured result in successor
context. Open detailed business output only when restoring that individual
task. Treat cached previews, catalog state, and synchronized timestamps as
discovery evidence rather than proof of work.

If both history and rollout are unavailable, allow degraded takeover so a dead
host does not permanently block the portfolio. List every evidence gap,
unconfirmed child, unknown operation, and assumption before proceeding.

## Acceptance protocol

Controller ownership changes only after the successor:

1. has a formal `(hostId, threadId)`, not a pending/client identifier
2. reads the manifest or reconstructs available history
3. locates and minimally verifies current owned sessions
4. reports the recovered frontier, pending user items, resources, and unknowns
5. announces `HANDOFF_ACCEPTED`

Until then, keep the predecessor current. A failed or ambiguous successor
creation leaves the predecessor title and ownership unchanged.

After acceptance:

- the successor replaces only the predecessor title's leading role/status with
  `🗑️`, preserving the remaining scope name and date
- archive the predecessor by default unless the user asked to keep it visible;
  never delete it
- continue managing existing child sessions rather than rebuilding them
- notify the global controller when a project controller changes owner
- replace a child only when it is confirmed failed/unreachable or the user asks
