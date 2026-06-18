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
- Translate the user's request into a compact workflow brief before dispatching
  agents. A good brief names the outcome, scope, constraints, evidence, and
  expected final artifact.
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
- If delegation is not useful or not available, either produce copy-ready goals
  for the user or proceed directly with the smallest honest workflow; disclose
  that fallback instead of pretending a multi-agent workflow happened.

## Workflow Brief

Start with a short brief before spawning agents:

```text
Outcome:
[The concrete result the user wants, not just the activity.]

Scope:
[The files, systems, topics, or decisions included and excluded.]

Constraints:
[User preferences, repository rules, safety limits, style, data, and policies.]

Evidence:
[What logs, tests, diffs, sources, screenshots, reviews, or artifacts will prove
the work is done.]

Final artifact:
[The answer, patch, document, commit, report, or handoff expected at the end.]
```

Use the brief to decide whether the task needs peer subagents, a coordinator,
or direct execution. Do not overbuild a workflow when one focused goal is enough.

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

## Synthesis

Synthesize results without flattening disagreement:

- Compare agent outputs against the workflow brief and evidence requirements.
- Resolve conflicts explicitly; do not blend incompatible recommendations into
  a vague compromise.
- Accept only claims that come with enough source grounding, test evidence, or
  review support for the task's risk level.
- Keep the final integration as small as the goal allows. Avoid unrelated
  cleanup, speculative abstractions, or extra workflow artifacts.
- When an agent result is shallow, stale, or unsupported, prefer a narrower
  follow-up goal or independent review before the lead agent takes over.

## Final Response

Report the result in terms of the workflow outcome, not the internal drama:
what was delegated, what changed or was produced, what review/verification
happened, what remains uncertain, and what the user should know next.
