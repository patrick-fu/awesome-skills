# Frontend Harness Slides

**[English](README.md)**

用前端工程化 harness 制作 HTML slides，让 deck 能扛住真实的多轮修改。

单体 HTML 很适合快速出第一版。但当 slides 变大、需要精调某一页，或者反复修改 CSS、动画
和布局时，一个小改动很容易悄悄影响其他页面。这个 Skill 主要解决的就是这个阶段的问题。

它的核心优势不只是做出更漂亮的 slides，而是把 deck 当成一个可测试的小型 Web 应用：scene
可以稳定访问，交互可以隔离，截图可以复现，最终可以部署成线上页面、导出 PDF，或者两者
都交付。

## Live preview

> 🖥️ 体验 Vercel 实时 Workbench：
> [动态风格预设预览](https://frontend-harness-slides-demo.vercel.app/)。
> 这是查看动效、信息密度和视觉范围最快的方式，比只读说明更直观。

## 为什么 harness 更重要

很多 slides 工具都能做出好看的第一版。真正困难的是 deck 变大、反馈变多以后，怎么继续
精修而不把其他页面改坏。`frontend-harness-slides` 会在 deck 周围加一层轻量工程框架：

- 稳定的 scene 和 beat 地址，方便直接打开任意页面或状态；
- registry 作为目录，让工具不需要靠抓取可见文字来理解 deck；
- 固定比例 stage，确保内容留在 slides 画布内；
- frozen mode，让截图和视觉检查可以稳定复现；
- 交互事件隔离，避免点击、拖拽、输入框和 tooltip 误触发全局翻页；
- 有意义的测试和 smoke checks，在交付前发现内容缺失、溢出、运行错误和导航泄漏。

视觉风格仍然重要。但这里的关键差异是：风格下面有一套能被编辑、测试、部署和导出的 deck
结构。

## 适合什么场景

- 需要动效、节奏和互动 beat 的现场演讲。
- 产品 walkthrough、教学课件、技术解释型 slides。
- 用户对视觉和修改精度要求高，后续还会反复改的 deck。
- 需要本地预览，也需要明确交付路径的项目，比如线上部署、PDF 导出，或两者兼顾。

如果只是非常小的一次性静态页面，单个 HTML 文件通常就够了。这个 Skill 更适合设计质量、
多轮迭代和交付检查都比较重要的 slides。

## 模型选择建议

做视觉型 slides 时，模型的前端审美很重要。我通常建议优先使用 Gemini，其次是 Claude。
GPT 5.5 也能做，我也针对它做过几轮提示和流程优化，但从我的实际测试看，它通常比 Gemini
更需要明确的视觉指导。

## 视觉风格画廊

> 📚 预览全部风格：[风格目录](references/style/preview.zh-CN.md)

这套风格系统不是让每一页套同一个模板。它更强调在一个统一风格里，根据内容语义切换版式、
动效、交互方式和出现节奏。

完整目录包含多种风格预设，覆盖演讲展示、混合阅读和高密度文档三类。下面是 6 个代表例子。

### Minimal keynote

#### [Style 06: Blackboard chalk talk](references/style/minimal-keynote.md#style-06-blackboard-chalk-talk)

手绘、教学、推理导向。用深绿色黑板、粉笔线条和公式来呈现推导过程。

<p align="center">
  <img src="references/style/screenshots/style-06-low.webp" width="32%" alt="低密度：核心公式" />
  <img src="references/style/screenshots/style-06-med.webp" width="32%" alt="中密度：推导流程" />
  <img src="references/style/screenshots/style-06-high.webp" width="32%" alt="高密度：量子便当" />
</p>

#### [Style 02: Sketch board emoji](references/style/minimal-keynote.md#style-02-sketch-board-emoji)

温暖、亲切，有人参与感。常用便利贴、胶带、emoji 角色和小型交互细节。

<p align="center">
  <img src="references/style/screenshots/style-02-low.webp" width="32%" alt="低密度：为什么离线优先" />
  <img src="references/style/screenshots/style-02-med.webp" width="32%" alt="中密度：同步时间线" />
  <img src="references/style/screenshots/style-02-high.webp" width="32%" alt="高密度：策略便当" />
</p>

### Balanced hybrid

#### [Style 13: Subway map of intent](references/style/balanced-hybrid.md#style-13-transit-flow-subway-map)

系统化、结构清楚。把复杂工作流表现成地铁线路和换乘站。

<p align="center">
  <img src="references/style/screenshots/style-13-low.webp" width="32%" alt="低密度：数据包旅程" />
  <img src="references/style/screenshots/style-13-med.webp" width="32%" alt="中密度：地铁线路图" />
  <img src="references/style/screenshots/style-13-high.webp" width="32%" alt="高密度：时刻表便当" />
</p>

#### [Style 16: Debug reaction board](references/style/balanced-hybrid.md#style-16-diagnostic-kanban-board)

开发者原生、偏诊断。使用霓虹状态标记、终端界面和行动看板。

<p align="center">
  <img src="references/style/screenshots/style-16-low.webp" width="32%" alt="低密度：系统就绪" />
  <img src="references/style/screenshots/style-16-med.webp" width="32%" alt="中密度：自检流水线" />
  <img src="references/style/screenshots/style-16-high.webp" width="32%" alt="高密度：风险看板" />
</p>

### Text report

#### [Style 18: Maintainer issue brief](references/style/text-report.md#style-18-developer-ticket-brief)

整洁、结构化、行动导向。灵感来自现代 issue tracker 和代码审查工具。

<p align="center">
  <img src="references/style/screenshots/style-18-low.webp" width="32%" alt="低密度：工单头部" />
  <img src="references/style/screenshots/style-18-med.webp" width="32%" alt="中密度：事故时间线" />
  <img src="references/style/screenshots/style-18-high.webp" width="32%" alt="高密度：代码审查 diff" />
</p>

#### [Style 21: Field notes report](references/style/text-report.md#style-21-field-notes-report)

有纸张触感，偏观察记录。使用账簿纸、木炭墨水和卡片网格。

<p align="center">
  <img src="references/style/screenshots/style-21-low.webp" width="32%" alt="低密度：调研封面" />
  <img src="references/style/screenshots/style-21-med.webp" width="32%" alt="中密度：用户旅程图" />
  <img src="references/style/screenshots/style-21-high.webp" width="32%" alt="高密度：观察网格" />
</p>

<p align="center">
  <a href="https://frontend-harness-slides-demo.vercel.app/"><b>🎬 动态 Demo</b></a>
  &nbsp;|&nbsp;
  <a href="references/style/preview.zh-CN.md"><b>📚 预览全部风格</b></a>
</p>

## 安装

```bash
npx skills add patrick-fu/frontend-harness-slides -g
```

后续更新：

```bash
npx skills update -g
```

## 典型流程

1. Plan：对齐内容、受众、演示形式、风格方向、技术栈、交付目标，以及是否先做风格预览。
2. Design：确定统一的风格系统，同时让不同 scene 在版式、动效和交互形式上有变化。
3. Build：创建稳定的 slide scene，配套键盘导航、交互元素、可复现预览和保护后续修改的测试。
4. Verify and ship：运行有实际价值的布局和交互检查，查看截图，本地预览，然后部署线上、
   导出 PDF，或两者都交付。

## 我的更多精选 Skill

更多我长期维护、偏实战的精选 Agent Skills，见
[Awesome Skills](https://github.com/patrick-fu/awesome-skills)。
