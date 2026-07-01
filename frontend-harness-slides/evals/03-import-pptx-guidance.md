---
name: PPTX 导入指引
description: 用户提供 PPTX 或旧 deck 时，将其作为内容源抽取并重建，而不是绑定具体抽取脚本
difficulty: low
tags: [import, guidance]
---

## Input
"我手头有个 source.pptx，20 多页，能不能把内容转换成你们的幻灯片项目？"

## Expected Output (all true)
- [ ] 建议使用当前可用的 PPTX/旧 deck 抽取方式，必要时说明低保真 fallback
- [ ] 说明目标抽取字段：页序、标题、文本块、图片、可选讲稿/备注
- [ ] 说明导入后应重建为 fixed-stage deck，不盲目保留原始绝对位置
- [ ] 说明图片、字体、speaker notes 等应进入项目资产、规划或 presenter material，不默认直接搬到 slide surface
- [ ] 建议先形成 narrative/registry draft，再写 scene code
