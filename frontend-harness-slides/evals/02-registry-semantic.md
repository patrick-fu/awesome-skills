---
name: 幻灯片 registry 语义一致性
description: 生成的 registry 数组中，每个 id 都是 slug，title 唯一，order 连续
difficulty: low
tags: [structure, consistency]
---

## Input
"给我生成一个关于 AI Agent 未来 5 年趋势的 10 页幻灯片结构"

## Expected Output (all true)
- [ ] registry.length === 10
- [ ] 所有 id 为 kebab-case slug（不含空格/中文/大写）
- [ ] order 字段为 0..9 连续整数（或无 order 字段依赖数组顺序）
- [ ] title 无重复
- [ ] 第一页是封面（title 含"AI Agent"或"趋势"等关键词），最后一页是 Q&A / 总结
