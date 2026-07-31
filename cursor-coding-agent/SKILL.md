---
name: cursor-coding-agent
description: >-
  Cursor CLI operating guide for external host agents. Use only when the user
  explicitly asks to run Cursor CLI as the external coding executor, or when the
  current orchestration/review workflow explicitly selects Cursor CLI by name.
  Do not trigger on generic agent, subagent, or unspecified delegation wording.
---

# Cursor Coding Agent

Use Cursor CLI only after the user or active workflow explicitly selects it as
the external executor.

## Minimal Workflow

1. Set `<launcher>` to the requested Cursor binary, absolute path, alias, or
   wrapper. Verify `<launcher> --version` identifies Cursor because the generic
   command name `agent` can resolve to another product. Preserve a provided
   wrapper; it may inject model, authentication, or permission settings,
   including bypass permissions.
2. Run `<launcher> --help` before composing version-sensitive flags. Use model
   listing or subcommand help only when needed.
3. Choose the model and thinking effort deliberately, following the guidance
   below and the choices currently exposed by the launcher.
4. Use monitor mode by default for any task that may take time. Use final mode
   only when the task is clearly trivial and short.
5. Run from the intended repository or workspace, pass a bounded task contract,
   and wait for the external process to finish.
6. Inspect the resulting diff, tests, and final answer before claiming success.

## Model and Effort

Honor explicit model or effort choices. Otherwise inspect current help and the
current account's model list before launching:

- For routine, bounded work, prefer a balanced model and moderate effort.
- For deep review, ambiguous debugging, cross-module design, or other high-risk
  work, prefer a frontier model and high or maximum supported effort.
- Use the highest tier only when its quality benefit justifies the extra latency
  or cost, and after checking whether that tier has additional behavior.

Do not hardcode model names or effort levels from this skill; the launcher's
current help and model list are authoritative.

## Monitor Mode (Default)

Use Cursor's semantic JSON stream without requesting partial assistant output:

```bash
<launcher> --print --trust --output-format stream-json "Your task"
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
`--stream-partial-output` for ordinary monitoring. Treat the terminal `result`
event together with process exit as completion evidence; do not kill a live
process merely because it has produced no recent semantic event.

## Final Mode

For a clearly trivial, short task, wait for one final response:

```bash
<launcher> --print --trust "Your task"
```

## Task Boundaries

- For read-only review or explanation, use the current help's read-only mode.
  Do not use a read-only mode for tasks expected to modify files.
- Follow the current help and wrapper contract for trust, permissions, sandbox,
  and automatic tool approval.
- Do not silently create worktrees, commit, push, deploy, or widen task scope.
- Put optional captures in the system temporary directory. Cleanup is optional.

For event mapping, terminal-state handling, launcher identity, and current
capability discovery, read [references/monitoring.md](references/monitoring.md).
