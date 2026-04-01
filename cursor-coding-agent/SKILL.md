---
name: cursor-coding-agent
description: 'Delegate coding tasks specifically to Cursor CLI (`agent`) via background process. Use this only when the user explicitly wants Cursor CLI or `agent` to do the work, such as building features, reviewing diffs, refactoring a codebase, or running a longer coding task in the background with Cursor. Do not use for simple one-line edits you can do directly, for read-only code inspection without delegation, or when the user did not ask to use Cursor CLI.'
---

# Cursor Coding Agent

Use the Cursor CLI command `agent` for delegated coding work.

This skill is for **Cursor CLI only**. Do not generalize it to Codex, Claude Code, Pi, or other coding agents.

## Execution Modes

Cursor CLI supports two practical execution styles:

1. **Headless mode** with `--print --trust`
2. **Interactive terminal mode** without `--print`

Use the right one for the task instead of treating them as interchangeable.

### Prefer headless mode for automation

Use `--print --trust` when you want one-shot execution, script-friendly output, or a background task that should run without an interactive TTY:

```bash
cd /path/to/project
agent --print --trust "Add request retry logic to the API client"
```

`--print` keeps the run non-interactive and works well for orchestration.
`--trust` avoids workspace trust prompts in headless mode.

### Use PTY when interaction is the point

Use interactive terminal mode when you want to watch a live session, steer it in real time, or use Cursor like a terminal-first coding assistant:

```bash
cd /path/to/project
agent "Help me debug the flaky sync job"
```

## Model Selection

Cursor CLI supports explicit model selection:

```bash
agent --model gpt-5.4-medium --print --trust "Your task"
```

If the user explicitly names a model, pass it through with `--model <id>`.

If the user does **not** specify a model, do **not** invent one. Let Cursor CLI use the model currently selected in that workspace/account configuration.

To inspect available models:

```bash
agent models
```

## Read-Only Modes

Cursor CLI also supports read-only execution modes. Use them when the user wants planning or explanation rather than file edits.

### Plan mode

Use `--mode plan` for analysis and implementation planning without edits:

```bash
cd /path/to/project
agent --print --trust --mode plan "Analyze the migration risk and propose a rollout plan"
```

### Ask mode

Use `--mode ask` for Q&A style help, explanations, or investigation without changes:

```bash
cd /path/to/project
agent --print --trust --mode ask "Explain how the caching layer works in this repo"
```

Do not use `plan` or `ask` for tasks that are supposed to modify code.

## Output Formats

When using `--print`, choose an output format that matches the caller:

```bash
# Human-readable
agent --print --trust --output-format text "Your task"

# Machine-readable
agent --print --trust --output-format json "Your task"

# Streaming structured events
agent --print --trust --output-format stream-json "Your task"
```

Use `text` by default unless a script or downstream parser clearly benefits from `json` or `stream-json`.

## Quick Start

### One-shot coding task

```bash
cd /path/to/project
agent --print --trust "Add input validation to the signup form"
```

### One-shot planning task

```bash
cd /path/to/project
agent --print --trust --mode plan "Compare two approaches for splitting the monolith service"
```

### Interactive debugging

```bash
cd /path/to/project
agent "Investigate why this build script hangs locally"
```

## Working Directory

Run Cursor CLI inside the intended repository or workspace:

```bash
cd /path/to/project
agent --print --trust "Implement the approved feature and summarize the changed files"
```

Why this matters: Cursor should wake up inside the intended repository, with the correct local files and repo rules in scope.

## Common Task Patterns

### Building or implementing

```bash
# Default behavior: use current selected model
cd /path/to/project
agent --print --trust "Build the admin export flow described in README-notes.md"

# Explicit model when the user asks for one
agent --model gpt-5.4-medium --print --trust "Implement the approved API pagination changes"
```

### Reviewing a diff or PR checkout

Use Cursor CLI when the user explicitly wants Cursor to perform the review.

```bash
cd /path/to/project
agent --print --trust --mode ask "Review the current git diff for bugs, regressions, and missing validation"
```

If the review target should be isolated, prepare that checkout first, then run `agent` inside that review directory.

### Background long task

```bash
cd /path/to/project
nohup agent --print --trust "Refactor the metrics pipeline, keep behavior intact, and summarize the final diff" > /tmp/cursor-agent.log 2>&1 &
```

### Resume previous Cursor sessions

If the user wants to continue prior Cursor work, use the built-in session commands:

```bash
agent ls
agent resume
agent --resume <chatId>
agent --continue
```

Use these only when resuming existing Cursor context is actually useful.

## Approval and Sandbox Flags

Cursor CLI exposes stronger-execution flags:

```bash
agent --force ...
agent --yolo ...
agent --sandbox enabled ...
agent --sandbox disabled ...
agent --approve-mcps ...
```

Treat these as **intentional overrides**, not the default happy path.

- Use them only when the user explicitly wants that behavior or the task clearly requires it.
- Do not silently add `--force` or `--yolo`.
- Do not change sandbox behavior unless there is a concrete reason.

## Rules

1. Use this skill only when the user explicitly wants **Cursor CLI** or `agent`.
2. Prefer `--print --trust` for automation, one-shot runs, and non-interactive execution.
3. Use interactive terminal mode only when a live session is actually useful.
4. If the user specifies a model, pass it through with `--model <id>`.
5. If the user does not specify a model, let Cursor CLI use the **current selected model**.
6. Use `--mode plan` and `--mode ask` only for read-only planning or explanation tasks.
7. Do not silently escalate to `--force` or `--yolo`.
8. If you run Cursor CLI as a long task in the background, choose a host-specific monitoring approach outside this skill.
