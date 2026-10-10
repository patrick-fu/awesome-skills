# Codex CLI Monitoring Reference

This reference contains version-sensitive operational details. Verify them
against the selected launcher before use.

## Discover current capabilities

```bash
<launcher> --version
<launcher> --help
<launcher> exec --help
<launcher> review --help
<launcher> debug models
```

Extract only needed model slugs, visibility, and reasoning levels; raw `debug models` can be large. Discover effort override syntax in current help. `--ignore-rules` skips user/project rules, not managed requirements; verify effective policy when strict protection matters.

## Semantic Stream

The compact monitoring baselines are:

```bash
<launcher> -a never exec --json --sandbox read-only --ignore-rules --ephemeral "Review or explain"
<launcher> exec --json --sandbox workspace-write "Implement the change"
```

`--ignore-rules` skips user and project `.rules`, not managed requirements.
An allow rule from managed requirements can still bypass the shell sandbox;
verify the effective policy or use host isolation when strict read-only matters.

`--json` changes stdout to JSONL events. Useful event classes:

| Codex event | Compact host state |
|---|---|
| `thread.started` or `turn.started` | `running` |
| `item.started` | `working — <item> started` |
| `item.completed` | `working — <item> completed` |
| `turn.completed` with a successful exit | `turn ended; verify task evidence` |
| `turn.failed` or nonzero exit | `failed` |

Items may represent command execution, file changes, or agent messages. Ignore
raw reasoning and avoid forwarding full command output when a short action
summary is enough.

Stdout mixes JSONL events with CLI status lines such as `Reading additional
input from stdin...`; parse only complete JSON lines. From each event, extract
the event type, item type, and state, and drop large `aggregated_output`
payloads from command items — a single poll can carry tens of thousands of
tokens. Classify the run from the terminal turn event plus the process's real
exit code, never from the item stream alone.

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

- `turn.completed` and `turn.failed` are terminal turn events.
- Combine the terminal event with process exit. A final-message file or a
  plausible agent message is not sufficient completion evidence.
- For tasks that require commands or edits, inspect their completed item results
  and output. A successful turn after blocked or missing task-critical items
  does not verify the requested outcome.
- A nonterminal warning or error-shaped item can occur in a successful turn.
  Do not classify the whole run from one item alone.
- Stderr may contain recoverable warnings. Preserve it for diagnosis, but use
  terminal state and exit code to classify the run.
- If output ends with an incomplete JSON line, report an incomplete stream
  rather than manufacturing completion.

`codex app-server` exposes deeper lifecycle and steering capabilities in some
versions. It is a separate integration surface; inspect its current help only
when protocol-level control is specifically required.
