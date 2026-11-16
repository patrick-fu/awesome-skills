# T3 Code Adapter

Use this adapter when running inside T3 Code (via native T3 MCP tools, or via
`acp-mcp-call` when `T3_ACP_MCP_NODE` is present in shell-only fallback).

## Environments and projects

- **Local by default:** omit `environmentId` for local work unless the user
  names another machine or supplies a remote `environmentId`.
- **Multi-machine routing:** list linked environments with
  `t3_environment_links` (or pair an unlinked named machine with
  `t3_environment_link(hint=...)`; never ask the user for a pairing code in
  chat). Pass the target `environmentId` on all subsequent T3 calls for that
  machine.
- **Projects:** resolve existing projects with `t3_project_list` and
  `t3_project_read`. Respect workspace rules when the environment uses a shared
  context repository as the orchestration entry point (avoid creating per-repo
  T3 projects or unnecessary top-level threads when conventions forbid it).

## Capability probe and three-tier delegation

- **Probe once per thread:** call `orchestrator_capabilities` (with
  `environmentId` when remote) before the first `delegate_task`, and again only
  after an error or explicit provider change.
- **Tier 1 (In-thread native subagent):** use the harness's native subagent tool
  only when the child uses your provider, an offered model, no extra settings,
  and the current checkout (for example Codex `spawn_agent`, Claude
  `Agent(run_in_background: false)`, or Antigravity `invoke_subagent`).
- **Tier 2 (Managed async delegate):** use `delegate_task` (`mode: "async"`) for
  another provider/model, custom `target.options` (from
  `orchestrator_capabilities`, e.g., `reasoningEffort`), background execution,
  or an isolated checkout (`isolation: "worktree"` unless workspace rules require
  pre-created linked worktrees with `isolation: "shared"` and explicit paths).
  - Follow the returned `next` guidance; never poll with `task_status`,
    `sleep`, or watchers.
  - Every new review or re-check is a fresh `delegate_task` (brief + findings),
    never `t3_thread_send`.
  - Stop or replace a delegate with `task_cancel(taskId)`, never
    `t3_thread_interrupt` on a `childThreadId`.
  - If a requested provider or model is unavailable, report it clearly rather
    than silently switching.
- **Tier 3 (Independent top-level threads):** use `t3_thread_launch` (single
  thread, with `workspaceStrategy: {type: "worktree" | "existing_worktree" | "root", baseRef, startFromOrigin}`)
  or `create_threads` (batch in the current checkout) only when independent
  user-visible threads are requested. Do not make shell worktrees for threads
  managed by `workspaceStrategy`.

## Inspect, steer, and recover

- **Inventory and search:** use `t3_thread_list` (filter by `projectId`,
  `allProjects`, `settled`, `statuses`, `environmentId`) and `t3_thread_search`.
- **Authoritative read:** use `t3_thread_read(threadId, view: "messages" | "activity", limit, maxCharsPerItem)`.
  Also check `t3_pending_request` (blocked approvals or user questions) and
  `t3_queue` (queued messages). Reading a child's final result marks it
  delivered.
- **Wait and steer:** use `t3_thread_wait` (with `untilDelegatedWorkSettled`
  when waiting on delegated work inside a thread) and `t3_thread_send`
  (`mode: "auto" | "queue" | "steer" | "restart"`, `freshContext: true` to
  reset context cleanly).
- **Context transfer:** use `t3_thread_transfer` (`fork`, `merge_back`,
  `status`) when branching or folding context back into a related thread.
- **Fallback persisted logs:** when `t3_thread_read` is empty, truncated, or
  contradictory, inspect the underlying harness's persisted log on the owning
  host (Codex rollout under `~/.codex/sessions` or `~/.codex-t3/sessions`,
  Antigravity `transcript.jsonl`, or Claude JSONL) located by session/thread ID.

## Scheduling, PR watches, titles, and lifecycle

- **Scheduled mode:** use `schedule_task` (`interval`, `fixed_time`, `once`, or
  `webhook`; check `bindToCurrentThread` and `freshSession`). Report the
  returned next run time or `webhookUrl`.
- **PR gates:** use `watch_pull_request` when monitoring an open PR, and
  `unwatch_pull_request` before closing or handing back.
- **Titles and settle:** rename threads with `t3_thread_update(action: "rename", title)`.
  Use `t3_thread_organize` (`settle` / `unsettle` / `archive` / `snooze` / `pin`)
  to settle verified completed child threads while keeping history recoverable;
  archive only accepted predecessors or confirmed duplicates.
- **Canonical links:** whenever citing a thread in a response, use the exact
  `link` string returned by T3 tools (`[<title>](t3-thread://v2/<envId>/<threadId>)`).

## ACP shell fallback

When T3 MCP tools are absent in a shell session and `T3_ACP_MCP_NODE` is set,
call T3 tools through:

`ELECTRON_RUN_AS_NODE=1 "$T3_ACP_MCP_NODE" ${T3_ACP_MCP_ENTRYPOINT:+"$T3_ACP_MCP_ENTRYPOINT"} acp-mcp-call <tool_name> '<json_args>'`
