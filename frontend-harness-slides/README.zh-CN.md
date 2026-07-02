# Frontend Harness Slides

**[English](README.md)**

制作更灵动、可交互、能部署，而且经得起多轮修改的 HTML slides。

这个 Skill 会引导 Agent 在写代码前先对齐受众、内容密度、视觉风格、动效、导航、交付方式
和部署目标。进入实现后，它会把 slides 当作一个小型 Web 应用来做：每个 scene 可以单独
访问，交互可以测试，截图可以稳定复现，最终可以部署成线上页面、导出 PDF，或者两者都做。

> 在线演示：在 [Style Preview Workbench](https://harness-slides-24-styles.vercel.app/)
> 里查看全部 24 个视觉风格和不同信息密度。

## 适合什么场景

- 需要动效、节奏和互动 beat 的现场演讲。
- 产品 walkthrough、教学课件、技术解释型 slides。
- 用户对视觉和修改精度要求高，后续还会反复改的 deck。
- 需要本地预览，也需要明确交付路径的项目，比如线上部署、PDF 导出，或两者兼顾。

如果只是非常小的一次性静态页面，单个 HTML 文件通常就够了。这个 Skill 更适合设计质量、
多轮迭代和交付检查都比较重要的 slides。

## 视觉风格画廊

这套风格系统不是让每一页套同一个模板。它更强调在一个统一风格里，根据内容语义切换版式、
动效、交互方式和出现节奏。

完整目录包含 24 个风格，覆盖演讲展示、混合阅读和高密度文档三类。下面是 6 个代表例子。

### Minimal keynote

#### [Style 06: Blackboard chalk talk](references/style/minimal-keynote.md#style-06-blackboard-chalk-talk)

手绘、教学、推理导向。用深绿色黑板、粉笔线条和公式来呈现推导过程。

题材：*量子计算的基本原理*

<p align="center">
  <img src="references/style/screenshots/style-06-low.webp" width="32%" alt="低密度：核心公式" />
  <img src="references/style/screenshots/style-06-med.webp" width="32%" alt="中密度：推导流程" />
  <img src="references/style/screenshots/style-06-high.webp" width="32%" alt="高密度：量子便当" />
</p>

#### [Style 02: Sketch board emoji](references/style/minimal-keynote.md#style-02-sketch-board-emoji)

温暖、亲切，有人参与感。常用便利贴、胶带、emoji 角色和小型交互细节。

题材：*离线优先同步引擎设计*

<p align="center">
  <img src="references/style/screenshots/style-02-low.webp" width="32%" alt="低密度：为什么离线优先" />
  <img src="references/style/screenshots/style-02-med.webp" width="32%" alt="中密度：同步时间线" />
  <img src="references/style/screenshots/style-02-high.webp" width="32%" alt="高密度：策略便当" />
</p>

### Balanced hybrid

#### [Style 13: Subway map of intent](references/style/balanced-hybrid.md#style-13-transit-flow-subway-map)

系统化、结构清楚。把复杂工作流表现成地铁线路和换乘站。

题材：*分布式请求的生命周期*

<p align="center">
  <img src="references/style/screenshots/style-13-low.webp" width="32%" alt="低密度：数据包旅程" />
  <img src="references/style/screenshots/style-13-med.webp" width="32%" alt="中密度：地铁线路图" />
  <img src="references/style/screenshots/style-13-high.webp" width="32%" alt="高密度：时刻表便当" />
</p>

#### [Style 16: Debug reaction board](references/style/balanced-hybrid.md#style-16-diagnostic-kanban-board)

开发者原生、偏诊断。使用霓虹状态标记、终端界面和行动看板。

题材：*微服务健康状况自检*

<p align="center">
  <img src="references/style/screenshots/style-16-low.webp" width="32%" alt="低密度：系统就绪" />
  <img src="references/style/screenshots/style-16-med.webp" width="32%" alt="中密度：自检流水线" />
  <img src="references/style/screenshots/style-16-high.webp" width="32%" alt="高密度：风险看板" />
</p>

### Text report

#### [Style 18: Maintainer issue brief](references/style/text-report.md#style-18-developer-ticket-brief)

整洁、结构化、行动导向。灵感来自现代 issue tracker 和代码审查工具。

题材：*数据库连接池耗尽事故复盘*

<p align="center">
  <img src="references/style/screenshots/style-18-low.webp" width="32%" alt="低密度：工单头部" />
  <img src="references/style/screenshots/style-18-med.webp" width="32%" alt="中密度：事故时间线" />
  <img src="references/style/screenshots/style-18-high.webp" width="32%" alt="高密度：代码审查 diff" />
</p>

#### [Style 21: Field notes report](references/style/text-report.md#style-21-field-notes-report)

有纸张触感，偏观察记录。使用账簿纸、木炭墨水和卡片网格。

题材：*智能家居用户体验实地调研*

<p align="center">
  <img src="references/style/screenshots/style-21-low.webp" width="32%" alt="低密度：调研封面" />
  <img src="references/style/screenshots/style-21-med.webp" width="32%" alt="中密度：用户旅程图" />
  <img src="references/style/screenshots/style-21-high.webp" width="32%" alt="高密度：观察网格" />
</p>

<p align="center">
  <a href="references/style/preview.zh-CN.md"><b>查看完整 24 风格预览指南</b></a>
  <br />
  <a href="https://harness-slides-24-styles.vercel.app/"><b>体验在线风格预览工作台</b></a>
</p>

## 为什么后续修改不容易坏

这个 Skill 不建议让 Agent 写一个巨大的 HTML 文件然后赌它能扛住反馈。它会在 deck 周围加
一层轻量 harness：

- 开工前对齐风格、受众、密度、舞台尺寸、技术栈和交付方式；
- 保持 scene 和 beat 地址稳定，方便单独检查某一页或某一步；
- 在固定比例舞台内渲染，确保内容不溢出 slides 画布；
- 提供 frozen mode，让截图和视觉检查可以稳定复现；
- 隔离自定义交互，避免输入、拖拽和点击误触发翻页；
- 做有意义的布局、交互、截图、导出和部署检查。

## 安装

```bash
npx skills add patrick-fu/frontend-harness-slides -g
```

后续更新：

```bash
npx skills update -g
```

## Agent 怎么使用

1. Plan：对齐内容、受众、演示形式、风格方向、技术栈、交付目标，以及是否先做风格预览。
2. Design：确定统一的风格系统，同时让不同 scene 在版式、动效和交互形式上有变化。
3. Build：实现稳定 scene、registry、固定舞台缩放、frozen mode、键盘导航和事件隔离交互。
4. Verify and ship：运行有实际价值的布局和交互检查，查看截图，本地预览，然后部署线上、
   导出 PDF，或两者都交付。

## Agent references

确认是非小型 deck 制作或大改后，Agent 应按顺序阅读：

| 文件 | 用途 |
|---|---|
| `references/01-plan.md` | 需求对齐、风格确认、技术栈选择、Context 跟踪和内容注册表。 |
| `references/style/index.md` | 风格方向和语义到视觉的映射方式。 |
| `references/style/preview.zh-CN.md` | 完整风格预览指南，包含 24 个风格和密度示例。 |
| `references/02-design.md` | 风格预览、版式变化、导航、字体和素材。 |
| `references/03-build.md` | 稳定帧、注册表、固定舞台、frozen mode 和事件隔离。 |
| `references/04-verify-and-ship.md` | 视觉检查、视口压力检查、部署、PDF 导出和交付。 |

## 更多 Skills

更多可复用 Agent Skills 见
[Awesome Skills](https://github.com/patrick-fu/awesome-skills)。
