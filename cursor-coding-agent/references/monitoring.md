# Cursor CLI Monitoring Reference

This reference contains version-sensitive operational details. Verify them
against the selected launcher before use.

## Discover Current Capabilities

```bash
<launcher> --version
<launcher> --help
<launcher> --list-models
<launcher> models
```

Confirm that `<launcher>` identifies Cursor CLI. The bare executable name
`agent` is not globally unique and may resolve to a different product.

Current help exposes `--model`, model listing, `--print`, and
`--output-format stream-json`. Some models expose effort as a model parameter
rather than a standalone flag. Use current help and model output for the exact
syntax and supported values.

`<launcher>` may be an absolute path or a user-provided wrapper. A wrapper may
inject model, authentication, permission, sandbox, or bypass settings. Preserve
those semantics and do not assume native defaults apply.

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
| terminal `result` with a successful exit | `completed` |
| terminal failure or nonzero exit | `failed` |

Ignore thinking events and raw reasoning. Do not enable
`--stream-partial-output` unless a separate live-text interface truly needs
character deltas. Partial mode can emit duplicate assistant flushes and is
unnecessary for liveness monitoring. Thinking deltas may still appear without
that flag; ignore them.

## Polling Contract

The host's running-task ID is not the Cursor chat/session ID and is not the OS
PID.

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

- Successful runs normally end with a terminal `result`.
- Failed runs may exit nonzero without emitting a terminal `result`; always
  observe the process exit.
- Preserve stderr for diagnosis, but do not treat stderr output alone as
  failure.
- If output ends with an incomplete JSON line, report an incomplete stream
  rather than manufacturing completion.

Cursor's protocol or cloud-worker commands serve different integration models.
Inspect their own help only when a workflow explicitly requires protocol-level
control or remote workers; they are not needed for ordinary monitoring.
