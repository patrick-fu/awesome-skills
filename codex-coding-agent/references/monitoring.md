# Codex CLI Reference

## Boundaries

For read-only work, choose exec options `-c 'approval_policy="never"'`,
`--sandbox read-only`, `--ignore-rules`, and optional `--ephemeral` when supported.
The runner forwards **exec** options: root `-a`/`--ask-for-approval` is not an
exec option. Use the selected native exec configuration, not a permission
fallback or automatic policy rewrite. `--ephemeral` controls persistence,
not read-only protection; retain persistence when continuation is needed.

Sandbox, approval and remote MCP effects are separate controls. User/project
execpolicy allow rules can bypass the shell sandbox; `--ignore-rules` skips
those rules, not managed requirements. Verify effective policy, including
wrapper overrides, or use host enforcement before claiming strict confinement.
For authorized writes, select the appropriate sandbox and roots deliberately;
`--add-dir` adds writable roots. Profile `-p` is not a prompt option.

## Stream

| Event | Evidence |
| --- | --- |
| `thread.started` | Session identity, not effective model/cwd |
| `turn.started` | Turn started |
| `item.started/updated/completed` | Item type and lifecycle; command exit/status are separate outcomes |
| `item.completed` agent_message | Last complete text becomes candidate answer |
| `turn.completed/failed` | Terminal turn plus real child exit classify the run |

Diagnostic `error` items and nonterminal error events may precede a successful
turn. Completed items need not all have a started event. Unknown optional
metadata stays UNKNOWN; request flags are not effective-setting evidence.
Large command `aggregated_output` and reasoning stay in raw captures. A final
message file alone is not completion evidence.

Known `Reading additional input from stdin...` status text is tolerated on
stdout for compatibility; the current probe emitted it on stderr. Other
non-JSON stdout remains a parse anomaly, not silently discarded text.

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

Inspect current `exec resume`/`fork` help separately: flags accepted after those
subcommands differ from fresh exec. Preserve native continuation rather than
forcing it through a generic option router; verify the selected session ID
against emitted identity and account for completed actions first. Native review
and app-server are separate integrations.
