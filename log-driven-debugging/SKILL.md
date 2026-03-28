---
name: log-driven-debugging
description: >
  Debug complex or unclear problems by instrumenting code with targeted logs, having the user rerun
  the scenario, and then analyzing the returned logs to locate the real failure point. Use this whenever
  the issue is hard to reason about statically, reproduction exists but the root cause is unclear, the
  user says things like "add some logs", "instrument this", "let me run it and send you the logs",
  "help me locate where it goes wrong", or any time a tricky bug needs a structured log-first diagnosis
  loop instead of guessing from code alone.
---

When the bug is slippery, stop guessing and build observability.

This skill is for situations where:
- the visible symptom is known, but the actual failure layer is not
- static code reading is no longer enough
- one execution with good logs can collapse a large search space

The workflow is simple:
1. decide where to instrument
2. add high-signal logs
3. have the user rerun the scenario
4. analyze the returned logs
5. only then propose or implement the real fix

## First move

Before adding any logs, ask the user for a **log prefix**.

This is required, not optional. Explain why briefly: the prefix makes the new logs searchable and prevents them from being lost in normal application output.

Good prefixes look like:
- `Patrick`
- `MyDebug`
- `DebugTrace`

Prefer a short prefix that:
- is unique in the current codebase
- is easy to grep
- is unlikely to collide with existing production logs

If the user does not care, ask for one and wait. Do not silently invent a prefix unless the user explicitly delegates that choice.

## Logging strategy

Do not scatter random prints everywhere. Instrument the execution path deliberately.

Choose logs around:
- entry points where the user action first enters the system
- state transitions where data changes shape
- serialization or conversion boundaries
- async handoff points
- final outbound effects such as send, save, render, request, or callback

For each log, include enough structure to reconstruct the flow:
- the shared prefix
- a timestamp
- a short tag for the subsystem or phase
- the minimum fields needed to compare expected vs actual behavior

Treat the timestamp as part of the standard format, not a nice-to-have. For tricky bugs, ordering is often as important as values.

Prefer logs that answer:
- Did this code path run?
- In what order did the steps happen?
- What data existed at this point?
- Where did duplication, loss, mutation, or branching first appear?

Avoid:
- giant object dumps unless they are truly needed
- vague messages like "here" or "called"
- logging so much that the signal disappears

## What to log

The exact fields depend on the bug, but in general log:
- identifiers
- counts
- ranges or indexes
- booleans for state
- input and output summaries
- boundary transformations

Examples:
- `count=4`
- `state=editing`
- `range={loc=12,len=3}`
- `contentList=[0] mention | [1] text`
- `requestID=...`

Prefer a consistent line shape such as:

```text
[<PREFIX>][2026-03-28T13:45:27.870+08:00][Serializer] contentList=[0] mention | [1] text
```

When strings are important, escape newlines so one logical log stays on one physical line.

## Handoff to the user

After instrumenting, tell the user exactly what to do next:
- rebuild or rerun the app/program
- reproduce the issue once
- collect the logs containing the chosen prefix
- send those logs back

Be explicit that they should return **only the lines with the prefix** when possible.

Recommend a filter like:

```bash
rg "\\[<PREFIX>\\]" <log-file>
```

or an equivalent grep/search flow in their environment.

## Analysis pass

When the user sends logs back, do not jump straight to a fix. Reconstruct the path first.

Read the logs in order and answer:
1. What is the first confirmed event?
2. What state is proven correct?
3. What is the first line where reality diverges from expectation?
4. Which layer owns that divergence?
5. Is the bug caused by duplication, missing data, wrong boundary detection, stale state, or ordering/race?

Call out the precise transition where the bug begins, not just where it becomes visible.

If the logs prove the current instrumentation is insufficient, ask for one more round and specify the next smallest set of logs needed. Do not ask for a broad second pass if one or two extra logs will do.

## Output expectations

Your response after log analysis should be crisp and causal:
- what the logs prove
- where the root cause starts
- what is not the root cause
- what code should change next

If proposing a fix, tie it directly to the observed divergence in logs.

## Scope

Keep this skill general. It applies to:
- app bugs
- backend handlers
- UI flows
- serialization problems
- async ordering issues
- duplicated side effects
- state machine bugs

It is not tied to any single language, framework, or repository.

## Practical rule

The user runs the instrumented build. You analyze the prefixed logs.

That division of labor is the whole point of this skill.
