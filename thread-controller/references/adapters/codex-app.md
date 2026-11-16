# Codex App Adapter

Use this adapter when running inside Codex App with native thread and
automation tools.

## Identities, projects, and links

- Identify tasks by `(hostId, threadId)` and saved projects by
  `(hostId, projectId)`.
- Resolve projects with `list_projects` before creating new threads, choosing
  the host, environment, and working state required by the assignment.
- Link non-current tasks in reports as `[<title>](codex://threads/<threadId>)`
  alongside their `hostId` and next useful evidence.

## Dispatch, check, and steer

- Use `spawn_agent` for bounded helper work inside the current task.
- Use `list_threads` to rebuild inventories alongside the control index.
- Take one non-blocking snapshot pass with `wait_threads` (`timeoutMs: 0`), in
  batches allowed by the current schema (typically up to 8).
- Inspect thread details with `read_thread`, and send concise deltas or
  routing updates with `send_message_to_thread`.

## Persisted rollout fallback

When `read_thread` returns empty or failed reads, repeated blank turns, missing
user/assistant/tool records, or contradictions with runtime status, inspect the
owning host's persisted rollout file located by `threadId`. Persisted rollout is
authoritative for persisted history; combine with current evidence for live
state.

## Scheduling

- Use `automation_update` (`destination: "thread"` or the designated target)
  when establishing, pausing, updating, or retiring controller-targeted
  Scheduled wakeups.
- Keep worker-internal continuation schedules separate from controller checks;
  a worker waiting on its own local build or subagent uses its own continuation
  without turning the controller's Poll relationship into a timer.
