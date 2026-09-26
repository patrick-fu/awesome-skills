---
name: antigravity-coding-agent
description: >-
  Run Google Antigravity CLI (`agy`) as an external coding executor. Use only
  when explicitly selected by name.
---

# Antigravity Coding Agent

Use Antigravity only after the user or active workflow explicitly selects it as
the external executor.

## Minimal Workflow

1. Set `<launcher>` to the requested Antigravity binary, absolute path, alias,
   or wrapper. Preserve a provided wrapper; it may inject model, authentication,
   or permission settings, including bypass permissions. Treat wrappers as
   opaque: discover their contract only by invoking `<launcher> --version` or
   `<launcher> --help`; do not run inspection commands that may print an alias
   or function definition, open or print wrapper source, or dump its
   environment because it may contain credentials.
2. Run `<launcher> --help` before composing version-sensitive flags. Use
   `<launcher> models` for the model catalog and other subcommand help only
   when the task needs it.
3. Choose the model and thinking effort deliberately, following the guidance
   below and the choices currently exposed by the launcher. `--model` and
   `--effort` interact: a base catalog ID such as `gemini-3.8-flash` requires
   `--effort` with a tier the model supports, while a tiered ID such as
   `gemini-3.8-flash-high` already carries its effort and rejects a
   conflicting `--effort`. Copy the catalog entry exactly; when unsure, omit
   `--effort`.
4. Use monitor mode by default for any task that may take time. Use final mode
   only when the task is clearly trivial and short.
5. Run from the intended repository or workspace, pass a bounded task contract,
   and wait for the external process to finish.
6. Inspect the resulting diff, tests, and final answer before claiming success.

## Model and Effort

Honor explicit model or effort choices. Otherwise inspect current help and
`<launcher> models` before launching:

- For routine, bounded work, prefer a balanced model and moderate effort.
- For deep review, ambiguous debugging, cross-module design, or other high-risk
  work, prefer a frontier model and high or maximum supported effort.
- Use the highest tier only when its quality benefit justifies the extra
  latency or cost, and after checking whether that tier has additional
  behavior.

Do not hardcode model names or effort levels from this skill; the launcher's
current help and model catalog are authoritative. In API-key mode the built-in
default model may not exist on the configured endpoint and fails with a 400
unknown-provider error; pick a model the endpoint's catalog actually serves
(references/api-mode.md).

## Monitor Mode (Default)

Pass the bounded task contract as the `-p` value and request the semantic JSONL
stream:

```bash
<launcher> -p "$TASK_PROMPT" --output-format stream-json
```

The prompt must be the `-p` value; a trailing positional prompt exits 2.
Place repeatable options such as `--add-dir` ahead of `-p`. Bound long tasks
explicitly with `--print-timeout`; the default waits until the turn completes,
with background tasks waited up to a 30-minute cap.

Start the command with the host's long-running process facility. Keep the task
ID returned by the host, then use the host's wait, poll, or resume facility to
read only newly available output while the process runs.

Reduce the stream to small liveness signals such as:

```text
running — process alive
working — step started (step_type)
running — no new semantic event; process alive
completed — result.status SUCCESS
```

Ignore raw thinking/reasoning and token deltas. Treat the terminal `result`
event together with process exit as completion evidence; do not kill a live
process merely because it has produced no recent semantic event.

## Final Mode

For a clearly trivial, short task, wait for one final response:

```bash
<launcher> -p "$TASK_PROMPT"
```

Add `--output-format json` when the caller wants a single JSON object with
`status`, `response`, and usage instead of prose.

## Task Boundaries

- For read-only review or explanation, keep the prompt findings-first and
  consider `--mode plan`, which researches and plans without making changes.
- Headless runs cannot show permission prompts: any tool permission that is not
  pre-approved is auto-denied, and the process can still exit 0. Judge
  completion by the terminal `result` status or the visible final answer, never
  by the exit code alone. Even a read-only run can no-op this way; see
  references/monitoring.md for the recovery pattern.
- `--dangerously-skip-permissions` auto-approves every tool request and is the
  supported headless path for write tasks. Add it only when the user explicitly
  authorizes that execution scope for the task at hand.
- Follow the current help and wrapper contract for sandbox and mode options.
- Do not silently create worktrees, commit, push, deploy, or widen task scope.
- Put optional captures in the system temporary directory. Cleanup is optional.

Account sign-in is the default authentication. For API-key or custom-endpoint
setups, read [references/api-mode.md](references/api-mode.md). For event
mapping, exit codes, headless permission behavior, session resume, and current
capability discovery, read [references/monitoring.md](references/monitoring.md).
