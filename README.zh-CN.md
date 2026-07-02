# Awesome Skills

**[English README](README.md)**

这个仓库是从一个更大的私有工作区中抽取出来的可复用 Agent Skills 集合，并作为独立的公开集合发布。

## 快速安装

一行安装全部：公开集合 + 3 个 standalone 精选。

```bash
npx skills add patrick-fu/awesome-skills && npx skills add patrick-fu/frontend-harness-slides && npx skills add patrick-fu/parallel-goal-workflows && npx skills add patrick-fu/llm-wiki-capture
```

只安装公开集合：

```bash
npx skills add patrick-fu/awesome-skills
```

更新已安装的 skills：

```bash
npx skills update
```

## 精选 Skills

这些较大的 skills 已经拆成独立仓库。需要完整版本，包括 references、evals 和 examples 时，建议直接安装对应仓库。

### 🎞️ `frontend-harness-slides`

制作 HTML slides，并且让后续修改不容易把其他页面静默改坏。它会引导 Agent 先对齐风格、受众、舞台尺寸、交互和交付方式，再用 harness、截图和导出检查来守住质量。

适合演讲、产品 walkthrough、教学课件，以及任何需要动效、导航、PDF 导出或线上部署的 slides 项目。

```bash
npx skills add patrick-fu/frontend-harness-slides
```

仓库：[`patrick-fu/frontend-harness-slides`](https://github.com/patrick-fu/frontend-harness-slides)

### 🧭 `parallel-goal-workflows`

处理复杂任务时，不把所有子任务都塞进同一个会话。Main Agent 会把宽泛请求整理成干净的本地 brief，为每个顶层目标启动一个 Goal Owner，并把 review、repair、acceptance 和最终报告分开处理。

适合需要并行调研、实现、审查，或者需要多路独立检查的任务。

```bash
npx skills add patrick-fu/parallel-goal-workflows
```

仓库：[`patrick-fu/parallel-goal-workflows`](https://github.com/patrick-fu/parallel-goal-workflows)

### 📚 `llm-wiki-capture`

把 source links 和 agent sessions 里的可复用知识沉淀到 Git-backed 长期 wiki。它会保留 evidence、ownership、verification 和本地 commit/push policy，让后续 Agent 不必只依赖聊天历史。

适合沉淀模式、决策、环境设置、踩坑记录，以及后面大概率还会用到的经验。

```bash
npx skills add patrick-fu/llm-wiki-capture
```

仓库：[`patrick-fu/llm-wiki-capture`](https://github.com/patrick-fu/llm-wiki-capture)

## 包含的 Skills

这些较小的 skills 会保留在当前集合里，适合作为日常构建块使用。

### 思考和计划

- `brainstorm`：还没到写计划或动手阶段时使用。它会先帮你澄清想法、受众、约束和第一个可执行方向。
- `explore-and-plan`：方向基本确定后使用，把想法拆成可执行计划，并明确边界、顺序和验收方式。
- `faster-learning-coach`：当用户真正想学习，而不是只要一个答案时使用。它会把解释变成小学习循环：练习、teach-back 和复习。

### 编码工作流

- `write-unit-test`：为生产业务代码写、审查或改进单元测试，重点是行为、回归、领域规则和可维护断言。
- `log-driven-debugging`：处理靠静态阅读很难定位的 bug：先加高信号日志，让用户复现，再根据返回日志找到第一个真实分歧点。
- `commit-staged-changes`：只提交已经 staged 的内容，提交前检查 staged diff，并生成事实准确的英文 commit message。
- `generate-commit-message`：只基于 staged diff 草拟 commit message，不创建 commit。

### 外部编码 Agent

- `claude-code-coding-agent`：当 Claude Code CLI 被明确选为外部执行器时使用，覆盖自动化执行、只读 review、交互会话，以及模型或权限参数透传。
- `codex-coding-agent`：当另一个宿主 Agent 或自动化流程需要启动本地 Codex CLI 时使用，覆盖 `codex exec`、`codex review`、交互式 resume/fork 和 Git 工作区预期。
- `cursor-coding-agent`：只有在明确选择 Cursor CLI 时使用，区分 headless 执行、只读 `--mode ask`、plan 模式和交互会话。

### 个人工作流和来源提取

- `home-config-sync`：初始化和维护 `~/.dotfiles` 下的个人 bare-repo dotfiles 工作流，覆盖首次 push、新机器部署、白名单更新、pull/merge 安全性和可选的 GUI-discoverable mode。
- `x-twitter-reader`：在总结、翻译、引用或归档之前，先从 X/Twitter 帖子、thread、Article、元数据、链接和媒体引用里提取原始内容。

## 同步模型

这个公开集合由私有源仓库自动生成。公开变更应该在源仓库中完成，不应直接修改这里。

同步流程会保留被发布路径的相关文件历史和 commit 元数据，但过滤导出会重写 commit hash。
