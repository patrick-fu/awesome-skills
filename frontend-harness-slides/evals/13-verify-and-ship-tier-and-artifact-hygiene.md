---
name: verify-and-ship-tier-and-artifact-hygiene
description: Final delivery should choose relevant verification tiers and avoid shipping local test artifacts by accident.
difficulty: high
tags: [verification, delivery, artifact-hygiene]
---

## Input
"slides 已经做完了，准备上线并交付给用户。"

## Expected Output (all true)
- [ ] 根据项目风险选择 relevant final checks，而不是机械运行最重或最轻的一套
- [ ] 至少考虑 structural audit、visual smoke、interaction/mobile coverage、production smoke 中和本 deck 相关的部分
- [ ] 如果有检查被跳过，明确说明跳过项和残留风险，不能默认当作通过
- [ ] production smoke 打开真实线上 URL 或最终交付入口，不只看部署平台显示 READY
- [ ] 检查或提醒 direct frame、基础导航、移动可见性、字体/图片/console/request failure 等关键交付风险
- [ ] 部署或静态交付前，确认本地截图、audit artifacts、test reports、临时导出、cache、local build output 等不会被误发布，除非项目明确有意公开
