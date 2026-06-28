# Awesome Skills

**[中文说明](README.zh-CN.md)**

This repository contains a small set of reusable agent skills extracted from a larger private workspace and published as a standalone public collection.

## 🚀 Featured Workflow

✨ **Parallel Goal Workflows** now lives in its own repository: [`patrick-fu/parallel-goal-workflows`](https://github.com/patrick-fu/parallel-goal-workflows).

Invoke it explicitly when a Main Agent should translate a broad request into a
task contract, start one Workflow Owner per delegated top-level goal, track
active owners, and let those owners manage worker goals, independent review,
acceptance, repair, and final workflow reports.

Install the standalone workflow:

```bash
npx skills add patrick-fu/parallel-goal-workflows
```

## 🎬 Featured Skill

🛠️ **Frontend Harness Slides** lives in its own repository: [`patrick-fu/frontend-harness-slides`](https://github.com/patrick-fu/frontend-harness-slides).

Build a slide deck as a harness-guarded engineering project — robust, maintainable, and hard to break as it grows, a step up from single-file HTML slides.

Install the standalone skill:

```bash
npx skills add patrick-fu/frontend-harness-slides
```

## Included Skills

### `aero-mint-glass-html-design`

Use this skill when a frontend surface should follow the Aero Mint Glass visual style: airy mint-cyan light, translucent white glass panels, soft rounded geometry, restrained shadows, clean typography, soft 3D focal imagery, and quiet motion.

### `brainstorm`

Use this skill when the right next step is conversation rather than execution. It pushes the assistant to ask clarifying questions first, uncover hidden assumptions, and guide the user toward a clearer problem statement before proposing solutions.

### `claude-code-coding-agent`

Use this skill when the user or an active orchestration/review workflow explicitly selects Claude Code CLI as the external coding executor. It covers headless `--print` runs, interactive sessions, model and effort pass-through, constrained read-only runs, review-only prompts, and long-running background execution patterns. It is not for generic subagents, ordinary Claude chat, or unspecified delegation.

### `codex-coding-agent`

Use this skill when the user or an active orchestration/review workflow explicitly selects Codex CLI as the external coding executor through another host agent or automation harness. It covers `codex exec` for non-interactive execution, `codex review` for review flows, interactive resume and fork flows, Git repo expectations, and safe handling of sandbox and approval controls. It is not for built-in subagents, ordinary Codex chat, or unspecified delegation.

### `commit-staged-changes`

Use this skill when changes are already staged and the task is to create a commit. It enforces a clean review of staged content and a factual English commit message without staging extra files implicitly.

### `cursor-coding-agent`

Use this skill when the user or an active orchestration/review workflow explicitly selects Cursor CLI as the external coding executor. It covers headless `--print --trust` runs, interactive sessions, explicit model pass-through, read-only `plan` and `ask` modes, review-only prompts, and safe handling of stronger execution flags. The `agent` command here means Cursor CLI, not a generic agent or subagent.

### `explore-and-plan`

Use this skill when an idea needs to be turned into a concrete execution plan. It drives the work from exploration to convergence to a plan with no unresolved decisions or placeholders.

### `faster-learning-coach`

Use this skill when the user's real goal is to learn, master, practice, review, or prepare for a topic rather than receive a finished answer. It turns the assistant into a learning coach that clarifies the goal, selects a learning mode, uses active practice, requires teach-back, and schedules review so the user can apply the concept independently.

### `generate-commit-message`

Use this skill when you want a high-quality commit message for staged changes but do not want to create the commit yet. It inspects the staged diff and outputs commit message text only.

### `home-config-sync`

Use this skill when you want to initialize, deploy, or maintain a personal bare-repo dotfiles workflow under `~/.dotfiles` with work-tree set to `$HOME`. It covers first-time setup from an empty private remote, starter-file handling, multi-machine sync, pull and merge safety, and ongoing push workflow.

### `llm-wiki-capture`

Use this skill when the user explicitly wants to capture reusable knowledge from
the current session, review whether something is worth saving, or ingest
explicit source links into a maintained LLM wiki or knowledge base. It keeps
the workflow generic while expecting local wiki path, branch, commit, and push
policy to be configured in local agent instructions.

Tip: the skill includes
[`references/configuration-guide.md`](llm-wiki-capture/references/configuration-guide.md)
with setup guidance for initializing a wiki, writing `AGENTS.md` memory rules,
choosing capture preferences, and selecting between automatic capture,
end-of-task review, and scheduled recap.

### `log-driven-debugging`

Use this skill when a bug is hard to reason about statically and one targeted rerun with better logs will collapse the search space. It requires a user-provided log prefix, guides deliberate instrumentation, and structures the follow-up analysis around the first proven divergence in the returned logs.

### `write-unit-test`

Use this skill when writing, reviewing, or improving unit tests for production business code. It favors behavior-focused tests, realistic fixtures, stable assertions, and maintainable coverage over implementation-detail checks.

### `x-twitter-reader`

Use this skill when you need to acquire original content from X/Twitter posts, reply threads, long-form Articles, media references, linked URLs, author metadata, or engagement metrics before summarizing, translating, archiving, or quoting that content.

## Usage

Install this Awesome Skills collection:

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
