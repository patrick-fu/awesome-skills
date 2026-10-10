---
name: codex-coding-agent
description: >-
  Run local Codex CLI (`codex`) as an external coding executor. Use only when
  explicitly selected by name.
---

# Codex Coding Agent

Use the selected launcher to carry a bounded task through execution and host
verification. Preserve the user's model, permissions, workspace, and scope.

## Establish the run

1. Invoke the requested binary or wrapper with `--version`, `--help`, and
   `exec --help`. Keep wrappers opaque: definitions, source, arguments, and
   full environments may contain credentials. Discover behavior through help
   and diagnostics; redact secret values from captures.
2. Honor explicit model/effort choices; otherwise select supported settings
   suited to the task. Use current help and the model catalog. Extract only
   the needed model fields from large catalogs. Record requested and effective
   settings separately; absent effective settings stay unverified.
3. Fix the absolute workspace, permitted actions, and acceptance evidence.
   Experiments use isolated workspaces; parallel writers need separate
   workspaces or a single writer. Sandbox and approval policy are separate
   controls; constrain remote MCP effects separately when relevant.

Read [monitoring](references/monitoring.md) before a monitored run, permission
recovery, partial failure, or session resume. Discover profiles, review
selectors, and configuration overrides through current subcommand help.

## Execute

Use monitor mode whenever the task needs tools or may take time:

```bash
# Read-only work
<launcher> -a never exec --json --sandbox read-only --ignore-rules --ephemeral "Your task"

# Authorized implementation
<launcher> exec --json --sandbox workspace-write "Your task"
```

For read-only work, disable approval prompts and user/project exec-policy
rules: an allowed command can run outside the shell sandbox. `--ignore-rules`
does not remove managed requirements. Verify effective policy, including
wrapper overrides, or use host-enforced isolation before claiming a strict
boundary. If these controls are unavailable, preserve the requirement rather
than silently weakening it.

Retain the host process handle and fresh stdout/stderr captures under system
temp. Consume complete records continuously; show short new semantic signals,
not reasoning or full command payloads. Stdout may mix JSON and status lines;
filter status text and summarize large `aggregated_output` values. Choose a
task-appropriate host deadline. A quiet live process remains running until
completion, cancellation, or its deliberate deadline.

For a trivial task needing no tool evidence, use the same task-appropriate
invocation without `--json`; preserve the read-only flags when applicable.

## Accept or recover

Observe `turn.completed` or `turn.failed` and actual process exit, then inspect
the answer, required completed items, stderr, and actual artifacts/diff.
A final-message file or a nonterminal error alone does not classify the run.
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
