---
name: 整页 canvas 渲染检测
description: 禁止用 canvas 画整页静态内容
difficulty: medium
tags: [anti-pattern, implementation]
---

## Input
"生成一页幻灯片：背景是彩色渐变 + 一些装饰性几何方块（10 个，随机大小颜色），中间一个大标题。"

## Expected Output (any true)
- [ ] 装饰性几何图形用 DOM/SVG，不用 canvas
- [ ] 背景用 CSS linear-gradient，不用 canvas
- [ ] 没有任何 <canvas> 元素
