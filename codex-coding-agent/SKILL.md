---
name: codex-coding-agent
description: 'Delegate coding tasks specifically to Codex CLI (`codex`) from another host agent or automation harness. Use this only when the user explicitly wants Codex or `codex` to do the work, such as building features, reviewing diffs, refactoring a codebase, continuing a prior Codex session, or running a longer coding task through Codex. Do not use for simple one-line edits you can do directly, for ordinary read-only code inspection that the current agent can answer itself, or when the user did not ask to use Codex.'
---

# Codex Coding Agent

Use the Codex CLI command `codex` for delegated coding work.

This skill is for **external orchestrators** such as Claude Code, Cursor, or similar agents that need to launch Codex as a subordinate coding agent.
It is **not** a self-referential skill for Codex itself.

Treat `codex` as the default launcher, not the only launcher.
If the user explicitly provides a wrapper, alias-like command name, shell function entrypoint, or absolute path for Codex, use that user-declared command instead of hardcoding bare `codex`.

Examples:

```bash
/path/to/bin/codex exec "Your task"
codex-prod exec "Your task"
```

Keep the rest of the invocation pattern the same unless the user's wrapper requires something different.

For exact flags and current behavior, prefer the local CLI help over memory:

```bash
codex --help
codex exec --help
codex review --help
codex resume --help
```

## Execution Modes

Codex supports three practical execution styles that matter for orchestration:

1. Non-interactive execution with `codex exec`
2. Non-interactive repository review with `codex review`
3. Interactive terminal execution with `codex`, `codex resume`, or `codex fork`

Use the right mode for the task instead of treating them as interchangeable.

## Host Harness Expectations

This skill is written for another agent that is launching Codex through a shell, task runner, or automation harness.

That host should choose the execution style deliberately:

- prefer plain non-interactive process execution for `codex exec` and `codex review`
- allocate a PTY only for truly interactive terminal flows such as `codex`, `codex resume`, or `codex fork`
- keep the working directory focused so Codex wakes up in the exact repository it should operate on

Do not default everything to PTY just because Codex also has an interactive terminal mode.
For automation, the non-interactive subcommands are usually the cleaner and more stable integration surface.

### Prefer `codex exec` for automation

Use `codex exec` when you want one-shot execution, script-friendly behavior, or a background task that should run without an interactive terminal session:

```bash
cd /path/to/project
codex exec "Add request retry logic to the API client"
```

`codex exec` is the default choice for orchestration.

If the host automation framework distinguishes plain pipes from PTY/TTY allocation, `codex exec` is the safest default because it is designed for non-interactive use.

Headless runs can take a **long** time.
This is especially true for review-like prompts or repo-wide refactors, where Codex may spend a long time gathering context before it emits the final answer.
If it appears quiet for a while, do **not** assume it is stuck and do **not** kill it just because there is no visible output yet.
Once you start a headless run, trust it to finish by itself and wait for the process to exit cleanly before taking the next action.

### Prefer `codex review` for repo review flows

Use `codex review` when the task is explicitly a code review of a repo state, branch diff, commit, or uncommitted changes:

```bash
cd /path/to/project
codex review --uncommitted "Review the current changes for bugs, regressions, compatibility issues, and hidden blast radius. Treat the supplied changes as primary scope, then inspect only the minimum necessary callers, references, consumers, contracts, compatibility assumptions, and immediate upstream/downstream paths needed to assess impact. Stay review-only."
```

This is usually a better fit than a generic `codex exec` prompt when the job is clearly "review code" rather than "work on code".

If the surrounding harness needs review-specific machine integration features such as `--model`, `--json`, `-o`, `--full-auto`, or `--ephemeral`, prefer `codex exec review` instead of the top-level `codex review` entrypoint:

```bash
cd /path/to/project
codex exec review --base origin/main --json -o /tmp/codex-review.txt "Review this branch for regressions, compatibility issues, and blast radius. Treat the branch diff as primary scope, then inspect the minimum necessary callers, references, consumers, contracts, and immediate upstream/downstream paths needed to assess impact. Stay review-only."
```

Use the simpler top-level `codex review` when you only need a straightforward human-readable review run.

### Use interactive terminal mode when live steering matters

Use interactive mode when you want to watch the session, answer follow-up questions in real time, or continue earlier Codex context:

```bash
cd /path/to/project
codex "Help me debug the flaky sync job"
```

If the host execution harness distinguishes between plain pipes and PTY/TTY sessions, allocate a PTY for interactive `codex`, `codex resume`, and `codex fork` runs.
Those flows are terminal-native and should not be forced into a fake non-interactive pattern unless the harness explicitly supports it.

## Model Selection

Codex supports explicit model selection:

```bash
codex exec --model gpt-5.4 "Your task"
```

If the user explicitly names a model, pass it through with `--model <id>`.

If the user does **not** specify a model, do **not** invent one. Let Codex use the current configured default or profile settings.

If the workflow already relies on a Codex profile, pass that through with `--profile <name>` instead of re-encoding all defaults manually.

## Working Directory and Repo Expectations

Run Codex inside the intended repository or workspace:

```bash
cd /path/to/project
codex exec "Implement the approved feature and summarize the changed files"
```

Why this matters: Codex should wake up inside the intended repository, with the correct files and repo rules in scope.

Codex expects a Git repository by default.
For scratch or throwaway work outside an existing repo, prefer creating a temporary Git repository rather than weakening the repo check automatically:

```bash
SCRATCH="$(mktemp -d)"
cd "$SCRATCH"
git init
codex exec "Prototype a parser and explain the approach"
```

Use `--skip-git-repo-check` only when the user explicitly wants that behavior or when the repo check itself is the only blocker and bypassing it is a conscious choice.

If the task needs access to sibling directories, add them explicitly:

```bash
codex exec --add-dir ../shared-lib "Update the app and shared library together"
```

## Read-Only and Constrained Runs

Codex does **not** expose Cursor-style `--mode plan` or `--mode ask`.

When the user wants analysis, explanation, or planning without edits:

1. Say so explicitly in the prompt.
2. Prefer `--sandbox read-only` for `codex exec` when the task should not modify files.
3. Use `--ephemeral` when you want the run to avoid persisting session state.

For read-only review work, bounded code-reading across callers, references, consumers, contracts, and compatibility assumptions is allowed when needed to assess impact. Restrict mutation, not necessary inspection.

Example:

```bash
cd /path/to/project
codex exec --sandbox read-only --ephemeral "Explain how the caching layer works in this repo. Do not modify files."
```

## Output Capture

When Codex is launched by another agent or harness, choose an output capture mode that matches the caller:

```bash
# Write the final assistant message to a file
codex exec -o /tmp/codex-last.txt "Your task"

# Emit JSONL events for a downstream parser
codex exec --json "Your task"
```

Use plain stdout by default unless the surrounding workflow clearly benefits from:

- `-o <file>` for a stable final-answer artifact
- `--json` for machine-readable event streams

## Quick Start

### One-shot coding task

```bash
cd /path/to/project
codex exec "Add input validation to the signup form"
```

### One-shot coding task with low-friction execution

```bash
cd /path/to/project
codex exec --full-auto "Implement the approved API pagination changes"
```

Use `--full-auto` only when the user or workflow clearly wants low-friction automated execution inside the workspace.

### Interactive debugging

```bash
cd /path/to/project
codex "Investigate why this build script hangs locally"
```

### Repo review

```bash
cd /path/to/project
codex review --base origin/main "Review this branch for bugs, regressions, and risk"
```

## Common Task Patterns

### Building or implementing

```bash
# Default behavior: use current configured model
cd /path/to/project
codex exec "Build the admin export flow described in README-notes.md"

# Explicit model when the user asks for one
codex exec --model gpt-5.4 "Implement the approved API pagination changes"
```

### Reviewing a diff or working tree

Use Codex when the user explicitly wants Codex to perform the review.

```bash
# Review staged, unstaged, and untracked changes
cd /path/to/project
codex review --uncommitted "Review the current changes for bugs, regressions, compatibility issues, and blast radius. Treat the current changes as primary scope, then inspect the minimum necessary callers, references, consumers, contracts, compatibility assumptions, and immediate upstream/downstream paths needed to assess impact. Stay review-only."

# Review against a base branch
codex review --base origin/main "Review this branch diff for regression risk, compatibility issues, and blast radius. Treat the branch diff as primary scope, then inspect the minimum necessary callers, references, consumers, contracts, and immediate upstream/downstream paths needed to assess impact. Stay review-only."

# Review a specific commit
codex review --commit abc1234 "Review this commit for correctness, regression risk, compatibility issues, and blast radius. Treat the commit as primary scope, then inspect the minimum necessary callers, references, consumers, contracts, compatibility assumptions, and immediate upstream/downstream paths needed to assess impact. Stay review-only."
```

If the review target should be isolated, prepare that checkout first, then run Codex inside that isolated review directory.
Do not surprise the user by mutating their main working tree just to conduct a review.

For PR or MR review, prefer an isolated checkout in a temporary directory or other disposable review location when the host workflow allows it.
The point is separation, not any specific Git mechanism.

### Background long task

```bash
cd /path/to/project
nohup codex exec --full-auto -o /tmp/codex-last.txt "Refactor the metrics pipeline, keep behavior intact, and summarize the final diff" > /tmp/codex-agent.log 2>&1 &
```

When a headless background run is in flight, the correct default is still patience.
Do not keep intervening, do not repeatedly check whether it is "still doing something", and do not terminate it early just because it has been running for a long time.
Wait for the run to finish naturally, then inspect the final result.

### Resume or fork previous Codex sessions

If the user wants to continue prior Codex work, use the built-in session commands:

```bash
codex resume --last
codex resume <session-id>
codex exec resume --last "Continue the refactor and finish the remaining cleanup"
codex fork --last
codex fork <session-id> "Try a different approach without altering the original thread"
```

Use these only when resuming or branching existing Codex context is actually useful.

## Scratch and Temporary Work

When another agent wants Codex to solve a one-off task outside an existing repository, the safest pattern is:

1. create a temporary directory
2. initialize a temporary Git repository there
3. run `codex exec` in that directory
4. collect the output
5. clean up afterward if the workflow does not need to persist the artifact

This is usually better than weakening repo expectations globally.

### Image-aware implementation prompts

If the user gives screenshots, mockups, or design captures, attach them explicitly:

```bash
codex exec -i ./mockup.png "Implement this UI in the current project"
```

## Sandbox and Approval Flags

Codex exposes stronger-execution controls:

```bash
codex exec --full-auto ...
codex exec --dangerously-bypass-approvals-and-sandbox ...
codex --sandbox read-only ...
codex --sandbox workspace-write ...
codex --ask-for-approval on-request ...
```

Treat these as **intentional overrides**, not the default happy path.

- Use them only when the user explicitly wants that behavior or the task clearly requires it.
- Do not silently add `--dangerously-bypass-approvals-and-sandbox`.
- Do not silently relax sandboxing or approval behavior just to make a run "easier".

## Rules

1. Use this skill only when the user explicitly wants **Codex** or `codex`.
2. This skill is for an external host agent launching Codex, not for Codex recursively invoking itself.
3. Treat bare `codex` as the default launcher only. If the user specifies a wrapper, alias-style command, or explicit path, use that command.
4. Prefer `codex exec` for automation and `codex review` for repository review tasks.
5. For repository review tasks, keep the diff or range as primary scope while explicitly requiring bounded impact tracing instead of narrow local inspection or uncontrolled repo-wide exploration.
6. When the host harness needs review-specific output capture or explicit model control, prefer `codex exec review` over top-level `codex review`.
7. Use interactive `codex`, `codex resume`, or `codex fork` only when live collaboration or prior session context is actually useful.
8. If the user specifies a model or profile, pass it through. If the user does not, let Codex use the current configured default.
9. For read-only tasks, encode that in the prompt and prefer `--sandbox read-only` where that command supports it.
10. Remember that Codex expects a Git repository by default. For scratch work, prefer a temporary Git repo over automatic repo-check bypass.
11. Do not silently escalate to `--dangerously-bypass-approvals-and-sandbox`.
12. Headless runs, especially reviews and refactors, may take a long time with little or no visible output. This is normal.
13. Do not kill a headless run just because it seems quiet, and do not keep poking it with frequent polling.
14. If the surrounding harness differentiates PTY from plain pipes, allocate PTY for interactive terminal sessions and prefer non-interactive subcommands for automation.
15. Use `-o` or `--json` only when the surrounding workflow genuinely benefits from a stable artifact or machine-readable event stream.
