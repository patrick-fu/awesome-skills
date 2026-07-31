# Claude Code Monitoring Reference

This reference contains version-sensitive operational details. Verify them
against the selected launcher before use.

## Discover Current Capabilities

```bash
<launcher> --version
<launcher> --help
<launcher> agents --help
```

Current Claude Code help exposes `--model`, `--effort`, `--print`, and
`--output-format stream-json`. Use current help for supported model aliases,
effort levels, permission modes, and option placement.

`<launcher>` is a placeholder. It may be `claude`, an absolute path, or a
user-provided wrapper. A wrapper may inject model, authentication, provider,
permission, or bypass settings. Preserve those semantics and do not assume the
raw `claude` defaults apply. Treat wrappers as opaque because their definitions
or environments may contain credentials: discover their contract only through
`<launcher> --version` and `<launcher> --help`; do not print definitions, source,
or environment contents.

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
| initialization | `running` |
| assistant message containing a tool call | `working — <tool> started` |
| tool result | `working — <tool> completed` |
| terminal `result` with a successful exit | `completed` |
| terminal failure or nonzero exit | `failed` |

Ignore thinking blocks and raw reasoning. Do not enable
`--include-partial-messages` unless a separate live-text interface truly needs
token deltas; it is noisy and unnecessary for liveness monitoring. Some
launchers may still emit thinking-token counters without that flag; ignore them.

Options such as `--tools`, `--allowedTools`, and `--add-dir` accept multiple
values and can consume a trailing positional prompt. Pass the prompt through
stdin whenever a variadic option is present. If Claude reports
`Input must be provided either through stdin or as a prompt argument when using
--print`, move the prompt to stdin and retry once; do not keep rearranging flags
blindly.

## Polling Contract

The host's running-task ID is not the Claude conversation/session ID and is not
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

- A terminal `result` is the stream-level completion marker.
- Combine it with the process exit code; neither a PID disappearing nor a
  plausible final-looking message is sufficient by itself.
- Preserve stderr for diagnosis, but do not convert an otherwise successful run
  into failure solely because stderr contains warnings.
- If output ends with an incomplete JSON line, report an incomplete stream
  rather than manufacturing completion.

Claude Code also exposes native background-agent commands in some versions.
Their availability and policy may differ from print-mode streaming; inspect
`<launcher> agents --help` when that capability is specifically required.
