---
name: long-task-control
description: >-
  Re-anchor an agent task when evidence shows drift, design bloat, repeated
  work without new evidence, stale delegation, unresolved review conflict, or
  unsupported completion. Not for ordinary long tasks.
---

# Long Task Control

Run a control loop that preserves verified work while correcting the course.
Its governing principle: **constrain the process, leave the tactics free** —
the gates below are hard, but how the agent improvises within them is not.

Reconstruct the **target** on every invocation from the original request,
later authorized changes, and acceptance criteria. Newer authorized changes
override older intent; keep unresolved conflicts visible.

1. **Observe.** Read the actual artifacts, checks, remaining work, history or
   rollout, and active agents — and trust *these*, not an agent's reported
   activity or self-claimed progress. Distinguish delegate liveness, observable
   progress, and completion: silence or elapsed time proves neither progress nor
   failure; active commands, dirty artifacts, and new check results are
   progress; only a terminal result backed by acceptance evidence is completion.
   Read that state from direct telemetry, and wait on defined checkpoints rather
   than prompting a delegate for running narration. Do not redo accepted work;
   optional work may be stopped once it can no longer change the outcome.
2. **Compare.** At each boundary, compare artifacts and trajectory against the
   target: missing outcomes, unsupported completion claims, scope drift,
   repeated loops, or effort that no longer moves acceptance. Redo this after
   every major phase, not only at the end.
3. **Challenge — run an adversarial pass by default.** At each major phase
   boundary challenge the work on two axes:
   - **Design Challenger:** ROI, design soundness, and **gold-plating** — scope
     creep, over-engineering, and redundant complexity the executor added on
     its own (加戏).
   - **Drift Watchdog:** alignment with the original intent, real progress since
     the last boundary, evidence quality, repeated work, and stale delegation.

   Finish any challenge that can change the contract, interface, or acceptance
   boundary before a writer begins; run only non-blocking guards concurrently.
   Run these as separate clean-context, read-only reviewers whenever the surface
   is non-trivial or the phase touched shared state; collapse to a single inline
   check only for a small, low-risk surface. Then give **one owner** the job of
   merging all findings: deduplicate, resolve conflicts, and classify each as
   actionable, boundary-only, overdesign, or false-positive. For each finding
   handed to a human, give its rationale with a code snippet so the call is
   reviewable item by item, not a bare label. Never staple reviewer outputs
   together as the decision, and let the agent that fixes differ from the one
   that reviewed.
4. **Correct.** Disposition each material finding — keep, prune, repair,
   replan, or escalate. When the Design Challenger flags gold-plating or drift,
   re-decompose the remaining work into commit-sized units before continuing,
   so the executor cannot smuggle in unrequested scope. Before interrupting an
   active delegate, inspect its status, dirty diff, active processes, and
   generated artifacts directly, and preserve and consume recoverable work; if
   an execution delegate with valuable context terminates with only a plan, give
   it one narrower outcome and exit condition before replacement. Reuse an agent
   whose context still serves the target; retire stale agents and their
   descendant work once it has no remaining outcome. Keep the three evidence
   types distinct — review yields candidate findings, runtime checks yield
   behavioral evidence, walkthroughs recover human understanding — and never let
   one stand in for another. After a correction, recheck the affected surface
   and any broader acceptance surface it may have disturbed.
5. **Continue, and close on evidence.** Resume work, but stop and replan the
   moment retries, polling, or agent activity produce no new acceptance evidence
   since the last boundary — the gate is "no new evidence," not a retry count.
   Interim passes review the current phase's diff; the terminal pass before
   closing reviews the **entire cumulative diff**, not just the last phase's. A
   typical rhythm: architecture-review + fix, then general-review + fix, once per
   module, then the same pair twice over the full diff at the end — adjust to the
   work, this is illustrative, not a fixed count. Before a turn, continuation, or
   handoff boundary, make every required delegated result terminal and consume
   it rather than assuming child-agent state will persist. Close only when that
   work is consumed and acceptance evidence supports completion; otherwise
   continue or surface the real blocker.

**Runlog.** At a durable boundary or handoff, leave a runlog — one line each:

- Surprises the run hit that the plan did not predict
- Adapted decisions: tactics you changed on your own, and why
- Unresolved judgments waiting on a human to decide
- Follow-ups deferred
- Evidence pointers: where the acceptance proof lives

A control pass is complete when the target is current, the adversarial pass has
run, every material finding has a disposition, stale work is retired, the
runlog is current at a boundary, and the next action or completion evidence is
clear.
