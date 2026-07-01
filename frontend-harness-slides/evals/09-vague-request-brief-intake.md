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
- [ ] 覆盖或明确假设内容取向、演讲形式、时长、内容占比、受众、stage、导航、技术栈、交付目标、素材来源、视觉偏好中的关键缺口
- [ ] 对关键点给出推荐默认值和可信替代方案，必要时说明理由，但不能把默认值当作用户已确认需求
- [ ] 当视觉方向不明确时，建议先做真实可交互 style preview；截图、本地 server 和三方向预览是推荐流程而非硬性产物
- [ ] 对非小型 deck，建议使用 context 文档和 narrative/content-mix plan 辅助长程跟踪，但不把它们当作额外审批 gate
