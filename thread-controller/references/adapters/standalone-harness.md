# Standalone Harness Adapter

Use this adapter when running in a standalone CLI or single-thread harness
without a cross-thread control-plane API (such as standalone Claude Code,
Codex CLI, Antigravity, Cursor CLI, or Grok CLI).

## External control state and identities

- Without a host thread registry, anchor controller state in an external file
  ledger (such as a workspace context repository `tasks/<id>/index.md` or a
  dedicated control markdown file). Follow the repository's write/locking
  conventions and keep a single writer per shared branch or file.
- Identify units by repository/workspace path, git branch or linked worktree
  path, task record path, and (for headless subprocesses) PID/log path.
- Reference tasks in reports by file path, branch/PR URL, or commit SHA.

## Execution and cross-harness delegation

- **In-thread subagents:** use the current harness's native subagent or workflow
  primitive (`Agent` in Claude Code, `spawn_agent` in Codex CLI,
  `invoke_subagent` / `run_workflow` in Antigravity).
- **Cross-harness or isolated workers:** when a task requires another model or
  CLI harness and no host orchestrator exists, invoke the target CLI headlessly
  (such as `codex exec --json`, `claude -p`, or the environment's configured CLI
  wrapper) in an isolated directory or linked worktree with a self-contained
  brief, and capture its exit status, changed files, and output log.
- **Peer sessions:** when another session runs independently in the same
  workspace, coordinate through persisted task files, git branches, PRs, or
  user-relayed updates rather than assuming direct message delivery.

## Follow-up degradation and recovery

- **Follow-up mode:** if the environment has no native scheduler or cross-thread
  delivery mechanism, keep **Poll** and state that limitation explicitly rather
  than simulating background checks. Report what finished, what waits remain,
  and the next verification command or artifact to inspect on the next turn.
- **Evidence recovery:** verify claims against actual workspace state (`git
  status`, branch commits, test/build logs) and the harness's local session
  transcript/rollout/JSONL files rather than trusting memory or summaries alone.
