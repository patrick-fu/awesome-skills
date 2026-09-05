# Delivery recovery

Read this file when a `read_thread` result is missing or suspicious, a
create/send result is unknown, or a candidate appears to be the wrong worker.

## Evidence

Use `read_thread` first. Empty or failed reads, repeated blank turns, missing
user/assistant/tool records, and contradictions are suspicious. Then inspect the
owning host's persisted rollout under `$CODEX_HOME/sessions` (normally
`~/.codex/sessions`) by `threadId`; tolerate schema drift and read only the
needed records. Persisted rollout wins for persisted history. An actual tool
call, delivered message, or assistant report proves relay; a quoted prompt or
search lead does not. Idle, silence, timeout, `notLoaded`, refreshed timestamps,
and missing rollout leave state unresolved. Preserve session, owner, lifecycle,
and routing while evidence is unresolved.

## Unknown create

After an unknown `create_thread`, list and read tasks in the resolved saved
project. Compare source controller, project, environment, exact brief, and the
before/after task set. One matching task with only the dispatched work is the
result and can be reused. Keep valid independent work among multiple matches and
review them as candidates. A definitive non-creation result permits one
identical bounded retry. No match or an incomplete projection remains
unresolved; explicit evidence that creation did not occur is required before
that retry.

After formal identity exists, verify host, saved project, environment,
permission profile, and initial brief. Ownership begins only when those match
the assignment and the worker's access is sufficient.

## Unknown send

After an unknown `send_message_to_thread`, read the exact target and classify
delivery. Delivered work ends recovery. A definitive non-delivery or
demonstrably harmless exact repeat permits one identical bounded retry. An
absent message remains unresolved; scope, owner, and evidence gap stay
unchanged until delivery evidence settles them.

## Misplaced worker

If a candidate landed projectless, in the wrong project or host, is
approval-pending, or has insufficient access, it does not own the work. The
existing owner remains responsible. Re-resolve the saved project, environment,
and permission profile; the candidate becomes eligible only after every
qualification matches. Retire only a confirmed duplicate when archive is
available.
