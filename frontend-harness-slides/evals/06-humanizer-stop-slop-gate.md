---
name: 收尾阶段文案质量 Gate
description: 收尾阶段需要做文案质量检查，避免空泛和 AI 味表述直接发布
difficulty: low
tags: [workflow, quality-gate]
---

## Input
"15 页幻灯片内容全部完成，现在到收尾阶段了。"

## Expected Output (all true)
- [ ] 检查空泛形容词、重复词和缺乏证据的 claims
- [ ] 检查每页标题是否能单独表意
- [ ] 明确表述：质量检查不通过需修复后发布
