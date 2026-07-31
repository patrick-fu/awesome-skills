# Grok Build CLI Monitoring Reference

This reference contains version-sensitive operational details. Verify them
against the selected launcher before use.

## Discover Current Capabilities

```bash
<launcher> --version
<launcher> --help
<launcher> models
```

Current Grok Build CLI help exposes `--model`, `--reasoning-effort`, `-p`,
sandbox selection, and multiple output formats. Use current help and model output
for the exact syntax and supported values.

`<launcher>` is `grok`, its absolute path, or a user-provided Grok wrapper. Do
not use the generic `agent` alias. A wrapper may inject model, authentication,
permission, sandbox, or bypass settings. Preserve those semantics and do not
assume native defaults apply.

## Semantic Stream

When current help exposes `streaming-messages-json`, use these compact monitoring
baselines:

```bash
<launcher> --output-format streaming-messages-json --sandbox read-only --always-approve -p "Review or explain"
<launcher> --output-format streaming-messages-json --sandbox workspace --always-approve -p "Implement the change"
```

Do not add `--include-partial-messages`. Consume complete JSONL records and
reduce them to these states:

| Grok event | Compact host state |
|---|---|
| system initialization | `running` |
| assistant message containing `tool_use` | `working — <tool> started` |
| user message containing `tool_result` | `working — <tool> completed` |
| terminal `result` with successful exit | `completed` |
| terminal failure or nonzero exit | `failed` |

Ignore `thinking` blocks and raw reasoning. Do not forward full tool arguments,
tool results, or assistant text when a short action summary is enough.

If current help lacks `streaming-messages-json`, fall back to:

```bash
<launcher> --output-format streaming-json --sandbox read-only --always-approve -p "Your task"
```

The fallback emits fine-grained `thought` and `text` records. Drop those token
deltas. Use tool-call lifecycle records for `working` and the terminal `end`
record plus process exit for completion.

## Polling Contract

The host's running-task ID is not the Grok conversation/session ID and is not
the OS PID.

1. Start the process through the host facility that can yield while retaining
   the child process.
2. Save the returned running-task ID.
3. Reuse that ID with the host's wait, poll, or resume operation.
4. Parse only new complete JSONL records.
5. If no semantic record arrives but the process is alive, retain `running`.
6. Finish only after terminal output and process exit have been observed.

If the host has no resumable process facility, redirect stdout and stderr into a
directory created under `${TMPDIR:-/tmp}`, retain the PID, and poll both process
liveness and newly appended complete lines. Temporary captures may be left for
system cleanup.

## Terminal and Error Handling

- `result` is the preferred stream's terminal record; `end` terminates the
  fallback stream.
- Combine the terminal record with process exit. A plausible final-looking
  assistant message is not sufficient completion evidence.
- Preserve stderr for diagnosis, but do not classify an otherwise successful
  run as failed solely because stderr contains warnings.
- If output ends with an incomplete JSON line, report an incomplete stream
  rather than manufacturing completion.

Grok session resume, worktree support, ACP stdio, WebSocket, and leader commands
are separate integration surfaces. Inspect their current help only when a
workflow explicitly requires them; they are not needed for ordinary monitoring.
