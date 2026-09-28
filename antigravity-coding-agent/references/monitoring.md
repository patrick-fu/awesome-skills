# Antigravity Monitoring Reference

This reference contains version-sensitive operational details, verified against
Antigravity CLI 1.2.11. Verify them against the selected launcher before use.

## Discover Current Capabilities

```bash
<launcher> --version
<launcher> --help
<launcher> help <subcommand>
<launcher> models
<launcher> changelog
```

Current help exposes `--model`, `--effort` (`low|medium|high|max`), `--print`
(`-p`), `--print-timeout`, `--output-format` (`text|json|stream-json`),
`--continue`/`--conversation`, `--mode` (`accept-edits|plan`), `--sandbox`, and
`--dangerously-skip-permissions`. `<launcher> models` lists the account or
endpoint catalog with effort-tiered display names. `<launcher> changelog` is
the authoritative record of behavioral changes between versions.

`<launcher>` is a placeholder. It may be `agy`, an absolute path, or a
user-provided wrapper. A wrapper may inject model, authentication, provider,
permission, or bypass settings. Preserve those semantics and do not assume the
raw `agy` defaults apply. Treat wrappers as opaque because their definitions or
environments may contain credentials: discover their contract only through
`<launcher> --version` and `<launcher> --help`; do not print definitions,
source, or environment contents.

## Semantic Stream

The compact monitoring baseline is:

```bash
<launcher> -p "$TASK_PROMPT" --output-format stream-json
```

The stream is JSONL. Consume complete lines continuously so the child process
cannot block on a full stdout pipe.

Useful event classes:

| Antigravity event | Compact host state |
|---|---|
| `init` (model, cwd, tools, permission_mode) | `running` |
| `step_update` with `state: ACTIVE` | `working — <step_type> started` |
| `step_update` with `state: DONE` | `working — <step_type> completed` |
| terminal `result` with `status: SUCCESS` and exit 0 | `turn ended; verify task evidence` |
| `result` with a non-SUCCESS status, `AGY_ERROR` on stderr, or exit 3 | `failed` |

`text_delta` is a field on `step_update`, not a separate event; ignore its
content for liveness. Short replies can go straight to `state: DONE` without a
visible `ACTIVE` state.

Parse the `event` key, not `type`. The terminal envelope is
`{"event":"result","result":{"status":"SUCCESS","response":"..."}}`:
`result` is an object and the answer is `result.response`. For a single-turn
read-only review, this extracts a non-empty successful answer from a saved
JSONL stream (and fails if no matching terminal record exists):

```bash
jq -er '
  select(.event == "result")
  | .result
  | select(.status == "SUCCESS" and ((.denied_actions // []) | length) == 0)
  | .response
  | select(length > 0)
' "$STREAM_FILE"
```

This is only an extraction check; also verify the process exit and required
tool results and inspect stderr for a timeout warning. Do not filter the live
stream through `grep` or `tail` as the sole capture: that can hide terminal
records and the CLI exit status.

## Exit Codes and Completion Evidence

- Exit 0 with a terminal `result.status: SUCCESS` and a non-empty response —
  turn completed; verify task-critical tool results and no timeout warning
  before claiming success.
- Exit 0 with `result.status: SUCCESS` but an empty response and
  `denied_actions` in the result — headless permission auto-denial; not a
  completed task (see below).
- Exit 1 — model or effort selection conflicts, such as a mismatched
  `--model`/`--effort` pair.
- Exit 2 — usage errors: unknown flags, a trailing positional prompt, or
  `--input-format stream-json` without `--output-format stream-json`.
- Exit 3 with an `AGY_ERROR: {...}` JSON line on stderr — model, agent, or API
  failure; the JSON carries `status`, `error_code`, `retryable`, and
  `error_id`. Since 1.2.10 this includes runs that streamed partial output
  before failing; older versions could exit 0 after partial output.
- When `AGY_ERROR.retryable` is false, stop retrying or resuming the same run.
  Keep complete JSONL records and any intermediate artifacts, then report
  which work was verified and which result was never produced. A fresh,
  smaller task is a separate attempt, not a successful resume.
- Invalid `--output-format` values are silently treated as text.
- If output ends with an incomplete JSON line, report an incomplete stream
  rather than manufacturing completion.
- If the process exits or its explicit `--print-timeout` expires without a
  terminal `event: result`, retain the partial stream and report an incomplete
  run. A zero-byte final-answer file is not a successful review.
- Since 1.2.6, `--print-timeout` expiry can return partial output and exit 0
  with a warning on stderr. Treat that warning as an incomplete run even when
  the stream contains a non-empty response.

## Headless Permissions

The default `permission_mode` is `request-review`: in a TTY, file writes pause
for an interactive diff review. In headless runs nothing can approve, so any
tool request needing an un-granted permission is auto-denied. Verified against
1.2.11:

- `permissions.allow` rules in `settings.json` did not rescue a `write_file`
  request in one 1.2.11 observation, and the binary carries conflicting
  messages about them; treat headless allow-rules as unverified and test
  before relying on them.
- The process exits 0 even when a tool was auto-denied; the empty response and
  `denied_actions` in the result are the tell.
- `--dangerously-skip-permissions` auto-approves all tool requests and is the
  supported headless path for write tasks. See the skill body for the
  authorization boundary.

### Read-only no-op recovery

Since 1.2.7 the default toolset has no directory-listing tools, so a headless
run over an unfamiliar repo probes with `run_command`, whose permission is
auto-denied; the run can end `SUCCESS` with an empty response. Recover without
bypass: list the files host-side (`git ls-files` or `ls -R`), put the list
into the prompt, and instruct the run to read only through `view_file`, which
is auto-approved for workspace paths. Confirm recovery by `denied_actions`
disappearing and a non-empty `response`.

Permission modes (`request-review`, `always-proceed`, `strict`,
`proceed-in-sandbox`) and the `--mode` execution modes are separate controls;
`--mode` accepts `accept-edits` and `plan` only (omitting it is the implicit
default; passing `default` errors), and `plan` researches and plans without
making changes. Treat `toolPermission` and permission-preset fields in
`settings.json` as version-sensitive; prefer documented CLI flags.

## Session Resume

`--continue` (or `-c`) resumes the most recent conversation in headless mode;
`--conversation <id>` targets a specific one. Each `-p` run against the same
conversation increments `num_turns` in the `result` and JSON output. An
unknown `--conversation` id only warns and starts a fresh conversation with
exit 0, so verify a resume by the matching `conversation_id` and an
incremented `num_turns` in the JSON result, not by exit status.

## Output Formats

- `text` (default): final-answer prose only.
- `json`: one JSON object with `conversation_id`, `status`, `response`,
  `duration_seconds`, `num_turns`, and token usage; failures add an `error`
  field. Parse this when the caller needs machine-readable final output.
- `stream-json`: the JSONL event stream used for monitoring. `--input-format
  stream-json` additionally accepts NDJSON turns on stdin for multi-turn
  driving and requires `--output-format stream-json`.

## Polling Contract

The host's running-task ID is not the Antigravity conversation ID and is not
the OS PID.

1. Start the process through the host facility that can yield while retaining
   the child process.
2. Save the returned running-task ID.
3. Reuse that ID with the host's wait, poll, or resume operation.
4. Parse only new complete JSONL records.
5. If no semantic record arrives but the process is alive, retain `running`.
6. Finish only after terminal output and process exit have been observed.

For any named report or stream file, use a fresh path for this invocation even
when the host retains the process. A prior run's file is not this run's result.

If the host has no resumable process facility, redirect stdout and stderr into
a fresh directory for each invocation under `${TMPDIR:-/tmp}`, retain the PID,
and have the launch wrapper write the child's exit code to a file when it ends.
Poll process liveness and newly appended complete lines; a later shell cannot
recover an exit code from a PID alone. Only accept artifacts created for that
invocation; a pre-existing report file can be residue from an aborted run.
Verify that the process survives the launching shell: some hosts reap
`nohup ... &` children as soon as that shell
exits. Prefer a foreground host session when available. Temporary captures may
be left for system cleanup.

## Terminal and Error Handling

- A terminal `result` is the stream-level completion marker; combine it with
  the process exit code; neither a PID disappearing nor a plausible
  final-looking message is sufficient by itself.
- Preserve stderr for diagnosis; `AGY_ERROR` is the structured failure record.
- Do not convert an otherwise successful run into failure solely because stderr
  contains warnings.
