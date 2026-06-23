---
name: parallel-goal-workflows
description: "User-invoked delegated workflows with Workflow Owner tracking."
disable-model-invocation: true
---

# Parallel Goal Workflows

Use this skill only when the user explicitly invokes it with
`/parallel-goal-workflows` or `$parallel-goal-workflows`.

The point is context, not control: the Main Agent turns each delegated
top-level goal into a clean task contract, then one Workflow Owner per goal
coordinates focused work through review, repair, acceptance, and final
reporting.

Use native goal mode when the host can attach goals to sessions, threads, or
spawned agents. If native per-subagent goals are unavailable, put the same
goal-shaped packet in the delegation message.

## Ownership Model

```text
Main Agent
  -> Workflow Owner per top-level goal
       -> focused agents or helpers as needed
       -> acceptance-ready report
  -> Main Agent user-facing handoff
```

The Main Agent is the user-facing session. It interprets each delegated
top-level goal, turns it into a clean task contract, starts one Workflow Owner
for that goal, then tracks active owners and relays. Each Workflow Owner owns
task-level decomposition, execution coordination, review, repair, acceptance,
and final judgment for its goal.

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
- start one Workflow Owner per delegated top-level goal with that contract in a
  clean context
- maintain the active Workflow Owner set across user turns
- wait with callback-style patience
- relay user clarifications to the Workflow Owner
- relay the final report to the user

MUST NOT fork or forward the full main conversation when starting the Workflow
Owner. If the host exposes a history-fork option such as `fork_context`, set it
to `false`. The Workflow Owner gets the compiled task contract only.

After the Workflow Owner starts, do not do task-level research, implementation,
review, repair, verification, or peer-worker spawning for the same task. If the
report has gaps, ask the Workflow Owner for a focused follow-up.

## Main Agent Session Goal

Keep the user-facing session open until every active Workflow Owner reports
`done`, `blocked`, or `needs-human`, and the result or question has been
relayed to the user. Starting a Workflow Owner is not completion.

If the user adds an independent complex task while waiting, start another
Workflow Owner for that top-level goal and update the active set. If the new
input changes or clarifies an existing active goal, relay it to that goal's
Workflow Owner instead.

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
Observation: Long silence is acceptable; report at meaningful milestones, when
blocked or needing human input, and on completion.
Deliverable: final judgment, evidence, review/repair notes, remaining risks,
unhandled items, and a concise report the Main Agent can relay.
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

1. Observe workflow state, not output volume. Silence is normal progress unless
   paired with evidence of failure.
2. Treat `running` as a wait state. Do not fill idle time with delegated task
   work.
3. Ask for status only when the user asks, the Workflow Owner reports
   `blocked` or `needs-human`, an external signal proves failure, or a
   user-visible decision needs current state.
4. Reclaim or replace ownership only on `blocked` with evidence, `needs-human`,
   an explicit user request, or a failed/dead session. Never reclaim because of
   silence or timeout alone.
5. Relay `done` reports plainly. If the report has gaps, ask the Workflow Owner
   for a focused follow-up instead of doing the missing task-level work.

## Final Handoff

The Workflow Owner's final report should tell the Main Agent what ran, what
changed or was produced, what review and acceptance happened, what evidence
supports completion, and what remains risky, unresolved, or unhandled.

The Main Agent should relay that report plainly. If obvious pieces are missing,
ask the Workflow Owner for a narrower follow-up instead of doing the missing
task-level work.

For Codex nested-subagent configuration, read
`references/codex-nested-subagents.md` only when depth or multi-agent tooling is
the blocker.
