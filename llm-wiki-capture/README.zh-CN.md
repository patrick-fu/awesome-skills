# LLM Wiki Capture

**[English README](README.md)**

`llm-wiki-capture` 帮助 Agent 把明确给出的资料和 AI 工作会话，转化成
Git-backed 长期知识库里的、可追溯证据的知识更新。

这个 Skill 不绑定特定目录结构。你可以使用自己的 notes repository、wiki 或
Markdown knowledge base；只要在本地 agent instructions 和仓库文档里说明规则即可。
Agent 会根据这些规则判断新记忆应该放在哪里、provenance 怎么记录，以及是否允许
edit、commit 或 push。

## 背景

这个 Skill 受到一些实践型长期记忆工作流启发，例如
[Karpathy's memory gist](https://gist.github.com/karpathy/1dd0294ef9567971c1e4348a90d69285)。
这个 gist 可以作为理解长期记忆工作流的参考：AI sessions 可以进入个人知识库，但前提是
capture loop 是明确的、可维护的。

`llm-wiki-capture` 不依赖这个 gist，也不要求采用完全相同的设置。实际运行行为由本
Skill、本地 agent instructions 和知识库仓库文档共同决定。

## 安装

```bash
npx skills add patrick-fu/llm-wiki-capture
```

后续更新：

```bash
npx skills update
```

## 你需要准备什么

在期待 Skill 写入文件之前，先准备一个 Git-backed knowledge base。推荐两种方式：

- **托管 Git 仓库**：GitHub、GitLab、Codeberg、公司 Git 平台或自托管 Git
  服务。适合需要跨机器同步、备份、commit history 和可选 push 的长期用法。
- **本地 Git 仓库**：在单机目录里 `git init`。适合私密场景或早期实验，同时仍然
  能提供 diff、clean-worktree 检查和 commit history。

这个 Skill 不需要 starter project。它只需要足够的本地上下文来安全工作：知识库在哪、
哪些文档说明 purpose 和 schema、哪些导航文件需要更新，以及是否允许 commit 或 push。

## 快速开始

1. 为知识库创建一个 Git 仓库。
2. 编写或确认说明知识库规则的文档。常见名字是 `purpose.md`、`schema.md`、
   `wiki/index.md` 和 `wiki/log.md`，但任何等价结构都可以。
3. 在本地 agent instructions 里配置知识库 root、branch、read-first 文件、
   update-after 文件、clean-worktree policy 和 commit/push policy。
4. 用 `$llm-wiki-capture` 显式调用这个 Skill。

最小配置示例：

```markdown
## LLM Wiki Capture
- Knowledge base root: ~/path/to/my-wiki
- Clone URL: git@github.com:you/my-wiki.git
- Integration branch: main
- Read first: purpose.md, schema.md, wiki/index.md, wiki/log.md
- Update after knowledge edits: wiki/index.md, wiki/log.md
- Require clean worktree before capture: yes
- Commit policy: no-commit, commit-only, or commit-and-push
- Commit identity: Your Name <you@example.com>
- If raw session evidence or user-provided source material is unavailable,
  downgrade to review and do not edit the knowledge base.
```

关于 setup pattern、policy 选择和本地 instruction snippet，见
[`references/configuration-guide.md`](references/configuration-guide.md)。

## 主要模式

### Source Ingest

当你提供 URL、文档、文件或其他明确 source material 时，使用 Source Ingest。

Agent 应把用户提供的 sources 当作证据。它可以解析 canonical URL、获取明确的
original、对比 translation / interpretation 和原文，并抓取相关的一跳 references。
写入前应先去重，并把稳定结论带 provenance 地整合进知识库。

示例：

```text
$llm-wiki-capture

Ingest these two articles into my LLM wiki. Keep the raw source notes separate
from durable conclusions, deduplicate against anything already captured, and
update the relevant concept pages.
```

### Capture

当当前 AI session 产生了可复用的决策、约束、命令、踩坑、领域事实或操作规则时，
使用 Capture。

Capture 只能写入有证据支撑的记忆。如果 Agent 无法访问 raw session record，也没有
用户提供的 source material，它应该降级到 Review，只报告本来会捕获什么，而不是编辑知识库。

示例：

```text
$llm-wiki-capture

Capture the reusable lessons from this debugging session.
```

### Review

当你只想让 Agent 评估候选内容、不希望它写文件时，使用 Review。Review 模式不会编辑、
commit 或 push。它应该报告候选记忆、证据、可能的 owner pages，以及为什么跳过弱候选。

示例：

```text
$llm-wiki-capture

Review this session and tell me whether anything is worth saving. Do not edit
the wiki yet.
```

### Full Integration

Full Integration 是已有知识库的高级维护模式。它会让 Agent 检查知识图谱、修复薄弱
ownership、改善 provenance、连接相关 sources，并提炼稳定 synthesis。只有当你明确
想做更大范围的知识库维护时才使用。

## 安全边界

- 不把 secrets、tokens、credentials、private keys、临时日志、噪音进度或无证据猜测
  写进知识库。
- 缺少必要本地配置时，先询问一次；如果用户不想配置，就降级 Review，而不是猜测。
- 只有本地 policy 允许时才 commit 或 push。
- push 前先 fetch；遇到 non-fast-forward 冲突就停止，不 force-push。
- 优先更新已有 canonical owner page，而不是创建重复页面。

## 更多 Skills

更多可复用 Agent Skills 见
[Awesome Skills](https://github.com/patrick-fu/awesome-skills)。
