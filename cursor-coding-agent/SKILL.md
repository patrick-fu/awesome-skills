---
name: cursor-coding-agent
description: >-
  Run Cursor CLI as an external coding executor. Use only when explicitly
  selected by name.
---

# Cursor Coding Agent

Use the selected launcher to carry a bounded task through execution and host
verification. Preserve the user's model, permissions, workspace, and scope.

## Establish the run

1. Invoke the requested binary or wrapper with `--version` and `--help`.
   Confirm `Start the Cursor Agent` in help: the generic name `agent` and a
   version number do not establish product identity. Keep wrappers opaque;
   definitions, source, arguments, and full environments may contain
   credentials. Discover behavior through help and diagnostics.
2. Honor explicit model/effort choices; otherwise select supported settings
   suited to the task using current help and authenticated model listing.
   Stop and report a model-list authentication failure rather than guessing.
   Record requested and effective settings separately; absent effective
   settings stay unverified.
3. Fix the absolute workspace, permitted actions, and acceptance evidence.
   Experiments use isolated workspaces; parallel writers need separate
   workspaces or a single writer. A separate checkout isolates state but does
   not prevent writes. Verify host protection when strict read-only is required.

Read [monitoring](references/monitoring.md) before a monitored run, permission
recovery, partial failure, or session resume.

## Execute

Use monitor mode whenever the task needs tools or may take time:

```bash
<launcher> --print --trust --output-format stream-json "Your task"
```

For file-only review add `--mode ask`. For command-based review or
implementation, omit `--mode`: current help's `ask` and `plan` modes are
read-only. Treat command-based review as write-capable and enforce its boundary.
`--trust` trusts the workspace; it does not approve shell execution.

When shell execution is authorized, check current approval/sandbox flags and
confirm a harmless command completed rather than `result.rejected`. Recent
`--force`/`--yolo` auto-approves commands unless explicitly denied; it is not a
file-write-only flag. Change the sandbox only within the authorized scope.

Retain the host process handle and fresh stdout/stderr captures under system
temp. Consume complete records continuously; show short new semantic signals,
not thinking or token deltas. Keep partial assistant streaming off. Choose a
task-appropriate host deadline. A quiet live process remains running; inspect
tool/permission state at a missed checkpoint before diagnosing model slowness.

For a trivial task needing no tool evidence, final mode is sufficient:

```bash
<launcher> --print --trust "Your task"
```

## Accept or recover

Observe the terminal result and actual process exit, then inspect the answer,
required completed tools, stderr, and actual artifacts. A `result.rejected`
call did not execute. Include untracked files when checking implementation;
exit zero with an empty tracked diff proves neither application nor failure.
Run checks appropriate to the authorized task and state those not performed.
Execution success and artifact acceptance are separate conclusions; retain
an error classification even when independently verified partial work is useful.

Before retrying or resuming, inspect completed actions and partial artifacts
so work or side effects are not repeated. Keep attempts separate. Stop a
canceled or superseded task's owned processes and confirm exit before releasing
its workspace. Clean only this run's runtime/captures and retain evidence for
acceptance or an unresolved failure.

Commit, push, deploy, worktree creation, and broader permissions require the
corresponding user authorization; the skill supplies no extra scope.
