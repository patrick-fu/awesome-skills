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

制作更灵动的 HTML slides，并且能扛住真实修改：风格预览、动效、交互、导航、截图检查、
PDF 导出和线上交付都在流程里。

适合需要好看、能动、能交互，而且后续还会反复修改的 slides 项目。

独立页面：[`patrick-fu/frontend-harness-slides`](https://github.com/patrick-fu/frontend-harness-slides)

### 🧭 `parallel-goal-workflows`

处理复杂任务时，不把所有子任务都塞进主会话。它会帮 Agent 拆分目标、按需派出聚焦
helper、审查结果，再把最终判断收束成一份清楚的报告。

适合代码审计、复杂调研、修复循环，或者任何需要独立检查的任务。

独立页面：[`patrick-fu/parallel-goal-workflows`](https://github.com/patrick-fu/parallel-goal-workflows)

### 📚 `llm-wiki-capture`

把链接、决策、环境设置、踩坑记录和有价值的 agent session 保存到 Git-backed 知识库，
并保留足够证据，方便以后继续用。

适合那些你下个月还想找得到、信得过的知识。

独立页面：[`patrick-fu/llm-wiki-capture`](https://github.com/patrick-fu/llm-wiki-capture)

## 单独安装某个 Skill

```bash
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

- `llm-wiki-capture`：把可复用的资料和会话经验保存到 Git-backed wiki 或知识库。
- `x-twitter-reader`：在总结、翻译、引用或归档前，先读取 X/Twitter 帖子、thread、
  Article、元数据、链接和媒体。

### Agent orchestration

- `parallel-goal-workflows`：把复杂任务拆成有 owner 的目标、聚焦 helper 工作、review、
  repair 和最终报告。
- `claude-code-coding-agent`：明确选择 Claude Code CLI 作为外部编码 Agent 时使用。
- `codex-coding-agent`：从另一个宿主 Agent 或自动化流程里调用本地 Codex CLI。
- `cursor-coding-agent`：明确选择 Cursor CLI 作为外部执行器时使用。

### Thinking and planning

- `brainstorm`：在计划或动手前，先把粗糙想法聊清楚。
- `explore-and-plan`：方向基本确定后，把它整理成可执行步骤和验收标准。
- `faster-learning-coach`：把解释变成短学习循环，包括练习、复述和复习。

### Engineering workflow

- `write-unit-test`：围绕行为、回归和领域规则编写或改进单元测试。
- `log-driven-debugging`：加高信号日志，让用户复现，再根据日志找到真实分歧点。
- `commit-staged-changes`：只提交 staged 内容，并写事实准确的英文 commit message。
- `generate-commit-message`：只根据 staged diff 草拟 commit message，不创建 commit。

### Personal setup

- `home-config-sync`：维护个人 `~/.dotfiles` bare-repo 工作流，包括首次设置、新机器部署、
  pull 安全和 push。
