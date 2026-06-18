---
name: parallel-goal-workflows
description: "Guides lead agents when users ask for subagents, parallel agents, multi-agent execution, delegated workflows, or goal decomposition. It favors orchestrator-first delegation: start an orchestrator subagent whenever possible, then have the lead observe status instead of doing parallel task work, while preserving context, patience, review signals, and final acceptance."
---

# Parallel Goal Workflows

Use this skill when delegated work should be shaped as goals, not just task
prompts. The point is context, not control: give each agent enough intent,
evidence, and boundaries to move independently without forcing a rigid script.

## Operating Principles

- Bias the lead agent toward orchestration when the user asks for subagents,
  parallel agents, multi-agent work, workflow coordination, or goal
  decomposition.
- When delegation is in scope, prefer starting with an orchestrator subagent
  whenever possible. Let that agent own workflow shaping, decide whether
  downstream workers are needed, route review or repair, and return an
  acceptance-ready report.
- Once the orchestrator is running, the lead should stop doing task work in
  parallel. The lead monitors status, relays user input, handles liveness, and
  waits for the orchestrator's result.
- Treat direct peer-worker dispatch as the exception. Use it when the user asks
  the lead to dispatch specific workers directly, nested delegation is not
  available, or an orchestrator would add no useful ownership.
- Orient agents before dispatching them. A few useful sentences are often
  better than a rigid form.
- Give every subagent a clear outcome-focused goal. If `/goal` is available,
  use it or ask the subagent to create one before execution.
- Provide rich context: why the work matters, what evidence counts, what must
  stay unchanged, and when the agent should pause.
- Prefer patient coordination over impatient takeover. A wait timeout means the
  wait window expired, not that the subagent failed.
- Nested delegation is the preferred shape for delegated workflows, not because
  it adds ceremony, but because it keeps the lead from becoming the hidden
  scheduler. The orchestrator may still decide that no downstream workers are
  needed.
- Treat review as its own goal when quality, safety, history, or source
  grounding matters. A fresh reviewer usually catches different failures than
  the worker who produced the result.
- The lead agent owns final acceptance and the user-facing answer, but should
  avoid becoming the hidden executor or hidden parallel worker unless the user
  asks for direct execution or delegation is unavailable.
- If delegation is not useful or not available, either produce copy-ready goals
  for the user or proceed directly with the smallest honest workflow; disclose
  that fallback instead of pretending a multi-agent workflow happened.

## Delegation Context

Before spawning agents, give them enough orientation to act independently. This
can be a paragraph, not a form. Useful context may include:

- what the user is trying to achieve
- why the work matters
- what would make the result good enough to accept
- known preferences, constraints, or nearby work
- evidence, artifacts, or review signals that would help the lead trust the
  result

Keep the context alive and flexible. Do not freeze every boundary before the
agents have learned from the repo, source material, logs, or user environment.
Use the orientation to prepare an orchestrator goal first when delegation is
available. Do not overbuild the downstream tree: the orchestrator can keep the
workflow small, use peer workers only when useful, or report that direct
execution is the honest fallback.

## Lead Observation Mode

After spawning an orchestrator, the lead agent shifts into observation mode.
This is the main guardrail: the lead should not keep researching, editing,
reviewing, repairing, or spawning workers for the same task while the
orchestrator is active.

Useful lead actions during observation mode:

- wait for the orchestrator
- request a status update after a wait timeout
- relay user clarifications or new constraints to the orchestrator
- replace a clearly failed or unresponsive orchestrator with a narrower
  orchestrator goal
- do final acceptance after the orchestrator returns

These are not useful lead actions during observation mode:

- reading files or sources to solve the same delegated work
- implementing, editing, or committing the delegated work
- running a parallel review or repair path that the orchestrator did not ask
  for
- spawning peer workers that bypass the orchestrator
- treating a wait timeout as permission to take over

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

For an orchestrator subagent, make the goal about owning the coordination,
not doing all work personally:

```text
/goal Orchestrate this delegated workflow to completion and return an
acceptance-ready report.

Context:
[Top-level objective, user constraints, repository rules, and quality bar.]

Deliverable:
[Agent graph, completed work, review result, verification evidence, remaining
risks, and final recommendation.]

Boundaries:
[What the orchestrator may assign, what it may edit, and what must remain
outside scope.]

Verification:
[Independent review, repair loop when needed, and final checks.]

Pause if:
[The workflow needs user judgment, external approval, secrets, or a repeated
blocker cannot be resolved by narrowing or reassigning work.]
```

## Coordination Rhythm

1. Clarify the top-level outcome and acceptance evidence.
2. Start with an orchestrator subagent whenever delegation is available.
3. Let the orchestrator decide whether to create downstream goals for workers,
   reviewers, repair agents, or no further agents.
4. While the orchestrator runs, observe instead of working in parallel: wait,
   request status, relay user input, or replace a failed orchestrator with a
   narrower orchestrator goal.
5. Let the orchestrator route important results through independent review when
   the cost of being wrong is meaningful.
6. Accept the work only after the orchestrator's reported evidence matches the
   user goal and any required checks pass.

## Synthesis

Synthesize results without flattening disagreement:

- Compare agent outputs against the delegation context and evidence needs.
- Resolve conflicts explicitly; do not blend incompatible recommendations into
  a vague compromise.
- Accept only claims that come with enough source grounding, test evidence, or
  review support for the task's risk level.
- Keep the final integration as small as the goal allows. Avoid unrelated
  cleanup, speculative abstractions, or extra workflow artifacts.
- When an agent result is shallow, stale, or unsupported, prefer asking the
  orchestrator for a narrower follow-up goal or independent review before
  accepting the work.

## Final Response

Report the result in terms of the workflow outcome, not the internal drama:
what was delegated, what changed or was produced, what review/verification
happened, what remains uncertain, and what the user should know next.
