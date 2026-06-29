---
name: 润色阶段必跑 Gate
description: 在 Phase III 提到调用 humanizer + stop-slop，且文案不通过 gate 不能发布
difficulty: low
tags: [workflow, quality-gate]
---

## Input
"15 页幻灯片内容全部完成，现在到收尾阶段了。"

## Expected Output (all true)
- [ ] 提到调用 humanizer skill（或 humanizer-zh）做 humanize
- [ ] 提到调用 stop-slop skill 做 slop check
- [ ] 明确表述：Gate 不通过「不得发布」或「需修复后发布」
