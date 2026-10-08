---
name: long-task-control
description: >-
  Re-anchor an agent task when evidence shows drift, design bloat, repeated
  work without new evidence, stale delegation, unresolved review conflict, or
  unsupported completion. Not for ordinary long tasks.
---

# Long Task Control

Preserve verified work while correcting the course. Constrain acceptance and
ownership; leave execution tactics free. This workflow needs no other skill.

## Target

Reconstruct the outcome, scope and acceptance criteria from the original request
and later authorized changes. Newer authorized intent wins; expose unresolved
conflicts. Compare the work against this target at each major phase boundary.

## Observe

Inspect artifacts, commands, checks and delegate state directly. Separate
liveness, progress toward the target and verified completion. Silence, elapsed
time, an active process or a dirty diff alone establishes neither progress nor
failure. Useful diagnosis and necessary preparation count as progress before
acceptance checks finish.

Wait for a meaningful checkpoint while work advances or a known dependency is
pending. A missed checkpoint prompts targeted diagnosis, not automatic
replacement. Repeated failures without changed conditions, a new hypothesis or
diagnostic information call for a new route. Preserve accepted work; stop the
unproductive attempts, not the overall task.

## Challenge

Default to separate, clean-context, read-only reviewers at major phase
boundaries. Challenge **Design** (soundness, ROI, gold-plating) and **Drift**
(intent, progress, evidence, stale work). Reviewers form their findings
independently before reconciliation. Complete contract-changing review before
dependent writing; non-blocking review may run concurrently.

Give one owner the findings: deduplicate, check the evidence, resolve conflicts
and classify actionable defects, boundary notes, overdesign and false positives.
Explain material findings with concrete evidence. Separate review and repair
ownership. Re-review material repairs. At closure, run both lenses twice over
the entire cumulative delivery; preserve any stronger requested review cadence.
Report unavailable independence or incomplete required rounds as review gaps.

## Correct

Disposition material findings: keep, prune, repair, replan or escalate. Break
remaining work into independently verifiable outcomes. Preserve useful context
and artifacts while retiring stale work and its descendants.

For delegated work or handoff, read [Delegation](references/delegation.md).

## Verify

Map the scoped acceptance criteria to real artifacts, actions and observable
outcomes. Identify the delivered version and relevant configuration; confirm the
instance and prerequisites before driving it. Use canonical repository checks
and public user paths, including relevant side effects and required failure or
rollback cases. For documents, check the actual output against its sources.
Existing project verification instructions may supply recipes; their absence
does not prevent direct verification.

Retain the actions, actual results, artifact identity and evidence locations.
Separate review findings from observed behavior. Diagnose environment or driver
failure separately from product failure; preserve the intended expectation.
Repair within scope, then repeat the affected checks and disturbed integration
paths. Reuse evidence that still applies. Clean only this run's resources and
keep its proof readable.

## Continue and close

Continue with the next action that advances the target. Claim task completion
only after necessary delegated results and required reviews are consumed,
material findings are resolved, and applicable acceptance checks pass. Report
failed, blocked and unexecuted paths explicitly.

At a durable boundary, update the existing run record with surprises, changed
decisions and reasons, unresolved judgments, deferred work, evidence pointers
and the next action. A control pass can end with a corrected next action while
the overall task remains pending.
