# Antigravity Monitoring

Read this for stream parsing, completion decisions, permission recovery, or
resume. The launch and authorization contract is in [SKILL.md](../SKILL.md).
Behavioral observations below cover 1.2.11–1.2.12; help was rechecked on
1.3.3. Verify version-sensitive behavior with the selected launcher.

## Retain the process and its evidence

Use the host's resumable process facility; save its task handle and consume
new complete stdout/stderr lines continuously. The host handle, OS PID, and
Antigravity conversation ID identify different things. Keep fresh captures
for each attempt; an earlier report is not evidence for this one.

Without that facility, capture to a fresh system-temp directory, retain the
PID, and arrange for the launch wrapper to save the child's exit code. A later
shell cannot recover that code from a vanished PID. Verify the child survives
its launching shell; some hosts reap even `nohup ... &` children. Prefer a
foreground host session when available.

Measure deadlines with host wall time. `result.duration_seconds` differed
substantially from elapsed time in a 1.2.12 failure. Choose the CLI deadline
deliberately and give a host watchdog time for CLI shutdown. Distinguish an
observed timeout warning, watchdog action, stream failure, and user cancel;
quiet output alone is not a termination signal.

## Parse the selected output

| Format | Evidence available |
| --- | --- |
| `text` | Final prose |
| `json` | One object: `conversation_id`, `status`, `response`, duration, `num_turns`, usage; failure may add `error` |
| `stream-json` | JSONL `init`, `step_update`, terminal `result`; use for required tool evidence |

`--input-format stream-json` accepts NDJSON turns on stdin and requires
`--output-format stream-json`. Invalid output-format values were silently
treated as text; use a supported value.

Parse `event`, not `type`. In
`{"event":"result","result":{"status":"SUCCESS","response":"..."}}`,
the answer is `result.response`. `step_update.text_delta` is a field, not a
separate event; omit thinking and token deltas from progress reports.

| Event | Host interpretation |
| --- | --- |
| `init` | Running; record cwd, tools, permission mode, conversation ID and model when emitted |
| `step_update.state: ACTIVE` | Step started |
| `step_update.state: DONE` | Step ended; inspect tool output/error before calling it successful |
| `result` | Classify the turn below, then confirm actual process exit |

Short replies may have no ACTIVE step. Missing `init.model` leaves the
effective model unverified; retain the explicit requested model separately.
Preserve full captures while parsing, rather than keeping only grep/tail
output. An incomplete final JSON line is incomplete stream evidence.

## Decide completion

| Observed evidence | Decision |
| --- | --- |
| SUCCESS, exit 0, nonempty response, required tools completed, no denied actions or timeout | Turn completed; independently accept or reject the answer/artifacts |
| SUCCESS/exit 0, empty response or `denied_actions` | Task not established; inspect permission/tool failures |
| ERROR with nonempty response, even exit 0 | Keep ERROR; inspect `result.error` and independently verify useful partial work |
| No terminal result, partial JSON, or timeout warning on stderr | Incomplete; preserve partial evidence even with response text or exit 0 |
| Other non-SUCCESS status, structured failure, or nonzero exit | Failed/interrupted/not completed; retain the actual status and cause |

Ordinary stderr warnings alone do not invalidate a successful turn. Since
1.2.6, print-timeout expiry can return partial output and exit 0 with a warning.
A zero-byte answer or disappearing PID does not establish completion.

For answer extraction only, after saving a stream:

```bash
jq -er '
  select(.event == "result") | .result
  | select(.status == "SUCCESS" and ((.denied_actions // []) | length) == 0)
  | .response | select(length > 0)
' "$STREAM_FILE"
```

This does not check the exit, timeout, completed tools, or artifact correctness.

| Exit | Diagnostic to inspect |
| --- | --- |
| 1 | Model/effort selection conflict |
| 2 | Usage: unknown flag, positional prompt, or incompatible input/output formats |
| 3 | `AGY_ERROR: {...}` on stderr: `status`, `error_code`, `retryable`, `error_id` |

Since 1.2.10, exit 3 can follow partial streamed output; older versions could
exit 0. Preserve this attempt's stream, stderr and artifacts before recovery.
If `AGY_ERROR.retryable` is false, stop retrying/resuming that run; a fresh
bounded task is a separate attempt. HTTP success does not prove a complete
model stream: an interrupted response needs its actual finish/error evidence.

## Recover permissions or resume

Headless tools cannot obtain interactive approval. Soft denial may still
exit 0; check `denied_actions`, tool errors and actual output. In 1.2.11 a
settings `permissions.allow` rule did not rescue a write request; current
[headless documentation](https://antigravity.google/docs/cli/headless/)
describes scoped allow rules and auto-allowed workspace writes. Probe the
intended permission setup before relying on either version's behavior.

For file-only recovery, list paths host-side, supply them in the prompt and
request `view_file`. Require DONE reads with usable output and no tool error
for every required target, then a nonempty successful answer and no denial.
Since 1.2.7 a missing listing tool could lead to denied `run_command` instead.
If commands are essential, establish the authorized host boundary before
broader approval. `--dangerously-skip-permissions` approves every tool.

Tool permission modes and `--mode` are separate. Observed execution modes
are `accept-edits` and `plan`; omit the flag for default (`--mode default`
errors). Planning does not enforce an OS read-only boundary. Discover current
permission fields/flags through help rather than guessing presets.

After the partial-action checks in the main skill, `--continue`/`-c` resumes
the latest conversation; `--conversation <id>` selects one. Verify the same
`conversation_id` and increasing `num_turns`. An unknown ID can warn and
start fresh with exit 0, so exit alone does not prove resume.

For capabilities not needed by an ordinary run, use `help <subcommand>` or
`changelog` on demand. Current help and online documentation can disagree:
1.3.3 help shows timeout default 0s and effort xhigh/max, while the online
reference still lists 5m and low/medium/high. Use the selected launcher's help
and model catalog; a global effort enum does not prove model-specific support.
