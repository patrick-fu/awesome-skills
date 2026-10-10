# Cursor CLI Monitoring Reference

This reference contains version-sensitive operational details. Verify them
against the selected launcher before use.

## Discover current capabilities

```bash
<launcher> --version
<launcher> --help
<launcher> --list-models
<launcher> models
```

Confirm `Start the Cursor Agent` in help; a version or the generic `agent` name is insufficient. Use authenticated listing for exact model and effort syntax; report an authentication failure. Discover opaque wrappers only through the supported help/version entry points.

## Semantic Stream

The compact monitoring baseline is:

```bash
<launcher> --print --trust --output-format stream-json "Your task"
```

Add the current help's read-only mode for review or explanation. For an approved
headless implementation, inspect current help and the wrapper contract to
determine whether automatic tool approval is required.

The stream is JSONL. Useful event classes:

| Cursor event | Compact host state |
|---|---|
| `system/init` | `running` |
| `tool_call` started | `working — <tool> started` |
| `tool_call` completed | `working — <tool> completed` |
| terminal `result` with a successful exit | `turn ended; verify task evidence` |
| terminal failure or nonzero exit | `failed` |

Tool calls appear under typed keys such as `globToolCall`, `grepToolCall`, and
`readToolCall`; the generic `tool_call.name` can be empty, so read the typed
key for the tool name. A shell or write call with `result.rejected` did not
execute, even if the terminal result says success. Classify any conclusion
depending on that call as unverified; preserve the rejection and rerun only
after the execution scope is authorized and the flags are corrected.

Ignore thinking events and raw reasoning. Do not enable
`--stream-partial-output` unless a separate live-text interface truly needs
character deltas. Partial mode can emit duplicate assistant flushes and is
unnecessary for liveness monitoring. Thinking deltas may still appear without
that flag; ignore them.

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

A live headless process may be waiting for approval. `--trust` allowed file
writes in an observed run but shell approval remained blocked. Inspect
`result.rejected` and permission state; correct flags only within authorized
execution scope, with a harmless completed-command probe.

## Terminal and Error Handling

- Successful runs normally end with a terminal `result`.
- Failed runs may exit nonzero without emitting a terminal `result`; always
  observe the process exit.
- Preserve stderr for diagnosis, but do not treat stderr output alone as
  failure.
- For implementation, compare the intended outcome with completed tool calls,
  `git status --short` (including untracked files), and the relevant diff or
  artifacts. Exit 0 with an empty tracked-file diff alone proves neither
  application nor failure. `--force`/`--yolo` auto-approves commands unless
  explicitly denied; use it only when shell execution is authorized.
- For command-based reviews or ablations, require completed command events and
  their output or artifacts. A prose-only conclusion after rejected calls is
  an unverified hypothesis, not an experiment.
- If output ends with an incomplete JSON line, report an incomplete stream
  rather than manufacturing completion.

Ordinary monitoring does not need Cursor's hidden integration subcommands
(`acp` for the Agent Client Protocol, `worker` for cloud workers); there is no
command literally named `protocol`. Inspect their own help only when a workflow
explicitly requires them.
