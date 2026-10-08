# Flaky Failures

Read for intermittent failures, races, or tests affected by order or shared
state. Preserve the original symptom while improving observability.

## Reproduce and discriminate

Record seeds, actors, workload, scheduling, environment, attempts, and observed
failures as relevant. Amplify suspected contention or control scheduling when
it helps distinguish a mechanism. Repeated successes do not prove absence of
a rare failure; report the actual observations.

Use state and event conditions with a bounded timeout for asynchronous checks.
Read fresh state at each observation. Arbitrary sleeps can mask the race;
elapsed-time checks remain appropriate when timing itself is the contract.
Instrumentation and injected delays can change behavior, so retain the
unmodified scenario for final verification.

## Ordering and pollution

Compare a fresh-process isolated run with the failing suite or workload order.
Preserve the failure-producing prefix while narrowing contributing actors or
tests. Use bisection only when the predicate is suitable; order-dependent
failures may require sequence reduction rather than independent test runs.

Probe globals, caches, environment variables, files, ports, timers, listeners,
and unfinished tasks. Reset each trial's environment enough to make the
comparison meaningful. Observe the actual pollution or leaked lifecycle;
running every file alone can miss a failure requiring a sequence.

## Shared premises

Repeated failures can share a wrong assumption about who performs the work,
state ownership, ordering, or lifetime. Measure actor/work distribution when
load skew is relevant, then test the suspected relationship. An even count
alone does not establish a correct workload or rule out another cause.

## Verify

Use the original failing order or workload and the narrowed regression case
after repair. Include a contrasting case when it distinguishes a timing,
ownership, or distribution explanation. Retain conditions, failure counts,
and uncertainty; separate temporary stress aids from the lasting fix.
