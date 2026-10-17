# Codex App

Use this reference only in Codex App; other environments choose their own
sources, links, scheduling, and notification facilities.

## Read and reconcile

Prefer available thread tools: discover with list_threads, inspect candidates
with read_thread, and use compact wait_threads snapshots for running work when
useful. Keep reads bounded and inspect the relevant latest user instructions
and results rather than treating titles or unread indicators as task facts.

Retain stable thread IDs, host provenance, and known handoff relationships.
Use source turn/message IDs and timestamps as durable read positions;
pagination cursors are paging aids. Declare inaccessible hosts or missing
history as coverage gaps.

## Link to the source

For local chats, use codex://threads/<thread-id> with the verified technical ID
and the actual returned title as link text. Preserve host provenance for remote
work and verify navigation rather than inventing remote link syntax. Group
related links under their matter and make the next action's owner easy to open.

The local chat URL form is documented in the official
[supported deep links](https://learn.chatgpt.com/docs/reference/commands#supported-links).

## Continue in the designated queue chat

Use the native automation tools when ongoing checks are requested. Inspect
existing schedules before creating one; preserve the requested target chat,
time zone, cadence, enabled state, and notification preferences. A minimal
continuation prompt such as "continue" is enough once this chat's durable
context identifies the workflow and reading positions.

Verify the actual schedule configuration after a change. Keep it separate from
other owners' schedules, and report any host limitation on background execution
or quiet notifications.
