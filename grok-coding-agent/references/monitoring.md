# Grok Build CLI Monitoring Reference

This reference contains version-sensitive operational details. Verify them
against the selected launcher before use.

## Discover current capabilities

```bash
<launcher> --version
<launcher> --help
<launcher> models
```

Use current help and `models` for model, effort, sandbox and output-format syntax. Wrapper identity and opacity are defined in the main skill.

## Semantic Stream

Use the sandbox-selected baselines from the skill body. Do not add
`--include-partial-messages`. Consume complete JSONL records and reduce them to
these states:

| Grok event | Compact host state |
|---|---|
| system initialization | `running` |
| assistant message containing `tool_use` | `working — <tool> started` |
| user message containing `tool_result` | `working — <tool> completed` |
| terminal `result` with successful exit | `turn ended; verify task evidence` |
| terminal failure or nonzero exit | `failed` |

Ignore `thinking` blocks and raw reasoning. Do not forward full tool arguments,
tool results, or assistant text when a short action summary is enough.

If current help lacks `streaming-messages-json`, fall back to:

```bash
<launcher> --output-format streaming-json --sandbox read-only --permission-mode dontAsk --no-subagents --tools "read_file,grep,list_dir" --deny 'MCPTool(*)' -p "Your task"
```

The fallback emits fine-grained `thought` and `text` records. Drop those token
deltas. Use tool-call lifecycle records for `working` and the terminal `end`
record plus process exit for completion.

## Retain the process and its evidence

Use the host's resumable process facility. Its handle, OS PID, and CLI session
ID are different identities. Save fresh captures for each attempt under system
temp and continuously consume new complete lines. An old report is not this
run's result. Preserve full evidence while returning only compact signals.

Without a retained host session, arrange for a supervisor to save the child's
real exit code. A later shell cannot recover it from a vanished PID. Verify
that the child survives its launching shell; some hosts reap `nohup ... &`
children. Prefer a retained foreground session when available.

Choose a task-appropriate host deadline, allowing any CLI deadline time to
finish shutdown. Distinguish actual deadline expiry, permission blockage,
stream failure and cancellation. Silence alone is not a failure. Inspect
relevant semantic events and process state at a missed checkpoint.

Before another attempt, check completed tools and partial artifacts to avoid
repeating side effects. Resume only through current CLI capabilities and verify
continuation identity when emitted. Keep failed and recovered attempts distinct.
For cancellation or supersession, stop owned processes and confirm exit before
releasing the workspace. Clean only this run's state, preserving its useful
acceptance and unresolved-failure evidence.

## Terminal and Error Handling

- `result` is the preferred stream's terminal record; `end` terminates the
  fallback stream.
- A nonzero exit before any stream record is a failed start: classify it from
  the exit code and stderr; do not wait for a terminal record that will never
  come. A built-in sandbox can instead warn and continue without enforcement;
  treat that warning as an isolation failure even when the run exits zero.
- Combine the terminal record with process exit. A plausible final-looking
  assistant message is not sufficient completion evidence. Confirm successful
  results for the tool actions the task needed before claiming task success.
- Preserve stderr for diagnosis, but do not classify an otherwise successful
  run as failed solely because stderr contains warnings.
- If output ends with an incomplete JSON line, report an incomplete stream
  rather than manufacturing completion.

Grok session resume, worktree support, ACP stdio, WebSocket, and leader commands
are separate integration surfaces. Inspect their current help only when a
workflow explicitly requires them; they are not needed for ordinary monitoring.
