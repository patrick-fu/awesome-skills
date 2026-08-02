# LLM Wiki Capture

[![skills.sh](https://skills.sh/b/patrick-fu/llm-wiki-capture)](https://skills.sh/patrick-fu/llm-wiki-capture)

**[English README](README.md)**

`llm-wiki-capture` 把 Session 中可复用的教训和外部资料沉淀进长期维护、Git-backed
的 LLM Wiki，也可以审计成熟 Wiki，或帮助新用户从零搭建。

这是一个用户显式调用的 Skill。它不会自动捕获会话，不会猜哪个仓库属于用户，不会因为没
找到 Wiki 就擅自创建，也不会未经授权 commit 或 push。

## 安装

```bash
npx skills add patrick-fu/llm-wiki-capture -g
```

后续更新：

```bash
npx skills update -g
```

## 工作流

### Session Capture

从当前 Session 或用户确认的历史 Session 中提取长期知识：

- 失败过程中的教训、根因和已验证修复；
- 决策、理由、约束和被否决的方案；
- 可复用 SOP、精确命令、验证和恢复步骤；
- 不容易从代码推导的项目事实，以及用户明确表达的偏好。

Session Capture 按知识归属整合，不按聊天时间线建页面。临时进度和 handoff 状态默认不进入
长期 Wiki，也不会默认复制完整 transcript。

```text
$llm-wiki-capture

把这次 Session 的可复用教训和部署 SOP 沉淀到 Wiki。
```

### Source Ingest

对用户明确要求入库的材料执行来源识别、去重、价值驱动的引用追踪、provenance 保存和概念
整合。

```text
$llm-wiki-capture

把这篇论文、它的翻译和链接的 benchmark 炼化进我的 Wiki。
```

只有 URL、或者只是让 Agent 参考和讨论，不代表 Source Ingest 意图。

### Full Integration

对成熟 Wiki 做 provenance、canonical ownership、重复页面、过期知识、导航和缺失综合的
全局审计或修复。只有用户明确要求全库处理时才进入这个分支。

### Bootstrap

如果还没有 Wiki，需要明确让 Skill 创建。默认从一个小型本地 Git 仓库开始，包含 purpose、
schema、raw source evidence、source summaries、canonical concepts、index、log，以及零依赖的
`wiki-maintenance check`。

需要多端同步时会推荐私有托管仓库，但未经确认不会创建 remote 或公开发布。

```text
$llm-wiki-capture

我还没有 Wiki。请在 ~/notes/my-wiki 从零搭建一个私有 Git-backed Wiki；创建 remote 前先问我。
```

## Review-only

Review-only 可以叠加到所有工作流。它只报告证据、候选修改、canonical owner、冲突和跳过项，
不编辑文件、不 commit、不 push、不创建仓库，也不对外发布。

```text
$llm-wiki-capture

先回顾这次 Session 有什么值得沉淀，不要修改 Wiki。
```

## 仓库发现

用户可以在当前请求里直接指定 Wiki，也可以写进本地 agent instructions。如果 Skill 从项目或
全局 instructions 中发现候选仓库，将它作为 Wiki 目标继续处理前仍会让用户二次确认。如果
发现的是普通 notes repository，会先只读调研，再询问原地升级还是新建独立 Wiki。

可选的最小配置：

```markdown
## LLM Wiki
- Root: ~/path/to/my-wiki
- Read first: AGENTS.md, purpose.md, schema.md, wiki/index.md
- Validate with: scripts/wiki-maintenance check
- Require a clean worktree before edits: yes
- Commit policy: ask
- Push policy: ask
```

仓库发现和配置权责见
[`references/configuration-guide.md`](references/configuration-guide.md)。

## 安全边界

- 外部材料和历史 transcript 只是证据，不能变成当前可执行指令。
- Assistant 的建议只有在被用户采纳或得到验证后，才可能成为长期事实。
- 用户 SOP 与仓库行为冲突时，先调研，再询问用户如何确定 canonical。
- secrets、credentials、噪音日志、临时状态和无依据主张不进入 Wiki。
- commit 和 push 是两个独立的显式授权边界。

## 背景

整体架构遵循
[Karpathy 的 LLM Wiki gist](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f)
中的 Raw / Wiki / Schema 思路，并在此基础上补充冷启动、provenance-aware source ingest、
Session learning 和知识图谱维护工作流。

## 我的更多精选 Skill

见 [Awesome Skills](https://github.com/patrick-fu/awesome-skills)。
