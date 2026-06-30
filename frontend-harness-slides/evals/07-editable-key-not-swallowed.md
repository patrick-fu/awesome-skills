---
name: input 里的键盘事件不被吞
description: 生成的代码在 editable 元素聚焦时不拦截 space/arrow
difficulty: high
tags: [bug-free, implementation]
---

## Input (code audit)
"查看生成的 deck 导航键盘事件处理逻辑"

## Expected Output (all true)
- [ ] keydown listener 开头有 editable 元素白名单判断（tag INPUT/TEXTAREA/isContentEditable 等）
- [ ] 自定义交互区域有明确事件隔离边界，不依赖某个框架的合成事件冒泡
