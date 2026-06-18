---
name: parallel-goal-workflows
description: "Guides lead agents when users ask for subagents, parallel agents, multi-agent execution, delegated workflows, or goal decomposition. It favors flexible workflow orchestration around clear subagent goals, rich context, patient waiting, optional nested delegation, independent review, and final acceptance without over-controlling the work."
---

# Parallel Goal Workflows

Use this skill when delegated work should be shaped as goals, not just task
prompts. The point is context, not control: give each agent enough intent,
evidence, and boundaries to move independently without forcing a rigid script.

## Operating Principles

- Bias the lead agent toward orchestration when the user asks for subagents,
  parallel agents, multi-agent work, workflow coordination, or goal
  decomposition.
- Give every subagent a clear outcome-focused goal. If `/goal` is available,
  use it or ask the subagent to create one before execution.
- Provide rich context: why the work matters, what evidence counts, what must
  stay unchanged, and when the agent should pause.
- Prefer patient coordination over impatient takeover. A wait timeout means the
  wait window expired, not that the subagent failed.
- Use nested delegation when it reduces lead-agent micromanagement. A
  coordinator subagent can own a broad workflow and create downstream goals for
  research, execution, review, and repair.
- Keep nesting optional. Simple tasks may need only one or two peer subagents;
  broad tasks may benefit from a coordinator plus specialized workers.
- Treat review as its own goal when quality, safety, history, or source
  grounding matters. A fresh reviewer usually catches different failures than
  the worker who produced the result.
- The lead agent owns final acceptance and the user-facing answer, but should
  avoid becoming the hidden executor unless the user asks for direct execution
  or delegation is unavailable.

## Goal Packet

Give subagents compact but complete goal packets:

```text
/goal [one concrete outcome]

Context:
[Why this matters, relevant background, and known constraints.]

Deliverable:
[The exact report, patch, artifact, decision, or evidence needed back.]

Boundaries:
[Owned files, systems, decisions, and areas to avoid.]

Verification:
[Checks to run or reasoning/evidence to provide.]

Pause if:
[Credentials, destructive actions, ownership conflicts, repeated blockers, or
user judgment are needed.]
```

For a coordinator subagent, make the goal about running the workflow rather
than doing all work personally:

```text
/goal Run this delegated workflow to completion and return an acceptance-ready
report.

Context:
[Top-level objective, user constraints, repository rules, and quality bar.]

Deliverable:
[Agent graph, completed work, review result, verification evidence, remaining
risks, and final recommendation.]

Boundaries:
[What the coordinator may assign, what it may edit, and what must remain
outside scope.]

Verification:
[Independent review, repair loop when needed, and final checks.]

Pause if:
[The workflow needs user judgment, external approval, secrets, or a repeated
blocker cannot be resolved by narrowing or reassigning work.]
```

## Coordination Rhythm

1. Clarify the top-level outcome and acceptance evidence.
2. Choose the lightest useful agent shape: peer subagents for independent
   slices, or a coordinator subagent for multi-stage work.
3. Dispatch goal packets with enough context for independent action.
4. While agents run, manage liveness: wait, request status, narrow scope, or
   spawn a recovery/review agent before taking over concrete execution.
5. Route important results through an independent review goal when the cost of
   being wrong is meaningful.
6. Accept the work only after the reported evidence matches the user goal and
   any required checks pass.

## Final Response

Report the result in terms of the workflow outcome, not the internal drama:
what was delegated, what changed or was produced, what review/verification
happened, what remains uncertain, and what the user should know next.
