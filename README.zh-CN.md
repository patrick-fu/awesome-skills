# Awesome Skills

**[English README](README.md)**

一组实用的 Agent Skills，覆盖计划梳理、工程工作流、slides 制作、知识沉淀、外部编码 Agent 和个人环境设置。

## 快速安装

全局安装完整集合：

```bash
npx skills add patrick-fu/awesome-skills -g
```

更新全局 skills：

```bash
npx skills update -g
```

## 精选 Skills

下面 3 个较大的 skills 已经包含在上面的集合里。它们也有独立仓库，适合只安装单个 skill，或者查看更完整的 README、references、evals 和 examples。

### 🎞️ `frontend-harness-slides`

制作 HTML slides，并且让后续修改不容易把其他页面静默改坏。它会引导 Agent 先对齐风格、受众、舞台尺寸、交互和交付方式，再用 harness、截图和导出检查来守住质量。

适合演讲、产品 walkthrough、教学课件，以及任何需要动效、导航、PDF 导出或线上部署的 slides 项目。

```bash
npx skills add patrick-fu/frontend-harness-slides -g
```

仓库：[`patrick-fu/frontend-harness-slides`](https://github.com/patrick-fu/frontend-harness-slides)

### 🧭 `parallel-goal-workflows`

处理复杂任务时，不把所有子任务都塞进同一个会话。Main Agent 会把宽泛请求整理成干净的本地 brief，为每个顶层目标启动一个 Goal Owner，并把 review、repair、acceptance 和最终报告分开处理。

适合需要并行调研、实现、审查，或者需要多路独立检查的任务。

```bash
npx skills add patrick-fu/parallel-goal-workflows -g
```

仓库：[`patrick-fu/parallel-goal-workflows`](https://github.com/patrick-fu/parallel-goal-workflows)

### 📚 `llm-wiki-capture`

把 source links 和 agent sessions 里的可复用知识沉淀到 Git-backed 长期 wiki。它会保留 evidence、ownership、verification 和本地 commit/push policy，让后续 Agent 不必只依赖聊天历史。

适合沉淀模式、决策、环境设置、踩坑记录，以及后面大概率还会用到的经验。

```bash
npx skills add patrick-fu/llm-wiki-capture -g
```

仓库：[`patrick-fu/llm-wiki-capture`](https://github.com/patrick-fu/llm-wiki-capture)

## Skill 分组

`npx skills add patrick-fu/awesome-skills -g` 会在交互安装里显示这些分组。

### Slides and visual delivery

- `frontend-harness-slides`：制作高标准 HTML slides，覆盖前期对齐、灵动动效和交互、harness 化迭代、截图检查、PDF/static 导出和线上交付检查。

### Knowledge and memory

- `llm-wiki-capture`：把 source links 和 agent sessions 里的可复用知识沉淀到维护中的 Git-backed wiki 或知识库。
- `x-twitter-reader`：在总结、翻译、引用或归档之前，先从 X/Twitter 帖子、thread、Article、元数据、链接和媒体引用里提取原始内容。

### Agent orchestration

- `parallel-goal-workflows`：用干净的本地 brief、Goal Owner、聚焦 helper、review、repair、acceptance 和最终报告来处理复杂委托工作。
- `claude-code-coding-agent`：当 Claude Code CLI 被明确选为外部执行器时使用，覆盖自动化执行、只读 review、交互会话，以及模型或权限参数透传。
- `codex-coding-agent`：当另一个宿主 Agent 或自动化流程需要启动本地 Codex CLI 时使用，覆盖 `codex exec`、`codex review`、交互式 resume/fork 和 Git 工作区预期。
- `cursor-coding-agent`：只有在明确选择 Cursor CLI 时使用，区分 headless 执行、只读 `--mode ask`、plan 模式和交互会话。

### Thinking and planning

- `brainstorm`：还没到写计划或动手阶段时使用。它会先帮你澄清想法、受众、约束和第一个可执行方向。
- `explore-and-plan`：方向基本确定后使用，把想法拆成可执行计划，并明确边界、顺序和验收方式。
- `faster-learning-coach`：当用户真正想学习，而不是只要一个答案时使用。它会把解释变成小学习循环：练习、teach-back 和复习。

### Engineering workflow

- `write-unit-test`：为生产业务代码写、审查或改进单元测试，重点是行为、回归、领域规则和可维护断言。
- `log-driven-debugging`：处理靠静态阅读很难定位的 bug：先加高信号日志，让用户复现，再根据返回日志找到第一个真实分歧点。
- `commit-staged-changes`：只提交已经 staged 的内容，提交前检查 staged diff，并生成事实准确的英文 commit message。
- `generate-commit-message`：只基于 staged diff 草拟 commit message，不创建 commit。

### Personal setup

- `home-config-sync`：初始化和维护 `~/.dotfiles` 下的个人 bare-repo dotfiles 工作流，覆盖首次 push、新机器部署、白名单更新、pull/merge 安全性和可选的 GUI-discoverable mode。

## 重复安装

集合和独立仓库使用相同的 skill name。如果已经在同一个全局 scope 里安装了 `awesome-skills`，之后再安装某个 standalone skill，本地同名 skill 会被 standalone 版本覆盖，不会生成两份副本。
