# Codex CLI Monitoring Reference

This reference contains version-sensitive operational details. Verify them
against the selected launcher before use.

## Discover Current Capabilities

```bash
<launcher> --version
<launcher> --help
<launcher> exec --help
<launcher> review --help
<launcher> debug models
```

Current help exposes `--model`, `--json`, and sandbox selection. The model
catalog reports available models and their supported reasoning levels. The raw
`debug models` output is very large: extract only each model's slug,
visibility, and supported reasoning levels instead of loading it whole. Inspect
current configuration help or reference material for the exact reasoning-effort
override rather than copying a stale key or value from this skill.

`<launcher>` is a placeholder. It may be `codex`, an absolute path, or a
user-provided wrapper. A wrapper may inject model, authentication, profile,
approval, sandbox, or bypass settings. Preserve those semantics and do not
assume native defaults apply.

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

## Polling Contract

The host's running-task ID is not the Codex thread/session ID and is not the OS
PID.

1. Start the process through the host facility that can yield while retaining
   the child process.
2. Save the returned running-task ID.
3. Reuse that ID with the host's wait, poll, or resume operation.
4. Parse only new complete JSONL records.
5. If no semantic record arrives but the process is alive, retain `running`.
6. Finish only after a terminal turn event and process exit have been observed.

For any named report or stream file, use a fresh path for this invocation even
when the host retains the process. A prior run's file is not this run's result.

If the host has no resumable process facility, redirect stdout and stderr into a
fresh directory for each invocation under `${TMPDIR:-/tmp}`, retain the PID and
have the launch wrapper write the child's exit code to a file when it ends.
Poll process liveness and newly appended complete lines; a later shell cannot
recover an exit code from a PID alone. Verify that the child survives its
launching shell; some hosts reap `nohup ... &` children on shell exit. Prefer a
foreground host session when available. Temporary captures may be left for
system cleanup.

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
