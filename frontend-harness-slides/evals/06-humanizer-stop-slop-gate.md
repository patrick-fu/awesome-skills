---
name: 收尾阶段文案质量检查
description: 收尾阶段需要做具体的 slide copy 质量检查，避免空泛、重复或缺少证据的表达直接发布
difficulty: low
tags: [workflow, copy-quality]
---

## Input
"15 页幻灯片内容全部完成，现在到收尾阶段了。"

## Expected Output (all true)
- [ ] 检查空泛形容词、重复词和缺乏证据的 claims
- [ ] 检查每页标题是否能单独表意
- [ ] 检查 speaker-led 与 reading-first 页面是否分别符合对应的文案密度
- [ ] 不要求调用外部 humanizer / stop-slop 工具；可以直接按具体质量标准审阅
- [ ] 若发现问题，修复或在交付说明中明确残留风险，不能默认为通过
