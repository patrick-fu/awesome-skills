---
name: claude-code-coding-agent
description: >-
  Run Claude Code CLI (`claude`) as an external coding executor. Use only when
  explicitly selected by name.
---

# Claude Code Coding Agent

Use the selected launcher to carry a bounded task through execution and host
verification. Preserve the user's model, permissions, workspace, and scope.

## Establish the run

1. Invoke the requested binary or wrapper with `--version` and `--help`.
   Keep wrappers opaque: definitions, source, arguments, and full environments
   may contain credentials. Discover behavior through help and diagnostics;
   redact secret values from captures.
2. Honor explicit model/effort choices; otherwise select supported settings
   suited to the task. Use current help, not cached model names. A wrapper may
   supply the model; check emitted init settings and alias warnings. Record
   requested and effective settings separately; absent fields stay unverified.
3. Fix the absolute workspace, permitted actions, and acceptance evidence.
   Experiments use isolated workspaces; parallel writers need separate
   workspaces or a single writer. Verify effective capabilities when a strict
   read-only boundary is required.

Read [monitoring](references/monitoring.md) before a monitored run, permission
recovery, partial failure, or session resume. Use subcommand help only for
capabilities the task needs.

## Execute

Use monitor mode whenever the task needs tools or may take time. Pass the
bounded prompt through stdin: variadic options such as `--tools`,
`--allowedTools`, and `--add-dir` can consume a positional prompt.

```bash
printf '%s' "$TASK_PROMPT" | <launcher> --print --output-format stream-json --verbose
```

For file-only read-only work:

```bash
printf '%s' "$TASK_PROMPT" | <launcher> --print --output-format stream-json --verbose --restricted --strict-mcp-config --tools Read Grep Glob
```

Check that init lists exactly `Glob`, `Grep`, and `Read`. Unknown tool names
can empty the list. `--strict-mcp-config` excludes configured MCP servers;
a wrapper's bypass flag reduces the guarantee to the verified tool allowlist.
Permission bypass flags require authorization for this run. Preserve a ban on
worktree creation, including `EnterWorktree`, when it is part of the task.

Retain the host process handle and fresh stdout/stderr captures under system
temp. Consume complete records continuously; show short new semantic signals,
not thinking or token deltas. Keep partial-message streaming off for ordinary
monitoring. Choose a task-appropriate host deadline; a quiet live process
remains running until completion, cancellation, or its deliberate deadline.

For a trivial task needing no tool evidence, final mode is sufficient:

```bash
printf '%s' "$TASK_PROMPT" | <launcher> --print --restricted --strict-mcp-config --tools ""
```

## Accept or recover

Observe the terminal result and actual process exit, then inspect the answer,
required completed tools, stderr, and actual artifacts/diff. Check `is_error`;
`subtype=success` alone can still describe an authentication failure. Run
checks appropriate to the authorized task and state those not performed.
Execution success and artifact acceptance are separate conclusions; retain
an error classification even when independently verified partial work is useful.

Before retrying or resuming, inspect completed actions and partial artifacts
so work or side effects are not repeated. Keep attempts separate. Stop a
canceled or superseded task's owned processes and confirm exit before releasing
its workspace. Clean only this run's runtime/captures and retain evidence for
acceptance or an unresolved failure.

Commit, push, deploy, worktree creation, and broader permissions require the
corresponding user authorization; the skill supplies no extra scope.
