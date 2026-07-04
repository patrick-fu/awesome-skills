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

## 安装

✨ 推荐：把当前页面链接复制给你的 Agent，然后说：`Please install this for me.`

```bash
npx skills add patrick-fu/frontend-harness-slides -g
```

后续更新：

```bash
npx skills update -g
```

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

## 典型流程

1. Plan：对齐内容、受众、演示形式、风格方向、技术栈、交付目标，以及是否先做风格预览。
2. Design：确定统一的风格系统，同时让不同 scene 在版式、动效和交互形式上有变化。
3. Build：创建稳定的 slide scene，配套键盘导航、交互元素、可复现预览和保护后续修改的测试。
4. Verify and ship：运行有实际价值的布局和交互检查，查看截图，本地预览，然后部署线上、
   导出 PDF，或两者都交付。

## 视觉风格画廊

这套风格系统不是让每一页套同一个模板。它更强调在一个统一风格里，根据内容语义切换版式、
动效、交互方式和出现节奏。

完整画廊覆盖三类密度：Minimal Keynote、Balanced Hybrid、Text Report。每个风格都展示
低、中、高三种密度示例。

### Minimal keynote

#### [Minimal Product Keynote](references/style/minimal-product-keynote.md)

高级、聚焦、稀疏。适合开场判断、产品亮相和单句大观点。

<p align="center">
  <img src="showcase/style-gallery/minimal-product-keynote-low.webp" width="32%" alt="低密度：产品发布主画面" />
  <img src="showcase/style-gallery/minimal-product-keynote-medium.webp" width="32%" alt="中密度：产品发布结构" />
  <img src="showcase/style-gallery/minimal-product-keynote-high.webp" width="32%" alt="高密度：产品发布细节" />
</p>

#### [Sketch Board Emoji](references/style/sketch-board-emoji.md)

温暖、亲切，有人参与感。常用便利贴、胶带、emoji 角色和小型交互细节。

<p align="center">
  <img src="showcase/style-gallery/sketch-board-emoji-low.webp" width="32%" alt="低密度：为什么离线优先" />
  <img src="showcase/style-gallery/sketch-board-emoji-medium.webp" width="32%" alt="中密度：同步时间线" />
  <img src="showcase/style-gallery/sketch-board-emoji-high.webp" width="32%" alt="高密度：策略便当" />
</p>

#### [Interactive Dialogue Stage](references/style/interactive-dialogue-stage.md)

对话驱动，带一点剧场感。适合呈现两个角色、系统或说话方之间的轮流互动。

<p align="center">
  <img src="showcase/style-gallery/interactive-dialogue-stage-low.webp" width="32%" alt="低密度：对话开场" />
  <img src="showcase/style-gallery/interactive-dialogue-stage-medium.webp" width="32%" alt="中密度：双控制台" />
  <img src="showcase/style-gallery/interactive-dialogue-stage-high.webp" width="32%" alt="高密度：对话记录" />
</p>

#### [Kinetic Type Punchline](references/style/kinetic-type-punchline.md)

强烈、海报化、高能量。适合章节转折、强对比观点和需要被记住的金句。

<p align="center">
  <img src="showcase/style-gallery/kinetic-type-punchline-low.webp" width="32%" alt="低密度：动感短句" />
  <img src="showcase/style-gallery/kinetic-type-punchline-medium.webp" width="32%" alt="中密度：文字对比" />
  <img src="showcase/style-gallery/kinetic-type-punchline-high.webp" width="32%" alt="高密度：海报细节" />
</p>

#### [Object Metaphor Hero](references/style/object-metaphor-hero.md)

拟物、触感强、隐喻驱动。把准备、规划、工具箱这类抽象概念变成可看的物件。

<p align="center">
  <img src="showcase/style-gallery/object-metaphor-hero-low.webp" width="32%" alt="低密度：核心物件" />
  <img src="showcase/style-gallery/object-metaphor-hero-medium.webp" width="32%" alt="中密度：物件分区" />
  <img src="showcase/style-gallery/object-metaphor-hero-high.webp" width="32%" alt="高密度：工具箱布局" />
</p>

#### [Blackboard Chalk Talk](references/style/blackboard-chalk-talk.md)

手绘、教学、推理导向。用深绿色黑板、粉笔线条和公式来呈现推导过程。

<p align="center">
  <img src="showcase/style-gallery/blackboard-chalk-talk-low.webp" width="32%" alt="低密度：核心公式" />
  <img src="showcase/style-gallery/blackboard-chalk-talk-medium.webp" width="32%" alt="中密度：推导流程" />
  <img src="showcase/style-gallery/blackboard-chalk-talk-high.webp" width="32%" alt="高密度：量子便当" />
</p>

#### [Arcade Boss Fight](references/style/arcade-boss-fight.md)

复古、游戏化、带风险感。把技术挑战表达成 boss fight、HP 条和道具栏。

<p align="center">
  <img src="showcase/style-gallery/arcade-boss-fight-low.webp" width="32%" alt="低密度：战斗界面" />
  <img src="showcase/style-gallery/arcade-boss-fight-medium.webp" width="32%" alt="中密度：街机进度" />
  <img src="showcase/style-gallery/arcade-boss-fight-high.webp" width="32%" alt="高密度：道具栏" />
</p>

#### [Spotlight Quote Poster](references/style/spotlight-quote-poster.md)

戏剧化、沉思感。用暗场、聚光和大字号 quote 营造停顿、收束和哲学表达。

<p align="center">
  <img src="showcase/style-gallery/spotlight-quote-poster-low.webp" width="32%" alt="低密度：聚光 quote" />
  <img src="showcase/style-gallery/spotlight-quote-poster-medium.webp" width="32%" alt="中密度：quote 上下文" />
  <img src="showcase/style-gallery/spotlight-quote-poster-high.webp" width="32%" alt="高密度：quote 海报细节" />
</p>

### Balanced hybrid

#### [Signal Pipeline Flow](references/style/balanced-hybrid.md#signal-pipeline-flow)

技术化、精确。用节点、路由和发光箭头表现数据、信号或决策流。

<p align="center">
  <img src="showcase/style-gallery/signal-pipeline-flow-low.webp" width="32%" alt="低密度：信号入口" />
  <img src="showcase/style-gallery/signal-pipeline-flow-medium.webp" width="32%" alt="中密度：路由管线" />
  <img src="showcase/style-gallery/signal-pipeline-flow-high.webp" width="32%" alt="高密度：系统地图" />
</p>

#### [Mechanical Scoring Funnel](references/style/balanced-hybrid.md#mechanical-scoring-funnel)

有能量、偏评估。把筛选、评分和优先级表现成轨道、弹珠、分数和漏斗路径。

<p align="center">
  <img src="showcase/style-gallery/mechanical-scoring-funnel-low.webp" width="32%" alt="低密度：评分瞬间" />
  <img src="showcase/style-gallery/mechanical-scoring-funnel-medium.webp" width="32%" alt="中密度：漏斗轨道" />
  <img src="showcase/style-gallery/mechanical-scoring-funnel-high.webp" width="32%" alt="高密度：评分面板" />
</p>

#### [Collaborative Pairing Board](references/style/balanced-hybrid.md#collaborative-pairing-board)

清爽、协作导向。适合展示角色分工、同步点，以及人、团队或系统之间的配合。

<p align="center">
  <img src="showcase/style-gallery/collaborative-pairing-board-low.webp" width="32%" alt="低密度：协作观点" />
  <img src="showcase/style-gallery/collaborative-pairing-board-medium.webp" width="32%" alt="中密度：协作看板" />
  <img src="showcase/style-gallery/collaborative-pairing-board-high.webp" width="32%" alt="高密度：同步计划" />
</p>

#### [Studio Mixing Console](references/style/balanced-hybrid.md#studio-mixing-console)

专业、拟物。用推子、旋钮和电平表表现参数调节、噪音过滤和多因素平衡。

<p align="center">
  <img src="showcase/style-gallery/studio-mixing-console-low.webp" width="32%" alt="低密度：主信号" />
  <img src="showcase/style-gallery/studio-mixing-console-medium.webp" width="32%" alt="中密度：推子面板" />
  <img src="showcase/style-gallery/studio-mixing-console-high.webp" width="32%" alt="高密度：调音台细节" />
</p>

#### [Subway Map of Intent](references/style/balanced-hybrid.md#subway-map-of-intent)

系统化、结构清楚。把复杂工作流表现成地铁线路和换乘站。

<p align="center">
  <img src="showcase/style-gallery/subway-map-of-intent-low.webp" width="32%" alt="低密度：数据包旅程" />
  <img src="showcase/style-gallery/subway-map-of-intent-medium.webp" width="32%" alt="中密度：地铁线路图" />
  <img src="showcase/style-gallery/subway-map-of-intent-high.webp" width="32%" alt="高密度：时刻表便当" />
</p>

#### [Kitchen Prep Station](references/style/balanced-hybrid.md#kitchen-prep-station)

温暖、具体。把原始输入到干净输出的过程表现成备料台、修剪、菜谱步骤和摆盘。

<p align="center">
  <img src="showcase/style-gallery/kitchen-prep-station-low.webp" width="32%" alt="低密度：备料观点" />
  <img src="showcase/style-gallery/kitchen-prep-station-medium.webp" width="32%" alt="中密度：备料台" />
  <img src="showcase/style-gallery/kitchen-prep-station-high.webp" width="32%" alt="高密度：菜谱细节" />
</p>

#### [Context Bento Box](references/style/balanced-hybrid.md#context-bento-box)

紧凑、有组织。用分格和层叠盒子表达 handoff、多类别概览和上下文包装。

<p align="center">
  <img src="showcase/style-gallery/context-bento-box-low.webp" width="32%" alt="低密度：便当概念" />
  <img src="showcase/style-gallery/context-bento-box-medium.webp" width="32%" alt="中密度：便当分格" />
  <img src="showcase/style-gallery/context-bento-box-high.webp" width="32%" alt="高密度：层叠便当" />
</p>

#### [Debug Reaction Board](references/style/balanced-hybrid.md#debug-reaction-board)

开发者原生、偏诊断。使用霓虹状态标记、终端界面和行动看板。

<p align="center">
  <img src="showcase/style-gallery/debug-reaction-board-low.webp" width="32%" alt="低密度：系统就绪" />
  <img src="showcase/style-gallery/debug-reaction-board-medium.webp" width="32%" alt="中密度：自检流水线" />
  <img src="showcase/style-gallery/debug-reaction-board-high.webp" width="32%" alt="高密度：风险看板" />
</p>

### Text report

#### [Research Memo](references/style/text-report.md#research-memo)

克制、可信、有研究感。适合研究发现、高管摘要和需要自洽阅读的证据页面。

<p align="center">
  <img src="showcase/style-gallery/research-memo-low.webp" width="32%" alt="低密度：研究封面" />
  <img src="showcase/style-gallery/research-memo-medium.webp" width="32%" alt="中密度：研究备忘录" />
  <img src="showcase/style-gallery/research-memo-high.webp" width="32%" alt="高密度：证据页面" />
</p>

#### [Maintainer Issue Brief](references/style/text-report.md#maintainer-issue-brief)

整洁、结构化、行动导向。灵感来自现代 issue tracker 和代码审查工具。

<p align="center">
  <img src="showcase/style-gallery/maintainer-issue-brief-low.webp" width="32%" alt="低密度：工单头部" />
  <img src="showcase/style-gallery/maintainer-issue-brief-medium.webp" width="32%" alt="中密度：事故时间线" />
  <img src="showcase/style-gallery/maintainer-issue-brief-high.webp" width="32%" alt="高密度：代码审查 diff" />
</p>

#### [Decision Record](references/style/text-report.md#decision-record)

严谨、架构化。用 ADR 节奏呈现上下文、决策、权衡和验证。

<p align="center">
  <img src="showcase/style-gallery/decision-record-low.webp" width="32%" alt="低密度：决策标题" />
  <img src="showcase/style-gallery/decision-record-medium.webp" width="32%" alt="中密度：决策记录" />
  <img src="showcase/style-gallery/decision-record-high.webp" width="32%" alt="高密度：权衡矩阵" />
</p>

#### [Benchmark Matrix](references/style/text-report.md#benchmark-matrix)

分析型、比较型。强调结构化证据、评估标准、指标和表格化对比。

<p align="center">
  <img src="showcase/style-gallery/benchmark-matrix-low.webp" width="32%" alt="低密度：基准结论" />
  <img src="showcase/style-gallery/benchmark-matrix-medium.webp" width="32%" alt="中密度：指标网格" />
  <img src="showcase/style-gallery/benchmark-matrix-high.webp" width="32%" alt="高密度：对比矩阵" />
</p>

#### [Field Notes Report](references/style/text-report.md#field-notes-report)

有纸张触感，偏观察记录。使用账簿纸、木炭墨水和卡片网格。

<p align="center">
  <img src="showcase/style-gallery/field-notes-report-low.webp" width="32%" alt="低密度：调研封面" />
  <img src="showcase/style-gallery/field-notes-report-medium.webp" width="32%" alt="中密度：用户旅程图" />
  <img src="showcase/style-gallery/field-notes-report-high.webp" width="32%" alt="高密度：观察网格" />
</p>

#### [Operating Manual](references/style/text-report.md#operating-manual)

流程化、高对比。用工业 runbook、终端块和步骤执行来表达可重复操作。

<p align="center">
  <img src="showcase/style-gallery/operating-manual-low.webp" width="32%" alt="低密度：操作手册标题" />
  <img src="showcase/style-gallery/operating-manual-medium.webp" width="32%" alt="中密度：命令控制台" />
  <img src="showcase/style-gallery/operating-manual-high.webp" width="32%" alt="高密度：流程细节" />
</p>

#### [Checklist Ledger](references/style/text-report.md#checklist-ledger)

可靠、务实。用账簿线、紧凑行和可见 check 表达验收标准和最终准备度。

<p align="center">
  <img src="showcase/style-gallery/checklist-ledger-low.webp" width="32%" alt="低密度：准备度结论" />
  <img src="showcase/style-gallery/checklist-ledger-medium.webp" width="32%" alt="中密度：审计清单" />
  <img src="showcase/style-gallery/checklist-ledger-high.webp" width="32%" alt="高密度：清单账簿" />
</p>

#### [Annotated Source & Diff](references/style/text-report.md#annotated-source-diff)

可审查、强调变化。用 before/after、注释和类源码界面直接证明改动价值。

<p align="center">
  <img src="showcase/style-gallery/annotated-source-diff-low.webp" width="32%" alt="低密度：diff 观点" />
  <img src="showcase/style-gallery/annotated-source-diff-medium.webp" width="32%" alt="中密度：源码注释" />
  <img src="showcase/style-gallery/annotated-source-diff-high.webp" width="32%" alt="高密度：源码 diff" />
</p>

<p align="center">
  <a href="https://frontend-harness-slides-demo.vercel.app/"><b>🎬 动态 Demo</b></a>
</p>

## 我的更多精选 Skill

更多我长期维护、偏实战的精选 Agent Skills，见
[Awesome Skills](https://github.com/patrick-fu/awesome-skills)。
