---
name: input 里的键盘事件不被吞
description: 生成的代码在 editable 元素聚焦时不拦截 space/arrow
difficulty: high
tags: [bug-free, implementation]
---

## Input (code audit)
"查看生成的 SlideDeck.tsx 中键盘事件处理逻辑"

## Expected Output (all true)
- [ ] keydown listener 开头有 editable 元素白名单判断（tag INPUT/TEXTAREA/isContentEditable 等）
- [ ] 如果存在 SandboxIsolator，它的实现是原生 capture 阶段监听（而不是 React 合成层 stopPropagation）
