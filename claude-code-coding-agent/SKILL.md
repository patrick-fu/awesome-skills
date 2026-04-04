---
name: claude-code-coding-agent
description: 'Delegate coding tasks specifically to Claude Code CLI (`claude`) via background process or headless print mode. Use this only when the user explicitly wants Claude Code or `claude`, such as building features, reviewing diffs, refactoring a codebase, or running a longer coding task in the background with Claude Code. Do not use for simple one-line edits you can do directly, for read-only code inspection without delegation, or when the user did not ask to use Claude Code.'
---

# Claude Code Coding Agent

Use the Claude Code CLI command `claude` for delegated coding work.

This skill is for **Claude Code only**. Do not generalize it to Cursor, Codex, Pi, or other coding agents.

Treat `claude` as the **default launcher**, not the only launcher.
If the user explicitly provides a wrapper, alias-like command name, shell function entrypoint, or absolute path for Claude Code, use that user-declared command instead of hardcoding bare `claude`.

Examples:

```bash
/path/to/bin/claude --print "Your task"
claude-xxx-yyy --print "Your task"
```

Keep the rest of the invocation pattern the same unless the user's wrapper requires something different.

For exact flags and current behavior, prefer the local CLI help over memory:

```bash
claude --help
claude agents --help
claude auth --help
```

## Execution Modes

Claude Code supports two practical execution styles:

1. **Headless mode** with `--print`
2. **Interactive terminal mode** without `--print`

Use the right one for the task instead of treating them as interchangeable.

### Prefer headless mode for automation

Use `--print` when you want one-shot execution, script-friendly output, or a background task that should run without an interactive TTY:

```bash
cd /path/to/project
claude --permission-mode bypassPermissions --print "Add request retry logic to the API client"
```

`--print` keeps the run non-interactive and is the default choice for orchestration.
Apply the same rule when the launcher is a wrapper, for example `claude-xxx-yyy --print ...`.

Headless runs can take a **long** time.
This is especially true for review tasks, where Claude Code may spend a long time reading context before it prints anything useful or exits.
If it appears quiet for a while, do **not** assume it is stuck and do **not** kill it just because there is no visible output yet.
Once you start a headless run, trust it to finish by itself and wait for the process to exit cleanly before taking the next action.
Do not babysit it with frequent checks or impatient polling in the middle.

### Use interactive terminal mode when live collaboration matters

Use interactive mode when you want to watch the session, answer follow-up questions in real time, or steer the agent while it works:

```bash
cd /path/to/project
claude "Help me debug the flaky sync job"
```

## Model Selection

Claude Code supports explicit model selection:

```bash
claude --model sonnet --permission-mode bypassPermissions --print "Your task"
```

If the user explicitly names a model, pass it through with `--model <id>`.

If the user does **not** specify a model, do **not** invent one. Let Claude Code use the current configured default.

If the user wants overload fallback in headless mode, Claude Code also supports:

```bash
claude --print --fallback-model sonnet "Your task"
```

## Effort Control

Claude Code supports explicit effort selection:

```bash
claude --effort high --permission-mode bypassPermissions --print "Investigate the regression and patch it"
```

Use `--effort <low|medium|high|max>` only when the user asks for a specific effort level or when the orchestration clearly benefits from it.

## Read-Only and Constrained Runs

Claude Code does **not** expose Cursor-style `--mode ask` or `--mode plan`.

When the user wants analysis, explanation, or planning without edits:

1. Say so explicitly in the prompt.
2. Tighten permissions with `--permission-mode` when appropriate.
3. Restrict tools when needed with `--allowed-tools`, `--disallowed-tools`, or `--tools`.

For read-only review work, bounded code-reading across callers, references, consumers, and contracts is allowed when needed to assess impact. Restrict file modification, not necessary inspection.

Example:

```bash
cd /path/to/project
claude --print --allowed-tools Read,Grep,Glob "Explain how the caching layer works in this repo. Do not modify files."
```

## Output Formats

When using `--print`, choose an output format that matches the caller:

```bash
# Human-readable
claude --print --output-format text "Your task"

# Machine-readable
claude --print --output-format json "Your task"

# Streaming structured events
claude --print --output-format stream-json "Your task"
```

Use `text` by default unless a script or downstream parser clearly benefits from `json` or `stream-json`.

## Quick Start

### One-shot coding task

```bash
cd /path/to/project
claude --permission-mode bypassPermissions --print "Add input validation to the signup form"
```

### Interactive debugging

```bash
cd /path/to/project
claude "Investigate why this build script hangs locally"
```

### Structured machine-readable run

```bash
cd /path/to/project
claude --permission-mode bypassPermissions --print --output-format json "Summarize the changed files and their purpose"
```

## Working Directory

Run Claude Code inside the intended repository or workspace:

```bash
cd /path/to/project
claude --permission-mode bypassPermissions --print "Implement the approved feature and summarize the changed files"
```

Why this matters: Claude Code should wake up inside the intended repository, with the correct files and repo rules in scope.

If the user gave a custom launcher, run that launcher in the intended repository instead of replacing it with bare `claude`.

If the task needs access to sibling directories, add them explicitly:

```bash
claude --add-dir ../shared-lib --permission-mode bypassPermissions --print "Update the app and shared library together"
```

## Common Task Patterns

### Building or implementing

```bash
# Default behavior: use current configured model
cd /path/to/project
claude --permission-mode bypassPermissions --print "Build the admin export flow described in README-notes.md"

# Explicit model when the user asks for one
claude --model sonnet --permission-mode bypassPermissions --print "Implement the approved API pagination changes"
```

### Reviewing a diff or PR checkout

Use Claude Code when the user explicitly wants Claude Code to perform the review.

```bash
cd /path/to/project
claude --permission-mode bypassPermissions --print "Review the current git diff for correctness, regression risk, compatibility issues, and blast radius. Treat the diff as primary scope, then inspect the minimum necessary callers, references, consumers, contracts, compatibility assumptions, and immediate upstream/downstream paths needed to assess impact. Stay review-only; do not modify files or start build/test work."
```

If the review target should be isolated, prepare that checkout first, then run `claude` inside that review directory.

### Background long task

```bash
cd /path/to/project
nohup claude --permission-mode bypassPermissions --print "Refactor the metrics pipeline, keep behavior intact, and summarize the final diff" > /tmp/claude-code-agent.log 2>&1 &
```

When a headless background run is in flight, the correct default is still patience.
Do not keep intervening, do not repeatedly check whether it is "still doing something", and do not terminate it early just because it has been running for a long time.
Wait for the run to finish naturally, then inspect the final result.

### Resume previous Claude Code sessions

If the user wants to continue prior Claude Code work, use the built-in session commands:

```bash
claude --continue
claude --resume
claude --resume <session-id>
claude --resume <session-id> --fork-session
```

Use these only when resuming existing Claude Code context is actually useful.

### Use named or custom agents

Claude Code can target a configured agent or inject custom agents for the current run:

```bash
claude --agent reviewer --print "Review the current diff as primary scope and inspect the minimum necessary impact chain around touched symbols, callers, references, consumers, contracts, and nearby integration seams."

claude --agents '{"reviewer":{"description":"Reviews code","prompt":"You are a strict code reviewer who treats the supplied diff as primary scope and follows bounded impact traces through relevant callers, references, consumers, contracts, and immediate upstream/downstream behavior without editing files."}}' \
  --agent reviewer \
  --print \
  "Review the current diff as primary scope and inspect the minimum necessary impact chain around touched symbols, callers, references, consumers, contracts, and nearby integration seams."
```

Use these only when the user explicitly wants a specific sub-agent persona or the workflow already defines one.

## Permissions, Tools, and Isolation

Claude Code exposes stronger-execution and environment-shaping flags:

```bash
claude --permission-mode bypassPermissions ...
claude --dangerously-skip-permissions ...
claude --allowed-tools Read,Grep,Glob ...
claude --disallowed-tools Bash ...
claude --tools Read,Edit,Bash ...
claude --mcp-config /path/to/mcp.json ...
claude --bare ...
claude --worktree review-branch ...
claude --tmux ...
```

Treat these as **intentional overrides**, not the default path.

- Use them only when the user explicitly wants that behavior or the task clearly requires it.
- Do not silently escalate to `--dangerously-skip-permissions`.
- Do not silently create worktrees or tmux sessions.
- Use `--bare` only when you intentionally want a stripped-down run with fewer ambient integrations.

## Rules

1. Use this skill only when the user explicitly wants **Claude Code** or `claude`.
2. Treat bare `claude` as the default launcher only. If the user specifies a wrapper, alias-style command, or explicit path, use that command.
3. Prefer `--print` for automation, one-shot runs, and non-interactive execution.
4. Use interactive terminal mode only when a live session is actually useful.
5. If the user specifies a model, pass it through with `--model <id>`.
6. If the user does not specify a model, let Claude Code use the current configured default.
7. For read-only tasks, encode that in the prompt and tighten permissions or tool access as needed.
8. For code review tasks, keep the diff or range as primary scope while explicitly requiring bounded impact tracing rather than narrow local inspection or repo-wide wandering.
9. Do not silently escalate to `--dangerously-skip-permissions`.
10. Do not silently create worktrees or tmux sessions.
11. Headless runs, especially reviews, may take a long time with little or no visible output. This is normal.
12. Do not kill a headless run just because it seems quiet, and do not keep poking it with frequent polling.
13. After starting a headless run, wait for it to exit cleanly before taking the next action.
14. If you run Claude Code as a long task in the background, choose a host-specific monitoring approach outside this skill.
