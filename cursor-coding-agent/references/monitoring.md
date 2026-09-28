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

Confirm identity by finding `Start the Cursor Agent` in `--help`; it is not the
first output line. `--version` prints only a version number, and the bare
executable name `agent` is not globally unique. Do not use another subcommand
to probe an opaque wrapper.

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

For any named report or stream file, use a fresh path for this invocation even
when the host retains the process. A prior run's file is not this run's result.

If the host has no resumable process facility, redirect stdout and stderr into a
fresh directory for each invocation under `${TMPDIR:-/tmp}`, retain the PID and
have the launch wrapper write the child's exit code to a file when it ends.
Poll process liveness and newly appended complete lines; a later shell cannot
recover an exit code from a PID alone.
Accept a report artifact only when it was produced for this invocation and its
content agrees with the completed tool and terminal events; an old `response.md`
can survive an aborted run while a later run writes a different report. Verify
that the child survives its launching shell; some hosts reap `nohup ... &`
children on shell exit. Prefer a foreground host session when available.
Temporary captures may be left for system cleanup.

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
