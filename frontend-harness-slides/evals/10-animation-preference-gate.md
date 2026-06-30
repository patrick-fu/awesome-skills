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
- [ ] 用普通文本确认 slides 风格、信息密度和动画方向，不使用结构化多选提问工具
- [ ] 推荐 keynote/product-launch 式逐 beat 动效，并说明它包含短过场、语义化 reveal、轻微 spring/scale、旧信息弱化或划掉、最后 takeaway highlight
- [ ] 同时给出更克制的报告型动效作为可选方向，但不把选择题写死
- [ ] 如果用户提供参考 URL 或源码，说明会先观察 stage、缩放、过场、beat reveal 和导航行为再实现
