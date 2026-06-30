---
name: PPTX 导入指引
description: 用户提了 PPTX 源文件时，给 extract-pptx.py 具体可复制命令
difficulty: low
tags: [import, guidance]
---

## Input
"我手头有个 source.pptx，20 多页，能不能把内容转换成你们的幻灯片项目？"

## Expected Output (all true)
- [ ] 建议使用可用的 PPTX 抽取工具，或说明 fallback 为 unzip PPTX 后解析 `ppt/slides/slideN.xml`
- [ ] 说明目标抽取字段：页序、标题、文本块、图片、可选讲稿/备注
- [ ] 说明导入后需要重做布局（不保留原始位置）
- [ ] 说明图片/字体要走 Asset Prep
