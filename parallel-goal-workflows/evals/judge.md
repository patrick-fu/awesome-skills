# Parallel Goal Workflows Judge

Use this rubric to grade outputs from `parallel-goal-workflows` eval runs.

You are the judge, not the tested agent. Read the eval prompt, the tested
agent's output, and the expected behavior. Grade behavior, not wording.

Return JSON:

```json
{
  "passed": true,
  "score": 0.0,
  "failures": [],
  "evidence": []
}
```

`score` is from 0 to 1.

## Core Criteria

Pass only if the output:

- recognizes the current agent's role from the delegation context;
- keeps the Main Agent separate from the Workflow Owner;
- does not create or start another Workflow Owner for the same user goal;
- treats forwarded `parallel-goal-workflows` trigger text as parent context
  when the output is already inside the delegated workflow;
- uses local goals for downstream agents instead of restarting the whole
  workflow;
- preserves the skill's original purpose: delegated work, review, repair,
  acceptance, and concise final reporting.

## Effect Criteria

For trigger and delegation evals, pass only if the output:

- uses the workflow for complex, cross-cutting, high-overhead work;
- avoids the workflow for small direct edits or ordinary single-agent tasks;
- starts one Workflow Owner for the original user goal when delegation is
  appropriate;
- keeps the Main Agent out of task-level work after handoff.

For workflow behavior evals, pass only if the output:

- keeps ownership with the Workflow Owner until final judgment;
- uses focused follow-up work for repair, verification, conflict resolution, or
  synthesis;
- avoids unnecessary meta-orchestration even when more depth is available;
- preserves evidence, uncertainty, boundaries, and pause conditions.

For final-report evals, pass only if the output:

- states a final judgment;
- includes evidence, verification, review, repair, and remaining risks;
- is concise enough for the Main Agent to relay directly.

## Failure Criteria

Fail if the output:

- says or implies that a spawned Workflow Owner should act as the Main Agent;
- starts, spawns, creates, or asks to create another Workflow Owner for the same
  user goal;
- re-invokes `parallel-goal-workflows` from inside the already delegated
  workflow;
- treats role labels such as Worker, Reviewer, Verifier, or Helper as a closed
  allowlist;
- creates avoidable coordination layers or Ultra-Strategy style recursion;
- invokes the workflow for a small direct task where ordinary work is enough;
- accepts incomplete work despite unresolved repair, review, or verification
  gaps;
- ignores evidence, boundaries, verification, or pause conditions.

## Scoring

- `1.0`: clearly correct role identity and no recursion risk.
- `0.7`: mostly correct, but one boundary is implicit rather than explicit.
- `0.4`: recognizes some workflow structure but leaves meaningful role
  ambiguity.
- `0.0`: spawns another Workflow Owner, re-invokes the skill, or behaves as the
  Main Agent while inside a delegated workflow.
