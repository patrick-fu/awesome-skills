---
name: cursor-coding-agent
description: >-
  Cursor CLI operating guide for external host agents using the Cursor CLI
  command (`agent`). Use only when the user explicitly asks to run Cursor CLI as
  the external coding executor, or when the current orchestration/review
  workflow explicitly selects Cursor CLI by name. Do not trigger on generic
  agent, subagent, or unspecified delegation wording.
---

# Cursor Coding Agent

Use Cursor CLI (`agent`) as an external coding executor after Cursor CLI has been explicitly selected.

This skill is for Cursor CLI only.
Because `agent` is also a generic word, treat it as the Cursor CLI launcher only when the user names Cursor CLI, provides a Cursor-specific launcher, or the active orchestration explicitly selects Cursor CLI.

## Launcher

Treat `agent` as the default Cursor CLI launcher, not as a generic agent label.
If the user provides a wrapper, alias-style command name, shell function entrypoint, or absolute path for Cursor CLI, use that command and keep the rest of the invocation pattern unless the wrapper requires otherwise.

```bash
/path/to/bin/agent --print --trust "Your task"
cursor-agent --print --trust "Your task"
```

Prefer local CLI help over memory for exact flags and current behavior:

```bash
agent --help
agent models
```

## Execution Modes

Choose the mode deliberately:

1. `agent --print --trust` for non-interactive implementation, investigation, and automation.
2. `agent --print --trust --mode ask` for review-only repository review.
3. `agent` without `--print` for interactive terminal sessions.

### Automation

Use `--print --trust` when the task should run once, return a final answer, or run under a script without an interactive terminal:

```bash
cd /path/to/project
agent --print --trust "Add request retry logic to the API client"
```

`--print` keeps the run non-interactive. `--trust` avoids workspace trust prompts in headless mode; it is not permission to add stronger execution flags.

### Review

Use Cursor CLI for review only when Cursor CLI has been explicitly selected. Prefer `--mode ask` so the review stays read-only:

```bash
cd /path/to/project
agent --print --trust --mode ask "$REVIEW_PROMPT"
```

In these examples, `$REVIEW_PROMPT` is a placeholder for the prompt text below; pass that text using the quoting or argument style your host harness expects.

Define `REVIEW_PROMPT` with this contract, adapted to the selected target:

```text
Review the current git diff for correctness, regression risk, compatibility issues, and hidden blast radius. Treat the supplied changes as primary scope, then inspect only the minimum necessary callers, references, consumers, contracts, compatibility assumptions, and immediate upstream/downstream paths needed to assess impact. Stay review-only; do not edit files or start build/test work. Lead with actionable findings, or say there are no clear findings.
```

If the review target should be isolated, prepare that checkout first and run Cursor CLI inside the isolated review directory.

### Interactive Terminal

Use interactive mode when live collaboration, follow-up answers, or hands-on steering matters:

```bash
cd /path/to/project
agent "Help me debug the flaky sync job"
```

Use built-in session commands only when continuing existing Cursor context is useful:

```bash
agent ls
agent resume
agent --resume <chatId>
agent --continue
```

## Host Harness

Run Cursor CLI from the intended repository or workspace so repo rules, files, and Git state are in scope:

```bash
cd /path/to/project
agent --print --trust "Implement the approved feature and summarize the changed files"
```

Headless Cursor CLI runs can be quiet for a long time, especially reviews and repo-wide refactors.
For short foreground runs, wait for clean exit. For long or background runs, check current output-capture flags with `agent --help`, then capture stdout and stderr in a small run directory so the caller can inspect progress without interrupting the process.

## Model Selection

Pass through model choices only when the user or surrounding workflow specifies them:

```bash
agent --model gpt-5.4-medium --print --trust "Your task"
```

If no model is specified, let Cursor CLI use the model currently selected in that workspace or account configuration.

Inspect available models when needed:

```bash
agent models
```

## Read-Only and Output Formats

Use Cursor read-only modes when the user wants planning, explanation, or review instead of file edits:

```bash
cd /path/to/project
agent --print --trust --mode plan "Analyze the migration risk and propose a rollout plan"
agent --print --trust --mode ask "Explain how the caching layer works in this repo"
```

Do not use `--mode plan` or `--mode ask` for tasks that are supposed to modify code.

Use text output by default. Choose structured output only when the caller benefits from it.
When the caller needs progress or machine-readable output, treat local help as the flag reference:

```bash
agent --help | rg -n "output-format|stream|partial|print|trust"
```

For long headless runs, prefer a streaming output mode if current help exposes one.

## Common Patterns

### Implementation

```bash
cd /path/to/project
agent --print --trust "Build the admin export flow described in README-notes.md"
```

### Planning or Explanation

```bash
cd /path/to/project
agent --print --trust --mode plan "Compare two approaches for splitting the monolith service"
agent --print --trust --mode ask "Explain why the sync job hangs"
```

### Review

```bash
cd /path/to/project
agent --print --trust --mode ask "$REVIEW_PROMPT"
```

### Background Run

```bash
cd /path/to/project
RUN_DIR="${TMPDIR:-/tmp}/coding-agent-runs/cursor/$(date -u +%Y%m%dT%H%M%SZ)-metrics-refactor"
mkdir -p "$RUN_DIR"
# Add verified streaming/output flags from `agent --help` before the prompt when progress output is needed.
nohup agent --print --trust "Refactor the metrics pipeline, keep behavior intact, and summarize the final diff" > "$RUN_DIR/stdout.log" 2> "$RUN_DIR/stderr.log" &
echo $! > "$RUN_DIR/pid"
```

After starting the background process, monitor it with `tail -f "$RUN_DIR/stdout.log" "$RUN_DIR/stderr.log"` when progress matters. Wait for completion, then inspect the captured logs.

## Safety Rules

1. Use this skill only when the user, wrapper, or active orchestration explicitly selects Cursor CLI.
2. Do not trigger it from generic `agent`, subagent, delegation, or unspecified coding-task wording.
3. Treat bare `agent` as the default Cursor CLI launcher only; preserve user-provided wrappers, aliases, shell entrypoints, and explicit paths.
4. Prefer `--print --trust` for automation, one-shot runs, and non-interactive execution.
5. Use interactive terminal mode only when live collaboration or prior Cursor context is useful.
6. Pass through explicit model choices; do not invent them.
7. Use `--mode plan` and `--mode ask` only for read-only planning, explanation, or review.
8. For review, treat the diff/range as primary scope, require bounded impact tracing, stay review-only, and lead with actionable findings or "no clear findings".
9. Do not silently add `--force`, `--yolo`, `--sandbox disabled`, or `--approve-mcps`.
10. Do not change sandbox behavior unless the user explicitly wants that behavior or the task clearly requires it.
11. Headless runs may be quiet for a long time; wait for clean exit instead of killing or repeatedly polling them.
