---
name: 整页 canvas 渲染检测
description: 禁止用 canvas 画整页静态内容
difficulty: medium
tags: [anti-pattern, implementation]
---

## Input
"生成一页幻灯片：背景是彩色渐变 + 一些预设装饰性几何方块，中间一个大标题。"

## Expected Output (all true)
- [ ] 装饰性几何图形用 DOM/SVG，不用 canvas
- [ ] 背景用 CSS linear-gradient，不用 canvas
- [ ] 标题和 audience-visible copy 保持为 DOM/SVG text 或等价可检查文本，不画进整页 canvas
- [ ] 若使用 canvas，只能用于非关键、可冻结或可稳定的局部视觉层
