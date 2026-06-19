# Awesome Skills

**[English README](README.md)**

这个仓库是从一个更大的私有工作区中抽取出来的可复用 Agent Skills 集合，并作为独立的公开集合发布。

## 🚀 推荐 Workflow

✨ **Parallel Goal Workflows** 已经独立到专门仓库：[`patrick-fu/parallel-goal-workflows`](https://github.com/patrick-fu/parallel-goal-workflows)。

当 Lead Agent 需要把任务交给 Orchestrator，并由 Orchestrator 管理 worker goals、独立 review、acceptance、repair 和最终报告时，使用这个 workflow。

安装这个独立 workflow：

```bash
npx skills add patrick-fu/parallel-goal-workflows
```

## 包含的 Skills

### `aero-mint-glass-html-design`

当前端界面需要采用 Aero Mint Glass 视觉风格时使用这个 Skill：薄荷青色空气感、半透明白色玻璃面板、柔和圆角、克制阴影、干净字体、软 3D 焦点视觉和安静动效。

### `brainstorm`

当正确的下一步是对话而不是执行时使用这个 Skill。它会推动助手先提澄清问题，暴露隐藏假设，并在提出方案前帮助用户把问题收敛得更清楚。

### `claude-code-coding-agent`

当用户明确希望把编码任务委托给 Claude Code CLI 时使用这个 Skill。它覆盖 headless `--print` 执行、交互式会话、模型和推理强度透传、受限只读运行，以及长时间后台执行模式。

### `codex-coding-agent`

当用户明确希望由另一个宿主 Agent 或自动化流程调用 Codex CLI 来执行编码任务时使用这个 Skill。它覆盖 `codex exec` 非交互执行、`codex review` 代码审查流程、交互式 resume/fork 流程、Git 仓库预期，以及 sandbox 和 approval 控制的安全处理。

### `coding-agent-review-method`

当代码审查需要由指定的外部 Coding Agent 完成，而不是由当前宿主 Agent 直接完成时使用这个 Skill。它提供一套可复用的 findings-first 审查方法：以 diff 或范围为主审查对象，同时要求沿相关调用方、引用、消费者、契约和影响边界做有界追踪；必要时要求用户指定审查 Agent，并把审查编排和补丁、构建、测试工作分开。

### `commit-staged-changes`

当变更已经 staged，任务是创建 commit 时使用这个 Skill。它要求先干净地审查 staged 内容，并生成事实准确的英文提交信息，不会隐式 stage 额外文件。

### `cursor-coding-agent`

当用户明确希望把编码任务委托给 Cursor CLI 时使用这个 Skill。它覆盖 headless `--print --trust` 执行、交互式会话、显式模型透传、只读 `plan` 和 `ask` 模式，以及更强执行参数的安全处理。

### `explore-and-plan`

当一个想法需要被转化成具体可执行的计划时使用这个 Skill。它推动工作从探索走向收敛，并产出没有悬空决策或占位步骤的计划。

### `faster-learning-coach`

当用户真正的目标是学习、掌握、练习、复习或准备某个主题，而不是直接拿到成品答案时使用这个 Skill。它会把助手切换成学习教练：澄清目标、选择学习模式、设计主动练习、要求 teach-back，并安排复习，让用户最终能独立应用概念。

### `generate-commit-message`

当你想基于 staged changes 生成高质量 commit message，但暂时不想真正创建 commit 时使用这个 Skill。它会检查 staged diff，并只输出 commit message 文本。

### `home-config-sync`

当你想初始化、部署或维护一个位于 `~/.dotfiles`、work-tree 指向 `$HOME` 的个人 bare-repo dotfiles 工作流时使用这个 Skill。它覆盖从空私有远端开始的首次 setup、starter 文件处理、多机器同步、pull/merge 安全性，以及日常 push 流程。

### `log-driven-debugging`

当一个 bug 很难靠静态阅读推理清楚，而一次带有高质量日志的重跑能显著缩小搜索空间时使用这个 Skill。它要求用户提供日志前缀，指导有目的地加日志，并在用户返回日志后围绕第一个被证明的分歧点做分析。

### `write-unit-test`

当需要为生产业务代码编写、审查或改进单元测试时使用这个 Skill。它强调以行为为中心的测试设计、真实可信的 fixture、稳定断言和可维护覆盖，而不是只检查实现细节。

### `x-twitter-reader`

当需要先获取 X/Twitter 帖子、回复线程、长文 Article、媒体引用、外链、作者元数据或互动指标的原始内容，再进行总结、翻译、归档或引用时使用这个 Skill。

## 使用方式

安装当前 Awesome Skills 集合：

```bash
npx skills add patrick-fu/awesome-skills
```

更新 skills：

```bash
npx skills update
```

## 同步模型

这个公开仓库由私有源仓库自动生成。公开变更应该在源仓库中完成，不应直接修改这里。

同步流程会保留被发布路径的相关文件历史和 commit 元数据，但过滤导出会重写 commit hash。
