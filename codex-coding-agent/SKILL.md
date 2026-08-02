---
name: codex-coding-agent
description: >-
  Run local Codex CLI (`codex`) as an external coding executor. Use only when
  explicitly selected by name.
---

# Codex Coding Agent

Use Codex CLI only after the user or active workflow explicitly selects it as
the external executor.

## Minimal Workflow

1. Set `<launcher>` to the requested Codex binary, absolute path, alias, or
   wrapper. Preserve a provided wrapper; it may inject model, authentication, or
   permission settings, including bypass permissions.
2. Run `<launcher> --help` and `<launcher> exec --help` before composing
   version-sensitive flags. Use other subcommand help only when needed.
3. Choose the model and thinking effort deliberately, following the guidance
   below and the choices currently exposed by the launcher.
4. Use monitor mode by default for any task that may take time. Use final mode
   only when the task is clearly trivial and short.
5. Run from the intended repository or workspace, pass a bounded task contract,
   and wait for the external process to finish.
6. Inspect the resulting diff, tests, and final answer before claiming success.

## Model and Effort

Honor explicit model or effort choices. Otherwise inspect current help and model
catalog before launching:

- For routine, bounded work, prefer a balanced model and moderate effort.
- For deep review, ambiguous debugging, cross-module design, or other high-risk
  work, prefer a frontier model and high or maximum supported effort.
- Use the highest tier only when its quality benefit justifies the extra latency
  or cost, and after checking whether that tier has additional behavior.

Do not hardcode model names or effort levels from this skill; the launcher's
current help and model catalog are authoritative.

## Monitor Mode (Default)

Use Codex's semantic JSON event stream and select the sandbox for the task:

```bash
# Review, explanation, or other read-only work
<launcher> exec --json --sandbox read-only --ephemeral "Your task"

# Approved implementation in the workspace
<launcher> exec --json --sandbox workspace-write "Your task"
```

Start the command with the host's long-running process facility. Keep the task ID
returned by the host, then use the host's wait, poll, or resume facility to read
only newly available output while the process runs.

Reduce the stream to small liveness signals such as:

```text
running — process alive
working — command completed
running — no new semantic event; process alive
completed
```

Ignore raw thinking/reasoning and token deltas. Treat the terminal turn event
together with process exit as completion evidence; do not kill a live process
merely because it has produced no recent semantic event.

## Final Mode

For a clearly trivial, short task, use the same task-appropriate sandbox without
`--json` and wait for the final response.

## Task Boundaries

- Use a read-only sandbox and read-only prompt for review or explanation. Use
  workspace-write only for tasks expected to edit files.
- Follow current subcommand help before using review selectors, resume, profiles,
  or configuration overrides.
- Do not silently bypass approvals or sandboxing, create worktrees, commit, push,
  deploy, or widen task scope.
- Put optional captures in the system temporary directory. Cleanup is optional.

For event mapping, terminal-state handling, model discovery, and current
capability discovery, read [references/monitoring.md](references/monitoring.md).
