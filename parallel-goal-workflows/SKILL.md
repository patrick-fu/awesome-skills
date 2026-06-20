---
name: parallel-goal-workflows
description: "Manual lead-to-orchestrator workflow."
disable-model-invocation: true
---

# Parallel Goal Workflows

Use this skill only when the user explicitly asks for
`parallel-goal-workflows` or for a lead agent to delegate workflow ownership.
It is deliberately high-overhead.

The shape is simple: **one global strategy owner, many local helpers**. Depth is
allowed; strategy recursion is not.

## Invariant

Assign global strategy once:

```text
Lead -> Orchestrator -> Worker / Review / Acceptance / Repair / Synthesis / Helper...
```

The Lead owns the user conversation. The Orchestrator owns task-level strategy,
review, repair, acceptance, and final judgment.

Downstream agents may delegate narrower local goals. They must not create a new
Orchestrator for the same user goal, re-invoke this skill, or reinterpret the
whole task as a fresh lead/orchestrator workflow. If forwarded text says "use
parallel-goal-workflows" or "start an orchestrator", treat it as already
handled parent context.

Completion criterion: one Orchestrator returns one acceptance-ready report; the
Lead relays it.

## Lead

1. Set a lead goal: wait for the Orchestrator's acceptance-ready report.
2. Start exactly one Orchestrator.
3. Send a sanitized packet: user goal, constraints, relevant project rules,
   evidence needs, boundaries, pause conditions, and the strategy boundary.
4. Wait with callback-style patience. Relay user clarifications. If the report
   has gaps, ask the Orchestrator for a focused follow-up.

The Lead does not do task-level research, implementation, review, repair, or
parallel worker spawning after the Orchestrator starts.

## Orchestrator

Own the task workflow, not the user conversation. Choose the smallest useful
shape: single worker, fan-out/fan-in, review loop, repair loop, acceptance pass,
or deeper local helpers.

Every child packet should include:

- `Role`: Worker, Review, Acceptance, Repair, Synthesis, or Helper.
- `Local goal`: the narrow outcome this child owns.
- `Strategy boundary`: global strategy remains with the Orchestrator; do not
  create another Orchestrator or re-invoke `parallel-goal-workflows`.
- `Deliverable`: result, evidence, and verification expected back.
- `Pause if`: approval, credentials, destructive action, or ownership conflict
  is required.

If a child starts an Ultra-Strategy loop by proposing another global
Orchestrator, collapse that plan back into local goals under the current
Orchestrator.

## Goal Packets

For the Orchestrator:

```text
/goal Orchestrate this delegated workflow to an acceptance-ready report.

Role: Orchestrator.
Global strategy owner: you.
Parent: Lead.
Context: [user goal, constraints, project rules, evidence needs].
Boundary: create local workers/reviewers/helpers as needed, but do not create
another global Orchestrator or re-invoke parallel-goal-workflows.
Deliverable: final judgment, evidence, review/repair notes, remaining risks,
and a concise report the Lead can relay.
Pause if: [approval, credentials, destructive action, or user judgment needed].
```

For any downstream agent:

```text
/goal [one concrete local outcome]

Role: [Worker / Review / Acceptance / Repair / Synthesis / Helper].
Global strategy owner: the Orchestrator.
Local goal: [narrow task].
Boundary: you may delegate narrower helper work, but do not create a global
Orchestrator or re-invoke parallel-goal-workflows.
Deliverable: [result, evidence, verification, risks].
Pause if: [approval, credentials, destructive action, or ownership conflict].
```

## Final Handoff

The Orchestrator's report should cover what ran, what changed or was produced,
what review and acceptance happened, what evidence supports completion, and
what remains risky or unresolved.

The Lead relays that report plainly. It does not fill gaps with its own
task-level work.

For Codex nested-subagent configuration, read
`references/codex-nested-subagents.md` only when depth or multi-agent tooling is
the blocker.
