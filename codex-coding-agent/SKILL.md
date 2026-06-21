---
name: codex-coding-agent
description: >-
  Codex CLI operating guide for external host agents. Use only when the user
  explicitly asks to run local Codex CLI (`codex`) as the external coding
  executor, or when the current orchestration/review workflow explicitly selects
  Codex CLI by name. Do not use for built-in subagents, ordinary Codex chat,
  generic agent delegation, or unspecified coding tasks.
---

# Codex Coding Agent

Use Codex CLI (`codex`) as an external coding executor after Codex has been explicitly selected.

This skill is for external host agents such as Claude Code, Cursor, or automation harnesses that need to launch Codex as a subordinate coding agent.
It is not a self-referential skill for Codex itself, and it should not turn generic "use an agent/subagent" wording into a Codex launch.

## Launcher

Treat `codex` as the default launcher, not the only launcher.
If the user provides a wrapper, alias-style command name, shell function entrypoint, or absolute path for Codex, use that command and keep the rest of the invocation pattern unless the wrapper requires otherwise.

```bash
/path/to/bin/codex exec "Your task"
codex-prod exec "Your task"
```

Prefer local CLI help over memory for exact flags and current behavior:

```bash
codex --help
codex exec --help
codex review --help
codex resume --help
```

## Execution Modes

Choose the mode deliberately:

1. `codex exec` for non-interactive implementation, investigation, and automation.
2. `codex review` for repository review of a diff, branch, commit, or working tree.
3. `codex`, `codex resume`, or `codex fork` for interactive terminal sessions.

### Automation

Use `codex exec` when the task should run once, return a final answer, or run under a script without an interactive terminal:

```bash
cd /path/to/project
codex exec "Add request retry logic to the API client"
```

Allocate a PTY only for interactive terminal flows. For `codex exec` and `codex review`, prefer plain non-interactive process execution.

### Review

Use `codex review` when the task is explicitly code review rather than code modification:

```bash
cd /path/to/project
codex review --uncommitted "$REVIEW_PROMPT"
```

In these examples, `$REVIEW_PROMPT` is a placeholder for the prompt text below; pass that text using the quoting or argument style your host harness expects.

Use `codex exec review` instead of top-level `codex review` when the host workflow needs review-specific automation features such as `--model`, `--json`, `-o`, `--full-auto`, or `--ephemeral`:

```bash
cd /path/to/project
codex exec review --base origin/main --json -o /tmp/codex-review.txt "$REVIEW_PROMPT"
```

Define `REVIEW_PROMPT` with this contract, adapted to the selected target:

```text
Review the current changes for bugs, regressions, compatibility issues, and hidden blast radius. Treat the supplied changes as primary scope, then inspect only the minimum necessary callers, references, consumers, contracts, compatibility assumptions, and immediate upstream/downstream paths needed to assess impact. Stay review-only; do not edit files or start build/test work. Lead with actionable findings, or say there are no clear findings.
```

If the review target should be isolated, prepare that checkout first and run Codex inside the isolated review directory. Do not mutate the user's main working tree just to conduct a review.

### Interactive Terminal

Use interactive mode when live steering, follow-up answers, or previous session context matters:

```bash
cd /path/to/project
codex "Help me debug the flaky sync job"
```

Use built-in session commands only when continuing or branching existing Codex context is actually useful:

```bash
codex resume --last
codex resume <session-id>
codex exec resume --last "Continue the refactor and finish the remaining cleanup"
codex fork --last
codex fork <session-id> "Try a different approach without altering the original thread"
```

## Host Harness

Run Codex from the intended repository or workspace so repo rules, files, and Git state are in scope:

```bash
cd /path/to/project
codex exec "Implement the approved feature and summarize the changed files"
```

Headless Codex runs can be quiet for a long time, especially reviews and repo-wide refactors.
After starting a headless run, wait for the process to exit cleanly before taking the next action; do not kill or repeatedly poll it just because no output has appeared yet.

Codex expects a Git repository by default. For scratch work, prefer a temporary Git repository over bypassing the repo check:

```bash
SCRATCH="$(mktemp -d)"
cd "$SCRATCH"
git init
codex exec "Prototype a parser and explain the approach"
```

Use `--skip-git-repo-check` only when the user explicitly wants that behavior or when the repo check itself is the only blocker and bypassing it is a conscious choice.

If the task needs sibling directories, add them explicitly:

```bash
codex exec --add-dir ../shared-lib "Update the app and shared library together"
```

## Model and Profile Selection

Pass through model and profile choices only when the user or surrounding workflow specifies them:

```bash
codex exec --model gpt-5.4 "Your task"
codex exec --profile production "Your task"
```

If no model or profile is specified, let Codex use its configured default.

## Read-Only and Output Capture

Codex does not expose Cursor-style `--mode plan` or `--mode ask`.
For analysis, explanation, or planning without edits, say so in the prompt and prefer read-only sandboxing when supported:

```bash
cd /path/to/project
codex exec --sandbox read-only --ephemeral "Explain how the caching layer works in this repo. Do not modify files."
```

Use plain stdout by default. Add output capture only when the caller benefits from it:

```bash
codex exec -o /tmp/codex-last.txt "Your task"
codex exec --json "Your task"
```

## Common Patterns

### Implementation

```bash
cd /path/to/project
codex exec "Build the admin export flow described in README-notes.md"
```

Use `--full-auto` only when the user or workflow clearly wants low-friction automated execution inside the workspace:

```bash
codex exec --full-auto "Implement the approved API pagination changes"
```

### Review Targets

```bash
cd /path/to/project
codex review --uncommitted "$REVIEW_PROMPT"
codex review --base origin/main "$REVIEW_PROMPT"
codex review --commit abc1234 "$REVIEW_PROMPT"
```

### Background Run

```bash
cd /path/to/project
nohup codex exec --full-auto -o /tmp/codex-last.txt "Refactor the metrics pipeline, keep behavior intact, and summarize the final diff" > /tmp/codex-agent.log 2>&1 &
```

Apply the headless patience rule after starting the background process: wait for completion, then inspect the final result.

### Image-Aware Work

If the user gives screenshots, mockups, or design captures, attach them explicitly:

```bash
codex exec -i ./mockup.png "Implement this UI in the current project"
```

## Safety Rules

1. Use this skill only when the user, wrapper, or active orchestration explicitly selects Codex CLI.
2. Do not use it for built-in subagents, ordinary Codex chat, generic agent delegation, or unspecified coding tasks.
3. Treat bare `codex` as the default launcher only; preserve user-provided wrappers, aliases, shell entrypoints, and explicit paths.
4. Prefer `codex exec` for automation and `codex review` for review-only repository review.
5. For review, treat the diff/range as primary scope, require bounded impact tracing, stay review-only, and lead with actionable findings or "no clear findings".
6. Use `codex exec review` when review needs machine-readable output, output files, explicit model control, or other `exec`-only harness features.
7. Use interactive `codex`, `codex resume`, or `codex fork` only when live collaboration or prior Codex context is useful.
8. Pass through explicit model/profile choices; do not invent them.
9. For read-only tasks, encode the no-edit constraint in the prompt and prefer `--sandbox read-only` where supported.
10. For scratch work, prefer a temporary Git repo over automatic repo-check bypass.
11. Do not silently add `--dangerously-bypass-approvals-and-sandbox`, relax sandboxing, or weaken approval behavior.
12. Headless runs may be quiet for a long time; wait for clean exit instead of killing or repeatedly polling them.
