---
name: claude-code-coding-agent
description: >-
  Claude Code CLI operating guide for external host agents. Use only when the
  user explicitly asks to run Claude Code CLI (`claude`) as the external coding
  executor, or when the current orchestration/review workflow explicitly selects
  Claude Code by name. Do not use for generic coding tasks, built-in subagents,
  ordinary Claude chat, or unspecified delegation.
---

# Claude Code Coding Agent

Use Claude Code only after the user or active workflow explicitly selects it as
the external executor.

## Minimal Workflow

1. Set `<launcher>` to the requested Claude Code binary, absolute path, alias, or
   wrapper. Preserve a provided wrapper; it may inject model, authentication, or
   permission settings, including bypass permissions.
2. Run `<launcher> --help` before composing version-sensitive flags. Use other
   subcommand help only when the task needs it.
3. Choose the model and thinking effort deliberately, following the guidance
   below and the choices currently exposed by the launcher.
4. Use monitor mode by default for any task that may take time. Use final mode
   only when the task is clearly trivial and short.
5. Run from the intended repository or workspace, pass a bounded task contract,
   and wait for the external process to finish.
6. Inspect the resulting diff, tests, and final answer before claiming success.

## Model and Effort

Honor explicit model or effort choices. Otherwise inspect current help before
launching:

- For routine, bounded work, prefer a balanced model and moderate effort.
- For deep review, ambiguous debugging, cross-module design, or other high-risk
  work, prefer a frontier model and high or maximum supported effort.
- Use the highest tier only when its quality benefit justifies the extra latency
  or cost, and after checking whether that tier has additional behavior.

Do not hardcode model names or effort levels from this skill; the launcher's
current help is authoritative.

## Monitor Mode (Default)

Use Claude Code's semantic JSON stream without requesting partial messages:

```bash
<launcher> --print --output-format stream-json --verbose "Your task"
```

Start the command with the host's long-running process facility. Keep the task ID
returned by the host, then use the host's wait, poll, or resume facility to read
only newly available output while the process runs.

Reduce the stream to small liveness signals such as:

```text
running — process alive
working — Read completed
running — no new semantic event; process alive
completed
```

Ignore raw thinking/reasoning and token deltas. Do not add
`--include-partial-messages` for ordinary monitoring. Treat the terminal
`result` event together with process exit as completion evidence; do not kill a
live process merely because it has produced no recent semantic event.

## Final Mode

For a clearly trivial, short task, wait for one final response:

```bash
<launcher> --print "Your task"
```

## Task Boundaries

- State explicitly whether the task may edit files. Keep review and explanation
  prompts read-only and findings-first.
- Follow the current help and wrapper contract for permissions and tool access.
- Do not silently create worktrees, commit, push, deploy, or widen task scope.
- Put optional captures in the system temporary directory. Cleanup is optional.

For event mapping, terminal-state handling, wrapper details, and current
capability discovery, read [references/monitoring.md](references/monitoring.md).
