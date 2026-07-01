---
name: input 里的键盘事件不被吞
description: 生成的导航逻辑在 editable 或自定义交互区域聚焦时不误触发 slide navigation
difficulty: high
tags: [bug-free, implementation]
---

## Input (code audit)
"查看生成的 deck 导航键盘事件处理逻辑"

## Expected Output (all true)
- [ ] 全局导航执行前有 editable、focusable、自定义交互区域 guard，或等价事件路由机制
- [ ] editable 聚焦时 Space/Arrow 不改变当前 scene/beat
- [ ] Stage 或 slide surface 聚焦时 Space/Arrow 仍按预期一步导航
- [ ] repeated keydown 不意外跳过多个 beat，除非项目显式支持
- [ ] 若支持 tap、touch、click 或 pointer 导航，一次物理输入不会因事件重复触发而前进多步
- [ ] 自定义交互区域有明确事件隔离边界，不只依赖某个框架的合成事件冒泡
