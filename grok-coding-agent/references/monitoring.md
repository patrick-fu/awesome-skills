# Grok CLI Reference

## Boundaries

For file-only work, choose `--sandbox read-only --permission-mode dontAsk
--no-subagents --tools read_file,grep,list_dir --deny 'MCPTool(*)'` when supported.
Tool filtering, permission policy and OS sandboxing are separate controls:
startup hooks and discovery tools require their own consideration. An init
list containing `search_tool`/`use_tool` is not proof that MCP access occurred,
nor that every possible path is confined. Deny wins over allow; replace a
blanket MCP deny narrowly only for an authorized tool.

For strict workspace writes, use an operator-configured fail-closed profile
extending workspace with the intended roots and required runtime paths. Repo
configuration is not trusted operator configuration. Verify enforcement;
explicit sandbox-disabled/unenforced warnings are isolation failures even if
exit is zero. Other configuration/plugin warnings are diagnostic, not blanket
failures. Built-in profiles can warn and continue; macOS read-only does not
block child network access. Preserve required network boundaries separately.
Do not impose read-probe restrictions on unrelated authorized implementations.

## Stream

The runner requires `streaming-messages-json`:

| Event | Evidence |
| --- | --- |
| root `system/init` | Observed model/cwd/permissionMode/tools/session ID; absent values UNKNOWN |
| assistant `tool_use` | ID records a call, names and payload remain in raw capture |
| user `tool_result` | Matching tool_use_id and is_error record the outcome |
| root `result` | subtype/is_error plus child exit classify the turn; result text is candidate answer |

Nested tool identities include their parent ID. Tool errors and permission
telemetry do not veto mechanical completion; the host judges necessary actions.
Missing denial telemetry stays UNKNOWN. Suppress thinking/token deltas in host
updates, retaining raw evidence.

If this transport is unavailable, report the capability gap. Native
`streaming-json` is a different ACP schema terminating with `end`; it needs a
separately verified host integration, not this parser with renamed fields.

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

Use current resume/continue/fork help and verify the intended session identity.
`--session-id` creates a new session; it does not resume one. Conversation
resume does not imply code restore; `--restore-code`/worktree behavior needs
separate authorization. ACP/leader/WebSocket are separate integrations.
