# Frontend Harness Slides

**[English](README.md)**

用**严谨的前端工程化思维**来制作 Slides。将你的演示文稿视为一个高标准、完全可测试的 Web 应用程序，并配套完善的自动化测试与验证 Harness 框架。

单体 HTML 很适合快速出第一版草稿。真正的噩梦发生在多轮迭代中：用户要求修改某页文案、调整动画节奏、更新图表或重构排版。在单体文件里，一个小小的 CSS 或脚本改动可能会意外破坏其他页面，而这种视觉回归（Regression）在没有自动化测试的情况下，往往直到现场演示时才会暴露。

`frontend-harness-slides` 将幻灯片制作变成一个**有工程保障、怎么改都改不坏的流水线**。它提供了一套框架无关的 Harness 契约：稳定帧地址、中心化注册表、固定舞台几何（Stage）、确定性冻结模式，以及自动化的布局与交互断言。

---

## 🛡️ 核心工程支柱 (怎么改都改不坏)

*   **完善的测试 Harness**：内置自动化回归测试（如 Playwright/Vitest），可在本地或 CI/CD 中一键运行，确保每次修改代码时，**绝对不会悄悄破坏其他页面**。
*   **稳定帧地址**：幻灯片的每一页、每一个交互 Beat 都是一个可独立路由、独立测试的单元。修改单页对其他页面没有任何副作用。
*   **固定舞台几何**：每页都在固定比例舞台（如 16:9）内编排并整体缩放。彻底杜绝因屏幕尺寸不同而导致的文字溢出、重叠或排版坍塌。
*   **确定性冻结模式**：一键冻结所有入场/出场动画、CSS 过渡、定时器和随机值，让 100% 稳定的视觉回归测试（Snapshot Testing）成为可能。
*   **交互事件隔离**：自定义交互组件（如拖拽旋钮、文本输入框）的事件被严格隔离，阻止冒泡，绝不误触发全局翻页。

---

## 🛡️ Harness 测试用例 (精简测试断言)

使用本技能构建的每套 Slides 都是一个可测试的 Web App。以下是一个精简、高价值的 Playwright 测试用例，可自动捕获所有幻灯片的布局破损、内容溢出和运行时异常：

```javascript
// test/slides.spec.ts
import { test, expect } from '@playwright/test';

test('验证所有幻灯片渲染正常，无内容溢出与控制台错误', async ({ page }) => {
  // 1. 获取集中管理的幻灯片注册表 (Registry)
  const scenes = await page.evaluate(() => window.SLIDE_REGISTRY);

  for (const scene of scenes) {
    // 2. 在确定性冻结模式下，导航到独立的幻灯片单页路由
    await page.goto(`/frame/${scene.id}?frozen=true`);

    // 3. 断言没有未捕获的控制台错误
    expect(page.errors).toHaveLength(0);

    // 4. 断言幻灯片内容没有溢出固定的 16:9 舞台边界
    const hasOverflow = await page.evaluate(() => {
      const stage = document.getElementById('stage');
      return stage.scrollHeight > stage.clientHeight || stage.scrollWidth > stage.clientWidth;
    });
    expect(hasOverflow).toBe(false);
  }
});
```

### 终端测试输出
```text
$ npm run test:slides

  ✓ [Scene 01: Intro] Passed (No overflow, 0 console errors)
  ✓ [Scene 02: Architecture] Passed (No overflow, 0 console errors)
  ✓ [Scene 03: Performance Table] Passed (No overflow, 0 console errors)

  Test Suites: 1 passed, 1 total
  Tests:       24 passed, 24 total
  Snapshots:   24 matched, 24 total
  Time:        4.82 s
  Active filters: stage-boundary, event-isolation, frozen-determinism
```

---

## 📺 视觉风格画廊

我们极力反对僵硬套用同一个模板。本技能倡导 **“单风格系统，多版式组合”**。排版完全由内容的语义结构驱动，并在三个信息密度带（低、中、高）之间流畅伸缩。

以下是从风格库中精选的 6 个代表性风格。点击任意风格可查看其详细的设计配方，或探索完整风格库。

### 🟢 Minimal Keynote (演讲展示流 - 极致表达)

#### [Style 06: Blackboard Chalk Talk (黑板粉笔)](references/style/minimal-keynote.md#style-06-blackboard-chalk-talk)
*手绘、教学、推理导向。在深绿色黑板上使用粉笔线条和公式，极具物理质感。*
*   **演示题材**：*《量子计算的基本原理》*
<p align="center">
  <img src="references/style/screenshots/style-06-low.webp" width="32%" alt="低密度：核心公式" />
  <img src="references/style/screenshots/style-06-med.webp" width="32%" alt="中密度：推导流程" />
  <img src="references/style/screenshots/style-06-high.webp" width="32%" alt="高密度：量子便当" />
</p>

#### [Style 02: Sketch Board Emoji (手绘工作坊)](references/style/minimal-keynote.md#style-02-sketch-board-emoji)
*温暖、亲切、人机协作。强调实体贴纸、半透明胶带和 Emoji 演员。*
*   **演示题材**：*《离线优先同步引擎设计》*
<p align="center">
  <img src="references/style/screenshots/style-02-low.webp" width="32%" alt="低密度：为何离线优先" />
  <img src="references/style/screenshots/style-02-med.webp" width="32%" alt="中密度：同步时间轴" />
  <img src="references/style/screenshots/style-02-high.webp" width="32%" alt="高密度：策略便当" />
</p>

---

### 🟡 Balanced Hybrid (路演与混合阅读)

#### [Style 13: Subway Map of Intent (意图地铁图)](references/style/balanced-hybrid.md#style-13-transit-flow-subway-map)
*系统化、整洁、高度结构化。将复杂的并行工作流抽象为地铁线路与换乘站。*
*   **演示题材**：*《分布式系统中的请求生命周期》*
<p align="center">
  <img src="references/style/screenshots/style-13-low.webp" width="32%" alt="低密度：数据包之旅" />
  <img src="references/style/screenshots/style-13-med.webp" width="32%" alt="中密度：地铁线路图" />
  <img src="references/style/screenshots/style-13-high.webp" width="32%" alt="高密度：时刻表便当" />
</p>

#### [Style 16: Debug Reaction Board (诊断看板)](references/style/balanced-hybrid.md#style-16-diagnostic-kanban-board)
*开发者原生、诊断性、行动导向。使用发光的霓虹状态徽章和等宽终端排版。*
*   **演示题材**：*《微服务健康状况自检》*
<p align="center">
  <img src="references/style/screenshots/style-16-low.webp" width="32%" alt="低密度：系统就绪" />
  <img src="references/style/screenshots/style-16-med.webp" width="32%" alt="中密度：自检流水线" />
  <img src="references/style/screenshots/style-16-high.webp" width="32%" alt="高密度：风险看板" />
</p>

---

### 🔵 Text Report (异步阅读与高密文档)

#### [Style 18: Maintainer Issue Brief (维护者工单)](references/style/text-report.md#style-18-developer-ticket-brief)
*整洁、结构化、行动导向。灵感源自现代开源工单系统和代码审查工具。*
*   **演示题材**：*《数据库连接池耗尽事故复盘》*
<p align="center">
  <img src="references/style/screenshots/style-18-low.webp" width="32%" alt="低密度：工单头部" />
  <img src="references/style/screenshots/style-18-med.webp" width="32%" alt="中密度：事故时间轴" />
  <img src="references/style/screenshots/style-18-high.webp" width="32%" alt="高密度：代码审查 Diff" />
</p>

#### [Style 21: Field Notes Report (实地调研笔记)](references/style/text-report.md#style-21-field-notes-report)
*触觉感、观察性、文学感。使用温暖的账簿纸、木炭墨水和拍立得式的卡片网格。*
*   **演示题材**：*《智能家居用户体验实地调研》*
<p align="center">
  <img src="references/style/screenshots/style-21-low.webp" width="32%" alt="低密度：调研封面" />
  <img src="references/style/screenshots/style-21-med.webp" width="32%" alt="中密度：用户旅程图" />
  <img src="references/style/screenshots/style-21-high.webp" width="32%" alt="高密度：观察网格" />
</p>

<p align="center">
  <a href="references/style/preview.zh-CN.md"><b>👉 前往完整风格预览指南，探索全部 24 个风格 →</b></a>
  <br />
  <a href="https://harness-slides-24-styles.vercel.app/"><b>🖥️ 立即体验在线风格预览工作台 →</b></a>
</p>

---

## 安装

```bash
npx skills add patrick-fu/frontend-harness-slides
```

后续更新：

```bash
npx skills update
```

---

## Agent 怎么使用

1.  **规划 (Plan)**：和用户对齐内容、演讲形式、技术栈和交付方式。确立“构建前对齐硬关卡”，并将决策记录在 context 文档中。
2.  **设计 (Design)**：从 24 风格库中挑选 2-3 个对比鲜明的风格进行推荐。构建交互式预览，捕获截图，并记录 selected theme notes。
3.  **实现 (Build)**：实现稳定的 scene、registry、固定舞台缩放，以及事件隔离的交互组件。
4.  **验证与交付 (Verify & Ship)**：运行自动化布局/交互测试，进行人工视觉 smoke 检查，部署上线或导出为 PDF。

---

## 阶段 Reference

确认是非小型 deck 制作或大改后，Agent 必须按顺序阅读：

| 文件 | 用途 |
|---|---|
| `references/01-plan.md` | 构建前对齐硬关卡、技术栈选择、Context 跟踪和内容注册表。 |
| `references/style/index.md` | 风格索引、24 个风格方向，以及语义到视觉的映射协议。 |
| `references/style/preview.zh-CN.md` | **完整风格预览指南**（收录全部 24 个风格，配有 3 图渐进线）。 |
| `references/02-design.md` | 风格预览、版式多样化、导航设计、字体/CJK 和素材管理。 |
| `references/03-build.md` | 稳定帧、注册表、固定舞台、冻结模式和交互事件隔离。 |
| `references/04-verify-and-ship.md` | 审计配置、视觉 smoke、视口压力审计和 PDF/静态交付。 |

---

## 什么时候适合

当 slides 不是很小的一次性静态页面，后续可能会收反馈、调动画、改结构、用到截图/图表，或者需要在交付前确认每一帧没有被改坏时，用它。

如果只是非常小的静态一次性页面，单体 HTML 已经足够，而且不需要任何回归 harness，那就没必要上这套工程。

---

## 更多 Skills

更多可复用的 agent skills，见 [Awesome Skills](https://github.com/patrick-fu/awesome-skills)。
