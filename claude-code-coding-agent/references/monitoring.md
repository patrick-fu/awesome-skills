# Claude Code Boundaries and Recovery

## Boundaries

Choose capabilities for the task; the launcher preserves those arguments and
does not add permission presets. For file-only reads, request
`--strict-mcp-config --tools Read Grep Glob`, then verify the receipt's actual
tools are exactly `Glob`, `Grep`, `Read`, with no MCP servers. Unknown tool names
can remove expected tools. Required paths still need successful read results.

`--restricted` adds directory confinement in compatible launchers. Claude Code
2.1.283 rejected a bypass wrapper before init with
`bypassPermissions not supported in restricted mode`; adding `dontAsk` did not
resolve it. Keep that failure; do not silently drop restricted or change the
selected launcher. Request a compatible boundary if confinement is required.

A separately chosen `--safe-mode --strict-mcp-config --tools Read Grep Glob`
run succeeded through that wrapper with only those tools and no MCP servers,
but permission mode remained `bypassPermissions`. This establishes the observed
tool set, not OS isolation or confinement to listed paths. Safe mode changes
customization loading, so choose it only when that fits the task; it is not a
default or automatic recovery. Empty permission denials under bypass are not
boundary proof. Check the authorized tree and actual file changes. Preserve
task-specific bans such as worktree creation, including `EnterWorktree`.

## Evidence

The attempt directory contains full `stream.jsonl`, `stderr.log`, child
`rc.txt`, extracted `answer.txt`, and atomically finalized `receipt.json`.
Receipts omit thinking, tool payloads and answer text; inspect raw captures
only for task-specific verification or diagnosis. Temporary captures are not
archives; retain evidence needed after system cleanup.

The script owns the Claude `type` schema: `system/init` supplies actual model,
cwd, permission mode, tools and MCP servers; assistant `tool_use` and user
`tool_result` are paired by ID; top-level `result` supplies subtype and
`is_error`. Unknown optional fields remain `UNKNOWN`; unrelated events are
retained in the raw stream. `api_retry` counts are liveness, not task progress.

`COMPLETED` requires child exit 0, one init and terminal result, success with
`is_error=false`, an answer, and complete parseable evidence with paired
tool calls/results. Tool errors and permission denials are recorded separately: a
recovered tool failure need not fail the turn, and a completed turn need not
satisfy the task. `answer_format=json` denotes a structured result in
`answer.txt`. A complete final JSON object without a newline sets
`incomplete_final_line=true` but is not a truncated record. Ordinary stderr
warnings do not change the verdict.

## Recovery

- **UNFINALIZED:** no final receipt exists. Check the retained host handle;
  this status does not prove the child is still running. A result line alone
  does not establish process exit.
- **FAILED:** retain child exit and the CLI's error. For a pre-init failure,
  inspect stderr, including wrapper/permission conflicts. Fix the actual cause
  without broadening permissions or switching launchers automatically.
- **INCOMPLETE:** preserve partial evidence; inspect truncation, duplicate
  terminal records, pending tools, and missing result/answer.
- **Cancel:** use the retained host handle, not process-name matching. On POSIX,
  the launcher terminates its own process group, allowing the child five seconds
  before escalation and stopping remaining group members. `stopped` records the host
  cancellation/deadline separately from actual rc, including a child exiting 0
  during shutdown. A signal after observed exit does not reverse completion.
  Confirm owned work has stopped before releasing the workspace. Detached
  processes outside the group need separate ownership; non-POSIX termination
  covers the direct child only.
  If termination is denied, the error names the owned PID and evidence remains
  `UNFINALIZED`. An OS-unreapable child can outlast escalation; the grace period
  is not proof of exit.
  An uncatchable kill or storage failure can leave no final receipt.
- **Resume:** inspect completed actions and partial artifacts first. Pass an
  explicitly selected resume/continue option through the launcher, then verify
  session identity and continuation in the captured events. The script never
  retries, resumes, changes HOME, or cleans old attempts on its own.

Native background agents are a separate lifecycle. Consult the selected
launcher's `agents --help` when explicitly needed; they are not print runs.

## Maintenance

Run `python3 evals/check_run.py`, `python3 evals/check_ablation.py` and
`python3 evals/check_contract.py` from this skill directory. They use offline
stubs; [evidence.json](../evals/evidence.json) distinguishes observed events
from constructed controls. CLI discovery remains version-specific.
