# Claude Code Monitoring Reference

This reference contains version-sensitive operational details. Verify them
against the selected launcher before use.

## Discover current capabilities

```bash
<launcher> --version
<launcher> --help
<launcher> agents --help
```

Inspect current model aliases, effort, and permission flags. Read emitted init settings rather than wrapper definitions. Use `agents --help` only for native background-agent work.

## Semantic Stream

The compact monitoring baseline is:

```bash
printf '%s' "$TASK_PROMPT" | <launcher> --print --output-format stream-json --verbose
```

The stream is JSONL. Consume complete lines continuously so the child process
cannot block on a full stdout pipe.

Useful event classes:

| Claude event | Compact host state |
|---|---|
| `type=system`, `subtype=init` | `running` — check `tools` and `permissionMode` here |
| assistant message containing a tool call | `working — <tool> started` |
| tool result | `working — <tool> completed` |
| `type=result` with `is_error` not true and exit 0 | `turn ended; verify task evidence` |
| `is_error: true` (e.g. `terminal_reason=api_error`), or nonzero exit | `failed` |

The result event's `subtype` (for example `success`) is not success evidence on
its own: an authentication failure can carry `subtype=success` with
`is_error: true` and exit 1.

Ignore thinking blocks and raw reasoning. Do not enable
`--include-partial-messages` unless a separate live-text interface truly needs
token deltas; it is noisy and unnecessary for liveness monitoring. Some
launchers may still emit thinking-token counters without that flag; ignore them.

A `type=system` event with `subtype=api_retry` reports model-call retries
(minutes between attempts, up to ten). It is a liveness signal, not progress:
if attempts stall near the limit with no new tool calls, stop the run through
the host instead of waiting indefinitely.

Options such as `--tools`, `--allowedTools`, and `--add-dir` accept multiple
values and can consume a trailing positional prompt. Pass the prompt through
stdin whenever a variadic option is present. If Claude reports
`Input must be provided either through stdin or as a prompt argument when using
--print`, move the prompt to stdin and retry once; do not keep rearranging flags
blindly. Print mode also requires `--verbose` for stream-json — the error only
appears at runtime, not in `--help`.

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

- A terminal `result` is the stream-level completion marker.
- Combine it with the process exit code; neither a PID disappearing nor a
  plausible final-looking message is sufficient by itself.
- For tasks that depend on file reads, commands, or edits, verify the matching
  successful tool results. A terminal success with rejected or absent tool
  evidence does not verify the task outcome.
- Preserve stderr for diagnosis, but do not convert an otherwise successful run
  into failure solely because stderr contains warnings.
- If output ends with an incomplete JSON line, report an incomplete stream
  rather than manufacturing completion.

Claude Code also exposes native background-agent commands in some versions.
Their availability and policy may differ from print-mode streaming; inspect
`<launcher> agents --help` when that capability is specifically required.
