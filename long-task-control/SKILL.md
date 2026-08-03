---
name: long-task-control
description: >-
  Re-anchor an agent task when evidence shows drift, repeated work without new
  evidence, stale delegation, unresolved review conflict, or unsupported
  completion. Not for ordinary long tasks.
---

# Long Task Control

Use a compact control loop that preserves verified work while correcting the
course.

Reconstruct the **target** on every invocation from the original request,
later authorized changes, and acceptance criteria. Newer authorized changes
override older intent; keep unresolved conflicts visible.

1. **Observe.** Read the actual artifacts, checks, remaining work, relevant
   history or rollout, and active agents. Separate completed outcomes from
   reported activity, and do not redo accepted work. Distinguish delegate
   liveness, observable progress, and completion: silence or elapsed time proves
   neither progress nor failure; active commands, dirty artifacts, and new check
   results are progress; only a terminal result backed by acceptance evidence is
   completion. Do not finalize synthesis or close until every required delegated
   result is terminal and consumed; optional work may be stopped when it can no
   longer change the outcome.
2. **Compare.** At the current boundary, compare the artifacts and trajectory
   with the target. Identify missing outcomes, unsupported completion claims,
   scope drift, repeated loops, or effort that no longer improves acceptance.
   Repeat this comparison after each meaningful phase.
3. **Challenge.** Examine both control axes:
   - **Design Challenger:** test ROI, design soundness, and unnecessary
     complexity or redundancy.
   - **Drift Watchdog:** test alignment with the original intent, progress after
     major phases, evidence quality, repeated work, and stale delegation.
   Finish any challenge that can change the contract, interface, or acceptance
   boundary before a writer begins; run only non-blocking guards concurrently.
   Use separate clean-context, read-only reviewers only when independence
   addresses a concrete failure mode or is likely to change the decision;
   otherwise perform both checks directly.
   Before correction, give one owner responsibility for synthesizing all
   findings: deduplicate them, resolve conflicts, and classify each as
   actionable, a false positive, a boundary note, or overdesign.
4. **Correct.** Disposition each material finding by keeping, pruning,
   repairing, replanning, or escalating it. Before interrupting an active
   delegate, inspect its status, dirty diff, active processes, and generated
   artifacts directly; preserve and consume recoverable work. If an execution
   delegate with valuable context terminates with only a plan, give it one
   narrower outcome and exit condition before replacement. Reuse an agent whose
   context still serves the target; retire stale agents and descendant work with
   no remaining outcome. Treat review as a source of candidate findings,
   runtime checks as behavioral evidence, and walkthroughs as recovery of human
   understanding; do not substitute one for another. After a correction,
   recheck the affected surface and any broader acceptance surface the change
   may have disturbed.
5. **Continue.** Resume the highest-value safe action. Stop and replan when
   retries, polling, or agent activity consume resources without producing new
   acceptance evidence. Do not demand terminal-only reports while repeatedly
   prompting for narration; either define meaningful checkpoints or wait using
   direct telemetry. Before a turn, continuation, or handoff boundary, make
   every required delegated result terminal and consume it rather than assuming
   child-agent state will persist. Retain a compact continuation record:
   surprises, adapted decisions, unresolved judgments, follow-ups, and evidence
   pointers. Close only when required delegated work has been consumed and
   acceptance evidence supports completion; otherwise continue or surface the
   real blocker.

A control pass is complete when the target is current, material findings have
a disposition, stale work is retired, and the next action or completion evidence
is clear.
