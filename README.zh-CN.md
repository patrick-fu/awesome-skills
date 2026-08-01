# Awesome Skills

**[English README](README.md)**

这是我的个人精选 Agent Skills，主要用于编码、计划、知识记录、slides 制作、多
Agent 协作和日常环境设置。

这个集合不追求塞满所有场景。我更关心这些 Skill 是否真的常用、是否能让任务更稳、
更清楚，或者让最终交付更好看。

## 安装完整集合

```bash
npx skills add patrick-fu/awesome-skills -g
```

后续更新：

```bash
npx skills update -g
```

推荐先安装完整集合。如果你只对下面某一个大 Skill 感兴趣，它们也有独立页面，适合单独
了解设计思路、演示效果和使用方式。

## 精选 Skills

### 🎞️ `frontend-harness-slides`

用前端工程化 harness 制作更灵动的 HTML slides：稳定 scene、可复现截图、有意义测试、
PDF 导出和线上交付都在流程里。

适合需要好看、能动、能交互，而且后续多轮修改也不容易改坏的 slides 项目。

> 🖥️ Live Demo：体验
> [动态 Workbench Demo](https://frontend-harness-slides-workbench.vercel.app/)。
> 视觉风格很直观，但它更大的价值是 harness-backed 迭代，而不是脆弱的单体 HTML。

独立页面：[`patrick-fu/frontend-harness-slides`](https://github.com/patrick-fu/frontend-harness-slides)

### 🧭 `parallel-goal-workflows`

处理复杂任务时，不把所有子任务都塞进主会话。它会把每个显式调用的顶层目标交给一个
Goal Owner，由它负责执行、按需派出聚焦 helper、审查、验收和最终报告。

适合代码审计、复杂调研、修复循环，或者任何需要独立检查的任务。

独立页面：[`patrick-fu/parallel-goal-workflows`](https://github.com/patrick-fu/parallel-goal-workflows)

### 🤖 External coding agents

把 Claude Code、Codex、Cursor 或 Grok 作为另一个宿主 Agent 明确选择的外部编码执行器。
这一组 Skill 统一了 wrapper、模型与推理强度选择、流式监控、permission、sandbox 和宿主
验收方式。

选择执行器：[`claude-code-coding-agent`](./claude-code-coding-agent) ·
[`codex-coding-agent`](./codex-coding-agent) ·
[`cursor-coding-agent`](./cursor-coding-agent) ·
[`grok-coding-agent`](./grok-coding-agent)

### 📚 `llm-wiki-capture`

把 Session 教训和外部资料沉淀进长期维护的 Git-backed LLM Wiki，也能审计现有 Wiki，
或帮助用户从零搭建。它保留 provenance 和 canonical ownership，并明确控制仓库写入边界。

独立页面：[`patrick-fu/llm-wiki-capture`](https://github.com/patrick-fu/llm-wiki-capture)

## 单独安装某个 Skill

```bash
npx skills add patrick-fu/awesome-skills -g -s deslop
npx skills add patrick-fu/frontend-harness-slides -g
npx skills add patrick-fu/parallel-goal-workflows -g
npx skills add patrick-fu/llm-wiki-capture -g
```

如果已经在同一个全局 scope 里安装了完整集合，之后再安装某个独立 Skill，本地同名
Skill 会被替换，不会多出第二份。

## 包含哪些 Skill

### Slides and visual delivery

- `frontend-harness-slides`：制作带风格对齐、交互、动效、截图检查、PDF 导出和线上交付的
  HTML slides。

### Knowledge and memory

- `llm-wiki-capture`：沉淀 Session 和外部资料、审计现有 LLM Wiki，或从零搭建，
  并明确控制仓库操作边界。
- `x-twitter-reader`：在总结、翻译、引用或归档前，先读取 X/Twitter 帖子、thread、
  Article、元数据、链接和媒体。

### Communication and writing

- `be-concise`：让 Agent 少说、直说，同时保留正确性、安全和执行所需的信息。
- `deslop`：改写或审查中文、英文和中英混排文本，去掉模板化 AI 味，同时保留事实、
  立场和作者声音。

### Agent orchestration

- `parallel-goal-workflows`：把每个顶层目标交给一个 Goal Owner，由它负责执行、按需派出
  聚焦 helper、review、repair 和最终报告。
- `claude-code-coding-agent`：明确选择 Claude Code CLI 作为外部编码 Agent 时使用。
- `codex-coding-agent`：从另一个宿主 Agent 或自动化流程里调用本地 Codex CLI。
- `cursor-coding-agent`：明确选择 Cursor CLI 作为外部执行器时使用。
- `grok-coding-agent`：明确选择 Grok Build CLI 作为外部编码 Agent 时使用。

### Thinking and planning

- `brainstorm`：在选择方向前，把想法或开放问题展开成覆盖不同维度的可能性地图。
- `explore-and-plan`：方向基本确定后，把它整理成可执行步骤和验收标准。
- `faster-learning-coach`：把解释变成短学习循环，包括练习、复述和复习。

### Engineering workflow

- `write-unit-test`：围绕行为、回归和领域规则编写或改进单元测试。
- `log-driven-debugging`：加高信号日志，让用户复现，再根据日志找到真实分歧点。
- `generate-commit-message`：按简单格式约束草拟精简的英文 commit message。

### Personal setup

- `home-config-sync`：维护个人 `~/.dotfiles` bare-repo 工作流，包括首次设置、新机器部署、
  pull 安全和 push。
