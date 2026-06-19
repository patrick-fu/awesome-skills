# Awesome Skills

**[中文说明](README.zh-CN.md)**

This repository contains a small set of reusable agent skills extracted from a larger private workspace and published as a standalone public collection.

## Included Skills

### `aero-mint-glass-html-design`

Use this skill when a frontend surface should follow the Aero Mint Glass visual style: airy mint-cyan light, translucent white glass panels, soft rounded geometry, restrained shadows, clean typography, soft 3D focal imagery, and quiet motion.

### `brainstorm`

Use this skill when the right next step is conversation rather than execution. It pushes the assistant to ask clarifying questions first, uncover hidden assumptions, and guide the user toward a clearer problem statement before proposing solutions.

### `claude-code-coding-agent`

Use this skill when the user explicitly wants Claude Code CLI to do delegated coding work. It covers headless `--print` runs, interactive sessions, model and effort pass-through, constrained read-only runs, and long-running background execution patterns.

### `codex-coding-agent`

Use this skill when the user explicitly wants Codex CLI to do delegated coding work through another host agent or automation harness. It covers `codex exec` for non-interactive execution, `codex review` for review flows, interactive resume and fork flows, Git repo expectations, and safe handling of sandbox and approval controls.

### `coding-agent-review-method`

Use this skill when code review should be performed by a specific external coding agent rather than by the current host agent. It provides a reusable findings-first review methodology that keeps the diff or range as primary scope while requiring bounded impact tracing across relevant callers, references, consumers, contracts, and blast-radius edges, requires the user to name the review agent when needed, and keeps review orchestration separate from patching, building, and testing.

### `commit-staged-changes`

Use this skill when changes are already staged and the task is to create a commit. It enforces a clean review of staged content and a factual English commit message without staging extra files implicitly.

### `cursor-coding-agent`

Use this skill when the user explicitly wants Cursor CLI to do delegated coding work. It covers headless `--print --trust` runs, interactive sessions, explicit model pass-through, read-only `plan` and `ask` modes, and safe handling of stronger execution flags.

### `explore-and-plan`

Use this skill when an idea needs to be turned into a concrete execution plan. It drives the work from exploration to convergence to a plan with no unresolved decisions or placeholders.

### `faster-learning-coach`

Use this skill when the user's real goal is to learn, master, practice, review, or prepare for a topic rather than receive a finished answer. It turns the assistant into a learning coach that clarifies the goal, selects a learning mode, uses active practice, requires teach-back, and schedules review so the user can apply the concept independently.

### `generate-commit-message`

Use this skill when you want a high-quality commit message for staged changes but do not want to create the commit yet. It inspects the staged diff and outputs commit message text only.

### `home-config-sync`

Use this skill when you want to initialize, deploy, or maintain a personal bare-repo dotfiles workflow under `~/.dotfiles` with work-tree set to `$HOME`. It covers first-time setup from an empty private remote, starter-file handling, multi-machine sync, pull and merge safety, and ongoing push workflow.

### `log-driven-debugging`

Use this skill when a bug is hard to reason about statically and one targeted rerun with better logs will collapse the search space. It requires a user-provided log prefix, guides deliberate instrumentation, and structures the follow-up analysis around the first proven divergence in the returned logs.

### `parallel-goal-workflows`

Use this skill when subagents, parallel agents, multi-agent execution, delegated workflows, or goal decomposition should be coordinated through flexible goals rather than rigid scripts. It helps the lead agent start an orchestrator, wait in observation mode, and report back while the orchestrator owns worker goals, independent review, acceptance or verification, repair routing, and the final workflow report.

### `write-unit-test`

Use this skill when writing, reviewing, or improving unit tests for production business code. It favors behavior-focused tests, realistic fixtures, stable assertions, and maintainable coverage over implementation-detail checks.

### `x-twitter-reader`

Use this skill when you need to acquire original content from X/Twitter posts, reply threads, long-form Articles, media references, linked URLs, author metadata, or engagement metrics before summarizing, translating, archiving, or quoting that content.

## Usage

Install the published skills:

```bash
npx skills add patrick-fu/awesome-skills
```

Update skills:

```bash
npx skills update
```

## Sync Model

This public repository is generated automatically from a private source repository. Public changes should be made in the source repository, not directly here.

The sync process preserves relevant file history and commit metadata for the published paths while rewriting commit hashes as part of the filtered export.
