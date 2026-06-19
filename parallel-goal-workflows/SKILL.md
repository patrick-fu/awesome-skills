---
name: parallel-goal-workflows
description: "This skill should be used only when the user explicitly asks to use `parallel-goal-workflows` or clearly requests a lead agent to delegate to an orchestrator that manages workers, review, acceptance, and repair while the lead only waits and reports. This is a deliberate high-overhead workflow pattern, not a default response to ordinary subagent, parallel work, coding, research, review, or goal-decomposition requests."
---

# Parallel Goal Workflows

Use this skill when a task should be handled through delegated goals rather
than direct lead-agent execution. The point is context, not control: give agents
enough intent and boundaries to act well, then let the workflow owner run the
workflow.

## Core Shape

Prefer this ownership model whenever delegation is in scope:

```text
Lead Agent
  -> Orchestrator Agent
       -> Worker / Research / Evidence Agents
       -> Review Agent
       -> Acceptance or Verification Agent
       -> Repair Agent when needed
       -> Orchestrator final report
  -> Lead user-facing handoff
```

The lead does not need to be the hidden worker, reviewer, or verifier. The
orchestrator owns task-level workflow acceptance. The lead owns only the
conversation-level handoff.

## Lead Agent

The lead agent is the entry point and reporting layer.

The lead should also hold its own goal. This goal is not "do the task" and is
not task-level acceptance. It is a conversation-level boundary goal:

```text
/goal Hold the delegated workflow boundary until the orchestrator returns an
acceptance-ready report, then relay it to the user without doing task-level
work.
```

Waiting is part of that goal. The lead is actively preserving the workflow
boundary, carrying user-facing communication, and preventing idle time from
turning back into direct execution. If the orchestrator's report is missing
obvious pieces, the lead asks the orchestrator for a narrower follow-up instead
of filling the gap itself.

Lead responsibilities:

- understand the user's goal, constraints, and any important context
- start an orchestrator subagent whenever delegated work is in scope
- give the orchestrator enough orientation to act independently
- wait with the longest reasonable wait window or callback-style interface
- relay user clarifications or new constraints to the orchestrator
- replace a clearly failed or unresponsive orchestrator with a narrower
  orchestrator goal when needed
- report the orchestrator's final report to the user

Lead non-responsibilities after the orchestrator starts:

- do not research, edit, implement, review, repair, or verify the same task
- do not spawn peer workers that bypass the orchestrator
- do not run a separate review or acceptance path unless the orchestrator asks
  for help
- do not treat a wait timeout as permission to take over
- do not re-open the content to perform task-level acceptance; check the report
  shape and surface its risks instead

## Orchestrator Agent

The orchestrator owns the workflow. Its job is to decide the shape of the work,
not necessarily to do all work personally.

Orchestrator responsibilities:

- turn the lead's context into downstream goals
- decide whether the workflow needs workers, reviewers, acceptance agents, or
  no further agents
- collect worker outputs and resolve conflicts explicitly
- route important work through independent review
- run repair loops when review fails
- ask an acceptance or verification agent to check the final result when useful
- make the final task-level acceptance decision
- return an acceptance-ready report for the lead to relay

The orchestrator may keep the workflow very small. Starting with an
orchestrator is not ceremony; it keeps scheduling, review, repair, and
acceptance out of the lead's hands.

## Downstream Agents

Every downstream agent should receive a goal, not a vague chore.

Common roles:

- Worker Agent: produces the artifact, patch, research, extraction, or other
  concrete work.
- Review Agent: independently checks worker output for bugs, unsupported
  claims, missed constraints, regression risk, or weak evidence.
- Acceptance / Verification Agent: checks whether the reviewed result satisfies
  the user goal, constraints, and evidence needs.
- Repair Agent: fixes a narrow problem found by review or acceptance.
- Synthesis Agent: merges several evidence or worker streams without hiding
  disagreement.

Do not over-regulate worker agents. A worker, reviewer, or acceptance agent may
choose to spawn its own subagents when that helps its goal. Do not encourage
extra nesting for its own sake, and do not forbid it. The harness can enforce
its own depth and concurrency limits.

If you are running inside Codex and a workflow needs nested subagents but the
environment appears limited to direct child agents, or if Codex multi-agent
tools seem unavailable, read `references/codex-nested-subagents.md` before
changing the workflow design.

## Delegation Context

Before spawning the orchestrator, provide enough orientation for independent
work. This can be a paragraph rather than a form. Useful context may include:

- what the user is trying to achieve
- why the work matters
- known preferences, constraints, and repository or project rules
- what would make the result good enough to accept
- evidence, artifacts, or review signals that would make the final report
  trustworthy

Keep the context flexible. Do not freeze every boundary before agents have
learned from the repo, source material, logs, or user environment.

## Goal Packets

For the lead, keep the packet lightweight and conversation-level:

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

For downstream agents, keep packets smaller:

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

Observation mode should feel closer to callback than polling.

After setting the lead goal and starting the orchestrator:

1. Use the longest reasonable wait window.
2. Do not fill idle time with delegated task work.
3. Ask for status only after a meaningful timeout, when the user asks, when an
   external signal suggests failure, or before replacing the orchestrator.
4. If the orchestrator is still running and not clearly blocked, keep waiting.

This patience matters because short polling creates gaps that invite the lead
to become a hidden worker.

## Workflow Patterns

Use these as patterns, not scripts.

Fan-out / fan-in:

```text
Orchestrator
  -> Worker A
  -> Worker B
  -> Worker C
  -> Synthesis
  -> Review
  -> Acceptance
  -> Final report
```

Pipeline:

```text
Research
  -> Modeling
  -> Worker
  -> Review
  -> Acceptance
  -> Final report
```

Review / repair loop:

```text
Worker
  -> Review
     -> pass: Acceptance
     -> fail: Repair -> Review
  -> Final report
```

Minimal orchestrated workflow:

```text
Orchestrator
  -> decides no downstream worker is needed
  -> does minimal coordination or validation
  -> Final report
```

Nested worker workflow:

```text
Orchestrator
  -> Worker
       -> optional sub-worker chosen by Worker
  -> Review
  -> Acceptance
  -> Final report
```

## Final Handoff

The orchestrator's final report should tell the lead:

- what workflow ran
- what changed or was produced
- what review and acceptance happened
- what evidence supports completion
- what remains risky or unresolved
- what the lead should tell the user

The lead should relay that report plainly. If the report is missing obvious
pieces, ask the orchestrator for a narrower follow-up instead of silently doing
the missing task-level work.
