---
name: parallel-goal-workflows
description: "Guides deliberate high-overhead multi-agent workflows only when the user explicitly requests `parallel-goal-workflows` or asks for a lead agent to delegate workflow ownership to an orchestrator while the lead waits and reports. It is not a default for ordinary subagent, parallel work, coding, research, review, or goal-decomposition requests."
---

# Parallel Goal Workflows

Use this skill for delegated goal workflows where the lead agent should not
become the hidden worker. The point is context, not control: give the workflow
owner enough intent, evidence needs, and boundaries to adapt.

Use native goal mode when the host can attach goals to sessions, threads, or
spawned agents. If native per-subagent goals are unavailable, put the same
goal-shaped packet in the delegation message.

## Execution Boundary

Use this ownership model:

```text
Lead Agent
  -> Orchestrator Agent
       -> Worker / Review / Acceptance / Repair / Synthesis agents as needed
       -> Acceptance-ready report
  -> Lead user-facing handoff
```

The high-trigger threshold is defined in the frontmatter description. Once this
skill is active, preserve the lead/orchestrator boundary rather than returning
to direct lead-agent execution.

## Lead Agent

The lead owns the user conversation and the workflow boundary, not task-level
execution.

Set the lead boundary goal from `Goal Packets` before starting the
orchestrator.

Do:

- collect the user's goal, constraints, preferences, and relevant project rules
- start an orchestrator whenever this workflow is in scope
- give the orchestrator enough context to act independently
- wait with the longest reasonable wait window or callback-style interface
- relay user clarifications to the orchestrator
- report the orchestrator's final report to the user

After the orchestrator starts, do not:

- research, edit, implement, review, repair, or verify the same task
- spawn peer workers that bypass the orchestrator
- run a separate acceptance path unless the orchestrator asks for help
- treat a wait timeout as permission to take over
- fill report gaps yourself; ask the orchestrator for a narrower follow-up

## Orchestrator Agent

The orchestrator owns task-level workflow acceptance. It decides the simplest
shape that satisfies the work, review, repair, and verification needs.

Do:

- turn the lead's context into downstream goals
- decide whether workers, reviewers, acceptance agents, repair agents, or
  synthesis agents are needed
- collect outputs and resolve conflicts explicitly
- route important work through independent review
- run repair loops when review or acceptance fails
- make the final task-level judgment
- return an acceptance-ready report for the lead to relay

The orchestrator may keep the workflow small. It may also choose fan-out,
fan-in, rolling waves, or nested delegation when the task warrants it.

## Downstream Agents

Every downstream agent should receive a goal, not a vague chore. Review,
Acceptance, Repair, and Synthesis agents need goals too.

Common roles:

- Worker Agent: produces the patch, artifact, extraction, research, or other
  concrete work.
- Review Agent: independently checks worker output for bugs, unsupported
  claims, missed constraints, regression risk, or weak evidence.
- Acceptance / Verification Agent: checks whether the reviewed result satisfies
  the user goal and evidence needs.
- Repair Agent: fixes a narrow issue found by review or acceptance.
- Synthesis Agent: merges multiple work or evidence streams without hiding
  disagreement.

Do not over-regulate workers. A worker, reviewer, or acceptance agent may spawn
its own subagents when that helps its goal. Do not encourage extra nesting for
its own sake, and do not forbid it; the harness can enforce depth and
concurrency limits.

If you are running inside Codex and nested subagents are needed but unavailable,
or Codex multi-agent tools seem unavailable, read
`references/codex-nested-subagents.md` before changing the workflow design.

## Goal Packets

Keep packets compact. They should describe the outcome, relevant context,
boundaries, evidence needs, and pause conditions.

For the lead:

```text
/goal Hold the delegated workflow boundary until the orchestrator returns an
acceptance-ready report, then relay it to the user without doing task-level
work.
```

For the orchestrator:

```text
/goal Orchestrate this delegated workflow to completion and return an
acceptance-ready report.

Context:
[User goal, constraints, relevant project rules, and quality bar.]

Deliverable:
[Worker results, independent review result, acceptance/verification result,
repair loop if any, final task-level judgment, remaining risks, and a concise
report the lead can relay.]

Boundaries:
[What the workflow may touch, what is outside scope, and what needs user
approval.]

Pause if:
[Credentials, destructive actions, external approval, user judgment, or a
repeated blocker is required.]
```

For downstream agents:

```text
/goal [one concrete outcome]

Context:
[Why this work matters and what upstream context is relevant.]

Deliverable:
[The report, patch, artifact, decision, or evidence needed back.]

Boundaries:
[Owned files, systems, decisions, and areas to avoid.]

Verification:
[Checks to run or evidence to provide.]

Pause if:
[Credentials, destructive actions, ownership conflicts, or user judgment are
needed.]
```

## Observation Rhythm

Observation should feel closer to callback than polling.

After setting the lead goal and starting the orchestrator:

1. Use the longest reasonable wait window.
2. Do not fill idle time with delegated task work.
3. Ask for status only after a meaningful timeout, when the user asks, when an
   external signal suggests failure, or before replacing the orchestrator.
4. If the orchestrator is still running and not clearly blocked, keep waiting.

## Final Handoff

The orchestrator's final report should tell the lead:

- what workflow ran
- what changed or was produced
- what review and acceptance happened
- what evidence supports completion
- what remains risky or unresolved
- what the lead should tell the user

The lead should relay that report plainly. If obvious pieces are missing, ask
the orchestrator for a narrower follow-up instead of doing the missing
task-level work.
