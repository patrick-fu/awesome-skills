---
name: claude-code-coding-agent
description: 'Delegate coding tasks specifically to Claude Code CLI (`claude`) via background process or headless print mode. Use this only when the user explicitly wants Claude Code or `claude`, such as building features, reviewing diffs, refactoring a codebase, or running a longer coding task in the background with Claude Code. Do not use for simple one-line edits you can do directly, for read-only code inspection without delegation, or when the user did not ask to use Claude Code.'
---

# Claude Code Coding Agent

Use the Claude Code CLI command `claude` for delegated coding work.

This skill is for **Claude Code only**. Do not generalize it to Cursor, Codex, Pi, or other coding agents.

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
claude --permission-mode bypassPermissions --print "Review the current git diff for bugs, regressions, and missing validation"
```

If the review target should be isolated, prepare that checkout first, then run `claude` inside that review directory.

### Background long task

```bash
cd /path/to/project
nohup claude --permission-mode bypassPermissions --print "Refactor the metrics pipeline, keep behavior intact, and summarize the final diff" > /tmp/claude-code-agent.log 2>&1 &
```

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
claude --agent reviewer --print "Review the current diff"

claude --agents '{"reviewer":{"description":"Reviews code","prompt":"You are a strict code reviewer."}}' \
  --agent reviewer \
  --print \
  "Review the current diff"
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
2. Prefer `--print` for automation, one-shot runs, and non-interactive execution.
3. Use interactive terminal mode only when a live session is actually useful.
4. If the user specifies a model, pass it through with `--model <id>`.
5. If the user does not specify a model, let Claude Code use the current configured default.
6. For read-only tasks, encode that in the prompt and tighten permissions or tool access as needed.
7. Do not silently escalate to `--dangerously-skip-permissions`.
8. Do not silently create worktrees or tmux sessions.
9. If you run Claude Code as a long task in the background, choose a host-specific monitoring approach outside this skill.
