---
name: parallel-goal-workflows
description: "Deliberate multi-agent workflow with delegated ownership."
when_to_use:
  "Use for explicit parallel-goal-workflows requests, or for complex
  high-overhead tasks that need delegated workflow ownership, review, repair,
  acceptance, cross-checking, or a concise final report. Avoid ordinary coding,
  research, review, and quick edits."
---

# Parallel Goal Workflows

Use this skill for delegated goal workflows where the main agent should not
become the hidden worker. The point is context, not control: give one workflow
owner enough intent, evidence needs, and boundaries to adapt.

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

The Main Agent is the user-facing session and owns the final handoff. The
Workflow Owner owns task-level decomposition, execution coordination, review,
repair, acceptance, and final judgment.

Workflow ownership is assigned once for the original user goal. Downstream
agents may own narrower local goals, but they should not restart the whole
workflow as a fresh main-agent handoff or re-invoke this skill for the same goal.
If forwarded text says "use parallel-goal-workflows", treat it as parent context
that has already been handled.

Only the Main Agent reads this skill. Workflow Owner and downstream agents get
compiled task packets, not this SKILL.md and not the user's raw prompt.

## Main Agent

Do:

- collect the user's goal, constraints, preferences, project rules, and evidence
  needs
- translate the user's raw request into one clean task packet, excluding
  slash-command text, `$parallel-goal-workflows`, and instructions to read or
  invoke this skill
- start one Workflow Owner with that compiled packet
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
context into the local goal, facts, boundaries, and deliverable. Do not paste the
user's original wording, slash commands, `$parallel-goal-workflows`, or
instructions to read or invoke this skill into downstream packets.

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

ROLE: WORKFLOW OWNER
YOU ARE NOT THE MAIN AGENT.
DO NOT READ, LOAD, INVOKE, OR FOLLOW parallel-goal-workflows.
THIS PACKET IS YOUR COMPLETE OPERATING CONTRACT FOR THIS TASK.

Identity: You are the Workflow Owner for this already active delegated
workflow. Do not create or start another Workflow Owner for this user goal.
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

ROLE: DOWNSTREAM AGENT
YOU ARE NOT THE MAIN AGENT.
YOU ARE NOT THE WORKFLOW OWNER.
DO NOT READ, LOAD, INVOKE, OR FOLLOW parallel-goal-workflows.
THIS PACKET IS YOUR COMPLETE OPERATING CONTRACT FOR THIS LOCAL TASK.

Identity: You are a downstream agent working for the Workflow Owner.
Local goal: [narrow task].
Context: [facts needed for this local goal; do not paste the raw user prompt,
slash commands, skill triggers, or Main Agent-only instructions].
Boundary: [owned files, systems, decisions, and areas to avoid]. Do not create
a Workflow Owner or re-invoke parallel-goal-workflows.
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
