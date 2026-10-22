# Cursor CLI Reference

## Boundaries

For file-only review, select `--mode ask`. Command-based review and implementation
need normal mode; ask/plan are read-only. `--trust` trusts the workspace, not
shell execution. `--force`/`--yolo` auto-approves commands unless denied; choose
it only with corresponding authorization, never as automatic recovery.

A completed `shellToolCall` with `result.rejected` did not execute, even with
turn success and exit zero. Confirm a harmless completed-command probe when
shell approval matters. `permissionMode=default` is not an echo of `--mode ask`.
Separate workspaces isolate state, not capabilities; verify host protection
before claiming strict read-only or confinement. Additional roots, MCPs,
plugins and worktree setup can broaden effects; inspect them for that boundary.

## Stream

| Event | Evidence |
| --- | --- |
| `system/init` | Observed model/cwd/permissionMode/session ID; missing fields stay UNKNOWN |
| `tool_call` started/completed | Typed keys such as `readToolCall`, not generic name; opaque call IDs may contain newlines |
| typed tool result | `success`, `rejected`, error or unknown outcome, separately from turn status |
| `assistant` | Last complete text becomes candidate `answer.txt` |
| terminal `result` | Aggregate saved as `aggregate.txt`; success/is_error plus child exit classify the turn |

Observed `result.result` concatenates preamble and final answer; it is not a
reliable exact-answer field. A candidate assistant alone is not completion.
Reasoning and partial text stay in raw captures, not the compact receipt.

Complete JSON without a trailing newline is valid; truncated JSON, duplicate
terminal records and unfinished known tool lifecycles remain incomplete.
Unknown event kinds are counted without inventing their meaning. Missing
initialization metadata does not block a valid terminal and real exit.

## Recovery

A final receipt is published only after observed child exit; `UNFINALIZED`
does not prove either liveness or death. Use the retained host handle. Signal
or deadline stop is separate from the actual child rc, even if the child handles
termination and returns zero. POSIX cancellation targets this attempt's process
group; detached workers, unkillable processes and non-POSIX child-only shutdown
are outside that guarantee. A stop/reap error leaves evidence unfinalized;
resolve the owned process state and confirm exit before releasing its workspace.

Inspect completed actions and partial artifacts before retrying or resuming;
keep attempts distinct. The runner neither retries nor widens permissions,
manages sessions, isolates HOME, or cleans captures. System temp is not permanent
storage: retain useful acceptance/failure evidence deliberately.

Use current `--resume`/`--continue` help and verify emitted session identity
against the intended conversation before continuing. Native persist/worker/ACP
are separate integration surfaces, not ordinary task-launch modes.
