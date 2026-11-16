# Delivery recovery

Read when a task read is missing or suspicious, a create/send result is unknown,
or a target may lack the assigned context or access.

## Establish evidence

Use the current host adapter's authoritative thread-read surface first (including
pending approval/question prompts and queued messages where exposed). Empty or
failed reads, repeated blank turns, missing user/assistant/tool records, and
contradictions call for the owning host or harness's persisted session log
(such as Codex rollout files, Antigravity transcripts, or Claude JSONL logs),
located by `threadId` or session identifier. Check the active host adapter under
`adapters/` for exact lookup tools and log locations. Persisted session logs are
authoritative for persisted history; use current evidence for current state.

Distinguish attempted dispatch from confirmed delivery. A successful delivery
result or the matching message in the target's records establishes receipt;
a recipient response confirming the specific dispatched message can also
establish it. A tool invocation alone, an uncorroborated sender summary, or a
quoted prompt is only a lead. Idle, silence, timeout, `notLoaded`, refreshed
timestamps, and missing persisted logs leave the relevant state unresolved.

Preserve the affected responsibility, lifecycle, and routing while resolving
that uncertainty. Continue unrelated authorized work and report any material
coverage gap.

## Unknown create

List and read tasks in the resolved saved project or external task ledger.
Compare source controller, environment/project, workspace, exact brief, and the
before/after task set. Reuse one verified match containing only the dispatched
work. Review multiple matches without discarding independent work. Retry once
only on definitive evidence of non-creation; incomplete results leave creation
unresolved.

## Unknown send

Read the exact target and classify delivery. Confirmed receipt ends recovery.
Definitive non-delivery or a demonstrably harmless exact repeat permits one
identical bounded retry. An absent message alone leaves delivery unresolved;
preserve the assignment, owner, and evidence gap until delivery evidence
settles them.

## Unsuitable target

Compare the actual environment, project, harness/model, workspace, and access
with the assignment. Keep the existing responsibility until the target can do
the assigned work. Retire only a confirmed duplicate; preserve independent work
in other candidates.
