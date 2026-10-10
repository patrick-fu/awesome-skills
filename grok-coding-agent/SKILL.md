---
name: grok-coding-agent
description: >-
  Run Grok Build CLI (`grok`) as an external coding executor. Use only when
  explicitly selected by name.
---

# Grok Coding Agent

Use the selected launcher to carry a bounded task through execution and host
verification. Preserve the user's model, permissions, workspace, and scope.

## Establish the run

1. Invoke `grok` or the requested absolute binary/wrapper with `--version`
   and `--help`; keep the generic `agent` alias out of this workflow. Keep
   wrappers opaque: definitions, source, arguments, and full environments may
   contain credentials. Discover behavior through help and diagnostics.
2. Honor explicit model/effort choices; otherwise select supported settings
   suited to the task using current help and `models`. When per-model effort
   is unclear, retain the launcher's default or consult official model docs.
   Record requested and effective settings separately; absent effective
   settings stay unverified.
3. Fix the absolute workspace, permitted actions, and acceptance evidence.
   Experiments use isolated workspaces; parallel writers need separate
   workspaces or a single writer. Permissions and sandbox enforcement are
   separate; inspect startup hooks before relying on a tool allowlist.

Read [monitoring](references/monitoring.md) before a monitored run, permission
recovery, partial failure, or session resume.

## Execute

Use monitor mode whenever the task needs tools or may take time. When current
help exposes `streaming-messages-json`, use:

```bash
# Read-only work
<launcher> --output-format streaming-messages-json --sandbox read-only --permission-mode dontAsk --no-subagents --tools "read_file,grep,list_dir" --deny 'MCPTool(*)' -p "Your task"

# Authorized implementation with a configured fail-closed profile
<launcher> --output-format streaming-messages-json --sandbox <custom-workspace-profile> --permission-mode dontAsk --allow 'Edit' --allow 'Write' --deny 'MCPTool(*)' -p "Your task"
```

Configure the custom profile in operator-controlled `~/.grok/sandbox.toml` to
extend `workspace`, allowing only the intended workspace and required runtime
paths. An unfamiliar repo's profile is not trusted configuration. Verify
host isolation or profile enforcement; custom-profile failure must stop the
run. Built-in profiles can warn and continue unenforced; that warning is an
isolation failure even with exit zero. macOS read-only does not block child
network access. Preserve any required network boundary separately.

`--tools` filters built-ins; retain a separate MCP deny. Deny wins over allow:
replace the blanket deny narrowly for an authorized MCP tool. `--no-subagents`
keeps the read-only tool boundary; it is not a default for general tasks.
Startup hooks may act outside model tools. Add only authorized shell allow
rules for implementation; preserve wrapper behavior.

Retain the host process handle and fresh stdout/stderr captures under system
temp. Consume complete records continuously; show short new semantic signals,
not thinking or token deltas. Keep partial-message streaming off. Choose a
task-appropriate host deadline. A quiet live process remains running until
completion, cancellation, or its deliberate deadline. If the preferred format
is unavailable, use the filtered fallback in the monitoring reference.

For a trivial task needing no tool evidence, use the same task-appropriate
sandbox without streaming output. Keep task-specific memory, search, and
subagent capabilities unless their restriction serves the requested boundary.

## Accept or recover

Observe the terminal result and actual process exit, then inspect the answer,
required completed tools, stderr, and actual artifacts/diff. A sandbox warning
is an enforcement failure. Plugin/hook configuration warnings are non-blocking
only with a successful terminal result and exit; report them once, diagnosing
configuration separately if it affects behavior.
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
