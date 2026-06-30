---
name: vague-request-brief-intake
description: 用户只给宽泛 slides 主题时，Skill 应先做偏好访谈而不是直接开工
difficulty: high
tags: [brief-intake, preference-alignment]
---

## Input
"帮我做一套关于 AI coding 的 slides。"

## Expected Output (all true)
- [ ] 不直接创建文件、初始化工程、选择框架或生成完整 deck
- [ ] 用普通文本追问真实需求，不使用结构化多选提问工具
- [ ] 明确确认 slides 风格、信息密度和动画方向；不能只问一个泛泛的“喜欢什么风格”
- [ ] 至少触达受众、stage 尺寸、触屏/内嵌导航、技术栈、交付目标、素材来源或视觉偏好中的关键缺口
- [ ] 每个关键点应给出推荐默认值、可选替代方案和理由，但不能把默认值当作已经确认的需求
- [ ] 当视觉方向不明确时，建议先做 1-2 张真实 slides 的多风格预览，再完整展开整套 deck
