# frontend-harness-slides

工程化幻灯片生成 Skill — 面向 ≥15 页、需要多轮迭代、团队协作或 CI 视觉回归测试的幻灯片项目。

## 与其他 slides skills 的边界

| Skill | 适用场景 | 产出 |
|-------|---------|------|
| **frontend-harness-slides**（本） | ≥15 页、需要 CI/review、多轮迭代 | React + Vite + Playwright + PDF |
| [frontend-slides](../../frontend-slides) | <10 页、一次性交付、零构建 | 单文件 HTML（React+Babel CDN） |
| [lark-slides](../../lark-slides) | 需要飞书原生编辑/分享/评论 | 飞书幻灯片文档 |

## 快速开始

```bash
npx skills add frontend-harness-slides
# 然后按 SKILL.md 的 Phase 0 → Phase I → ... 执行
```

## 文档入口

- **SKILL.md**：完整工作流 + 使用规范（用户必读）
- **`assets/starter/`**：工程脚手架（React + Vite + Tailwind + Playwright）
- **`references/`**：主题、字体、无障碍、部署等专项文档

## 测试与 CI

```bash
cd assets/starter
npm install
npm run test:auditor   # 结构审计（beat 正确、无 0×0、无溢出）
npm run test:visual    # 视觉快照对比
npm run export:pdf     # 导出 1920×1080 PDF
```

## Related Skills

- [stop-slop](../../stop-slop)
- [humanizer](../../humanizer)
- [design-taste-frontend](../../design-taste-frontend)
- [aero-mint-glass-html-design](../../aero-mint-glass-html-design)
