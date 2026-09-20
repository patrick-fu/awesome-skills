# Delivery recovery

Read when a task read is missing or suspicious, a create/send result is unknown,
or a target may lack the assigned context or access.

## Establish evidence

Use `read_thread` first. Empty or failed reads, repeated blank turns, missing
user/assistant/tool records, and contradictions call for the owning host's
persisted rollout, located by `threadId`. Persisted rollout is authoritative for
persisted history; use current evidence for current state.

Distinguish attempted dispatch from confirmed delivery. A successful delivery
result or the matching message in the target's records establishes receipt;
a recipient response confirming the specific dispatched message can also
establish it. A tool invocation alone, an uncorroborated sender summary, or a
quoted prompt is only a lead. Idle, silence, timeout, `notLoaded`, refreshed
timestamps, and missing rollout leave the relevant state unresolved.

Preserve the affected responsibility, lifecycle, and routing while resolving
that uncertainty. Continue unrelated authorized work and report any material
coverage gap.

## Unknown create

List and read tasks in the resolved saved project. Compare source controller,
host/project, environment, exact brief, and the before/after task set. Reuse one
verified match containing only the dispatched work. Review multiple matches
without discarding independent work. Retry once only on definitive evidence of
non-creation; incomplete results leave creation unresolved.

## Unknown send

Read the exact target and classify delivery. Confirmed receipt ends recovery.
Definitive non-delivery or a demonstrably harmless exact repeat permits one
identical bounded retry. An absent message alone leaves delivery unresolved;
preserve the assignment, owner, and evidence gap until delivery
evidence settles them.

## Unsuitable target

Compare the actual host, project, environment, and access with the assignment.
Keep the existing responsibility until the target can do the assigned work.
Retire only a confirmed duplicate; preserve independent work in other candidates.
