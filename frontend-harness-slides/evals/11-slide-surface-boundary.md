---
name: slide-surface-boundary
description: 用户 brief 中的时长、风格、stage 和部署信息不能被默认写到 slides 画布上
difficulty: medium
tags: [copy-boundary, registry, planning-metadata]
---

## Input
"把这份 AI coding 材料做成 40 分钟现场演讲用的 slides，低文字密度，黑白灰手绘 emoji 风格，1920x1080，支持手机 swipe，最后部署到 Vercel。"

## Expected Output (all true)
- [ ] 不直接开始写页面代码；先整理已给约束，并追问或确认缺失的 minimum decisions / 素材内容
- [ ] 若产出 registry draft，则包含 `visible_copy`、`speaker_intent`、`beats`、`visual_idea`，并把时长、stage、触屏、部署等放入内部约束
- [ ] 明确说明 `40 分钟`、`1920x1080`、`Vercel`、`手机 swipe` 这些是规划/实现信息，默认不写到 slide 标题、副标题或可见正文里
- [ ] `visible_copy` 只包含观众应看到的标题、短句或标签
- [ ] 仍然保留用户给出的风格方向：低文字密度、黑白灰手绘、emoji 视觉元素；动效方向作为推荐项继续确认
