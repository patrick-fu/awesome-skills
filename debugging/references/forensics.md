# Forensics

Read for logs, HARs, traces, profiles, heap snapshots, crash dumps, or live
runtime captures. Prefer tools already available for the artifact's format.

## Existing capture

Check the capture's instance, version/build, configuration, workload, time
window, and relevant symbols or source maps. Analyze a usable capture directly;
request another run only for a specific missing or contradictory observation.

Reduce to the relevant events, call paths, samples, or retainer chains. Query a
large capture with an appropriate parser or database when it saves repeated
inspection. A one-off small capture rarely needs a new analysis framework.

Map the signal back to the source and affected behavior. Separate observations
from mechanism claims: a hot function, allocation site, timestamp coincidence,
or before/after pair is a lead whose causal interpretation needs support.
State missing mapping and capture limitations.

## Live capture

Select the evidence for the suspected mechanism: CPU/wall-time profiles for
execution or waiting, heap retainers for retained memory, network traces for
requests, or stacks for crashes and blocking. Target the relevant window and
record capture overhead.

Prefer a controlled environment. Use existing authorization for access and
instrumentation; obtain any missing authorization before changing a live
production process. A capture request does not authorize a production hotfix.

## Performance and memory

Record the baseline, actual work/output, artifact, workload, and measurement
boundary. Compare after a scoped change under comparable conditions, checking
errors and skipped work. Recheck the original slow or growing scenario.

Use a discriminating experiment to connect a suspected hotspot, wait, or
retainer to the symptom. Report measured effects separately from confidence in
the explanation. For noisy or intermittent behavior, give the observed sample
and conditions; choose further sampling to fit the claim rather than a fixed
universal run count.

Keep diagnosis-only findings distinct from proposed changes. Preserve useful
captures and analysis commands with secrets redacted.
