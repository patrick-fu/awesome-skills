---
name: antigravity-coding-agent
description: >-
  Run Google Antigravity CLI (`agy`) as an external coding executor. Use only
  when explicitly selected by name.
---

# Antigravity Coding Agent

Use the selected launcher to carry a bounded task through execution and host
verification. Preserve the user's model, permissions, workspace, and scope.

## Establish the run

1. Invoke the requested binary or wrapper with `--version` and `--help`.
   Preserve wrappers as opaque: their source, definitions, arguments, and full
   environment may contain credentials. Discover behavior through help and
   emitted diagnostics, keeping secret values out of captures.
2. Use `models` to select a supported model/effort. A tiered model ID already
   carries effort; add `--effort` only when the selected entry requires it.
   Honor explicit choices; otherwise match capability and effort to the task.
   Record requested settings and verify effective settings when emitted.
3. Fix the absolute workspace, permitted actions, and acceptance evidence.
   Use isolated workspaces for experiments. Parallel writers need separate
   workspaces or an explicit single writer.
   Permissions grant actions; isolation constrains their effects. Verify the
   effective boundary when strict read-only or confined writes are required.

Read [API mode](references/api-mode.md) before API-key/custom-endpoint setup
or route verification. Read [monitoring](references/monitoring.md) before a
monitored run, permission recovery, partial failure, or session resume.

## Execute

Use monitor mode for tool-dependent or potentially long work:

```bash
<launcher> --output-format stream-json -p "$TASK_PROMPT"
```

The prompt is the `-p` value. Put repeatable options before it. Choose an
explicit, unit-bearing `--print-timeout` for bounded work; check current help
rather than relying on a default. Retain the host process handle and fresh
stdout/stderr captures under the system temporary directory. Consume streams
continuously, showing only new short semantic signals; omit thinking and token deltas. A quiet live process remains
running until completion, cancellation, or its deliberate deadline.

For file-only read-only work, list target files host-side, add authorized
external directories with `--add-dir`, and request reads through `view_file`.
Require completed reads for the target paths. Planning mode is not an OS read-only guarantee. Headless permission denial can still
exit zero: inspect tool errors and `denied_actions`. For writes,
`--dangerously-skip-permissions` requires explicit authorization for that run;
it approves every tool, so retain the authorized workspace boundary.

For a trivial task needing no tool evidence, final mode is sufficient:

```bash
<launcher> -p "$TASK_PROMPT"
```

## Accept or recover

Observe both the terminal result and actual process exit. Then inspect the
answer, required completed tools, denied actions, stderr timeouts, and actual
artifacts/diff. Run task-appropriate checks only within the authorized scope;
report checks not performed. Execution success and artifact acceptance are
separate conclusions. Keep a run's error classification even if independently
verified work is useful.

Before retrying or resuming, inspect completed actions and partial artifacts
so work or side effects are not repeated. Keep attempts separate. A canceled
or superseded task needs its owned processes stopped and exit confirmed before
its workspace is released. Clean only runtime/captures owned by this run,
retaining the evidence needed for its acceptance or unresolved failure.

Commit, push, deploy, worktree creation, and broader permissions require the
corresponding user authorization; the skill supplies no extra scope.
