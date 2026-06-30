---
name: Stage 内不使用 responsive breakpoints
description: "生成的 Stage 内部布局不依赖 viewport responsive breakpoints"
difficulty: medium
tags: [anti-pattern, implementation]
---

## Input (code snippet context)
"给我一页幻灯片，左侧文字右侧 App 截图：左边是三行 bullet（标题 + 副标题 + 说明），右边是 16:9 手机 mockup，整体 1920×1080。"

## Expected Output (all true)
- [ ] Stage 内部布局不依赖 `md:`、`lg:`、`sm:`、`xl:` 或等价 viewport 断点
- [ ] 使用固定舞台坐标或等价的固定比例布局
- [ ] Stage 容器暴露可供审计识别的稳定属性或角色
