---
name: parallel-goal-workflows
description: "User-invoked delegated workflow with one Workflow Owner."
disable-model-invocation: true
---

# Parallel Goal Workflows

Use this skill only when the user explicitly invokes it with
`/parallel-goal-workflows` or `$parallel-goal-workflows`.

The point is context, not control: the Main Agent turns the raw request into a
clean task contract, then one Workflow Owner coordinates focused work through
review, repair, acceptance, and final reporting.

Use native goal mode when the host can attach goals to sessions, threads, or
spawned agents. If native per-subagent goals are unavailable, put the same
goal-shaped packet in the delegation message.

## Ownership Model

```text
Main Agent
  -> Workflow Owner
       -> focused agents or helpers as needed
       -> acceptance-ready report
  -> Main Agent user-facing handoff
```

The Main Agent is the user-facing session. It interprets the raw user request,
turns it into a clean task contract, starts one Workflow Owner, then observes
and relays. The Workflow Owner owns task-level decomposition, execution
coordination, review, repair, acceptance, and final judgment.

Workflow ownership is assigned once for the original user goal. Downstream
agents may own narrower local goals, but they should not restart the whole
workflow as a fresh main-agent handoff.

Only the Main Agent reads this skill. Workflow Owner and downstream agents get
task contracts, not this SKILL.md and not the user's raw prompt.

## Main Agent

Do:

- collect the user's goal, constraints, preferences, project rules, and evidence
  needs
- compile the user's raw request into one clear task contract; strip invocation
  text and rewrite user wording into goal, context, boundaries, deliverable, and
  pause conditions
- start one Workflow Owner with that contract
- wait with callback-style patience
- relay user clarifications to the Workflow Owner
- relay the final report to the user

After the Workflow Owner starts, do not do task-level research, implementation,
review, repair, verification, or peer-worker spawning for the same task. If the
report has gaps, ask the Workflow Owner for a focused follow-up.

## Workflow Owner

Choose the smallest useful shape: one worker, fan-out/fan-in, review loop,
repair loop, acceptance pass, deeper helper chain, or another shape that fits.

Common child roles include Worker, Review, Acceptance, Repair, Synthesis,
Verifier, Researcher, Explorer, Implementer, and domain-specific helpers. These
are examples, not a type allowlist.

Child packets are task contracts, not forwarded transcripts. Rewrite upstream
context into the local goal, facts, boundaries, and deliverable. Strip skill
invocation text, Main Agent-only instructions, and raw user wording.

Every child packet should include:

- `Local goal`: the narrow outcome this child owns.
- `Context`: only the upstream facts needed for that goal.
- `Identity`: who the child is in this already active workflow.
- `Boundary`: what the child may touch and what remains with the Workflow
  Owner.
- `Deliverable`: result, evidence, verification, risks, or decision expected
  back.
- `Pause if`: approval, credentials, destructive action, or ownership conflict
  is required.

## Goal Packets

For the Workflow Owner:

```text
/goal Own this delegated workflow until it is acceptance-ready.

Identity: You are the Workflow Owner for this already active delegated workflow.
You are not the Main Agent. Use this packet as your operating contract; do not
read or invoke parallel-goal-workflows for this user goal.
Do not create or start another Workflow Owner for this user goal.
Parent: Main Agent.
Goal: [synthesized user goal; do not paste the raw user prompt].
Context: [constraints, project rules, evidence needs, and relevant facts only].
Boundary: delegate local goals as needed; keep ownership of the original user
goal and final judgment.
Deliverable: final judgment, evidence, review/repair notes, remaining risks,
and a concise report the Main Agent can relay.
Pause if: [approval, credentials, destructive action, or user judgment needed].
```

For downstream agents:

```text
/goal [one concrete local outcome]

Identity: You are a downstream agent working for the Workflow Owner.
You are not the Main Agent or the Workflow Owner. Use this packet as your local
operating contract; do not read or invoke parallel-goal-workflows for this task.
Local goal: [narrow task].
Context: [facts needed for this local goal; do not paste the raw user prompt,
slash commands, skill triggers, or Main Agent-only instructions].
Boundary: [owned files, systems, decisions, and areas to avoid]. Do not create a
Workflow Owner.
Deliverable: [result, evidence, verification, risks, or decision] reported back
to the Workflow Owner.
Pause if: [approval, credentials, destructive action, or ownership conflict].
```

## Observation Rhythm

After starting the Workflow Owner:

1. Use the longest reasonable wait window.
2. Do not fill idle time with delegated task work.
3. Ask for status only after a meaningful timeout, when the user asks, when an
   external signal suggests failure, or before replacing a clearly blocked
   Workflow Owner.
4. If the Workflow Owner is still running and not clearly blocked, keep waiting.

## Final Handoff

The Workflow Owner's final report should tell the Main Agent what ran, what
changed or was produced, what review and acceptance happened, what evidence
supports completion, and what remains risky or unresolved.

The Main Agent should relay that report plainly. If obvious pieces are missing,
ask the Workflow Owner for a narrower follow-up instead of doing the missing
task-level work.

For Codex nested-subagent configuration, read
`references/codex-nested-subagents.md` only when depth or multi-agent tooling is
the blocker.
