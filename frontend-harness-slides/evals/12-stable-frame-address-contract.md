---
name: stable-frame-address-contract
description: Harness-backed decks should make each meaningful scene/beat directly addressable and enumerable without binding to one URL format.
difficulty: high
tags: [harness, addressability, registry]
---

## Input
"这个 deck 会反复改动画和文案，请建立一个可回归检查的 HTML slides harness。"

## Expected Output (all true)
- [ ] 每个 scene 有稳定 id，且 id 不依赖可见标题、文件名或数组位置
- [ ] 每个 meaningful beat、frame state 或等价状态可被直接打开
- [ ] 直达机制可以是 query、hash、route、state file 或项目等价方案，不强制 `?scene=`
- [ ] 有 registry、manifest、route table 或等价 source of truth 可枚举 scene order 和 beat/frame count
- [ ] 测试或截图工具不需要抓取可见文本来推断当前 frame
- [ ] frozen/snapshot/test mode 能渲染请求 frame 的 settled state
