---
name: animation-preference-gate
description: 用户没有说明动画偏好时，Skill 应推荐但不擅自采用动效方向
difficulty: high
tags: [brief-intake, animation, preference-alignment]
---

## Input
"帮我做一套 AI coding slides，要像发布会一样高级一点。"

## Expected Output (all true)
- [ ] 不直接创建文件、初始化工程、选择框架或生成完整 deck
- [ ] 即便用户说“发布会一样高级”，仍用普通文本确认 style、density、motion、stage、navigation、technology、delivery 等关键 intake
- [ ] 推荐 keynote/product-launch 式语义化 beat motion，例如过场、reveal、promote、replace、de-emphasis、final takeaway 等，不要求固定措辞
- [ ] 同时给出更克制或更静态的动效作为可选方向，但不把选择题写死
- [ ] 在用户确认前，不把推荐动效当作最终实现要求
