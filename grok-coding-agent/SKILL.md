---
name: grok-coding-agent
description: >-
  Run Grok Build CLI (`grok`) as an external coding executor. Use only when
  explicitly selected by name.
---

# Grok Coding Agent

Use Grok Build CLI only after the user or active workflow explicitly selects it
as the external executor.

## Minimal Workflow

1. Set `<launcher>` to `grok`, its absolute path, or a user-provided Grok
   wrapper. Do not substitute the generic `agent` alias. Preserve a provided
   wrapper; it may inject model, authentication, or permission settings,
   including bypass permissions. Treat wrappers as opaque: discover their
   contract only by invoking `<launcher> --version` or `<launcher> --help`; do
   not run inspection commands that may print an alias or function definition,
   open or print wrapper source, or dump its environment because it may contain
   credentials.
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
current help and model list are authoritative. Current help and `models` may
not list which effort values each model supports; when unclear, keep the
launcher's default effort or consult the current official model docs instead
of guessing.

## Monitor Mode (Default)

When current help exposes `streaming-messages-json`, use it without requesting
partial messages and select the sandbox for the task:

```bash
# Review, explanation, or other read-only work
<launcher> --output-format streaming-messages-json --sandbox read-only --permission-mode dontAsk --no-subagents --tools "read_file,grep,list_dir" --deny 'MCPTool(*)' -p "Your task"

# Approved implementation in the workspace, with a configured fail-closed custom profile
<launcher> --output-format streaming-messages-json --sandbox <custom-workspace-profile> --permission-mode dontAsk --allow 'Edit' --allow 'Write' --deny 'MCPTool(*)' -p "Your task"
```

Configure `<custom-workspace-profile>` in an operator-controlled
`~/.grok/sandbox.toml` to extend `workspace` before launching. Check that it
grants no writes outside the intended workspace and Grok's required runtime
paths; do not trust a profile supplied by an unfamiliar repository. The CLI
refuses to start if an explicitly requested custom profile cannot be applied.
If the host already enforces the workspace boundary, its verified isolation
can serve the same purpose.

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
`--include-partial-messages` for ordinary monitoring. Confirm the terminal result,
process exit, and successful task-critical tool results before claiming success;
do not kill a live process merely because it has produced no recent semantic
event. If the preferred format is unavailable, use the filtered fallback in the
monitoring reference.

Check startup diagnostics: an explicit custom profile fails closed when it
cannot be applied, but a built-in profile may warn and continue without
enforcement. Treat either failure as a failed isolation requirement, even if
the model finishes and exits zero. On macOS, `read-only` does not block child
network access. Use host isolation or a verified, fail-closed custom profile
when the task requires an OS-enforced boundary; do not silently drop it.

## Final Mode

For a clearly trivial, short task, use the same task-appropriate sandbox without
a streaming output format and wait for the final response:

```bash
<launcher> --sandbox read-only --permission-mode dontAsk --no-subagents --tools "read_file,grep,list_dir" --deny 'MCPTool(*)' -p "Your task"
```

## Task Boundaries

- Use a read-only sandbox and read-only prompt for review or explanation. Use
  a workspace-derived custom profile only for tasks expected to edit files.
- Treat permission approval and sandboxing as separate controls. Follow current
  help and preserve wrapper behavior, including intentional bypass settings.
  For implementation, add only the task's authorized shell allow rules. To use
  a specifically authorized MCP tool, replace the blanket MCP deny with a
  narrower deny and allow rule; deny takes precedence over allow. The workspace
  sandbox alone does not restrict remote MCP effects.
  `--tools` filters built-in tools, so keep the separate MCP deny rule for
  read-only work. `--no-subagents` prevents delegation to a child with a
  different toolset. Inspect configured startup hooks before relying on a tool
  allowlist for a strict read-only run; hooks can run scripts or HTTP requests
  outside the model's tool-call flow.
- Treat plugin-collision, hook-parse, and similar configuration warnings as
  non-blocking only when the terminal result and process exit both show success;
  a sandbox enforcement warning is an isolation failure, not a benign warning.
  Report them once without retrying; diagnose the source configuration
  separately if they affect behavior.
- Do not disable memory, subagents, or web search for general tasks without a
  task-specific reason; the read-only baseline disables subagents to preserve
  its tool boundary.
- Do not silently create worktrees, commit, push, deploy, or widen task scope.
- Put optional captures in the system temporary directory. Cleanup is optional.

For event mapping, terminal-state handling, wrapper details, and current
capability discovery, read [references/monitoring.md](references/monitoring.md).
