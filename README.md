# Awesome Skills

**[中文说明](README.zh-CN.md)**

My personal collection of agent skills for coding, planning, knowledge capture,
slides, multi-agent work, and day-to-day setup.

This is not a warehouse of every Skill I could install. It is the smaller set I
actually reach for: useful enough to earn a place, compact enough to browse. 🧰

## 🚀 Install the collection

```bash
npx skills add patrick-fu/awesome-skills -g
```

Update later:

```bash
npx skills update -g
```

## 🧩 Install one Skill

```bash
npx skills add patrick-fu/awesome-skills -g -s <skill-name>
```

`frontend-harness-slides`, `parallel-goal-workflows`, and `llm-wiki-capture`
also have standalone repositories, linked from their entries below. Installing
one of them from its standalone repository in the same global scope replaces
the matching Skill; it does not create a second copy.

## ✨ Skills

### 🎨 Slides and visual delivery

#### 🎞️ [`frontend-harness-slides`](./frontend-harness-slides)

Build HTML slide decks with a frontend harness: stable scene URLs, a registry,
a fixed stage, tests, visual checks, and verified delivery. Repeated edits stay
manageable instead of quietly breaking earlier slides.

Use it when a deck needs to look good, feel alive, and ship online, as a PDF or
static export, or in all three forms.

> 🖥️ Live demo: explore the
> [dynamic Workbench Demo](https://frontend-harness-slides-workbench.vercel.app/).
> The styles show the range; the real win is harness-backed iteration instead
> of fragile single-file HTML.

📦 Standalone repository: [`patrick-fu/frontend-harness-slides`](https://github.com/patrick-fu/frontend-harness-slides)

### 🧠 Knowledge and memory

#### 🗂️ [`llm-wiki-capture`](./llm-wiki-capture)

Capture session lessons and external sources into a maintained, Git-backed LLM
Wiki. It can also audit an existing Wiki or bootstrap one from zero while
preserving provenance, canonical ownership, and explicit repository boundaries.

Use it when knowledge should survive the current session without handing the
Wiki's Git history over to opaque automation.

📦 Standalone repository: [`patrick-fu/llm-wiki-capture`](https://github.com/patrick-fu/llm-wiki-capture)

#### 🗞️ [`x-twitter-reader`](./x-twitter-reader)

Retrieve X/Twitter posts, reply threads, long-form Articles, metadata, links,
and media before summarizing, translating, quoting, or archiving them. Source
acquisition stays faithful; downstream transformation happens afterward.

Use it when an X page requires login, exposes only a preview, or simply is not
a reliable source of the complete content.

### ✍️ Communication and writing

#### ✂️ [`be-concise`](./be-concise)

A user-invoked response style that makes an answer as short as the task allows
without dropping information needed for correctness, safety, or action.

Use it when the agent has found three paragraphs where one sentence would do.

#### 🧹 [`deslop`](./deslop)

Review or rewrite Chinese, English, and mixed-language prose to remove
formulaic AI patterns while preserving facts, intent, stance, register, and the
author's voice.

Use it on existing text that sounds templated or over-produced—not as a generic
trigger for every writing task.

### 🤖 Agent orchestration

#### 🧩 [`parallel-goal-workflows`](./parallel-goal-workflows)

Give each top-level goal one Goal Owner and a clean, task-local brief. The Owner
handles execution, focused helpers when useful, review, repair, verification,
and the final report without flooding the main conversation.

Use it for audits, complex research, repair loops, or any task where independent
checks matter.

📦 Standalone repository: [`patrick-fu/parallel-goal-workflows`](https://github.com/patrick-fu/parallel-goal-workflows)

#### 🎯 [`long-task-control`](./long-task-control)

Re-anchor a task only when evidence shows design bloat, objective drift,
no-evidence repetition, stale delegation, unresolved reviewer conflict, or an
unsupported completion claim. It preserves verified work, cuts activity that no
longer serves the goal, and resumes from the highest-value next step.

Use it when a task is genuinely drifting—not merely because it is long.

The four coding-agent guides below share one workflow: preserve the selected CLI
wrapper, discover current model and reasoning controls, monitor semantic output,
respect permissions and sandboxes, and verify diffs and tests from the host.
Each guide triggers only when its CLI is explicitly selected as the executor.

#### 🟣 [`claude-code-coding-agent`](./claude-code-coding-agent)

Run Claude Code CLI as the explicitly selected external coding executor. It
preserves the supplied wrapper, discovers current options from the CLI, and
monitors long-running work through verbose streaming JSON.

#### 🟢 [`codex-coding-agent`](./codex-coding-agent)

Run Codex CLI as the explicitly selected external coding executor. It uses
`codex exec --json` with an explicit read-only sandbox for review or a
workspace-write sandbox for approved implementation.

#### 🔵 [`cursor-coding-agent`](./cursor-coding-agent)

Run Cursor CLI as the explicitly selected external coding executor. Because the
generic `agent` launcher can point to another product, the workflow verifies its
identity before trusting it.

#### ⚡ [`grok-coding-agent`](./grok-coding-agent)

Run Grok Build CLI as the explicitly selected external coding executor. It
treats approval policy and sandbox access as separate controls and chooses the
appropriate read-only or workspace sandbox explicitly.

### 🧭 Thinking and planning

#### 💡 [`brainstorm`](./brainstorm)

Expand an idea or open problem into a possibility map spanning genuinely
different dimensions before deciding where to go deeper.

Use it while the solution space is still open and breadth is more valuable than
an early verdict.

#### 🗺️ [`explore-and-plan`](./explore-and-plan)

Turn a mostly chosen direction into an executable plan: surface blocking
decisions, map affected areas, order steps by dependency, and tie verification
to each outcome.

Use it when the direction is settled enough that an implementer should not have
to rediscover the intent.

#### 🎓 [`faster-learning-coach`](./faster-learning-coach)

Teach through short, active learning loops built around practice, teach-back,
and review instead of defaulting to a long explanation. The FASTER workflow
adapts to the learner's goal, current level, and available time.

Use it when the goal is understanding and retention, not merely receiving an
answer.

### 🛠️ Engineering workflow

#### 🧪 [`write-unit-test`](./write-unit-test)

Write, review, or improve unit tests around behavior, regressions, and domain
rules. It starts from a caller-visible contract, keeps decisive inputs visible,
and asserts observable effects.

Use it for production code where breaking the contract should turn the test red
while harmless internal refactoring stays green.

#### 🔦 [`log-driven-debugging`](./log-driven-debugging)

Add focused, prefixed logs, have the user rerun the real scenario, and inspect
the returned evidence to locate the first meaningful divergence. When static
reading is not enough, observability replaces guesswork.

Use it for reproducible bugs whose root cause is still hiding.

#### 📝 [`generate-commit-message`](./generate-commit-message)

Draft a concise English commit message with a sentence-case subject, no
conventional prefix, and optional bullets for the important changes.

Use it when the change is ready but the copy-ready commit message is not.

### 🏠 Personal setup

#### 🔄 [`home-config-sync`](./home-config-sync)

Maintain a personal `~/.dotfiles` bare-repository workflow: first-time setup,
new-machine deployment, safe pulls and merges, and pushes. Its work tree is the
whole home directory, so the guardrails are part of the feature.

Use it when dotfiles should be versioned without letting a convenience script
treat the home directory casually.
