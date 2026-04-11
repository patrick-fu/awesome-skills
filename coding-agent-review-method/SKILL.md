---
name: coding-agent-review-method
description: >-
  Methodology for orchestrating an external code review through a
  delegated coding-agent sub-agent. Use this whenever the user wants a
  code review performed by a specific coding agent rather than by the
  primary agent, wants to review a diff, patch, staged changes, PR, MR, or
  specific files through an external coding agent, or needs a rigorous
  findings-first review workflow that stays separate from patching,
  building, and testing. This skill is methods-only: it does not define
  how to invoke any specific coding agent, so when the user has not named
  the coding agent you must ask which one to use.
---

# Coding Agent Review Method

## Mission

Provide the methodology for running an external code review through a delegated coding-agent sub-agent.

Your job is to:
- resolve the review target, review scope, and review intent
- require the user to name the coding agent when they have not done so
- prepare high-context review inputs that a chosen coding agent can consume
- treat the user-supplied diff, range, patch, commit, or file list as the primary review scope
- require bounded impact tracing into the minimum necessary related context when local risk depends on callers, references, consumers, contracts, compatibility assumptions, or adjacent upstream/downstream behavior
- keep review-only work separate from implementation, build, and test workflows
- require unique per-run artifacts and a clear findings-first output contract
- direct the executor to consult the chosen coding agent's own operating guide for invocation details

This skill is methodology only. It does not define how to invoke Claude, Cursor, Codex, or any other coding agent.

## Applicability gate

Use this skill when the user wants:
- an external coding agent to review code
- a reusable review methodology that works across multiple coding agents
- a clean separation between review orchestration and agent-specific execution details

Do not use this skill as the direct execution guide for a specific coding agent. Once the coding agent is known, the executor must consult that agent's own operating guide for:
- the command or API shape
- prompt submission mechanics
- output capture mechanics
- retry or resume behavior
- any agent-specific limits or caveats

## Required clarification

If the user has not named a coding agent, stop and ask which coding agent should perform the review.

Do not silently pick one.
Do not treat the current host agent as the answer unless the user explicitly said to use it.

Examples of sufficient answers:
- `Use Claude Code`
- `Use Cursor`
- `Use Codex`
- `Use my team's custom coding agent wrapper`

## Inputs to resolve before review planning

Resolve these from the conversation first. If one is missing and you can infer it safely, do so. Only ask the user when the missing item changes the review result materially.

1. `coding agent`
   The external coding agent that should perform the review.

2. `workdir`
   The repository or folder the coding agent should review inside.

3. `review scope`
   One of:
   - staged diff
   - unstaged diff
   - branch diff
   - specific files
   - PR or MR patch
   - pasted code

4. `background`
   Why this change exists, what behavior is expected, and any risk areas the user already cares about.

5. `already reviewed`
   Any context that has already been checked so the external coding agent does not waste time repeating it.

6. `review run id`
   A unique identifier for this exact review invocation.

7. `impact focus`
   The likely affected callers, references, consumers, contracts, compatibility assumptions, or integration seams worth tracing beyond the edited lines.

## Core review method

### 1. Lock the scope before delegation

Lock the user-supplied diff, range, patch, commit, or file list as the primary review scope before involving the external coding agent.

Prefer:
- the exact staged diff
- a specific branch range
- a concrete file list
- a pasted patch

Avoid sending the external coding agent on a whole-repository exploration when the user gave a narrower surface.

### 2. Follow bounded impact traces by default

Do not stop at the edited lines when the risk depends on nearby usage or integration seams.

The delegated coding agent should proactively inspect the minimum necessary related context needed to evaluate impact and chained risk. Prefer tracing:
- touched symbols and their definitions
- direct callers or call sites
- references and consumers
- implemented, inherited, or overridden contracts
- compatibility assumptions relied on elsewhere
- adjacent configuration, flags, schemas, serialization boundaries, or immediate upstream/downstream behavior

This is bounded impact tracing, not repo-wide exploration.
Stop once additional context no longer changes the risk assessment materially.

### 3. Preserve the user's real context

Every review run should carry:
- the change intent
- the expected behavior
- the concrete review scope
- what is already known or already checked
- the focus areas that matter for this change
- the likely impact edges worth tracing, such as callers, consumers, contracts, compatibility assumptions, or adjacent module boundaries

Do not make the external coding agent rediscover basic context that the user already gave you.

### 4. Enforce review-only boundaries

The review run must stay review-only unless the user explicitly broadened the task.

The external coding agent must be told:
- review only
- do not modify files
- do not start building or testing
- do not drift into implementation planning unless the user asked for that

Keep review, patching, build validation, and testing as separate phases.
Review-only does not forbid bounded code-reading needed to assess impact; it forbids editing, building, testing, and implementation work.

### 5. Require findings-first output

The external coding agent should lead with actionable findings.

The preferred structure is:
- findings first
- then any clarifying notes
- explicitly state when there are no clear findings

Each finding should explain the local issue and, when relevant, the impacted caller, consumer, contract, compatibility assumption, or propagation path that makes the issue meaningful.

This keeps the result usable inside larger closeout workflows.

### 6. Isolate every review run

Every review run must have a unique `<review-run-id>`.

Recommended composition:
- a stable topic fragment such as branch or feature name
- the current short `HEAD`
- a timestamp
- a short random suffix

Every run should use unique artifacts derived from that id, such as:
- prompt file
- output file
- stderr or diagnostic file

Do not reuse artifacts across concurrent runs or repeated passes on the same branch.

### 7. Delegate to a dedicated review sub-agent

When the host framework supports sub-agents, delegate the review execution to a dedicated coding-agent sub-agent for that run.

That delegated sub-agent should have a narrow role:
- consult the chosen coding agent's operating guide
- execute one review run through that coding agent
- return the raw review result and any relevant diagnostics

It should not become a second orchestrator that rewrites scope, makes product decisions, or starts implementation work.

## Coding agent operating guide contract

This methodology depends on a separate operating guide for the chosen coding agent.

That guide must tell the executor all of the following:

1. How to name and resolve the coding agent
   Examples:
   - fixed command name
   - user-provided wrapper path
   - API-backed agent name

2. How to submit the review prompt
   Examples:
   - inline command argument
   - prompt file
   - stdin
   - API payload

3. How to capture raw output
   Examples:
   - stdout file
   - structured response file
   - result artifact path

4. How to capture diagnostics or failures
   Examples:
   - stderr file
   - status metadata
   - exit code handling

5. Whether the agent supports delegated or background execution cleanly

6. Any agent-specific retry rules, guardrails, or limitations

If the chosen coding agent does not have an operating guide that answers these questions, stop and say the methodology cannot be executed safely yet.

## Prompt construction

Before execution, prepare a high-context review prompt. Prefer the template in [assets/review_prompt_template.md](assets/review_prompt_template.md).

The prompt should include:
- repository path
- exact review scope
- background
- already-reviewed facts
- focus areas
- the rule that the supplied diff or range is the primary scope
- explicit impact targets such as callers, references, consumers, contracts, compatibility assumptions, and likely blast-radius edges
- review-only constraints
- the required findings-first output behavior

If a domain-specific review guide is relevant, include it explicitly in the prompt package. Examples:
- platform-specific review guides
- architecture-specific review guides
- design-system review guides
- security review guides

Only include domain guides that genuinely apply to the reviewed surface.

## Failure handling method

If the external coding agent fails immediately:
- inspect the raw output artifact first
- then inspect diagnostics from that agent's operating guide
- distinguish between invocation failure and a genuine review result

If the external coding agent returns weak or generic review fluff:
- tighten the primary scope when the reviewed surface was still vague
- add the exact files or diff range
- add already-reviewed facts
- explicitly name the symbols, callers, references, consumers, contracts, or compatibility assumptions that should be checked
- restate the findings-first and bounded impact-tracing contract
- rerun once with fresh artifacts

If the external coding agent tries to edit files or broaden the task:
- restate that this run is review-only
- separate that follow-up work into a later phase

## What context to give the external coding agent

Good context:
- change intent
- expected behavior
- affected files
- touched symbols and likely callers, references, or consumers
- known risky areas
- compatibility or contract assumptions that may matter
- validation already completed
- the user's explicit concerns

Bad context:
- huge unrelated repository history
- broad instructions like `review everything`
- open-ended prompts that invite repo-wide wandering without a concrete impact hypothesis
- long raw logs with no diagnosis
- irrelevant domain guidance

## Output contract

Your final response back to the user should include:

```markdown
## External Review
- Coding agent: <chosen coding agent>
- Scope: <what the external coding agent reviewed>
- Operating guide used: <which guide you consulted>

## Findings
- <high-confidence findings, or "No clear findings">

## Notes
- <any execution detail that matters: narrowed scope, rerun, diagnostics consulted, etc.>
```

If the external coding agent reported no issues, say so plainly and mention any residual validation gap only if it is real.

## Guardrails

- Do not silently choose the coding agent when the user did not specify one.
- Do not confuse this methodology skill with a concrete execution guide.
- Do not let the external coding agent free-roam the repository when the user gave a narrow scope.
- Do not stop at the edited lines when nearby callers, consumers, references, or contracts materially affect risk.
- Do not follow impact traces indefinitely; stop once added context no longer changes the risk assessment materially.
- Do not reuse artifacts across review runs.
- Do not treat an invocation failure as `No clear findings`.
- Do not mix code review and code edits in the same external review run unless the user explicitly asked for both.
- Do not ask the external coding agent to build, test, or patch unless the user asked for that broader workflow.
- Do not lose the user's background context between passes.

## Quick example

User request:

```text
Use Cursor to review these files for regression risk and lifecycle issues. Build already passed.
```

What you do:
- confirm the coding agent is `Cursor`
- lock the primary scope to the exact files or diff
- prepare a prompt file with background, already-reviewed facts, focus areas, likely impact edges, and review-only constraints
- tell the review agent to inspect the minimum necessary callers, references, consumers, contracts, and nearby integration seams needed to judge blast radius
- consult Cursor's own operating guide for execution details
- delegate the review run to a dedicated coding-agent sub-agent when the host framework supports it
- return findings in a findings-first structure
