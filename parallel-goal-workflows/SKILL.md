---
name: parallel-goal-workflows
description: "User-invoked delegated workflows with clean local briefs."
disable-model-invocation: true
---

# Parallel Goal Workflows

Use this skill only when the user explicitly invokes it with
`/parallel-goal-workflows` or `$parallel-goal-workflows`.

The point is context, not control: the Main Agent turns each delegated
top-level goal into a clean local brief, then one Goal Owner per goal
coordinates focused work through review, repair, acceptance, and final
reporting.

Use native goal mode when the host can attach goals to sessions, threads, or
spawned agents. Prefer out-of-band goal APIs when available. If the host needs
an in-band command to put a new thread or spawned agent into goal mode, put that
runtime mode prefix on its own first line before the brief; for Codex-style
prompt delegation, use `/goal`. Treat the prefix as runtime syntax, not task
context, and do not explain it inside the local brief. If native per-subagent
goals and goal-mode prefixes are unavailable, put the same goal-shaped brief in
the delegation message.

## Ownership Model

```text
Main Agent
  -> Goal Owner per top-level goal
       -> focused agents or helpers as needed
       -> acceptance-ready report
  -> Main Agent user-facing handoff
```

The Main Agent is the user-facing session. It interprets each delegated
top-level goal, turns it into a clean local brief, starts one Goal Owner
for that goal, then tracks active owners and relays. Each Goal Owner owns
task-level decomposition, execution coordination, review, repair, acceptance,
and final judgment for its goal.

Goal ownership is assigned once for the original user goal. Downstream agents
may own narrower local outcomes, but every nested handoff must make the work
smaller, more specific, and independently verifiable.

Only the Main Agent reads this skill. Goal Owners and downstream agents get
local briefs, not this SKILL.md, not the user's raw prompt, and not the
delegation chain that produced the assignment.

## Main Agent

Do:

- collect the user's goal, constraints, preferences, project rules, and evidence
  needs
- compile the user's raw request into one clear local brief; strip invocation
  text and rewrite user wording into goal, context, boundaries, deliverable,
  evidence needs, and pause conditions
- start one Goal Owner per delegated top-level goal in goal mode with that local
  brief in a clean context
- maintain the active Goal Owner set across user turns
- wait with callback-style patience
- relay user clarifications to the Goal Owner
- relay the final report to the user

MUST NOT fork or forward the full main conversation when starting the Goal
Owner. If the host exposes a history-fork option such as `fork_context`, set it
to `false`. The Goal Owner gets the compiled local brief only.

After the Goal Owner starts, do not do task-level research, implementation,
review, repair, verification, or peer-worker spawning for the same task. If the
report has gaps, ask the Goal Owner for a focused follow-up.

## Main Agent Session Goal

Keep the user-facing session open until every active Goal Owner reports
`done`, `blocked`, or `needs-human`, and the result or question has been
relayed to the user. Starting a Goal Owner is not completion.

If the user adds an independent complex task while waiting, start another
Goal Owner for that top-level goal and update the active set. If the new
input changes or clarifies an existing active goal, relay it to that goal's
Goal Owner instead.

## Goal Owner

Choose the smallest useful shape: one worker, fan-out/fan-in, review loop,
repair loop, acceptance pass, deeper helper chain, or another shape that fits.

Common child roles include Worker, Review, Acceptance, Repair, Synthesis,
Verifier, Researcher, Explorer, Implementer, and domain-specific helpers. These
are examples, not a type allowlist.

Child packets are natural local briefs, not forwarded transcripts. Rewrite the
assignment into the local goal, facts, boundaries, and deliverable. Strip skill
invocation text, orchestration-only instructions, raw user wording, and any
details about the delegation chain.

When the host requires an in-band goal-mode command for child agents, place the
command on the first line of the child packet. For Codex-style prompt
delegation, this means `/goal` followed by a blank line and then the local
brief. Do not describe the prefix as part of the task.

Delegation is a local execution choice, not a new top-level workflow. A Goal
Owner may ask focused helpers to inspect, implement, review, repair, verify, or
research narrower outcomes when that reduces risk or saves time. Each nested
handoff must be narrower than the current assignment and have an independently
checkable result. Do not create coordination-only layers, and do not ask another
agent to own the entire assignment. Keep synthesis, acceptance judgment, and the
final report with the current Goal Owner.

Every child packet should include:

- `Local goal`: the narrow outcome this child owns.
- `Context`: only the facts needed for that goal.
- `Boundary`: what the child may touch and what remains outside the local task.
- `Deliverable`: result, evidence, verification, risks, or decision expected
  back.
- `Pause if`: approval, credentials, destructive action, or ownership conflict
  is required.

## Goal Packets

The examples below show the Codex-style in-band goal-mode prefix. If the host
provides an out-of-band goal start mechanism, apply the goal there instead and
omit the prefix from the message body.

For the Goal Owner:

```text
/goal

Take this goal to an acceptance-ready result.

I need you to carry the following goal end to end:

[Natural-language goal summary. Preserve the user's intent, but do not paste the
raw request.]

Useful context:
[Only the constraints, project rules, evidence needs, and facts required for
this work.]

Please decide the execution shape yourself. You can work directly, ask focused
helpers to inspect or implement narrower parts, request independent review, run
repair follow-ups, or add verification where it reduces risk or saves time.

When asking helpers for help, give them only the local task they need: what to
inspect or change, the relevant context, boundaries, expected evidence, and when
to pause. Keep synthesis, acceptance judgment, and the final report with you.

A good final result should include:
[Acceptance criteria, required evidence, verification, review/repair notes,
remaining risks, and unhandled items.]

Long silence is acceptable while work is active. Report on meaningful
milestones, blocked states, needed human input, and completion.

Pause if approval, credentials, destructive action, unclear ownership, or a
judgment call that cannot be resolved from the provided context is needed.
```

For downstream agents:

```text
/goal

[one concrete local outcome.]

Please [inspect / implement / review / verify / research] the following local
task:

[Specific task details.]

Relevant context:
[Only the facts needed for this local task.]

Scope and boundaries:
[Owned files, systems, decisions, and areas to avoid.]

Return:
- what you inspected, changed, verified, or decided
- evidence with file references, commands, citations, screenshots, or other
  proof requested by the task
- risks, uncertainty, and unhandled items
- anything that should pause further work

Pause if approval, credentials, destructive action, or an ownership conflict is
required.
```

## Observation Rhythm

After starting the Goal Owner:

1. Observe workflow state, not output volume. Silence is normal progress unless
   paired with evidence of failure.
2. Treat `running` as a wait state. Do not fill idle time with delegated task
   work.
3. Ask for status only when the user asks, the Goal Owner reports
   `blocked` or `needs-human`, an external signal proves failure, or a
   user-visible decision needs current state.
4. Reclaim or replace ownership only on `blocked` with evidence, `needs-human`,
   an explicit user request, or a failed/dead session. Never reclaim because of
   silence or timeout alone.
5. Relay `done` reports plainly. If the report has gaps, ask the Goal Owner
   for a focused follow-up instead of doing the missing task-level work.

## Final Handoff

The Goal Owner's final report should tell the Main Agent what ran, what
changed or was produced, what review and acceptance happened, what evidence
supports completion, and what remains risky, unresolved, or unhandled.

The Main Agent should relay that report plainly. If obvious pieces are missing,
ask the Goal Owner for a narrower follow-up instead of doing the missing
task-level work.

For Codex nested-subagent configuration, read
`references/codex-nested-subagents.md` only when depth or multi-agent tooling is
the blocker.
