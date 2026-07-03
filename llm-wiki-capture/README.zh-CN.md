# LLM Wiki Capture

**[English README](README.md)**

`llm-wiki-capture` 帮助 Agent 把有价值的链接、决策、环境设置、踩坑记录和工作会话，
保存到一个以后还能信得过的 Git-backed 知识库。

目标很简单：不要让可复用知识只留在聊天记录里。一次好的 capture 应该保留来源、结论、
归属页面，以及为什么这条信息值得以后再找。

你可以使用自己的 notes repository、wiki 或 Markdown knowledge base。这个 Skill 不强制
目录结构，它会按照你在本地 agent instructions 和仓库文档里写好的规则工作。

## 适合什么内容

- 保存一次 debugging 或实现过程里的稳定经验。
- 把 source links、论文、帖子或文档整理成可复用笔记。
- 记录未来 Agent 应该知道的项目决策和环境设置。
- 在写入前先 review 一次会话，判断哪些内容值得保存。

它不适合存 raw logs、临时进度、猜测或 secrets。

## 安装

```bash
npx skills add patrick-fu/llm-wiki-capture -g
```

后续更新：

```bash
npx skills update -g
```

## 需要准备什么

在期待 Skill 写文件之前，先准备一个 Git-backed knowledge base。两种方式都可以：

- 托管 Git 仓库：适合同步、备份、历史记录和可选 push。
- 本地 Git 仓库：适合私密或早期实验，同时仍然保留 diff、clean-worktree 检查和历史记录。

Agent 需要足够的本地上下文来安全工作：

- 知识库在哪里；
- 哪些文档说明它的用途和结构；
- 编辑后需要更新哪些 index 或 log 文件；
- 是否允许 commit 或 push。

## 快速开始

1. 创建或选择一个 Git 仓库作为知识库。
2. 写一份小文档，说明知识库如何组织。
3. 在本地 agent instructions 里配置仓库路径、read-first 文件、update-after 文件和 commit
   policy。
4. 用 `$llm-wiki-capture` 显式调用，并说明想用哪个模式。

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

更多 setup pattern 和 policy 选择见
[`references/configuration-guide.md`](references/configuration-guide.md)。

## 模式

### Source ingest

当你提供 URL、文档、文件或其他明确 source material 时，使用 Source Ingest。

Agent 会把用户提供的 sources 当作证据，写入前先去重，并把稳定结论带 provenance 地整合进
知识库。

示例：

```text
$llm-wiki-capture

Ingest these two articles into my LLM wiki. Keep the raw source notes separate
from durable conclusions, deduplicate against anything already captured, and
update the relevant concept pages.
```

### Capture

当当前 AI session 产生了可复用的决策、约束、命令、踩坑、领域事实或操作规则时，使用
Capture。

Capture 只应该写入有证据支撑的记忆。如果 Agent 无法访问 source material 或 session
evidence，它应该降级到 Review，只报告本来会捕获什么，而不是直接编辑 wiki。

示例：

```text
$llm-wiki-capture

Capture the reusable lessons from this debugging session.
```

### Review

当你只想看候选内容、不希望写文件时，使用 Review。Review 会报告候选记忆、证据、可能的
owner pages，以及为什么跳过弱候选。

示例：

```text
$llm-wiki-capture

Review this session and tell me whether anything is worth saving. Do not edit
the wiki yet.
```

### Full integration

只有当你想对已有知识库做一次更大范围维护时，才使用 Full Integration：检查薄弱 ownership、
缺失 provenance、重复页面，以及相关笔记之间的连接。

## 安全边界

- 不把 secrets、tokens、credentials、private keys、临时日志、噪音进度或无证据猜测写进
  知识库。
- 缺少必要本地配置时，先询问一次；如果用户不想配置，就降级 Review。
- 只有本地 policy 允许时才 commit 或 push。
- push 前先 fetch；遇到 non-fast-forward 冲突就停止。
- 优先更新已有 owner page，而不是创建重复页面。

## 背景

这个 Skill 受到一些实践型长期记忆工作流启发，例如
[Karpathy's memory gist](https://gist.github.com/karpathy/1dd0294ef9567971c1e4348a90d69285)。
这个 gist 适合理解背后的思路：只要 capture loop 足够明确、可维护，AI sessions 就可以
进入个人知识库。

`llm-wiki-capture` 不依赖这个 gist，也不要求采用完全相同的设置。实际运行行为由本
Skill、本地 agent instructions 和知识库仓库文档共同决定。

## 我的更多精选 Skill

更多我长期维护、偏实战的精选 Agent Skills，见
[Awesome Skills](https://github.com/patrick-fu/awesome-skills)。
