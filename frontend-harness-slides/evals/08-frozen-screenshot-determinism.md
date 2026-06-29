---
name: 视觉快照确定性
description: 截图前确保动画暂停、相位固定
difficulty: high
tags: [test, determinism]
---

## Input (code audit)
"检查视觉快照测试的 freeze 逻辑"

## Expected Output (all true)
- [ ] FREEZE_CSS 中存在 `animation-play-state: paused !important`
- [ ] FREEZE_CSS **不**覆盖 `animation-delay`（不破坏负 delay 定相位意图）
- [ ] 在 page.screenshot() 之前调用了 freeze 逻辑（或 beforeEach）
- [ ] 有 `waitForAnimationsToSettle` 或等价的「等稳定」函数
