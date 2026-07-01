---
name: 视觉快照确定性
description: 视觉捕获前确保 frame 进入 deterministic frozen/snapshot state
difficulty: high
tags: [test, determinism]
---

## Input (code audit)
"检查视觉快照测试的 freeze 逻辑"

## Expected Output (all true)
- [ ] 视觉捕获前启用 frozen、snapshot、test mode 或等价确定性渲染机制
- [ ] CSS animation、transition、timer、clock、random、SVG draw-line、media/canvas/live widget 等会影响画面的状态被停止、固定或稳定
- [ ] 捕获的是指定 scene/beat 的 settled end state，而不是入口动画中间态
- [ ] 机制不绑定特定测试库、常量名或函数名
- [ ] 如采用 CSS 注入冻结，不应粗暴破坏项目用于定相位的合法 animation timing
