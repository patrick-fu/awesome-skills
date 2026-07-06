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
> [动态风格预设预览](https://frontend-harness-slides-workbench.vercel.app/)。
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

完整画廊覆盖六类视觉家族：极简主题演讲、平衡混合、编辑与印刷、工艺与文化传统、当代数字、文本报告。每个风格都展示
低、中、高三种密度示例。

### 极简主题演讲

#### [Minimal Product Keynote](references/style/minimal-product-keynote.md)

高级、聚焦、稀疏。适合开场判断、产品亮相和单句大观点。

<p align="center">
  <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/01-minimal-product-keynote-nova-launch-scene1.webp" width="32%" alt="Minimal Product Keynote — 场景 1：开场" />
  <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/01-minimal-product-keynote-nova-launch-scene3.webp" width="32%" alt="Minimal Product Keynote — 场景 3：Nova Launch" />
  <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/01-minimal-product-keynote-nova-launch-scene5.webp" width="32%" alt="Minimal Product Keynote — 场景 5：结尾" />
</p>

#### [Sketch Board Emoji](references/style/sketch-board-emoji.md)

温暖、亲切，有人参与感。常用便利贴、胶带、emoji 角色和小型交互细节。

<p align="center">
  <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/07-sketch-board-emoji-collab-workshop-scene1.webp" width="32%" alt="Sketch Board Emoji — 场景 1：开场" />
  <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/07-sketch-board-emoji-collab-workshop-scene3.webp" width="32%" alt="Sketch Board Emoji — 场景 3：Collab Workshop" />
  <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/07-sketch-board-emoji-collab-workshop-scene5.webp" width="32%" alt="Sketch Board Emoji — 场景 5：结尾" />
</p>

#### [Interactive Dialogue Stage](references/style/interactive-dialogue-stage.md)

对话驱动，带一点剧场感。适合呈现两个角色、系统或说话方之间的轮流互动。

<p align="center">
  <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/04-interactive-dialogue-stage-human-ai-collaboration-scene1.webp" width="32%" alt="Interactive Dialogue Stage — 场景 1：开场" />
  <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/04-interactive-dialogue-stage-human-ai-collaboration-scene3.webp" width="32%" alt="Interactive Dialogue Stage — 场景 3：Human-AI Collaboration" />
  <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/04-interactive-dialogue-stage-human-ai-collaboration-scene5.webp" width="32%" alt="Interactive Dialogue Stage — 场景 5：结尾" />
</p>

#### [Kinetic Type Punchline](references/style/kinetic-type-punchline.md)

强烈、海报化、高能量。适合章节转折、强对比观点和需要被记住的金句。

<p align="center">
  <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/06-kinetic-type-punchline-punchline-impact-scene1.webp" width="32%" alt="Kinetic Type Punchline — 场景 1：开场" />
  <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/06-kinetic-type-punchline-punchline-impact-scene3.webp" width="32%" alt="Kinetic Type Punchline — 场景 3：Punchline Impact" />
  <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/06-kinetic-type-punchline-punchline-impact-scene5.webp" width="32%" alt="Kinetic Type Punchline — 场景 5：结尾" />
</p>

#### [Object Metaphor Hero](references/style/object-metaphor-hero.md)

拟物、触感强、隐喻驱动。把准备、规划、工具箱这类抽象概念变成可看的物件。

<p align="center">
  <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/48-object-metaphor-hero-system-metaphor-scene1.webp" width="32%" alt="Object Metaphor Hero — 场景 1：开场" />
  <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/48-object-metaphor-hero-system-metaphor-scene3.webp" width="32%" alt="Object Metaphor Hero — 场景 3：System Metaphor" />
  <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/48-object-metaphor-hero-system-metaphor-scene5.webp" width="32%" alt="Object Metaphor Hero — 场景 5：结尾" />
</p>

#### [Blackboard Chalk Talk](references/style/blackboard-chalk-talk.md)

手绘、教学、推理导向。用深绿色黑板、粉笔线条和公式来呈现推导过程。

<p align="center">
  <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/39-blackboard-chalk-talk-chalkboard-derivation-scene1.webp" width="32%" alt="Blackboard Chalk Talk — 场景 1：开场" />
  <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/39-blackboard-chalk-talk-chalkboard-derivation-scene3.webp" width="32%" alt="Blackboard Chalk Talk — 场景 3：Chalkboard Derivation" />
  <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/39-blackboard-chalk-talk-chalkboard-derivation-scene5.webp" width="32%" alt="Blackboard Chalk Talk — 场景 5：结尾" />
</p>

#### [Arcade Boss Fight](references/style/arcade-boss-fight.md)

复古、游戏化、带风险感。把技术挑战表达成 boss fight、HP 条和道具栏。

<p align="center">
  <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/40-arcade-boss-fight-gamified-risk-framing-scene1.webp" width="32%" alt="Arcade Boss Fight — 场景 1：开场" />
  <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/40-arcade-boss-fight-gamified-risk-framing-scene3.webp" width="32%" alt="Arcade Boss Fight — 场景 3：Gamified Risk Framing" />
  <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/40-arcade-boss-fight-gamified-risk-framing-scene5.webp" width="32%" alt="Arcade Boss Fight — 场景 5：结尾" />
</p>

#### [Spotlight Quote Poster](references/style/spotlight-quote-poster.md)

戏剧化、沉思感。用暗场、聚光和大字号 quote 营造停顿、收束和哲学表达。

<p align="center">
  <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/08-spotlight-quote-poster-mission-philosophy-scene1.webp" width="32%" alt="Spotlight Quote Poster — 场景 1：开场" />
  <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/08-spotlight-quote-poster-mission-philosophy-scene3.webp" width="32%" alt="Spotlight Quote Poster — 场景 3：Mission Philosophy" />
  <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/08-spotlight-quote-poster-mission-philosophy-scene5.webp" width="32%" alt="Spotlight Quote Poster — 场景 5：结尾" />
</p>

### 平衡混合

#### [Signal Pipeline Flow](references/style/signal-pipeline-flow.md)

技术化、精确。用节点、路由和发光箭头表现数据、信号或决策流。

<p align="center">
  <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/11-signal-pipeline-flow-data-pipeline-flow-scene1.webp" width="32%" alt="Signal Pipeline Flow — 场景 1：开场" />
  <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/11-signal-pipeline-flow-data-pipeline-flow-scene3.webp" width="32%" alt="Signal Pipeline Flow — 场景 3：Data Pipeline Flow" />
  <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/11-signal-pipeline-flow-data-pipeline-flow-scene5.webp" width="32%" alt="Signal Pipeline Flow — 场景 5：结尾" />
</p>

#### [Mechanical Scoring Funnel](references/style/mechanical-scoring-funnel.md)

有能量、偏评估。把筛选、评分和优先级表现成轨道、弹珠、分数和漏斗路径。

<p align="center">
  <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/32-mechanical-scoring-funnel-evaluation-funnel-scoring-scene1.webp" width="32%" alt="Mechanical Scoring Funnel — 场景 1：开场" />
  <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/32-mechanical-scoring-funnel-evaluation-funnel-scoring-scene3.webp" width="32%" alt="Mechanical Scoring Funnel — 场景 3：Evaluation Funnel Scoring" />
  <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/32-mechanical-scoring-funnel-evaluation-funnel-scoring-scene5.webp" width="32%" alt="Mechanical Scoring Funnel — 场景 5：结尾" />
</p>

#### [Collaborative Pairing Board](references/style/collaborative-pairing-board.md)

清爽、协作导向。适合展示角色分工、同步点，以及人、团队或系统之间的配合。

<p align="center">
  <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/14-collaborative-pairing-board-cross-team-pairing-scene1.webp" width="32%" alt="Collaborative Pairing Board — 场景 1：开场" />
  <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/14-collaborative-pairing-board-cross-team-pairing-scene3.webp" width="32%" alt="Collaborative Pairing Board — 场景 3：Cross-Team Pairing" />
  <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/14-collaborative-pairing-board-cross-team-pairing-scene5.webp" width="32%" alt="Collaborative Pairing Board — 场景 5：结尾" />
</p>

#### [Studio Mixing Console](references/style/studio-mixing-console.md)

专业、拟物。用推子、旋钮和电平表表现参数调节、噪音过滤和多因素平衡。

<p align="center">
  <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/15-studio-mixing-console-project-roadmap-scene1.webp" width="32%" alt="Studio Mixing Console — 场景 1：开场" />
  <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/15-studio-mixing-console-project-roadmap-scene3.webp" width="32%" alt="Studio Mixing Console — 场景 3：Project Roadmap" />
  <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/15-studio-mixing-console-project-roadmap-scene5.webp" width="32%" alt="Studio Mixing Console — 场景 5：结尾" />
</p>

#### [Subway Map of Intent](references/style/subway-map-of-intent.md)

系统化、结构清楚。把复杂工作流表现成地铁线路和换乘站。

<p align="center">
  <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/09-subway-map-of-intent-parallel-track-convergence-scene1.webp" width="32%" alt="Subway Map of Intent — 场景 1：开场" />
  <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/09-subway-map-of-intent-parallel-track-convergence-scene3.webp" width="32%" alt="Subway Map of Intent — 场景 3：Parallel Track Convergence" />
  <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/09-subway-map-of-intent-parallel-track-convergence-scene5.webp" width="32%" alt="Subway Map of Intent — 场景 5：结尾" />
</p>

#### [Kitchen Prep Station](references/style/kitchen-prep-station.md)

温暖、具体。把原始输入到干净输出的过程表现成备料台、修剪、菜谱步骤和摆盘。

<p align="center">
  <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/13-kitchen-prep-station-brainstorm-ideation-scene1.webp" width="32%" alt="Kitchen Prep Station — 场景 1：开场" />
  <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/13-kitchen-prep-station-brainstorm-ideation-scene3.webp" width="32%" alt="Kitchen Prep Station — 场景 3：Brainstorm Ideation" />
  <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/13-kitchen-prep-station-brainstorm-ideation-scene5.webp" width="32%" alt="Kitchen Prep Station — 场景 5：结尾" />
</p>

#### [Context Bento Box](references/style/context-bento-box.md)

紧凑、有组织。用分格和层叠盒子表达 handoff、多类别概览和上下文包装。

<p align="center">
  <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/47-context-bento-box-project-context-scene1.webp" width="32%" alt="Context Bento Box — 场景 1：开场" />
  <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/47-context-bento-box-project-context-scene3.webp" width="32%" alt="Context Bento Box — 场景 3：Project Context" />
  <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/47-context-bento-box-project-context-scene5.webp" width="32%" alt="Context Bento Box — 场景 5：结尾" />
</p>

#### [Debug Reaction Board](references/style/debug-reaction-board.md)

开发者原生、偏诊断。使用霓虹状态标记、终端界面和行动看板。

<p align="center">
  <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/16-debug-reaction-board-system-diagnostics-scene1.webp" width="32%" alt="Debug Reaction Board — 场景 1：开场" />
  <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/16-debug-reaction-board-system-diagnostics-scene3.webp" width="32%" alt="Debug Reaction Board — 场景 3：System Diagnostics" />
  <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/16-debug-reaction-board-system-diagnostics-scene5.webp" width="32%" alt="Debug Reaction Board — 场景 5：结尾" />
</p>

### 编辑与印刷

源自编辑设计、出版版式和印刷字体传统的风格。

#### [Magazine Masthead](references/style/magazine-masthead.md)

新闻摊封面般的自信，饱和墨色底色和超大时尚衬线标题引人注目。

<p align="center">
  <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/18-magazine-masthead-creative-intelligence-scene1.webp" width="32%" alt="杂志刊头 — 场景 1：开场" />
  <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/18-magazine-masthead-creative-intelligence-scene3.webp" width="32%" alt="杂志刊头 — 场景 3：Creative Intelligence" />
  <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/18-magazine-masthead-creative-intelligence-scene5.webp" width="32%" alt="杂志刊头 — 场景 5：结尾" />
</p>

#### [Solar Biennale Poster](references/style/solar-biennale-poster.md)

展览海报般的温暖，羊皮纸底色、日光黄氛围和一句巨大的衬线宣言。

<p align="center">
  <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/21-solar-biennale-poster-slow-light-biennale-scene1.webp" width="32%" alt="太阳双年展海报 — 场景 1：开场" />
  <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/21-solar-biennale-poster-slow-light-biennale-scene3.webp" width="32%" alt="太阳双年展海报 — 场景 3：Slow Light Biennale" />
  <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/21-solar-biennale-poster-slow-light-biennale-scene5.webp" width="32%" alt="太阳双年展海报 — 场景 5：结尾" />
</p>

#### [Warm Editorial Feature](references/style/warm-editorial-feature.md)

杂志专题页风格，暖奶油纸底色、衬线展示字体和引用节奏，适合叙事阅读。

<p align="center">
  <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/19-warm-editorial-feature-attention-rebellion-scene1.webp" width="32%" alt="暖色编辑特写 — 场景 1：开场" />
  <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/19-warm-editorial-feature-attention-rebellion-scene3.webp" width="32%" alt="暖色编辑特写 — 场景 3：Attention Rebellion" />
  <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/19-warm-editorial-feature-attention-rebellion-scene5.webp" width="32%" alt="暖色编辑特写 — 场景 5：结尾" />
</p>

#### [Scholars' Vellum](references/style/scholars-vellum.md)

古典手稿，古老羊皮纸、页边批注和衬线权威感，适合深度思想内容。

<p align="center">
  <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/20-scholars-vellum-nature-of-knowing-scene1.webp" width="32%" alt="学者羊皮纸 — 场景 1：开场" />
  <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/20-scholars-vellum-nature-of-knowing-scene3.webp" width="32%" alt="学者羊皮纸 — 场景 3：Nature of Knowing" />
  <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/20-scholars-vellum-nature-of-knowing-scene5.webp" width="32%" alt="学者羊皮纸 — 场景 5：结尾" />
</p>

#### [Front Page Broadsheet](references/style/front-page-broadsheet.md)

报纸头版，多栏布局和标题层级，适合密集信息交付。

<p align="center">
  <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/17-front-page-broadsheet-urban-transformation-scene1.webp" width="32%" alt="头版大报 — 场景 1：开场" />
  <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/17-front-page-broadsheet-urban-transformation-scene3.webp" width="32%" alt="头版大报 — 场景 3：Urban Transformation" />
  <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/17-front-page-broadsheet-urban-transformation-scene5.webp" width="32%" alt="头版大报 — 场景 5：结尾" />
</p>

#### [Duotone Session](references/style/duotone-session.md)

Blue Note 黑胶封套，双色照片和超大压缩哥特字体——冷静、克制、匠人感。

<p align="center">
  <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/22-duotone-session-recording-session-scene1.webp" width="32%" alt="双调录音 — 场景 1：开场" />
  <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/22-duotone-session-recording-session-scene3.webp" width="32%" alt="双调录音 — 场景 3：Recording Session" />
  <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/22-duotone-session-recording-session-scene5.webp" width="32%" alt="双调录音 — 场景 5：结尾" />
</p>

### 工艺与文化传统

根植于工艺技法、文化视觉传统和实体媒介的风格。

#### [Botanical Specimen Plate](references/style/botanical-specimen-plate.md)

科学植物插画，精细墨线和拉丁标注，适合自然世界主题。

<p align="center">
  <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/26-botanical-specimen-plate-botanical-taxonomy-specimens-scene1.webp" width="32%" alt="植物标本板 — 场景 1：开场" />
  <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/26-botanical-specimen-plate-botanical-taxonomy-specimens-scene3.webp" width="32%" alt="植物标本板 — 场景 3：Botanical Taxonomy Specimens" />
  <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/26-botanical-specimen-plate-botanical-taxonomy-specimens-scene5.webp" width="32%" alt="植物标本板 — 场景 5：结尾" />
</p>

#### [Woodblock Floating World](references/style/woodblock-floating-world.md)

日本浮世绘木刻，浮动世界构图和水墨纹理，适合沉思视觉叙事。

<p align="center">
  <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/25-woodblock-floating-world-ukiyo-e-floating-world-scene1.webp" width="32%" alt="木版浮世绘 — 场景 1：开场" />
  <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/25-woodblock-floating-world-ukiyo-e-floating-world-scene3.webp" width="32%" alt="木版浮世绘 — 场景 3：Ukiyo-e Floating World" />
  <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/25-woodblock-floating-world-ukiyo-e-floating-world-scene5.webp" width="32%" alt="木版浮世绘 — 场景 5：结尾" />
</p>

#### [Cyanotype Drafting Table](references/style/cyanotype-drafting-table.md)

蓝图制图，蓝晒色调和技术线稿，适合系统架构和工程图表。

<p align="center">
  <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/05-cyanotype-drafting-table-system-architecture-scene1.webp" width="32%" alt="蓝图制图台 — 场景 1：开场" />
  <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/05-cyanotype-drafting-table-system-architecture-scene3.webp" width="32%" alt="蓝图制图台 — 场景 3：System Architecture" />
  <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/05-cyanotype-drafting-table-system-architecture-scene5.webp" width="32%" alt="蓝图制图台 — 场景 5：结尾" />
</p>

#### [Expedition Screenprint](references/style/expedition-screenprint.md)

田野日志丝网印，叠印图层和地图坐标，适合探索发现叙事。

<p align="center">
  <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/28-expedition-screenprint-public-lands-expedition-scene1.webp" width="32%" alt="探险丝网印 — 场景 1：开场" />
  <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/28-expedition-screenprint-public-lands-expedition-scene3.webp" width="32%" alt="探险丝网印 — 场景 3：Public Lands Expedition" />
  <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/28-expedition-screenprint-public-lands-expedition-scene5.webp" width="32%" alt="探险丝网印 — 场景 5：结尾" />
</p>

#### [Machine-Age Deco](references/style/machine-age-deco.md)

Art Deco 机器时代，几何图案和阶梯造型，适合宏大愿景和雄心路线图。

<p align="center">
  <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/27-machine-age-deco-flagship-product-launch-scene1.webp" width="32%" alt="机器时代装饰 — 场景 1：开场" />
  <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/27-machine-age-deco-flagship-product-launch-scene3.webp" width="32%" alt="机器时代装饰 — 场景 3：Flagship Product Launch" />
  <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/27-machine-age-deco-flagship-product-launch-scene5.webp" width="32%" alt="机器时代装饰 — 场景 5：结尾" />
</p>

#### [Wabi-Sabi Ceramic](references/style/wabi-sabi-ceramic.md)

手捏陶瓷，侘寂不规则感和哑光釉面，适合工艺和天然产品主题。

<p align="center">
  <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/03-wabi-sabi-ceramic-craft-philosophy-scene1.webp" width="32%" alt="侘寂陶瓷 — 场景 1：开场" />
  <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/03-wabi-sabi-ceramic-craft-philosophy-scene3.webp" width="32%" alt="侘寂陶瓷 — 场景 3：Craft Philosophy" />
  <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/03-wabi-sabi-ceramic-craft-philosophy-scene5.webp" width="32%" alt="侘寂陶瓷 — 场景 5：结尾" />
</p>

#### [Analog Cutout Collage](references/style/analog-cutout-collage.md)

手工剪纸拼贴，撕纸边缘和混合质感，适合创意过程和想法组装。

<p align="center">
  <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/24-analog-cutout-collage-desk-fragments-scene1.webp" width="32%" alt="模拟拼贴 — 场景 1：开场" />
  <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/24-analog-cutout-collage-desk-fragments-scene3.webp" width="32%" alt="模拟拼贴 — 场景 3：Desk Fragments" />
  <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/24-analog-cutout-collage-desk-fragments-scene5.webp" width="32%" alt="模拟拼贴 — 场景 5：结尾" />
</p>

#### [Cassette-Era Packaging](references/style/cassette-era-packaging.md)

磁带 J-card 设计，80-90 年代图形能量和混音带布局，适合音乐和怀旧内容。

<p align="center">
  <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/29-cassette-era-packaging-retro-audio-catalogue-scene1.webp" width="32%" alt="磁带时代包装 — 场景 1：开场" />
  <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/29-cassette-era-packaging-retro-audio-catalogue-scene3.webp" width="32%" alt="磁带时代包装 — 场景 3：Retro Audio Catalogue" />
  <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/29-cassette-era-packaging-retro-audio-catalogue-scene5.webp" width="32%" alt="磁带时代包装 — 场景 5：结尾" />
</p>

#### [Riso Print Zine](references/style/riso-print-zine.md)

Risograph 手工 zine，限色调、手工拼贴密度和 DIY 反叛气质。

<p align="center">
  <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/23-riso-print-zine-underground-music-scene1.webp" width="32%" alt="孔版印刷杂志 — 场景 1：开场" />
  <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/23-riso-print-zine-underground-music-scene3.webp" width="32%" alt="孔版印刷杂志 — 场景 3：Underground Music" />
  <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/23-riso-print-zine-underground-music-scene5.webp" width="32%" alt="孔版印刷杂志 — 场景 5：结尾" />
</p>

#### [Neo-Brutalist Bulletin](references/style/neo-brutalist-bulletin.md)

抗议海报能量，粗黑边框、硬投影和一个高电压强调色。

<p align="center">
  <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/30-neo-brutalist-bulletin-product-launch-bulletin-scene1.webp" width="32%" alt="新野兽派公告 — 场景 1：开场" />
  <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/30-neo-brutalist-bulletin-product-launch-bulletin-scene3.webp" width="32%" alt="新野兽派公告 — 场景 3：Product Launch Bulletin" />
  <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/30-neo-brutalist-bulletin-product-launch-bulletin-scene5.webp" width="32%" alt="新野兽派公告 — 场景 5：结尾" />
</p>

#### [Red Wedge Agitprop](references/style/red-wedge-agitprop.md)

构成主义政治海报，红色楔形几何和对角线动能，适合行动号召。

<p align="center">
  <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/31-red-wedge-agitprop-movement-call-to-action-scene1.webp" width="32%" alt="红色楔子宣传 — 场景 1：开场" />
  <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/31-red-wedge-agitprop-movement-call-to-action-scene3.webp" width="32%" alt="红色楔子宣传 — 场景 3：Movement Call to Action" />
  <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/31-red-wedge-agitprop-movement-call-to-action-scene5.webp" width="32%" alt="红色楔子宣传 — 场景 5：结尾" />
</p>

### 当代数字

源自当前 UI 趋势和平台美学的现代数字优先风格。

#### [Mid-Century Grove](references/style/mid-century-grove.md)

中世纪有机沉静，天然木色调和柔和曲线，适合可持续和天然产品故事。

<p align="center">
  <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/35-mid-century-grove-brand-storytelling-scene1.webp" width="32%" alt="中世纪树林 — 场景 1：开场" />
  <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/35-mid-century-grove-brand-storytelling-scene3.webp" width="32%" alt="中世纪树林 — 场景 3：Brand Storytelling" />
  <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/35-mid-century-grove-brand-storytelling-scene5.webp" width="32%" alt="中世纪树林 — 场景 5：结尾" />
</p>

#### [After-Hours Luxe](references/style/after-hours-luxe.md)

深夜鸡尾酒会奢华，深宝石色调和金色点缀，适合高端定位和夜间场景。

<p align="center">
  <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/36-after-hours-luxe-luxury-brand-launch-scene1.webp" width="32%" alt="夜间奢华 — 场景 1：开场" />
  <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/36-after-hours-luxe-luxury-brand-launch-scene3.webp" width="32%" alt="夜间奢华 — 场景 3：Luxury Brand Launch" />
  <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/36-after-hours-luxe-luxury-brand-launch-scene5.webp" width="32%" alt="夜间奢华 — 场景 5：结尾" />
</p>

#### [Soft Pastel Friendly](references/style/soft-pastel-friendly.md)

亲切粉彩温暖，圆角药丸几何和柔和弹簧动效，适合引导页和社区 deck。

<p align="center">
  <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/12-soft-pastel-friendly-workspace-onboarding-scene1.webp" width="32%" alt="柔和粉彩 — 场景 1：开场" />
  <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/12-soft-pastel-friendly-workspace-onboarding-scene3.webp" width="32%" alt="柔和粉彩 — 场景 3：Workspace Onboarding" />
  <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/12-soft-pastel-friendly-workspace-onboarding-scene5.webp" width="32%" alt="柔和粉彩 — 场景 5：结尾" />
</p>

#### [Retro Windows](references/style/retro-windows.md)

Windows 3.1/95 怀旧，斜面镀铬和系统灰调色板，适合开发者工具和复古科技氛围。

<p align="center">
  <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/34-retro-windows-nostalgic-computing-scene1.webp" width="32%" alt="复古窗口 — 场景 1：开场" />
  <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/34-retro-windows-nostalgic-computing-scene3.webp" width="32%" alt="复古窗口 — 场景 3：Nostalgic Computing" />
  <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/34-retro-windows-nostalgic-computing-scene5.webp" width="32%" alt="复古窗口 — 场景 5：结尾" />
</p>

#### [Objective Swiss Grid](references/style/objective-swiss-grid.md)

瑞士国际风格，刚性网格结构和无衬线清晰度，适合数据报告和分析框架。

<p align="center">
  <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/02-objective-swiss-grid-migration-sequence-scene1.webp" width="32%" alt="客观瑞士网格 — 场景 1：开场" />
  <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/02-objective-swiss-grid-migration-sequence-scene3.webp" width="32%" alt="客观瑞士网格 — 场景 3：Migration Sequence" />
  <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/02-objective-swiss-grid-migration-sequence-scene5.webp" width="32%" alt="客观瑞士网格 — 场景 5：结尾" />
</p>

#### [Liquid Glass](references/style/liquid-glass.md)

Apple 设计语言，毛玻璃深度和空间分层，适合高端科技和 Apple 平台内容。

<p align="center">
  <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/33-liquid-glass-museum-collection-showcase-scene1.webp" width="32%" alt="液态玻璃 — 场景 1：开场" />
  <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/33-liquid-glass-museum-collection-showcase-scene3.webp" width="32%" alt="液态玻璃 — 场景 3：Museum Collection Showcase" />
  <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/33-liquid-glass-museum-collection-showcase-scene5.webp" width="32%" alt="液态玻璃 — 场景 5：结尾" />
</p>

#### [Widescreen Title Card](references/style/widescreen-title-card.md)

电影宽银幕标题卡，电影字体和氛围静止感，适合开场标题和宏大揭示。

<p align="center">
  <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/38-widescreen-title-card-cinematic-title-cards-scene1.webp" width="32%" alt="宽屏标题卡 — 场景 1：开场" />
  <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/38-widescreen-title-card-cinematic-title-cards-scene3.webp" width="32%" alt="宽屏标题卡 — 场景 3：Cinematic Title Cards" />
  <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/38-widescreen-title-card-cinematic-title-cards-scene5.webp" width="32%" alt="宽屏标题卡 — 场景 5：结尾" />
</p>

### 文本报告

#### [Research Memo](references/style/research-memo.md)

克制、可信、有研究感。适合研究发现、高管摘要和需要自洽阅读的证据页面。

<p align="center">
  <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/41-research-memo-model-performance-scene1.webp" width="32%" alt="Research Memo — 场景 1：开场" />
  <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/41-research-memo-model-performance-scene3.webp" width="32%" alt="Research Memo — 场景 3：Model Performance" />
  <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/41-research-memo-model-performance-scene5.webp" width="32%" alt="Research Memo — 场景 5：结尾" />
</p>

#### [Maintainer Issue Brief](references/style/maintainer-issue-brief.md)

整洁、结构化、行动导向。灵感来自现代 issue tracker 和代码审查工具。

<p align="center">
  <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/43-maintainer-issue-brief-bug-fix-brief-scene1.webp" width="32%" alt="Maintainer Issue Brief — 场景 1：开场" />
  <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/43-maintainer-issue-brief-bug-fix-brief-scene3.webp" width="32%" alt="Maintainer Issue Brief — 场景 3：Bug Fix Brief" />
  <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/43-maintainer-issue-brief-bug-fix-brief-scene5.webp" width="32%" alt="Maintainer Issue Brief — 场景 5：结尾" />
</p>

#### [Decision Record](references/style/decision-record.md)

严谨、架构化。用 ADR 节奏呈现上下文、决策、权衡和验证。

<p align="center">
  <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/42-decision-record-architecture-decision-scene1.webp" width="32%" alt="Decision Record — 场景 1：开场" />
  <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/42-decision-record-architecture-decision-scene3.webp" width="32%" alt="Decision Record — 场景 3：Architecture Decision" />
  <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/42-decision-record-architecture-decision-scene5.webp" width="32%" alt="Decision Record — 场景 5：结尾" />
</p>

#### [Benchmark Matrix](references/style/benchmark-matrix.md)

分析型、比较型。强调结构化证据、评估标准、指标和表格化对比。

<p align="center">
  <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/10-benchmark-matrix-competitive-benchmark-scene1.webp" width="32%" alt="Benchmark Matrix — 场景 1：开场" />
  <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/10-benchmark-matrix-competitive-benchmark-scene3.webp" width="32%" alt="Benchmark Matrix — 场景 3：Competitive Benchmark" />
  <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/10-benchmark-matrix-competitive-benchmark-scene5.webp" width="32%" alt="Benchmark Matrix — 场景 5：结尾" />
</p>

#### [Field Notes Report](references/style/field-notes-report.md)

有纸张触感，偏观察记录。使用账簿纸、木炭墨水和卡片网格。

<p align="center">
  <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/44-field-notes-report-field-research-scene1.webp" width="32%" alt="Field Notes Report — 场景 1：开场" />
  <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/44-field-notes-report-field-research-scene3.webp" width="32%" alt="Field Notes Report — 场景 3：Field Research" />
  <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/44-field-notes-report-field-research-scene5.webp" width="32%" alt="Field Notes Report — 场景 5：结尾" />
</p>

#### [Operating Manual](references/style/operating-manual.md)

流程化、高对比。用工业 runbook、终端块和步骤执行来表达可重复操作。

<p align="center">
  <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/37-operating-manual-industrial-runbook-scene1.webp" width="32%" alt="Operating Manual — 场景 1：开场" />
  <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/37-operating-manual-industrial-runbook-scene3.webp" width="32%" alt="Operating Manual — 场景 3：Industrial Runbook" />
  <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/37-operating-manual-industrial-runbook-scene5.webp" width="32%" alt="Operating Manual — 场景 5：结尾" />
</p>

#### [Checklist Ledger](references/style/checklist-ledger.md)

可靠、务实。用账簿线、紧凑行和可见 check 表达验收标准和最终准备度。

<p align="center">
  <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/46-checklist-ledger-release-readiness-scene1.webp" width="32%" alt="Checklist Ledger — 场景 1：开场" />
  <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/46-checklist-ledger-release-readiness-scene3.webp" width="32%" alt="Checklist Ledger — 场景 3：Release Readiness" />
  <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/46-checklist-ledger-release-readiness-scene5.webp" width="32%" alt="Checklist Ledger — 场景 5：结尾" />
</p>

#### [Annotated Source & Diff](references/style/annotated-source-and-diff.md)

可审查、强调变化。用 before/after、注释和类源码界面直接证明改动价值。

<p align="center">
  <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/45-annotated-source-diff-code-refactor-scene1.webp" width="32%" alt="Annotated Source Diff — 场景 1：开场" />
  <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/45-annotated-source-diff-code-refactor-scene3.webp" width="32%" alt="Annotated Source Diff — 场景 3：Code Refactor" />
  <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/45-annotated-source-diff-code-refactor-scene5.webp" width="32%" alt="Annotated Source Diff — 场景 5：结尾" />
</p>

<p align="center">
  <a href="https://frontend-harness-slides-workbench.vercel.app/"><b>🎬 动态 Demo</b></a>
</p>

## 我的更多精选 Skill

更多我长期维护、偏实战的精选 Agent Skills，见
[Awesome Skills](https://github.com/patrick-fu/awesome-skills)。
