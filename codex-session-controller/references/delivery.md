# Delivery recovery

Read this file when a `read_thread` result is missing or suspicious, a
create/send result is unknown, or a candidate appears to be the wrong worker.

## Evidence

Use `read_thread` first. Empty or failed reads, repeated blank turns, missing
user/assistant/tool records, and contradictions are suspicious. Then inspect the
owning host's persisted rollout by `threadId`. Persisted rollout wins for
persisted history. An actual tool call, delivered message, or assistant report
proves relay; a quoted prompt or
search lead does not. Idle, silence, timeout, `notLoaded`, refreshed timestamps,
and missing rollout leave state unresolved. Preserve session, owner, lifecycle,
and routing while evidence is unresolved.

## Unknown create

After an unknown `create_thread`, list and read tasks in the resolved saved
project. Compare source controller, project, environment, exact brief, and the
before/after task set. One matching task with only the dispatched work is the
result and can be reused. Review multiple matches without discarding independent
work. Retry once only on definitive evidence of non-creation; missing or
incomplete results remain unresolved.

## Unknown send

After an unknown `send_message_to_thread`, read the exact target and classify
delivery. Delivered work ends recovery. A definitive non-delivery or
demonstrably harmless exact repeat permits one identical bounded retry. An
absent message remains unresolved; scope, owner, and evidence gap stay
unchanged until delivery evidence settles them.

## Misplaced worker

Compare the actual host, project, environment, and access with the assignment.
If they do not match, keep the existing responsibility until the target can do
the assigned work. Retire only a confirmed duplicate.
