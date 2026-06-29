---
name: Stage 内不使用 responsive breakpoints
description: 生成的 Stage 内部 React 代码不包含 md:/lg:/sm: 等 Tailwind responsive 前缀
difficulty: medium
tags: [anti-pattern, implementation]
---

## Input (code snippet context)
"给我一页幻灯片，左侧文字右侧 App 截图：左边是三行 bullet（标题 + 副标题 + 说明），右边是 16:9 手机 mockup，整体 1920×1080。"

## Expected Output (all true)
- [ ] 生成的 JSX 中没有 `md:`、`lg:`、`sm:`、`xl:` 响应式前缀
- [ ] 用 `w-920`、`ml-120` 等绝对像素值定位
- [ ] Stage 容器有 `[data-slide-stage]` 属性
