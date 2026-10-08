# Instrumentation

Read when the failure path needs targeted runtime observation. Prefer an
available debugger, breakpoint, or inspection tool when it can answer the
question directly; use logs when they fit the environment or cross boundaries.

## Boundaries

Choose points that distinguish the current hypotheses:

**Entry → State → Conversion → Handoff → Effect.**

Capture the last confirmed correct state and the first divergence, including
the owning layer. For an unexplained bad value, trace callers and input origins;
a targeted stack can identify the producer. Follow IDs across asynchronous
handoffs rather than inferring that nearby lines belong to one operation.

## Signal

Reuse the project's logger and supplied prefix; otherwise choose a unique,
searchable prefix. Include a phase tag and minimal distinguishing fields:
IDs, state, counts, ranges, input/output summaries, or transformed values.
Escape newlines when a logical event should occupy one physical line.

Use timestamps where useful. Establish ordering with correlation IDs, sequence
numbers, or happens-before evidence when clocks or actors differ. Wall-clock
sorting alone cannot prove causality across processes.

Keep sensitive payloads out of logs. Inspect only fields needed for the probe;
mask secrets before sharing output and limit overhead that could alter timing.

## Execute and interpret

Run the instrumented scenario yourself when reachable. For a user-only device,
provide exact build/run steps, the trigger, and the specific output to return.
Recommend a prefix filter when it preserves the relevant sequence; request
necessary surrounding context if filtering would discard causal evidence.

Reconstruct confirmed events, then compare the predicted and observed boundary
transitions. Distinguish stale state, loss, duplication, conversion, branching,
and ordering as evidence warrants. If a gap remains, specify the smallest next
probe rather than repeating a broad logging pass.

Remove only the temporary probes you introduced when their evidence has been
collected. Preserve existing observability and retain useful redacted evidence.
Follow the main workflow's final-artifact check when cleanup changes behavior.
