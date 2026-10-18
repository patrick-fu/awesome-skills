---
name: attention-frontier
disable-model-invocation: true
description: >-
  Maintain a person's prioritized follow-up frontier across parallel projects
  and agent conversations. Use to consolidate pending decisions, reviews, and
  coordination into a current workbench with brief change notifications.
---

# Attention Frontier

Reduce the person's cost of surveying work, chasing progress, and recovering
context while keeping important unfinished work accounted for.

## Ground

**Scope, incremental evidence, reconciliation.** Start from the user's working
scope and existing task map. Establish an initial baseline, then discover new
work and read source increments. Recent activity is a discovery window, not an
expiry date for older unfinished work.

Group related conversations by business matter; retain distinct user actions
and unfinished side or parallel tasks, including those within one conversation.
Recover the main objective and relevant backstory from source context when a
recent turn only describes a local step.
Reconcile candidates against current user instructions, related conversations,
and relevant delivery evidence. Later resolutions must retire stale requests.
Distinguish an agent's finished turn, compilation, tests, delivered artifacts,
and business acceptance. Preserve the evidence level of each claim.

## Select and order

**Human action, ownership, business priority.** Identify the next decision,
review, hands-on action, or coordination that actually needs the person.
Ordinary authorized execution stays with its owner. When the person's action
is done and ownership continues elsewhere, move the matter to observation;
bring it back when a new user action becomes ready. Reading a report alone
does not complete an action.

Proactively investigate missing evidence. Remaining uncertainty belongs in a
clearly labeled area with its gap and possible impact; elevate it to a user
action only when the person is needed to resolve it.

Rank by explicit user priorities, deadlines and business impact, delay cost,
dependencies released, and waiting time. Preserve relative order where these
have not materially changed. Use judgment rather than invented deadlines,
fixed scores, quotas, or Top-N limits. Keep all unfinished matters accessible,
including work progressing independently and external waits.

## Publish

**Full coverage, selective emphasis, easy re-entry.** Maintain an HTML workbench
at a stable entry point by default; adapt the medium to the environment.
Read [presentation.md](references/presentation.md) when creating or updating it.
In Codex App, also read [codex.md](references/codex.md).

Use the independent view across matters to recommend the most useful next move
and briefly explain why. Lead with that recommendation when user action is
ready. Orient the reader to each matter's purpose, background, and related work
before showing the next step, next owner, reason, source entry, and a short
suggested prompt the person can send to its owning conversation.

Reflect priority, overdue status, and uncertainty whenever they change. Keep
polling replies to a sentence or two about meaningful changes plus the entry
link; stay quiet when nothing substantive changed. An unresolved item remains
visible without requiring repeated identical messages.

## Continue

**Durable context, honest freshness.** Keep a compact continuation record:
scope and source coverage, matter-to-source mappings, stable read positions,
unresolved and resolved user actions, owners, check conditions, and the previous
reported state. Choose the storage format for the environment. Preserve
resolution provenance so old requests do not reappear. On a failed read,
retain the last known state and its original verification time; mark the gap.

Run one pass unless ongoing checks were requested. For ongoing work, use the
host's native scheduler with the agreed cadence and time zone, reuse an
existing matching schedule, and report unavailable capabilities. End the turn
between scheduled runs. Stop this watcher's continuation when it is canceled.

This role observes, prioritizes, presents, and notifies. Leave task execution
with existing owners; messaging them or restarting their work requires
separate authorization.
