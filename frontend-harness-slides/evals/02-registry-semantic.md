---
name: 幻灯片 registry 语义一致性
description: 生成的 registry、manifest 或 draft 能稳定枚举 scene/frame 语义
difficulty: low
tags: [structure, consistency]
---

## Input
"给我生成一个关于 AI Agent 未来 5 年趋势的 10 页幻灯片结构"

## Expected Output (all true)
- [ ] 有 registry、manifest、route table、draft，或等价结构，可枚举 10 个 scene/frame 条目
- [ ] 每个条目有稳定 id，id 不依赖可见标题、文件名或数组位置
- [ ] 每个条目有 title 或 human label，且不会因标题重复导致寻址歧义
- [ ] 每个条目包含 beats、beat_count、frame states 或等价 frame 数量信息
- [ ] 顺序可由数组顺序或显式 order 表达，但不能需要抓取可见文本来推断
- [ ] 开头和结尾有清楚的 opening / closing / takeaway 语义，不强制 Q&A
