---
name: Stage 内不使用 responsive breakpoints
description: "生成的 Stage 内部布局不依赖 viewport responsive breakpoints"
difficulty: medium
tags: [anti-pattern, implementation]
---

## Input (code snippet context)
"给我一页幻灯片，左侧文字右侧 App 截图：左边是三行 bullet（标题 + 副标题 + 说明），右边是 16:9 手机 mockup，整体 1920×1080。"

## Expected Output (all true)
- [ ] Stage 内部内容布局不依赖 viewport/container breakpoints 或等价 utility breakpoint 来重排
- [ ] Stage 外壳可以响应 viewport 做整体缩放，但不改变 slide 内部构图语义
- [ ] 使用固定舞台坐标、stage-relative 固定比例布局，或等价的固定 stage 设计系统
- [ ] Stage/scene/beat 暴露可供审计识别的稳定属性、角色或等价 selector
