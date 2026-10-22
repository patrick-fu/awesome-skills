# Antigravity Boundaries and Recovery

## Boundaries

For file-only work, list target paths host-side, pass authorized external
directories with `--add-dir`, and request `view_file`. Require DONE reads with
usable output and no tool error for each target. A missing listing capability
can instead lead to denied `run_command`; exit 0 does not establish completion.

Planning mode is not OS read-only isolation. Permission modes and `--mode` are
separate; observed modes are `plan` and `accept-edits`, while default means
omitting the flag. Check the selected launcher's current capabilities.
Headless tools cannot obtain interactive approval; permission behavior has
changed across versions, so verify the intended boundary before relying on it.

`--dangerously-skip-permissions` approves every tool and requires explicit
authorization for that run. Under skip-permissions, `denied_actions` is always
empty; use the authorization tree/status-diff as boundary evidence instead.
Neither correct `init.cwd` nor absent denials proves confinement.

## Evidence

`stream.jsonl` and `stderr.log` retain raw evidence; `rc.txt` records the actual
child exit; `answer.txt` extracts the first terminal response, including useful
partial text from a failed run. `receipt.json` is published atomically after exit. Before then,
`inspect` reports `UNFINALIZED`, which does not prove the process is alive.
Use the retained host handle. Inspect exit 0 means the snapshot was obtained,
not that the task succeeded. Host handle, PID and conversation ID are distinct.
Temporary captures are not archives; preserve needed evidence before cleanup.

The parser owns the `event` schema: `init.model`/`init.cwd` are nested, and the
answer is `result.response`. Unknown values are the string `UNKNOWN`; known
values retain JSON types. `result_status` preserves the CLI terminal status;
receipt `status` combines it with exit, response, parseable records and
stderr timeout/error evidence. Unknown event kinds remain in raw captures and
cannot substitute for init/result. `step_update` ACTIVE/DONE describes tool
lifecycle; DONE still requires checking tool output/errors. Omit thinking and
text deltas from progress reports.

In observed 1.3.6 successful streams, `denied_actions` can be omitted. Preserve
`UNKNOWN` without invalidating completion; it does not establish an empty denial
list or a permission boundary. Known denials remain visible but do not veto
completion: check whether required work was denied or recovered. Invalid field
types still prevent `SUCCESS`. A complete final JSON object without a newline
sets `incomplete_final_line=true` but is not a truncated record.

For answer extraction only, after saving a stream:

```bash
jq -er '
  select(.event == "result") | .result
  | select(.status == "SUCCESS" and ((.denied_actions // []) | length) == 0)
  | .response | select(length > 0)
' "$STREAM_FILE"
```

This does not check the exit, timeout, completed tools, or artifact correctness.

## Recovery

Before retrying or resuming, inspect completed actions and partial artifacts
so work and side effects are not repeated.

- **SUCCESS:** independently accept the answer/artifacts and required tools.
- **FAILED:** retain the error even if partial work is useful. Inspect stderr:
  exit 1 can indicate model/effort conflict; exit 2 usage/format errors or
  `missing unit in duration`; exit 3 can carry `AGY_ERROR` with `error_code`,
  `retryable`, and `error_id`. If retryable is false, stop retrying/resuming that
  run; a fresh bounded task is a separate attempt.
- **INCOMPLETE:** inspect empty response, missing identity/result,
  malformed or truncated JSONL, duplicate terminal events and timeout warnings.
  Since 1.2.6 a print timeout can return partial output with exit 0.
  Only explicit print-timeout expiry diagnostics set `timeout_warning`;
  auxiliary `timed out` messages remain in stderr for diagnosis.
- **Deadline / Cancel:** measure host wall time; `result.duration_seconds` has
  disagreed with elapsed time. Give a host watchdog time for CLI shutdown.
  Distinguish CLI timeout, watchdog, stream interruption and user cancellation.
  Cancel through the retained host handle, not process-name matching. On POSIX,
  the script terminates its own process group, escalating after a five-second
  child grace period and stopping remaining group members. It records
  `stopped` (the host cancellation cause) separately from actual rc; interrupted
  runs cannot claim success even if the child handles termination with exit 0. Signals after observed
  child exit do not change that outcome. Detached processes outside the group
  need separate ownership; non-POSIX termination covers the direct child only.
  If termination is denied, the script reports its owned PID and leaves evidence
  `UNFINALIZED`. An OS-unreapable child can outlast escalation; never infer exit
  from the grace period alone.
  Confirm owned work has stopped before releasing the workspace.
  Signal exits are negative in `rc.txt` and returned as 128 + signal number.
- **Resume:** `--continue` / `-c` selects the latest conversation;
  `--conversation <id>` selects one.
  Verify conversation ID and increasing `num_turns`: an unknown ID can silently
  start fresh with exit 0. HTTP success alone does not prove a complete stream.

The script never retries, elevates permissions, manages conversations, changes
HOME or cleans attempts. Use `help <subcommand>` / `changelog` for capabilities
outside print tasks. Protocol observations span 1.2.11–1.3.6; current launcher
help and model catalog take precedence over cached flags and online defaults.

## Maintenance

Run `python3 evals/check_launch_guards.py`, `python3 evals/check_stream_parser.py`,
`python3 evals/check_cancel.py` and `python3 evals/check_ablation.py` from this
skill directory. These inject offline stubs. [Evidence](../evals/evidence.json) separates historical incidents,
the reconstructed denied fixture, constructed controls and ablation limits.
