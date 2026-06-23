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

- uses this workflow only after explicit user invocation such as
  `/parallel-goal-workflows` or `$parallel-goal-workflows`;
- recognizes the current agent's role from the delegation context;
- keeps the Main Agent separate from the Workflow Owner;
- does not create or start another Workflow Owner for the same user goal;
- treats delegation packets as compiled task contracts, not forwarded user
  transcripts;
- starts the Workflow Owner from clean context instead of full-history fork;
- uses `fork_context: false`, or an equivalent no-history-fork setting, when a
  host exposes that option;
- excludes raw user wording, slash-command syntax, skill triggers, and
  instructions to read or invoke `parallel-goal-workflows` from downstream
  packets;
- treats forwarded `parallel-goal-workflows` trigger text as parent context
  when the output is already inside the delegated workflow;
- uses local goals for downstream agents instead of restarting the whole
  workflow;
- observes workflow state instead of output volume, and treats silence during
  `running` work as normal progress rather than failure;
- preserves the skill's original purpose: delegated work, review, repair,
  acceptance, and concise final reporting.

## Effect Criteria

For trigger and delegation evals, pass only if the output:

- uses the workflow for complex, cross-cutting, high-overhead work only when
  the user explicitly invoked it;
- avoids the workflow for small direct edits, ordinary single-agent tasks, or
  complex tasks where the user did not explicitly invoke this skill;
- starts one Workflow Owner for the original user goal after explicit
  invocation;
- passes only the compiled task contract to the Workflow Owner and not the full
  main conversation;
- keeps the Main Agent out of task-level work after handoff.

For workflow behavior evals, pass only if the output:

- keeps ownership with the Workflow Owner until final judgment;
- acts on `blocked` with evidence, `needs-human`, `done`, failed-session, or
  explicit user-request signals instead of silence or timeout alone;
- uses focused follow-up work for repair, verification, conflict resolution, or
  synthesis;
- avoids unnecessary meta-orchestration even when more depth is available;
- preserves evidence, uncertainty, boundaries, and pause conditions.

For final-report evals, pass only if the output:

- states a final judgment;
- includes evidence, verification, review, repair, remaining risks, and
  unhandled items;
- is concise enough for the Main Agent to relay directly.

## Failure Criteria

Fail if the output:

- says or implies that a spawned Workflow Owner should act as the Main Agent;
- starts, spawns, creates, or asks to create another Workflow Owner for the same
  user goal;
- re-invokes `parallel-goal-workflows` from inside the already delegated
  workflow;
- forwards the user's raw prompt, `$parallel-goal-workflows`, slash-command
  syntax, or Main Agent-only instructions into a Workflow Owner or worker
  packet;
- starts the Workflow Owner by forking or forwarding the full main conversation;
- sets `fork_context` or an equivalent history-fork option to true when
  creating the Workflow Owner;
- includes the root `SKILL.md` body, UI directive rules, or other Main
  Agent-only runtime instructions in the Workflow Owner packet;
- tells a Workflow Owner or downstream worker to read, load, invoke, or follow
  the skill body;
- treats role labels such as Worker, Reviewer, Verifier, or Helper as a closed
  allowlist;
- creates avoidable coordination layers or Ultra-Strategy style recursion;
- treats silence, low output, or timeout alone as evidence that the delegated
  workflow is stuck;
- restarts, replaces, reclaims, or duplicates delegated work without a blocked
  signal with evidence, a needs-human signal, a failed/dead session, or an
  explicit user request;
- auto-invokes the workflow for a complex task where the user did not explicitly
  request `/parallel-goal-workflows` or `$parallel-goal-workflows`;
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
