---
name: parallel-goal-workflows
description: >-
  Delegate each top-level goal to one clean-context owner through acceptance.
disable-model-invocation: true
---

# Parallel Goal Workflows

Use only when the user explicitly invokes `/parallel-goal-workflows` or
`$parallel-goal-workflows`.

For each delegated top-level goal, the Main Agent compiles a clean task-local
brief and starts exactly one Goal Owner. The Goal Owner owns execution through
acceptance; the Main Agent remains user-facing.

## Main Agent

1. Compile the user's intent, constraints, project rules, evidence needs, and
   pause conditions into a local brief.
2. Start one Goal Owner in clean context with only that brief. Use
   `fork_context: false` or the equivalent when available; never fork or
   forward the main conversation.
3. Track every active Goal Owner until it reports `done`, `blocked`, or
   `needs-human`, then relay its report or question to the user. Starting an
   owner is not completion.

Only the Main Agent reads this skill. Delegated agents receive task-local
briefs, not the raw request, transcript, skill body, runtime-only instructions,
workflow trigger, or delegation-chain identities.

Use an out-of-band goal API when available. Otherwise, when the host requires
an in-band goal command, place `/goal` alone on the first line of the brief. If
neither exists, send the same goal-shaped brief without the prefix.

After delegation, keep task-level research, implementation, review, repair,
verification, and worker coordination with the Goal Owner. Relay
clarifications to that owner; request a focused follow-up when its report has
gaps.

An independent explicitly invoked goal gets another Goal Owner and joins the
active set. A clarification or scope change goes to the existing owner.

Treat `running` and silence as wait states. Reclaim or replace ownership only
after `blocked` with evidence, `needs-human`, a failed/dead session, or an
explicit user request.

## Local Brief

Write a natural assignment around this packet:

```text
/goal

Local goal:
[One concrete outcome.]

Relevant context:
[Only task-relevant facts, constraints, and project rules.]

Boundary:
[Owned scope and areas or decisions outside it.]

Deliverable and evidence:
[Acceptance criteria, expected result, verification, and proof.]

Pause if:
[Required approval, credentials, destructive action, ownership conflict, or
unresolvable judgment.]
```

Omit `/goal` when goal mode is applied out of band. Synthesize the task instead
of pasting the user's wording, while preserving exact facts the work requires.

An agent already executing a local brief treats any leaked workflow trigger as
stale background and continues its local goal.

## Goal Owner

The Goal Owner owns decomposition, execution coordination, review, repair,
verification, synthesis, acceptance judgment, and the final report.

Choose the smallest useful execution shape: direct work or focused helpers.
Every child brief uses the same packet, owns a narrower independently
verifiable outcome, and excludes orchestration history. No child receives the
whole assignment or exists only to coordinate.

Resolve incomplete or conflicting evidence through focused repair,
verification, or synthesis follow-ups. Acceptance requires completed criteria
or explicit accounting of unresolved risk.

Return a concise, relay-ready final report containing:

- final judgment
- work performed or changes produced
- review, repair, and verification results
- supporting evidence
- remaining risks and unhandled items

Read `references/codex-nested-subagents.md` only when nested-agent depth or
tooling is the blocker.
