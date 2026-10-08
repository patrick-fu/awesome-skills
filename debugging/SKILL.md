---
name: debugging
description: >-
  Diagnose bugs or performance regressions when static inspection stalls,
  attempted fixes fail, or runtime evidence needs interpretation.
---

# Debugging

Build causal evidence for the reported failure. Match the request: diagnosis
ends with findings and remaining uncertainty; a fix request includes the
related repair and verification. Use project conventions and relevant domain
or architecture documentation. Redact secrets from shared commands, outputs,
and captures; pass credentials through the environment.

## Anchor

Identify the expected behavior, actual symptom, affected scenario, and relevant
artifact/version, configuration, and state. Distinguish observations from
hypotheses. Reuse prior evidence when its identity and conditions still match.

Keep the original scenario as the acceptance target. A nearby error, mock-only
failure, or different instance is not a substitute for the reported symptom.

## Observe

Choose the smallest available evidence that can distinguish likely causes.
Start with the relevant route; load further references only when the evidence
gap requires them.

- **Reproduce:** run a symptom-specific test, request, CLI, replay, or harness.
  Verify that it actually fails on this bug. Tighten or minimize the loop where
  useful, retaining the original inputs and conditions.
- **Instrument:** when a running path needs observation, read
  [instrumentation](references/instrumentation.md).
- **Forensics:** for existing captures or profiling a live process, read
  [forensics](references/forensics.md).
- **Flaky:** for intermittent, concurrent, or order-dependent failures, read
  [flaky failures](references/flaky-failures.md).

Use credible logs, captures, and source evidence even when a full reproducer is
unavailable. State which claims they support and which remain untested.
Run reachable checks yourself. When a device, permission, or physical action
requires the user, request the smallest concrete action and evidence return.

## Probe

Rank plausible alternatives. For each useful probe, state its prediction:
"If X causes the failure, observing or changing Y should produce Z."
Change one discriminating factor where practical and compare the result with
the prediction. Trace the first divergence back through boundaries and callers
to the originating state or input. Negative results narrow the search too.

Keep hypotheses provisional until evidence distinguishes their mechanism from
credible alternatives. Choose the next probe from the remaining evidence gap.

## Reframe

When failed attempts repeat without distinguishing causes, inspect the premise
they share before another patch. Check artifact identity, actors, inputs,
state, ordering, lifetime, and environment; change the evidence channel when
needed. Revert your refuted speculative changes while preserving user edits.
If access or evidence blocks progress, report what was tried and the smallest
missing action or artifact.

## Fix

Apply the smallest repair supported by the evidence and requested scope.
At a seam that exercises the real failure pattern, turn the reproducer into a
regression check and observe its failure before the repair when feasible.
If deliberately mutating code to establish that a check catches the bug,
verify the mutation landed against a pristine copy before trusting the result.
Document a missing seam or baseline rather than manufacturing a passing proxy.

## Verify

Run the original, unminimized scenario against the repaired artifact and run
the applicable regression and affected-path checks. For intermittent or
performance failures, retain comparable conditions and report the actual
observations. A green reduced test alone does not establish original-scenario
success. Keep unavailable or inconclusive checks explicit.

Remove this investigation's temporary instrumentation, processes, and debug
resources; preserve existing product logs, user work, and useful evidence.
When cleanup changes executable behavior or measurement conditions, recheck
the original scenario on the cleaned artifact. Report any unverified final
artifact explicitly.
Report the supported cause, relevant change, executed checks and outcomes,
and remaining limitations. Claim resolution only to the extent verified.
