# Awesome Skills

[![skills.sh](https://skills.sh/b/patrick-fu/awesome-skills)](https://skills.sh/patrick-fu/awesome-skills)

**[English README](README.md)**

这是我的个人 Agent Skills 集合，覆盖编码、计划、知识沉淀、slides 制作、多 Agent
协作和日常环境设置。

不打算把能装的 Skill 都挂满墙。这里只留我真的会反复用到的：值得占一个位置，也方便
随时翻一遍。🧰

## 🚀 安装完整集合

```bash
npx skills add patrick-fu/awesome-skills -g
```

后续更新：

```bash
npx skills update -g
```

## 🧩 单独安装某个 Skill

```bash
npx skills add patrick-fu/awesome-skills -g -s <skill-name>
```

`frontend-harness-slides`、`parallel-goal-workflows` 和 `llm-wiki-capture`
也有独立仓库，链接放在下方对应条目里。在同一个全局 scope 中从独立仓库安装，会替换
同名 Skill，不会多出第二份。

## ✨ Skills

### 🎨 Slides 与视觉交付

#### 🎞️ [`frontend-harness-slides`](./frontend-harness-slides)

用前端 harness 制作 HTML slides：稳定 scene 地址、registry、固定 stage、测试、视觉检查
和经过验证的交付链路都在流程里。反复改稿仍然可控，不会悄悄改坏前面的页面。

适合既要好看、能动，又要支持线上链接、PDF、静态导出或多种形式一起交付的 slides。

> 🖥️ Live Demo：体验
> [动态 Workbench Demo](https://frontend-harness-slides-workbench.vercel.app/)。
> 各种风格展示的是能力范围；真正的价值是 harness-backed 迭代，而不是脆弱的单体
> HTML。

📦 独立仓库：[`patrick-fu/frontend-harness-slides`](https://github.com/patrick-fu/frontend-harness-slides)

### 🧠 知识与记忆

#### 🗂️ [`llm-wiki-capture`](./llm-wiki-capture)

把 Session 教训和外部资料沉淀进长期维护、Git-backed 的 LLM Wiki，也能审计现有 Wiki，
或从零搭建一个。provenance、canonical ownership 和仓库操作边界都会被保留下来。

适合希望知识跨 Session 留存，又不想把 Wiki 的 Git 历史交给不透明自动化的场景。

📦 独立仓库：[`patrick-fu/llm-wiki-capture`](https://github.com/patrick-fu/llm-wiki-capture)

#### 🗞️ [`x-twitter-reader`](./x-twitter-reader)

在总结、翻译、引用或归档之前，先忠实抓取 X/Twitter 帖子、回复串、长文 Article、
元数据、链接和媒体。抽取阶段不改写原文，下游加工等内容到手后再做。

适合页面要求登录、只露出预览，或者无法可靠提供完整内容的情况。

### ✍️ 沟通与写作

#### ✂️ [`be-concise`](./be-concise)

一个由用户主动调用的回复风格：把回答压到任务允许的最短，同时保留正确性、安全和
下一步行动需要的信息。

适合 Agent 明明一句话能说完，却已经找到了三个自然段的时候。

#### 🧹 [`deslop`](./deslop)

改写或审查中文、英文和中英混排文本，去掉模板化 AI 味，同时保留事实、意图、立场、
语域和作者声音。

适合已经写出来、但读起来太像模板或过度加工的文本；不该成为所有写作任务的通用触发器。

### 🤖 Agent 编排

#### 🧩 [`parallel-goal-workflows`](./parallel-goal-workflows)

每个顶层目标交给一个 Goal Owner，再配一份干净的任务本地 brief。Owner 负责执行、按需
派出聚焦 helper、review、repair、验证和最终报告，不让主会话被所有子任务淹没。

适合代码审计、复杂调研、修复循环，或任何需要独立检查的任务。

📦 独立仓库：[`patrick-fu/parallel-goal-workflows`](https://github.com/patrick-fu/parallel-goal-workflows)

#### 🎯 [`long-task-control`](./long-task-control)

只有证据表明任务出现方案膨胀、目标漂移、无证据重复、失效委托、review 未收敛或无依据
完成时，才重新锚定目标。它保留已经验证的工作，剪掉不再服务于目标的动作，再从价值
最高的下一步继续。

适合任务真的开始跑偏时，而不是仅仅因为它很长。

下面四个 coding-agent 指南共用一套流程：保留选定的 CLI wrapper、发现当前模型和推理
控制、监控语义输出、尊重 permission 与 sandbox，并由宿主验证 diff 和测试。每个 Skill
只在对应 CLI 被明确选为执行器时触发。

#### 🟣 [`claude-code-coding-agent`](./claude-code-coding-agent)

把 Claude Code CLI 作为明确选择的外部编码执行器来运行。它会保留给定的 wrapper，从
当前 CLI 发现可用选项，并通过 verbose streaming JSON 监控耗时任务。

#### 🟢 [`codex-coding-agent`](./codex-coding-agent)

把 Codex CLI 作为明确选择的外部编码执行器来运行。它使用 `codex exec --json`，review
时显式选择 read-only sandbox，已批准的实现则使用 workspace-write sandbox。

#### 🔵 [`cursor-coding-agent`](./cursor-coding-agent)

把 Cursor CLI 作为明确选择的外部编码执行器来运行。由于通用的 `agent` launcher 可能
指向其他产品，流程会先验证身份，再决定是否信任它。

#### ⚡ [`grok-coding-agent`](./grok-coding-agent)

把 Grok Build CLI 作为明确选择的外部编码执行器来运行。它把 approval policy 和 sandbox
访问视为两项独立控制，并显式选择合适的 read-only 或 workspace sandbox。

### 🧭 思考与规划

#### 💡 [`brainstorm`](./brainstorm)

把想法或开放问题展开成一张覆盖不同维度的可能性地图，再决定往哪里深入。

适合方案空间还没有收窄、先看广面比过早下结论更有价值的阶段。

#### 🗺️ [`explore-and-plan`](./explore-and-plan)

把基本确定的方向变成可执行计划：暴露阻塞决策、梳理受影响面、按依赖排序步骤，并把
验证绑定到每个结果上。

适合方向已经足够明确，执行者不该再重新猜一遍意图的时候。

#### 🎓 [`faster-learning-coach`](./faster-learning-coach)

用练习、teach-back 和复习组成短而主动的学习循环，而不是默认给一篇长解释。FASTER
流程会根据学习目标、当前水平和可用时间调整。

适合真正目标是理解和留存，而不只是拿到答案的场景。

### 🛠️ 工程工作流

#### 🧪 [`write-unit-test`](./write-unit-test)

围绕行为、回归和领域规则编写、审查或改进单元测试。从调用方可观察的契约出发，让关键
输入在调用点可见，并断言可观察的效果。

适合生产代码：契约被破坏时测试要红，无害的内部重构则保持绿。

#### 🔦 [`log-driven-debugging`](./log-driven-debugging)

加入带前缀的聚焦日志，让用户重新跑真实场景，再根据返回的证据定位第一个有意义的分歧点。
静态读码不够时，用可观测性代替猜。

适合能够复现、但根因还藏着的 bug。

#### 📝 [`generate-commit-message`](./generate-commit-message)

草拟精简的英文 commit message：sentence-case 标题、不加 conventional prefix，重要改动
可以用可选 bullet 补充。

适合改动已经完成，但能直接复制使用的 commit message 还没写出来的时候。

### 🏠 个人环境

#### 🔄 [`home-config-sync`](./home-config-sync)

维护个人 `~/.dotfiles` bare-repository 工作流：首次设置、新机器部署、安全 pull/merge 和
push。它的 work tree 是整个 home 目录，所以安全边界本身就是功能的一部分。

适合希望把 dotfiles 纳入版本管理，又不想让便利脚本随便对待整个家目录的场景。
