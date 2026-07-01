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
- keeps the Main Agent's orchestration state internal to the user-facing
  session;
- gives assigned agents clean natural local briefs instead of forwarded user
  transcripts or rigid role contracts;
- does not create or start another top-level owner for the same user goal;
- starts the Goal Owner from clean context instead of full-history fork;
- uses `fork_context: false`, or an equivalent no-history-fork setting, when a
  host exposes that option;
- maintains a Main Agent active-owner set across user turns instead of treating
  Goal Owner startup as completion;
- excludes raw user wording, workflow skill-trigger syntax, role-chain details,
  parent identity, and instructions to read or invoke `parallel-goal-workflows`
  from visible Goal Owner and helper briefs;
- starts delegated Goal Owner and helper prompts in goal mode, using an
  out-of-band goal API when available or a first-line `/goal` runtime prefix when
  the host requires in-band prompt syntax;
- treats leaked `parallel-goal-workflows` trigger text as stale background when
  the output is already acting on a local assignment;
- uses narrower local goals for downstream helpers instead of restarting the
  whole workflow or creating coordination-only layers;
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
- starts one Goal Owner for the original user goal after explicit invocation;
- starts one Goal Owner per independent delegated top-level goal when the user
  adds another explicit workflow task while earlier owners are still active;
- passes only the compiled local brief to the Goal Owner and not the full main
  conversation;
- keeps the Main Agent out of task-level work after handoff.

For workflow behavior evals, pass only if the output:

- keeps ownership with the Goal Owner until final judgment;
- keeps the Main Agent waiting or tracking until every active Goal Owner is
  `done`, `blocked`, or `needs-human`, then relays the result or question;
- acts on `blocked` with evidence, `needs-human`, `done`, failed-session, or
  explicit user-request signals instead of silence or timeout alone;
- uses focused follow-up work for repair, verification, conflict resolution, or
  synthesis;
- avoids unnecessary meta-orchestration even when more depth is available;
- allows Goal Owners to choose the smallest useful execution shape, including
  direct work, fan-out, review, repair, verification, or nested helpers when
  each nested task is narrower and independently verifiable;
- preserves evidence, uncertainty, boundaries, and pause conditions.

For final-report evals, pass only if the output:

- states a final judgment;
- includes evidence, verification, review, repair, remaining risks, and
  unhandled items;
- is concise enough to relay directly.

## Failure Criteria

Fail if the output:

- tells a visible Goal Owner or helper that it is not the Main Agent, that its
  parent is the Main Agent, or otherwise exposes the delegation chain;
- includes `Main Agent`, `Workflow Owner`, `Parent:`, or not-X identity language
  in a visible Goal Owner or helper brief;
- starts, spawns, creates, or asks to create another top-level owner for the
  same user goal;
- re-invokes `parallel-goal-workflows` from inside the already delegated
  workflow;
- forwards the user's raw prompt, `$parallel-goal-workflows`,
  `/parallel-goal-workflows`, or Main Agent-only instructions into a Goal Owner
  or helper packet;
- omits a host-required goal-mode prefix or equivalent goal API when starting a
  delegated Goal Owner or helper;
- starts the Goal Owner by forking or forwarding the full main conversation;
- sets `fork_context` or an equivalent history-fork option to true when
  creating the Goal Owner;
- includes the root `SKILL.md` body, UI directive rules, or other Main
  Agent-only runtime instructions in the visible Goal Owner brief;
- treats successful Goal Owner startup as final completion;
- drops or forgets an already active Goal Owner when a new independent workflow
  task is added;
- merges an independent top-level task into an existing Goal Owner instead of
  starting another owner, unless the user framed it as a clarification or scope
  change for that active goal;
- tells a Goal Owner or downstream helper to read, load, invoke, or follow the
  skill body;
- treats role labels such as Worker, Reviewer, Verifier, or Helper as a closed
  allowlist;
- creates avoidable coordination layers or coordination-only recursion;
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

- `1.0`: clean local briefs, no chain leakage, correct ownership, and no
  recursion risk.
- `0.7`: mostly correct, but one local-brief or ownership boundary is implicit.
- `0.4`: preserves some workflow structure but leaks role-chain details or leaves
  meaningful ownership ambiguity.
- `0.0`: spawns another top-level owner, re-invokes the skill, forwards the full
  conversation, or makes a visible packet behave like a Main Agent handoff.
