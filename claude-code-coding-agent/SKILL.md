---
name: claude-code-coding-agent
description: >-
  Claude Code CLI operating guide for external host agents. Use only when the
  user explicitly asks to run Claude Code CLI (`claude`) as the external coding
  executor, or when the current orchestration/review workflow explicitly selects
  Claude Code by name. Do not use for generic coding tasks, built-in subagents,
  ordinary Claude chat, or unspecified delegation.
---

# Claude Code Coding Agent

Use Claude Code CLI (`claude`) as an external coding executor after Claude Code has been explicitly selected.

This skill is for external host agents or automation harnesses launching Claude Code.
It is not a generic coding-agent guide, and it should not turn generic "use an agent/subagent" wording into a Claude Code launch.

## Launcher

Treat `claude` as the default launcher, not the only launcher.
If the user provides a wrapper, alias-style command name, shell function entrypoint, or absolute path for Claude Code, use that command and keep the rest of the invocation pattern unless the wrapper requires otherwise.

```bash
/path/to/bin/claude --print "Your task"
claude-prod --print "Your task"
```

Prefer local CLI help over memory for exact flags and current behavior:

```bash
claude --help
claude agents --help
claude auth --help
```

## Execution Modes

Choose the mode deliberately:

1. `claude --print` for non-interactive implementation, investigation, and automation.
2. `claude --print` plus a review prompt contract for review-only repository review.
3. `claude` without `--print` for interactive terminal sessions.

### Automation

Use `--print` when the task should run once, return a final answer, or run under a script without an interactive terminal:

```bash
cd /path/to/project
claude --print "Add request retry logic to the API client"
```

For unattended implementation where the user or workflow has already allowed low-friction editing, add `--permission-mode bypassPermissions` explicitly:

```bash
cd /path/to/project
claude --permission-mode bypassPermissions --print "Implement the approved API pagination changes"
```

Do not treat `--permission-mode bypassPermissions` as implicit. It is a deliberate host workflow choice, separate from the stronger `--dangerously-skip-permissions` flag.

### Review

Use Claude Code for review only when Claude Code has been explicitly selected. Keep the run review-only and findings-first:

```bash
cd /path/to/project
claude --print "$REVIEW_PROMPT"
```

In these examples, `$REVIEW_PROMPT` is a placeholder for the prompt text below; pass that text using the quoting or argument style your host harness expects.

Define `REVIEW_PROMPT` with this contract, adapted to the selected target:

```text
Review the current git diff for correctness, regression risk, compatibility issues, and hidden blast radius. Treat the supplied changes as primary scope, then inspect only the minimum necessary callers, references, consumers, contracts, compatibility assumptions, and immediate upstream/downstream paths needed to assess impact. Stay review-only; do not modify files or start build/test work. Lead with actionable findings, or say there are no clear findings.
```

If the review target should be isolated, prepare that checkout first and run Claude Code inside the isolated review directory.

### Interactive Terminal

Use interactive mode when live collaboration, follow-up answers, or hands-on steering matters:

```bash
cd /path/to/project
claude "Help me debug the flaky sync job"
```

Use built-in session commands only when continuing existing Claude Code context is useful:

```bash
claude --continue
claude --resume
claude --resume <session-id>
claude --resume <session-id> --fork-session
```

## Host Harness

Run Claude Code from the intended repository or workspace so repo rules, files, and Git state are in scope:

```bash
cd /path/to/project
claude --print "Implement the approved feature and summarize the changed files"
```

Headless Claude Code runs can be quiet for a long time, especially reviews and repo-wide refactors.
After starting a headless run, wait for the process to exit cleanly before taking the next action; do not kill or repeatedly poll it just because no output has appeared yet.

If the task needs sibling directories, add them explicitly:

```bash
claude --add-dir ../shared-lib --print "Update the app and shared library together"
```

## Model and Effort Selection

Pass through model, fallback model, and effort choices only when the user or surrounding workflow specifies them:

```bash
claude --model sonnet --print "Your task"
claude --print --fallback-model sonnet "Your task"
claude --effort high --print "Investigate the regression and patch it"
```

If no model or effort is specified, let Claude Code use its configured default.

## Read-Only and Output Formats

Claude Code does not expose Cursor-style `--mode ask` or `--mode plan`.
For analysis, explanation, or planning without edits, say so in the prompt and tighten tools or permissions when appropriate:

```bash
cd /path/to/project
claude --print --allowed-tools Read,Grep,Glob "Explain how the caching layer works in this repo. Do not modify files."
```

Use text output by default. Choose structured output only when the caller benefits from it:

```bash
claude --print --output-format text "Your task"
claude --print --output-format json "Your task"
claude --print --output-format stream-json "Your task"
```

## Common Patterns

### Implementation

```bash
cd /path/to/project
claude --print "Build the admin export flow described in README-notes.md"
```

Add `--permission-mode bypassPermissions` only when unattended write access is an explicit choice:

```bash
claude --permission-mode bypassPermissions --print "Implement the approved API pagination changes"
```

### Review

```bash
cd /path/to/project
claude --print "$REVIEW_PROMPT"
```

### Background Run

```bash
cd /path/to/project
nohup claude --permission-mode bypassPermissions --print "Refactor the metrics pipeline, keep behavior intact, and summarize the final diff" > /tmp/claude-code-agent.log 2>&1 &
```

Apply the headless patience rule after starting the background process: wait for completion, then inspect the final result.

### Named Agents

Use Claude Code named or injected agents only when the user explicitly wants that persona or the workflow already defines it:

```bash
claude --agent reviewer --print "$REVIEW_PROMPT"
```

For ad hoc injected agents, keep the injected prompt bounded to the selected role and do not forward unrelated orchestration instructions.

## Safety Rules

1. Use this skill only when the user, wrapper, or active orchestration explicitly selects Claude Code CLI.
2. Do not use it for generic coding tasks, built-in subagents, ordinary Claude chat, or unspecified delegation.
3. Treat bare `claude` as the default launcher only; preserve user-provided wrappers, aliases, shell entrypoints, and explicit paths.
4. Prefer `--print` for automation, one-shot runs, and non-interactive execution.
5. Use interactive terminal mode only when live collaboration or prior Claude Code context is useful.
6. Pass through explicit model, fallback model, and effort choices; do not invent them.
7. For read-only tasks, encode the no-edit constraint in the prompt and tighten permissions or tool access where appropriate.
8. For review, treat the diff/range as primary scope, require bounded impact tracing, stay review-only, and lead with actionable findings or "no clear findings".
9. Do not silently add `--permission-mode bypassPermissions`; use it only when unattended editing is an explicit workflow choice.
10. Do not silently escalate to `--dangerously-skip-permissions`.
11. Do not silently create worktrees or tmux sessions.
12. Use `--bare` only when a stripped-down run with fewer ambient integrations is intentional.
13. Headless runs may be quiet for a long time; wait for clean exit instead of killing or repeatedly polling them.
