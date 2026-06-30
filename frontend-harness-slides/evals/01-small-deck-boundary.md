---
name: 小页数边界判断
description: 当用户要做 3-8 页一次性静态幻灯片时，Skill 应建议单体 HTML 而非本 skill
difficulty: medium
tags: [trigger-boundary, decision]
---

## Input
"做一个 5 页的团队周会 slides，给组里 5 个人看一下就行。"

## Expected Output (any true)
- [ ] 明确建议单体 HTML 足够（理由：页数少、一次性交付、工程化成本不必要）
- [ ] 同时告知：若后续需要多轮改造、动画状态或视觉回归，可迁移到此 skill
- [ ] 不主动创建 harness 工程
