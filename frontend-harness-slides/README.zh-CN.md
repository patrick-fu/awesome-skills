# Frontend Harness Slides

[![skills.sh](https://skills.sh/b/patrick-fu/frontend-harness-slides)](https://skills.sh/patrick-fu/frontend-harness-slides)

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

下面的画廊展示已接入 Workbench 的预设风格，覆盖六类视觉家族：极简主题演讲、平衡混合、编辑与印刷、
工艺与文化传统、当代数字、文本报告。每个已展示风格从左到右对比 Doubao-Seed-Evolving、GPT 5.6 Sol
和 Claude Opus 4.8 各自的 Hero 最终帧。

### 极简主题演讲

#### [Minimal Product Keynote](references/style/minimal-product-keynote.md)

高级、聚焦、稀疏。适合开场判断、产品亮相和单句大观点。

<p align="center">
  <a href="https://frontend-harness-slides-workbench.vercel.app/?view=lab&amp;style=minimal-product-keynote&amp;topic=product-keynote&amp;scene=1&amp;beat=0&amp;lang=zh">
    <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/product-keynote.webp" width="32%" alt="极简产品主题演讲 — Doubao-Seed-Evolving — 产品主题 — Hero 最终帧" />
  </a>
  <a href="https://frontend-harness-slides-workbench.vercel.app/?view=lab&amp;style=minimal-product-keynote&amp;topic=presolar-grain&amp;scene=1&amp;beat=0&amp;lang=zh">
    <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/presolar-grain.webp" width="32%" alt="极简产品主题演讲 — GPT 5.6 Sol — 太阳前尘 — Hero 最终帧" />
  </a>
  <a href="https://frontend-harness-slides-workbench.vercel.app/?view=lab&amp;style=minimal-product-keynote&amp;topic=last-feature-cut&amp;scene=1&amp;beat=0&amp;lang=zh">
    <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/last-feature-cut.webp" width="32%" alt="极简产品主题演讲 — Claude Opus 4.8 — 删掉的功能 — Hero 最终帧" />
  </a>
</p>

#### [Sketch Board Emoji](references/style/sketch-board-emoji.md)

温暖、亲切，有人参与感。常用便利贴、胶带、emoji 角色和小型交互细节。

<p align="center">
  <a href="https://frontend-harness-slides-workbench.vercel.app/?view=lab&amp;style=sketch-board-emoji&amp;topic=workshop-board&amp;scene=1&amp;beat=0&amp;lang=zh">
    <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/workshop-board.webp" width="32%" alt="草图白板表情 — Doubao-Seed-Evolving — 工作坊 — Hero 最终帧" />
  </a>
  <a href="https://frontend-harness-slides-workbench.vercel.app/?view=lab&amp;style=sketch-board-emoji&amp;topic=stadium-wave&amp;scene=1&amp;beat=0&amp;lang=zh">
    <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/stadium-wave.webp" width="32%" alt="草图白板表情 — GPT 5.6 Sol — 看台人浪 — Hero 最终帧" />
  </a>
  <a href="https://frontend-harness-slides-workbench.vercel.app/?view=lab&amp;style=sketch-board-emoji&amp;topic=how-we-named-it&amp;scene=1&amp;beat=0&amp;lang=zh">
    <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/how-we-named-it.webp" width="32%" alt="草图白板表情 — Claude Opus 4.8 — 起名字 — Hero 最终帧" />
  </a>
</p>

#### [Interactive Dialogue Stage](references/style/interactive-dialogue-stage.md)

对话驱动，带一点剧场感。适合呈现两个角色、系统或说话方之间的轮流互动。

<p align="center">
  <a href="https://frontend-harness-slides-workbench.vercel.app/?view=lab&amp;style=interactive-dialogue-stage&amp;topic=dialogue-stage&amp;scene=1&amp;beat=0&amp;lang=zh">
    <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/dialogue-stage.webp" width="32%" alt="互动对话舞台 — Doubao-Seed-Evolving — 对话舞台 — Hero 最终帧" />
  </a>
  <a href="https://frontend-harness-slides-workbench.vercel.app/?view=lab&amp;style=interactive-dialogue-stage&amp;topic=vocal-folds&amp;scene=1&amp;beat=0&amp;lang=zh">
    <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/vocal-folds.webp" width="32%" alt="互动对话舞台 — GPT 5.6 Sol — 声带 — Hero 最终帧" />
  </a>
  <a href="https://frontend-harness-slides-workbench.vercel.app/?view=lab&amp;style=interactive-dialogue-stage&amp;topic=rubber-duck&amp;scene=1&amp;beat=0&amp;lang=zh">
    <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/rubber-duck.webp" width="32%" alt="互动对话舞台 — Claude Opus 4.8 — 橡皮鸭 — Hero 最终帧" />
  </a>
</p>

#### [Kinetic Type Punchline](references/style/kinetic-type-punchline.md)

强烈、海报化、高能量。适合章节转折、强对比观点和需要被记住的金句。

<p align="center">
  <a href="https://frontend-harness-slides-workbench.vercel.app/?view=lab&amp;style=kinetic-type-punchline&amp;topic=type-poster&amp;scene=1&amp;beat=0&amp;lang=zh">
    <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/type-poster.webp" width="32%" alt="动感字体金句 — Doubao-Seed-Evolving — 字体海报 — Hero 最终帧" />
  </a>
  <a href="https://frontend-harness-slides-workbench.vercel.app/?view=lab&amp;style=kinetic-type-punchline&amp;topic=before-a&amp;scene=1&amp;beat=0&amp;lang=zh">
    <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/before-a.webp" width="32%" alt="动感字体金句 — GPT 5.6 Sol — A之前 — Hero 最终帧" />
  </a>
  <a href="https://frontend-harness-slides-workbench.vercel.app/?view=lab&amp;style=kinetic-type-punchline&amp;topic=ship-it&amp;scene=1&amp;beat=0&amp;lang=zh">
    <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/ship-it.webp" width="32%" alt="动感字体金句 — Claude Opus 4.8 — 发布 — Hero 最终帧" />
  </a>
</p>

#### [Object Metaphor Hero](references/style/object-metaphor-hero.md)

拟物、触感强、隐喻驱动。把准备、规划、工具箱这类抽象概念变成可看的物件。

<p align="center">
  <a href="https://frontend-harness-slides-workbench.vercel.app/?view=lab&amp;style=object-metaphor-hero&amp;topic=object-metaphor&amp;scene=1&amp;beat=0&amp;lang=zh">
    <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/object-metaphor.webp" width="32%" alt="物体隐喻主视觉 — Doubao-Seed-Evolving — 物体主视觉 — Hero 最终帧" />
  </a>
  <a href="https://frontend-harness-slides-workbench.vercel.app/?view=lab&amp;style=object-metaphor-hero&amp;topic=cocoon-to-cloth&amp;scene=1&amp;beat=0&amp;lang=zh">
    <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/cocoon-to-cloth.webp" width="32%" alt="物体隐喻主视觉 — GPT 5.6 Sol — 茧到织物 — Hero 最终帧" />
  </a>
  <a href="https://frontend-harness-slides-workbench.vercel.app/?view=lab&amp;style=object-metaphor-hero&amp;topic=onboarding-toolkit&amp;scene=1&amp;beat=0&amp;lang=zh">
    <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/onboarding-toolkit.webp" width="32%" alt="物体隐喻主视觉 — Claude Opus 4.8 — 入职工具包 — Hero 最终帧" />
  </a>
</p>

#### [Blackboard Chalk Talk](references/style/blackboard-chalk-talk.md)

手绘、教学、推理导向。用深绿色黑板、粉笔线条和公式来呈现推导过程。

<p align="center">
  <a href="https://frontend-harness-slides-workbench.vercel.app/?view=lab&amp;style=blackboard-chalk-talk&amp;topic=chalk-talk&amp;scene=1&amp;beat=0&amp;lang=zh">
    <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/chalk-talk.webp" width="32%" alt="黑板粉笔演讲 — Doubao-Seed-Evolving — 粉笔推导 — Hero 最终帧" />
  </a>
  <a href="https://frontend-harness-slides-workbench.vercel.app/?view=lab&amp;style=blackboard-chalk-talk&amp;topic=hearing-path&amp;scene=1&amp;beat=0&amp;lang=zh">
    <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/hearing-path.webp" width="32%" alt="黑板粉笔演讲 — GPT 5.6 Sol — 听觉起点 — Hero 最终帧" />
  </a>
  <a href="https://frontend-harness-slides-workbench.vercel.app/?view=lab&amp;style=blackboard-chalk-talk&amp;topic=deriving-big-o&amp;scene=1&amp;beat=0&amp;lang=zh">
    <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/deriving-big-o.webp" width="32%" alt="黑板粉笔演讲 — Claude Opus 4.8 — 推导复杂度 — Hero 最终帧" />
  </a>
</p>

#### [Arcade Boss Fight](references/style/arcade-boss-fight.md)

复古、游戏化、带风险感。把技术挑战表达成 boss fight、HP 条和道具栏。

<p align="center">
  <a href="https://frontend-harness-slides-workbench.vercel.app/?view=lab&amp;style=arcade-boss-fight&amp;topic=boss-fight&amp;scene=1&amp;beat=0&amp;lang=zh">
    <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/boss-fight.webp" width="32%" alt="街机 Boss 战 — Doubao-Seed-Evolving — Boss 战 — Hero 最终帧" />
  </a>
  <a href="https://frontend-harness-slides-workbench.vercel.app/?view=lab&amp;style=arcade-boss-fight&amp;topic=egg-mimicry&amp;scene=1&amp;beat=0&amp;lang=zh">
    <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/egg-mimicry.webp" width="32%" alt="街机 Boss 战 — GPT 5.6 Sol — 卵拟态 — Hero 最终帧" />
  </a>
  <a href="https://frontend-harness-slides-workbench.vercel.app/?view=lab&amp;style=arcade-boss-fight&amp;topic=defeating-tech-debt&amp;scene=1&amp;beat=0&amp;lang=zh">
    <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/defeating-tech-debt.webp" width="32%" alt="街机 Boss 战 — Claude Opus 4.8 — 打败技术债 — Hero 最终帧" />
  </a>
</p>

#### [Spotlight Quote Poster](references/style/spotlight-quote-poster.md)

戏剧化、沉思感。用暗场、聚光和大字号 quote 营造停顿、收束和哲学表达。

<p align="center">
  <a href="https://frontend-harness-slides-workbench.vercel.app/?view=lab&amp;style=spotlight-quote-poster&amp;topic=quote-poster&amp;scene=1&amp;beat=0&amp;lang=zh">
    <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/quote-poster.webp" width="32%" alt="聚光引言海报 — Doubao-Seed-Evolving — 引言海报 — Hero 最终帧" />
  </a>
  <a href="https://frontend-harness-slides-workbench.vercel.app/?view=lab&amp;style=spotlight-quote-poster&amp;topic=freedive&amp;scene=1&amp;beat=0&amp;lang=zh">
    <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/freedive.webp" width="32%" alt="聚光引言海报 — GPT 5.6 Sol — 自由潜水 — Hero 最终帧" />
  </a>
  <a href="https://frontend-harness-slides-workbench.vercel.app/?view=lab&amp;style=spotlight-quote-poster&amp;topic=on-quitting-well&amp;scene=1&amp;beat=0&amp;lang=zh">
    <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/on-quitting-well.webp" width="32%" alt="聚光引言海报 — Claude Opus 4.8 — 好好离开 — Hero 最终帧" />
  </a>
</p>

### 平衡混合

#### [Signal Pipeline Flow](references/style/signal-pipeline-flow.md)

技术化、精确。用节点、路由和发光箭头表现数据、信号或决策流。

<p align="center">
  <a href="https://frontend-harness-slides-workbench.vercel.app/?view=lab&amp;style=signal-pipeline-flow&amp;topic=pipeline&amp;scene=1&amp;beat=0&amp;lang=zh">
    <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/pipeline.webp" width="32%" alt="信号管道流 — Doubao-Seed-Evolving — 管道流程 — Hero 最终帧" />
  </a>
  <a href="https://frontend-harness-slides-workbench.vercel.app/?view=lab&amp;style=signal-pipeline-flow&amp;topic=district-heat&amp;scene=1&amp;beat=0&amp;lang=zh">
    <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/district-heat.webp" width="32%" alt="信号管道流 — GPT 5.6 Sol — 城市余热 — Hero 最终帧" />
  </a>
  <a href="https://frontend-harness-slides-workbench.vercel.app/?view=lab&amp;style=signal-pipeline-flow&amp;topic=where-request-goes&amp;scene=1&amp;beat=0&amp;lang=zh">
    <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/where-request-goes.webp" width="32%" alt="信号管道流 — Claude Opus 4.8 — 请求去哪了 — Hero 最终帧" />
  </a>
</p>

#### [Engineering Whiteboard Explainer](references/style/engineering-whiteboard-explainer.md)

清晰、工程导向、强调图解。使用干净白色画布推进技术机制与分步说明。

<p align="center">
  <a href="https://frontend-harness-slides-workbench.vercel.app/?view=lab&amp;style=engineering-whiteboard-explainer&amp;topic=tcp-congestion-control&amp;scene=1&amp;beat=0&amp;lang=zh">
    <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/tcp-congestion-control.webp" width="32%" alt="工程讲解白板 — Doubao-Seed-Evolving — TCP 拥塞控制 — Hero 最终帧" />
  </a>
  <a href="https://frontend-harness-slides-workbench.vercel.app/?view=lab&amp;style=engineering-whiteboard-explainer&amp;topic=water-tower&amp;scene=1&amp;beat=0&amp;lang=zh">
    <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/water-tower.webp" width="32%" alt="工程讲解白板 — GPT 5.6 Sol — 城市水塔 — Hero 最终帧" />
  </a>
  <a href="https://frontend-harness-slides-workbench.vercel.app/?view=lab&amp;style=engineering-whiteboard-explainer&amp;topic=two-triangles-one-pixel&amp;scene=1&amp;beat=0&amp;lang=zh">
    <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/two-triangles-one-pixel.webp" width="32%" alt="工程讲解白板 — Claude Opus 4.8 — 双三角，争一像素 — Hero 最终帧" />
  </a>
</p>

#### [Mechanical Scoring Funnel](references/style/mechanical-scoring-funnel.md)

有能量、偏评估。把筛选、评分和优先级表现成轨道、弹珠、分数和漏斗路径。

<p align="center">
  <a href="https://frontend-harness-slides-workbench.vercel.app/?view=lab&amp;style=mechanical-scoring-funnel&amp;topic=scoring-funnel&amp;scene=1&amp;beat=0&amp;lang=zh">
    <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/scoring-funnel.webp" width="32%" alt="机械评分漏斗 — Doubao-Seed-Evolving — 评分漏斗 — Hero 最终帧" />
  </a>
  <a href="https://frontend-harness-slides-workbench.vercel.app/?view=lab&amp;style=mechanical-scoring-funnel&amp;topic=snowflake-branches&amp;scene=1&amp;beat=0&amp;lang=zh">
    <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/snowflake-branches.webp" width="32%" alt="机械评分漏斗 — GPT 5.6 Sol — 雪花分支 — Hero 最终帧" />
  </a>
  <a href="https://frontend-harness-slides-workbench.vercel.app/?view=lab&amp;style=mechanical-scoring-funnel&amp;topic=triage-the-backlog&amp;scene=1&amp;beat=0&amp;lang=zh">
    <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/triage-the-backlog.webp" width="32%" alt="机械评分漏斗 — Claude Opus 4.8 — 需求分拣 — Hero 最终帧" />
  </a>
</p>

#### [Collaborative Pairing Board](references/style/collaborative-pairing-board.md)

清爽、协作导向。适合展示角色分工、同步点，以及人、团队或系统之间的配合。

<p align="center">
  <a href="https://frontend-harness-slides-workbench.vercel.app/?view=lab&amp;style=collaborative-pairing-board&amp;topic=pairing-board&amp;scene=1&amp;beat=0&amp;lang=zh">
    <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/pairing-board.webp" width="32%" alt="协作配对板 — Doubao-Seed-Evolving — 配对板 — Hero 最终帧" />
  </a>
  <a href="https://frontend-harness-slides-workbench.vercel.app/?view=lab&amp;style=collaborative-pairing-board&amp;topic=elevator-counterweight&amp;scene=1&amp;beat=0&amp;lang=zh">
    <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/elevator-counterweight.webp" width="32%" alt="协作配对板 — GPT 5.6 Sol — 电梯配重 — Hero 最终帧" />
  </a>
  <a href="https://frontend-harness-slides-workbench.vercel.app/?view=lab&amp;style=collaborative-pairing-board&amp;topic=human-reviews-ai&amp;scene=1&amp;beat=0&amp;lang=zh">
    <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/human-reviews-ai.webp" width="32%" alt="协作配对板 — Claude Opus 4.8 — 人审 AI — Hero 最终帧" />
  </a>
</p>

#### [Studio Mixing Console](references/style/studio-mixing-console.md)

专业、拟物。用推子、旋钮和电平表表现参数调节、噪音过滤和多因素平衡。

<p align="center">
  <a href="https://frontend-harness-slides-workbench.vercel.app/?view=lab&amp;style=studio-mixing-console&amp;topic=mixing-console&amp;scene=1&amp;beat=0&amp;lang=zh">
    <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/mixing-console.webp" width="32%" alt="录音混音控制台 — Doubao-Seed-Evolving — 混音台 — Hero 最终帧" />
  </a>
  <a href="https://frontend-harness-slides-workbench.vercel.app/?view=lab&amp;style=studio-mixing-console&amp;topic=tidal-time&amp;scene=1&amp;beat=0&amp;lang=zh">
    <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/tidal-time.webp" width="32%" alt="录音混音控制台 — GPT 5.6 Sol — 潮汐时差 — Hero 最终帧" />
  </a>
  <a href="https://frontend-harness-slides-workbench.vercel.app/?view=lab&amp;style=studio-mixing-console&amp;topic=tuning-the-model&amp;scene=1&amp;beat=0&amp;lang=zh">
    <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/tuning-the-model.webp" width="32%" alt="录音混音控制台 — Claude Opus 4.8 — 调模型 — Hero 最终帧" />
  </a>
</p>

#### [Subway Map of Intent](references/style/subway-map-of-intent.md)

系统化、结构清楚。把复杂工作流表现成地铁线路和换乘站。

<p align="center">
  <a href="https://frontend-harness-slides-workbench.vercel.app/?view=lab&amp;style=subway-map-of-intent&amp;topic=subway-flow&amp;scene=1&amp;beat=0&amp;lang=zh">
    <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/subway-flow.webp" width="32%" alt="意图地铁图 — Doubao-Seed-Evolving — 地铁流程 — Hero 最终帧" />
  </a>
  <a href="https://frontend-harness-slides-workbench.vercel.app/?view=lab&amp;style=subway-map-of-intent&amp;topic=tea-cha-routes&amp;scene=1&amp;beat=0&amp;lang=zh">
    <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/tea-cha-routes.webp" width="32%" alt="意图地铁图 — GPT 5.6 Sol — 茶与 Cha — Hero 最终帧" />
  </a>
  <a href="https://frontend-harness-slides-workbench.vercel.app/?view=lab&amp;style=subway-map-of-intent&amp;topic=three-teams-launch&amp;scene=1&amp;beat=0&amp;lang=zh">
    <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/three-teams-launch.webp" width="32%" alt="意图地铁图 — Claude Opus 4.8 — 三队一发 — Hero 最终帧" />
  </a>
</p>

#### [Kitchen Prep Station](references/style/kitchen-prep-station.md)

温暖、具体。把原始输入到干净输出的过程表现成备料台、修剪、菜谱步骤和摆盘。

<p align="center">
  <a href="https://frontend-harness-slides-workbench.vercel.app/?view=lab&amp;style=kitchen-prep-station&amp;topic=prep-station&amp;scene=1&amp;beat=0&amp;lang=zh">
    <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/prep-station.webp" width="32%" alt="厨房备料台 — Doubao-Seed-Evolving — 备料台 — Hero 最终帧" />
  </a>
  <a href="https://frontend-harness-slides-workbench.vercel.app/?view=lab&amp;style=kitchen-prep-station&amp;topic=cocoa-fermentation&amp;scene=1&amp;beat=0&amp;lang=zh">
    <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/cocoa-fermentation.webp" width="32%" alt="厨房备料台 — GPT 5.6 Sol — 可可发酵 — Hero 最终帧" />
  </a>
  <a href="https://frontend-harness-slides-workbench.vercel.app/?view=lab&amp;style=kitchen-prep-station&amp;topic=raw-logs-to-report&amp;scene=1&amp;beat=0&amp;lang=zh">
    <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/raw-logs-to-report.webp" width="32%" alt="厨房备料台 — Claude Opus 4.8 — 日志到报告 — Hero 最终帧" />
  </a>
</p>

#### [Context Bento Box](references/style/context-bento-box.md)

紧凑、有组织。用分格和层叠盒子表达 handoff、多类别概览和上下文包装。

<p align="center">
  <a href="https://frontend-harness-slides-workbench.vercel.app/?view=lab&amp;style=context-bento-box&amp;topic=context-bento&amp;scene=1&amp;beat=0&amp;lang=zh">
    <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/context-bento.webp" width="32%" alt="上下文便当盒 — Doubao-Seed-Evolving — 上下文盒 — Hero 最终帧" />
  </a>
  <a href="https://frontend-harness-slides-workbench.vercel.app/?view=lab&amp;style=context-bento-box&amp;topic=lichen-partners&amp;scene=1&amp;beat=0&amp;lang=zh">
    <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/lichen-partners.webp" width="32%" alt="上下文便当盒 — GPT 5.6 Sol — 地衣伙伴 — Hero 最终帧" />
  </a>
  <a href="https://frontend-harness-slides-workbench.vercel.app/?view=lab&amp;style=context-bento-box&amp;topic=everything-the-intern-needs&amp;scene=1&amp;beat=0&amp;lang=zh">
    <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/everything-the-intern-needs.webp" width="32%" alt="上下文便当盒 — Claude Opus 4.8 — 新人须知 — Hero 最终帧" />
  </a>
</p>

#### [Debug Reaction Board](references/style/debug-reaction-board.md)

开发者原生、偏诊断。使用霓虹状态标记、终端界面和行动看板。

<p align="center">
  <a href="https://frontend-harness-slides-workbench.vercel.app/?view=lab&amp;style=debug-reaction-board&amp;topic=debug-board&amp;scene=1&amp;beat=0&amp;lang=zh">
    <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/debug-board.webp" width="32%" alt="调试反应面板 — Doubao-Seed-Evolving — 调试面板 — Hero 最终帧" />
  </a>
  <a href="https://frontend-harness-slides-workbench.vercel.app/?view=lab&amp;style=debug-reaction-board&amp;topic=acoustic-crack&amp;scene=1&amp;beat=0&amp;lang=zh">
    <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/acoustic-crack.webp" width="32%" alt="调试反应面板 — GPT 5.6 Sol — 听裂缝 — Hero 最终帧" />
  </a>
  <a href="https://frontend-harness-slides-workbench.vercel.app/?view=lab&amp;style=debug-reaction-board&amp;topic=safe-to-deploy&amp;scene=1&amp;beat=0&amp;lang=zh">
    <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/safe-to-deploy.webp" width="32%" alt="调试反应面板 — Claude Opus 4.8 — 能发布吗 — Hero 最终帧" />
  </a>
</p>

### 编辑与印刷

源自编辑设计、出版版式和印刷字体传统的风格。

#### [Magazine Masthead](references/style/magazine-masthead.md)

新闻摊封面般的自信，饱和墨色底色和超大时尚衬线标题引人注目。

<p align="center">
  <a href="https://frontend-harness-slides-workbench.vercel.app/?view=lab&amp;style=magazine-masthead&amp;topic=masthead&amp;scene=1&amp;beat=0&amp;lang=zh">
    <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/masthead.webp" width="32%" alt="杂志刊头 — Doubao-Seed-Evolving — 杂志刊头 — Hero 最终帧" />
  </a>
  <a href="https://frontend-harness-slides-workbench.vercel.app/?view=lab&amp;style=magazine-masthead&amp;topic=moth-experiment&amp;scene=1&amp;beat=0&amp;lang=zh">
    <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/moth-experiment.webp" width="32%" alt="杂志刊头 — GPT 5.6 Sol — 桦尺蛾实验 — Hero 最终帧" />
  </a>
  <a href="https://frontend-harness-slides-workbench.vercel.app/?view=lab&amp;style=magazine-masthead&amp;topic=comeback-issue&amp;scene=1&amp;beat=0&amp;lang=zh">
    <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/comeback-issue.webp" width="32%" alt="杂志刊头 — Claude Opus 4.8 — 回归特刊 — Hero 最终帧" />
  </a>
</p>

#### [Solar Biennale Poster](references/style/solar-biennale-poster.md)

展览海报般的温暖，羊皮纸底色、日光黄氛围和一句巨大的衬线宣言。

<p align="center">
  <a href="https://frontend-harness-slides-workbench.vercel.app/?view=lab&amp;style=solar-biennale-poster&amp;topic=biennale-poster&amp;scene=1&amp;beat=0&amp;lang=zh">
    <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/biennale-poster.webp" width="32%" alt="日光双年展海报 — Doubao-Seed-Evolving — 双年展 — Hero 最终帧" />
  </a>
  <a href="https://frontend-harness-slides-workbench.vercel.app/?view=lab&amp;style=solar-biennale-poster&amp;topic=iron-from-stars&amp;scene=1&amp;beat=0&amp;lang=zh">
    <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/iron-from-stars.webp" width="32%" alt="日光双年展海报 — GPT 5.6 Sol — 恒星炼铁 — Hero 最终帧" />
  </a>
  <a href="https://frontend-harness-slides-workbench.vercel.app/?view=lab&amp;style=solar-biennale-poster&amp;topic=festival-slow-ideas&amp;scene=1&amp;beat=0&amp;lang=zh">
    <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/festival-slow-ideas.webp" width="32%" alt="日光双年展海报 — Claude Opus 4.8 — 慢想节 — Hero 最终帧" />
  </a>
</p>

#### [Warm Editorial Feature](references/style/warm-editorial-feature.md)

杂志专题页风格，暖奶油纸底色、衬线展示字体和引用节奏，适合叙事阅读。

<p align="center">
  <a href="https://frontend-harness-slides-workbench.vercel.app/?view=lab&amp;style=warm-editorial-feature&amp;topic=editorial-feature&amp;scene=1&amp;beat=0&amp;lang=zh">
    <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/editorial-feature.webp" width="32%" alt="暖色专题特稿 — Doubao-Seed-Evolving — 专题特稿 — Hero 最终帧" />
  </a>
  <a href="https://frontend-harness-slides-workbench.vercel.app/?view=lab&amp;style=warm-editorial-feature&amp;topic=oral-to-written&amp;scene=1&amp;beat=0&amp;lang=zh">
    <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/oral-to-written.webp" width="32%" alt="暖色专题特稿 — GPT 5.6 Sol — 史诗成文 — Hero 最终帧" />
  </a>
  <a href="https://frontend-harness-slides-workbench.vercel.app/?view=lab&amp;style=warm-editorial-feature&amp;topic=letter-to-past-self&amp;scene=1&amp;beat=0&amp;lang=zh">
    <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/letter-to-past-self.webp" width="32%" alt="暖色专题特稿 — Claude Opus 4.8 — 写给过去 — Hero 最终帧" />
  </a>
</p>

#### [Scholars' Vellum](references/style/scholars-vellum.md)

古典手稿，古老羊皮纸、页边批注和衬线权威感，适合深度思想内容。

<p align="center">
  <a href="https://frontend-harness-slides-workbench.vercel.app/?view=lab&amp;style=scholars-vellum&amp;topic=scholar-notes&amp;scene=1&amp;beat=0&amp;lang=zh">
    <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/scholar-notes.webp" width="32%" alt="学者羊皮卷 — Doubao-Seed-Evolving — 学者笔记 — Hero 最终帧" />
  </a>
  <a href="https://frontend-harness-slides-workbench.vercel.app/?view=lab&amp;style=scholars-vellum&amp;topic=hidden-text&amp;scene=1&amp;beat=0&amp;lang=zh">
    <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/hidden-text.webp" width="32%" alt="学者羊皮卷 — GPT 5.6 Sol — 重写羊皮卷 — Hero 最终帧" />
  </a>
  <a href="https://frontend-harness-slides-workbench.vercel.app/?view=lab&amp;style=scholars-vellum&amp;topic=what-ancients-knew&amp;scene=1&amp;beat=0&amp;lang=zh">
    <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/what-ancients-knew.webp" width="32%" alt="学者羊皮卷 — Claude Opus 4.8 — 古人的智慧 — Hero 最终帧" />
  </a>
</p>

#### [Front Page Broadsheet](references/style/front-page-broadsheet.md)

报纸头版，多栏布局和标题层级，适合密集信息交付。

<p align="center">
  <a href="https://frontend-harness-slides-workbench.vercel.app/?view=lab&amp;style=front-page-broadsheet&amp;topic=broadsheet&amp;scene=1&amp;beat=0&amp;lang=zh">
    <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/broadsheet.webp" width="32%" alt="头版大报 — Doubao-Seed-Evolving — 大报头版 — Hero 最终帧" />
  </a>
  <a href="https://frontend-harness-slides-workbench.vercel.app/?view=lab&amp;style=front-page-broadsheet&amp;topic=rogue-wave&amp;scene=1&amp;beat=0&amp;lang=zh">
    <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/rogue-wave.webp" width="32%" alt="头版大报 — GPT 5.6 Sol — 怪浪 — Hero 最终帧" />
  </a>
  <a href="https://frontend-harness-slides-workbench.vercel.app/?view=lab&amp;style=front-page-broadsheet&amp;topic=day-feed-stopped&amp;scene=1&amp;beat=0&amp;lang=zh">
    <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/day-feed-stopped.webp" width="32%" alt="头版大报 — Claude Opus 4.8 — 信息流停摆 — Hero 最终帧" />
  </a>
</p>

#### [Duotone Session](references/style/duotone-session.md)

Blue Note 黑胶封套，双色照片和超大压缩哥特字体——冷静、克制、匠人感。

<p align="center">
  <a href="https://frontend-harness-slides-workbench.vercel.app/?view=lab&amp;style=duotone-session&amp;topic=session-poster&amp;scene=1&amp;beat=0&amp;lang=zh">
    <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/session-poster.webp" width="32%" alt="双调录制 — Doubao-Seed-Evolving — 录制海报 — Hero 最终帧" />
  </a>
  <a href="https://frontend-harness-slides-workbench.vercel.app/?view=lab&amp;style=duotone-session&amp;topic=dance-notation&amp;scene=1&amp;beat=0&amp;lang=zh">
    <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/dance-notation.webp" width="32%" alt="双调录制 — GPT 5.6 Sol — 舞谱 — Hero 最终帧" />
  </a>
  <a href="https://frontend-harness-slides-workbench.vercel.app/?view=lab&amp;style=duotone-session&amp;topic=cut-in-one-take&amp;scene=1&amp;beat=0&amp;lang=zh">
    <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/cut-in-one-take.webp" width="32%" alt="双调录制 — Claude Opus 4.8 — 一条过 — Hero 最终帧" />
  </a>
</p>

### 工艺与文化传统

根植于工艺技法、文化视觉传统和实体媒介的风格。

#### [Botanical Specimen Plate](references/style/botanical-specimen-plate.md)

科学植物插画，精细墨线和拉丁标注，适合自然世界主题。

<p align="center">
  <a href="https://frontend-harness-slides-workbench.vercel.app/?view=lab&amp;style=botanical-specimen-plate&amp;topic=specimen-plate&amp;scene=1&amp;beat=0&amp;lang=zh">
    <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/specimen-plate.webp" width="32%" alt="植物标本板 — Doubao-Seed-Evolving — 标本板 — Hero 最终帧" />
  </a>
  <a href="https://frontend-harness-slides-workbench.vercel.app/?view=lab&amp;style=botanical-specimen-plate&amp;topic=leaf-stomata&amp;scene=1&amp;beat=0&amp;lang=zh">
    <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/leaf-stomata.webp" width="32%" alt="植物标本板 — GPT 5.6 Sol — 叶片气孔 — Hero 最终帧" />
  </a>
  <a href="https://frontend-harness-slides-workbench.vercel.app/?view=lab&amp;style=botanical-specimen-plate&amp;topic=anatomy-of-an-idea&amp;scene=1&amp;beat=0&amp;lang=zh">
    <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/anatomy-of-an-idea.webp" width="32%" alt="植物标本板 — Claude Opus 4.8 — 想法解剖 — Hero 最终帧" />
  </a>
</p>

#### [Woodblock Floating World](references/style/woodblock-floating-world.md)

日本浮世绘木刻，浮动世界构图和水墨纹理，适合沉思视觉叙事。

<p align="center">
  <a href="https://frontend-harness-slides-workbench.vercel.app/?view=lab&amp;style=woodblock-floating-world&amp;topic=woodblock&amp;scene=1&amp;beat=0&amp;lang=zh">
    <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/woodblock.webp" width="32%" alt="木版浮世绘 — Doubao-Seed-Evolving — 木版画 — Hero 最终帧" />
  </a>
  <a href="https://frontend-harness-slides-workbench.vercel.app/?view=lab&amp;style=woodblock-floating-world&amp;topic=whistled-language&amp;scene=1&amp;beat=0&amp;lang=zh">
    <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/whistled-language.webp" width="32%" alt="木版浮世绘 — GPT 5.6 Sol — 口哨语言 — Hero 最终帧" />
  </a>
  <a href="https://frontend-harness-slides-workbench.vercel.app/?view=lab&amp;style=woodblock-floating-world&amp;topic=a-rivers-journey&amp;scene=1&amp;beat=0&amp;lang=zh">
    <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/a-rivers-journey.webp" width="32%" alt="木版浮世绘 — Claude Opus 4.8 — 一条河 — Hero 最终帧" />
  </a>
</p>

#### [Cyanotype Drafting Table](references/style/cyanotype-drafting-table.md)

蓝图制图，蓝晒色调和技术线稿，适合系统架构和工程图表。

<p align="center">
  <a href="https://frontend-harness-slides-workbench.vercel.app/?view=lab&amp;style=cyanotype-drafting-table&amp;topic=blueprint&amp;scene=1&amp;beat=0&amp;lang=zh">
    <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/blueprint.webp" width="32%" alt="蓝图制图台 — Doubao-Seed-Evolving — 蓝图 — Hero 最终帧" />
  </a>
  <a href="https://frontend-harness-slides-workbench.vercel.app/?view=lab&amp;style=cyanotype-drafting-table&amp;topic=comet-anatomy&amp;scene=1&amp;beat=0&amp;lang=zh">
    <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/comet-anatomy.webp" width="32%" alt="蓝图制图台 — GPT 5.6 Sol — 彗星解剖 — Hero 最终帧" />
  </a>
  <a href="https://frontend-harness-slides-workbench.vercel.app/?view=lab&amp;style=cyanotype-drafting-table&amp;topic=drawing-a-bridge&amp;scene=1&amp;beat=0&amp;lang=zh">
    <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/drawing-a-bridge.webp" width="32%" alt="蓝图制图台 — Claude Opus 4.8 — 桥的设计 — Hero 最终帧" />
  </a>
</p>

#### [Expedition Screenprint](references/style/expedition-screenprint.md)

田野日志丝网印，叠印图层和地图坐标，适合探索发现叙事。

<p align="center">
  <a href="https://frontend-harness-slides-workbench.vercel.app/?view=lab&amp;style=expedition-screenprint&amp;topic=expedition-print&amp;scene=1&amp;beat=0&amp;lang=zh">
    <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/expedition-print.webp" width="32%" alt="探险丝网印 — Doubao-Seed-Evolving — 探险海报 — Hero 最终帧" />
  </a>
  <a href="https://frontend-harness-slides-workbench.vercel.app/?view=lab&amp;style=expedition-screenprint&amp;topic=saharan-dust&amp;scene=1&amp;beat=0&amp;lang=zh">
    <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/saharan-dust.webp" width="32%" alt="探险丝网印 — GPT 5.6 Sol — 撒哈拉尘 — Hero 最终帧" />
  </a>
  <a href="https://frontend-harness-slides-workbench.vercel.app/?view=lab&amp;style=expedition-screenprint&amp;topic=mapping-unknown-ground&amp;scene=1&amp;beat=0&amp;lang=zh">
    <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/mapping-unknown-ground.webp" width="32%" alt="探险丝网印 — Claude Opus 4.8 — 勘探未知 — Hero 最终帧" />
  </a>
</p>

#### [Machine-Age Deco](references/style/machine-age-deco.md)

Art Deco 机器时代，几何图案和阶梯造型，适合宏大愿景和雄心路线图。

<p align="center">
  <a href="https://frontend-harness-slides-workbench.vercel.app/?view=lab&amp;style=machine-age-deco&amp;topic=deco-gala&amp;scene=1&amp;beat=0&amp;lang=zh">
    <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/deco-gala.webp" width="32%" alt="机器时代装饰艺术 — Doubao-Seed-Evolving — 装饰仪式 — Hero 最终帧" />
  </a>
  <a href="https://frontend-harness-slides-workbench.vercel.app/?view=lab&amp;style=machine-age-deco&amp;topic=reinforced-concrete&amp;scene=1&amp;beat=0&amp;lang=zh">
    <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/reinforced-concrete.webp" width="32%" alt="机器时代装饰艺术 — GPT 5.6 Sol — 钢筋混凝土 — Hero 最终帧" />
  </a>
  <a href="https://frontend-harness-slides-workbench.vercel.app/?view=lab&amp;style=machine-age-deco&amp;topic=grand-unveiling&amp;scene=1&amp;beat=0&amp;lang=zh">
    <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/grand-unveiling.webp" width="32%" alt="机器时代装饰艺术 — Claude Opus 4.8 — 盛大揭幕 — Hero 最终帧" />
  </a>
</p>

#### [Wabi-Sabi Ceramic](references/style/wabi-sabi-ceramic.md)

手捏陶瓷，侘寂不规则感和哑光釉面，适合工艺和天然产品主题。

<p align="center">
  <a href="https://frontend-harness-slides-workbench.vercel.app/?view=lab&amp;style=wabi-sabi-ceramic&amp;topic=ceramic-calm&amp;scene=1&amp;beat=0&amp;lang=zh">
    <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/ceramic-calm.webp" width="32%" alt="侘寂陶器 — Doubao-Seed-Evolving — 陶器静场 — Hero 最终帧" />
  </a>
  <a href="https://frontend-harness-slides-workbench.vercel.app/?view=lab&amp;style=wabi-sabi-ceramic&amp;topic=stone-to-soil&amp;scene=1&amp;beat=0&amp;lang=zh">
    <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/stone-to-soil.webp" width="32%" alt="侘寂陶器 — GPT 5.6 Sol — 石成土 — Hero 最终帧" />
  </a>
  <a href="https://frontend-harness-slides-workbench.vercel.app/?view=lab&amp;style=wabi-sabi-ceramic&amp;topic=beauty-unfinished&amp;scene=1&amp;beat=0&amp;lang=zh">
    <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/beauty-unfinished.webp" width="32%" alt="侘寂陶器 — Claude Opus 4.8 — 未完成之美 — Hero 最终帧" />
  </a>
</p>

#### [Analog Cutout Collage](references/style/analog-cutout-collage.md)

手工剪纸拼贴，撕纸边缘和混合质感，适合创意过程和想法组装。

<p align="center">
  <a href="https://frontend-harness-slides-workbench.vercel.app/?view=lab&amp;style=analog-cutout-collage&amp;topic=cutout-collage&amp;scene=1&amp;beat=0&amp;lang=zh">
    <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/cutout-collage.webp" width="32%" alt="模拟剪纸拼贴 — Doubao-Seed-Evolving — 剪纸拼贴 — Hero 最终帧" />
  </a>
  <a href="https://frontend-harness-slides-workbench.vercel.app/?view=lab&amp;style=analog-cutout-collage&amp;topic=concealed-objects&amp;scene=1&amp;beat=0&amp;lang=zh">
    <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/concealed-objects.webp" width="32%" alt="模拟剪纸拼贴 — GPT 5.6 Sol — 墙中藏物 — Hero 最终帧" />
  </a>
  <a href="https://frontend-harness-slides-workbench.vercel.app/?view=lab&amp;style=analog-cutout-collage&amp;topic=piecing-idea-together&amp;scene=1&amp;beat=0&amp;lang=zh">
    <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/piecing-idea-together.webp" width="32%" alt="模拟剪纸拼贴 — Claude Opus 4.8 — 拼出想法 — Hero 最终帧" />
  </a>
</p>

#### [Cassette-Era Packaging](references/style/cassette-era-packaging.md)

磁带 J-card 设计，80-90 年代图形能量和混音带布局，适合音乐和怀旧内容。

<p align="center">
  <a href="https://frontend-harness-slides-workbench.vercel.app/?view=lab&amp;style=cassette-era-packaging&amp;topic=cassette-pack&amp;scene=1&amp;beat=0&amp;lang=zh">
    <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/cassette-pack.webp" width="32%" alt="卡带时代包装 — Doubao-Seed-Evolving — 卡带包装 — Hero 最终帧" />
  </a>
  <a href="https://frontend-harness-slides-workbench.vercel.app/?view=lab&amp;style=cassette-era-packaging&amp;topic=ice-core-archive&amp;scene=1&amp;beat=0&amp;lang=zh">
    <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/ice-core-archive.webp" width="32%" alt="卡带时代包装 — GPT 5.6 Sol — 冰芯档案 — Hero 最终帧" />
  </a>
  <a href="https://frontend-harness-slides-workbench.vercel.app/?view=lab&amp;style=cassette-era-packaging&amp;topic=greatest-hits-vol1&amp;scene=1&amp;beat=0&amp;lang=zh">
    <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/greatest-hits-vol1.webp" width="32%" alt="卡带时代包装 — Claude Opus 4.8 — 精选辑一 — Hero 最终帧" />
  </a>
</p>

#### [Riso Print Zine](references/style/riso-print-zine.md)

Risograph 手工 zine，限色调、手工拼贴密度和 DIY 反叛气质。

<p align="center">
  <a href="https://frontend-harness-slides-workbench.vercel.app/?view=lab&amp;style=riso-print-zine&amp;topic=riso-zine&amp;scene=1&amp;beat=0&amp;lang=zh">
    <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/riso-zine.webp" width="32%" alt="孔版印刷杂志 — Doubao-Seed-Evolving — 孔版杂志 — Hero 最终帧" />
  </a>
  <a href="https://frontend-harness-slides-workbench.vercel.app/?view=lab&amp;style=riso-print-zine&amp;topic=seven-blues&amp;scene=1&amp;beat=0&amp;lang=zh">
    <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/seven-blues.webp" width="32%" alt="孔版印刷杂志 — GPT 5.6 Sol — 七种蓝 — Hero 最终帧" />
  </a>
  <a href="https://frontend-harness-slides-workbench.vercel.app/?view=lab&amp;style=riso-print-zine&amp;topic=make-something-weekly&amp;scene=1&amp;beat=0&amp;lang=zh">
    <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/make-something-weekly.webp" width="32%" alt="孔版印刷杂志 — Claude Opus 4.8 — 每周做点 — Hero 最终帧" />
  </a>
</p>

#### [Neo-Brutalist Bulletin](references/style/neo-brutalist-bulletin.md)

抗议海报能量，粗黑边框、硬投影和一个高电压强调色。

<p align="center">
  <a href="https://frontend-harness-slides-workbench.vercel.app/?view=lab&amp;style=neo-brutalist-bulletin&amp;topic=brutalist-bulletin&amp;scene=1&amp;beat=0&amp;lang=zh">
    <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/brutalist-bulletin.webp" width="32%" alt="新粗野公告 — Doubao-Seed-Evolving — 粗野公告 — Hero 最终帧" />
  </a>
  <a href="https://frontend-harness-slides-workbench.vercel.app/?view=lab&amp;style=neo-brutalist-bulletin&amp;topic=sinking-delta&amp;scene=1&amp;beat=0&amp;lang=zh">
    <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/sinking-delta.webp" width="32%" alt="新粗野公告 — GPT 5.6 Sol — 下沉三角洲 — Hero 最终帧" />
  </a>
  <a href="https://frontend-harness-slides-workbench.vercel.app/?view=lab&amp;style=neo-brutalist-bulletin&amp;topic=read-before-merge&amp;scene=1&amp;beat=0&amp;lang=zh">
    <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/read-before-merge.webp" width="32%" alt="新粗野公告 — Claude Opus 4.8 — 合并前必读 — Hero 最终帧" />
  </a>
</p>

#### [Red Wedge Agitprop](references/style/red-wedge-agitprop.md)

构成主义政治海报，红色楔形几何和对角线动能，适合行动号召。

<p align="center">
  <a href="https://frontend-harness-slides-workbench.vercel.app/?view=lab&amp;style=red-wedge-agitprop&amp;topic=red-wedge&amp;scene=1&amp;beat=0&amp;lang=zh">
    <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/red-wedge.webp" width="32%" alt="红楔宣传画 — Doubao-Seed-Evolving — 红楔海报 — Hero 最终帧" />
  </a>
  <a href="https://frontend-harness-slides-workbench.vercel.app/?view=lab&amp;style=red-wedge-agitprop&amp;topic=pneumatic-post&amp;scene=1&amp;beat=0&amp;lang=zh">
    <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/pneumatic-post.webp" width="32%" alt="红楔宣传画 — GPT 5.6 Sol — 气动邮政 — Hero 最终帧" />
  </a>
  <a href="https://frontend-harness-slides-workbench.vercel.app/?view=lab&amp;style=red-wedge-agitprop&amp;topic=refactor-the-system&amp;scene=1&amp;beat=0&amp;lang=zh">
    <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/refactor-the-system.webp" width="32%" alt="红楔宣传画 — Claude Opus 4.8 — 重构体制 — Hero 最终帧" />
  </a>
</p>

### 当代数字

源自当前 UI 趋势和平台美学的现代数字优先风格。

#### [Mid-Century Grove](references/style/mid-century-grove.md)

中世纪有机沉静，天然木色调和柔和曲线，适合可持续和天然产品故事。

<p align="center">
  <a href="https://frontend-harness-slides-workbench.vercel.app/?view=lab&amp;style=mid-century-grove&amp;topic=botanical-brand&amp;scene=1&amp;beat=0&amp;lang=zh">
    <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/botanical-brand.webp" width="32%" alt="中世纪林间 — Doubao-Seed-Evolving — 植物品牌 — Hero 最终帧" />
  </a>
  <a href="https://frontend-harness-slides-workbench.vercel.app/?view=lab&amp;style=mid-century-grove&amp;topic=monarch-migration&amp;scene=1&amp;beat=0&amp;lang=zh">
    <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/monarch-migration.webp" width="32%" alt="中世纪林间 — GPT 5.6 Sol — 帝王蝶迁徙 — Hero 最终帧" />
  </a>
  <a href="https://frontend-harness-slides-workbench.vercel.app/?view=lab&amp;style=mid-century-grove&amp;topic=growing-slowly-on-purpose&amp;scene=1&amp;beat=0&amp;lang=zh">
    <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/growing-slowly-on-purpose.webp" width="32%" alt="中世纪林间 — Claude Opus 4.8 — 慢成长 — Hero 最终帧" />
  </a>
</p>

#### [After-Hours Luxe](references/style/after-hours-luxe.md)

深夜鸡尾酒会奢华，深宝石色调和金色点缀，适合高端定位和夜间场景。

<p align="center">
  <a href="https://frontend-harness-slides-workbench.vercel.app/?view=lab&amp;style=after-hours-luxe&amp;topic=after-hours&amp;scene=1&amp;beat=0&amp;lang=zh">
    <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/after-hours.webp" width="32%" alt="深夜奢华 — Doubao-Seed-Evolving — 奢华揭幕 — Hero 最终帧" />
  </a>
  <a href="https://frontend-harness-slides-workbench.vercel.app/?view=lab&amp;style=after-hours-luxe&amp;topic=urushi-cure&amp;scene=1&amp;beat=0&amp;lang=zh">
    <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/urushi-cure.webp" width="32%" alt="深夜奢华 — GPT 5.6 Sol — 漆的固化 — Hero 最终帧" />
  </a>
  <a href="https://frontend-harness-slides-workbench.vercel.app/?view=lab&amp;style=after-hours-luxe&amp;topic=the-midnight-release&amp;scene=1&amp;beat=0&amp;lang=zh">
    <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/the-midnight-release.webp" width="32%" alt="深夜奢华 — Claude Opus 4.8 — 午夜上线 — Hero 最终帧" />
  </a>
</p>

#### [Soft Pastel Friendly](references/style/soft-pastel-friendly.md)

亲切粉彩温暖，圆角药丸几何和柔和弹簧动效，适合引导页和社区 deck。

<p align="center">
  <a href="https://frontend-harness-slides-workbench.vercel.app/?view=lab&amp;style=soft-pastel-friendly&amp;topic=friendly-onboard&amp;scene=1&amp;beat=0&amp;lang=zh">
    <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/friendly-onboard.webp" width="32%" alt="柔和粉彩友好 — Doubao-Seed-Evolving — 友好入门 — Hero 最终帧" />
  </a>
  <a href="https://frontend-harness-slides-workbench.vercel.app/?view=lab&amp;style=soft-pastel-friendly&amp;topic=chrysalis-rebuild&amp;scene=1&amp;beat=0&amp;lang=zh">
    <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/chrysalis-rebuild.webp" width="32%" alt="柔和粉彩友好 — GPT 5.6 Sol — 蛹中重建 — Hero 最终帧" />
  </a>
  <a href="https://frontend-harness-slides-workbench.vercel.app/?view=lab&amp;style=soft-pastel-friendly&amp;topic=first-week-here&amp;scene=1&amp;beat=0&amp;lang=zh">
    <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/first-week-here.webp" width="32%" alt="柔和粉彩友好 — Claude Opus 4.8 — 入职第一周 — Hero 最终帧" />
  </a>
</p>

#### [Retro Windows](references/style/retro-windows.md)

Windows 3.1/95 怀旧，斜面镀铬和系统灰调色板，适合开发者工具和复古科技氛围。

<p align="center">
  <a href="https://frontend-harness-slides-workbench.vercel.app/?view=lab&amp;style=retro-windows&amp;topic=retro-desktop&amp;scene=1&amp;beat=0&amp;lang=zh">
    <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/retro-desktop.webp" width="32%" alt="复古 Windows — Doubao-Seed-Evolving — 复古桌面 — Hero 最终帧" />
  </a>
  <a href="https://frontend-harness-slides-workbench.vercel.app/?view=lab&amp;style=retro-windows&amp;topic=voyager-boundary&amp;scene=1&amp;beat=0&amp;lang=zh">
    <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/voyager-boundary.webp" width="32%" alt="复古 Windows — GPT 5.6 Sol — 日球层边界 — Hero 最终帧" />
  </a>
  <a href="https://frontend-harness-slides-workbench.vercel.app/?view=lab&amp;style=retro-windows&amp;topic=setup-exe&amp;scene=1&amp;beat=0&amp;lang=zh">
    <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/setup-exe.webp" width="32%" alt="复古 Windows — Claude Opus 4.8 — 安装向导 — Hero 最终帧" />
  </a>
</p>

#### [Objective Swiss Grid](references/style/objective-swiss-grid.md)

瑞士国际风格，刚性网格结构和无衬线清晰度，适合数据报告和分析框架。

<p align="center">
  <a href="https://frontend-harness-slides-workbench.vercel.app/?view=lab&amp;style=objective-swiss-grid&amp;topic=swiss-grid&amp;scene=1&amp;beat=0&amp;lang=zh">
    <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/swiss-grid.webp" width="32%" alt="客观瑞士网格 — Doubao-Seed-Evolving — 瑞士网格 — Hero 最终帧" />
  </a>
  <a href="https://frontend-harness-slides-workbench.vercel.app/?view=lab&amp;style=objective-swiss-grid&amp;topic=bridge-movement&amp;scene=1&amp;beat=0&amp;lang=zh">
    <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/bridge-movement.webp" width="32%" alt="客观瑞士网格 — GPT 5.6 Sol — 桥的位移 — Hero 最终帧" />
  </a>
  <a href="https://frontend-harness-slides-workbench.vercel.app/?view=lab&amp;style=objective-swiss-grid&amp;topic=anatomy-timetable&amp;scene=1&amp;beat=0&amp;lang=zh">
    <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/anatomy-timetable.webp" width="32%" alt="客观瑞士网格 — Claude Opus 4.8 — 时刻表解剖 — Hero 最终帧" />
  </a>
</p>

#### [Liquid Glass](references/style/liquid-glass.md)

Apple 设计语言，毛玻璃深度和空间分层，适合高端科技和 Apple 平台内容。

<p align="center">
  <a href="https://frontend-harness-slides-workbench.vercel.app/?view=lab&amp;style=liquid-glass&amp;topic=liquid-glass&amp;scene=1&amp;beat=0&amp;lang=zh">
    <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/liquid-glass.webp" width="32%" alt="液态玻璃 — Doubao-Seed-Evolving — 液态玻璃 — Hero 最终帧" />
  </a>
  <a href="https://frontend-harness-slides-workbench.vercel.app/?view=lab&amp;style=liquid-glass&amp;topic=safety-glass&amp;scene=1&amp;beat=0&amp;lang=zh">
    <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/safety-glass.webp" width="32%" alt="液态玻璃 — GPT 5.6 Sol — 夹层玻璃 — Hero 最终帧" />
  </a>
  <a href="https://frontend-harness-slides-workbench.vercel.app/?view=lab&amp;style=liquid-glass&amp;topic=layers-of-a-product&amp;scene=1&amp;beat=0&amp;lang=zh">
    <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/layers-of-a-product.webp" width="32%" alt="液态玻璃 — Claude Opus 4.8 — 产品的层 — Hero 最终帧" />
  </a>
</p>

#### [Widescreen Title Card](references/style/widescreen-title-card.md)

电影宽银幕标题卡，电影字体和氛围静止感，适合开场标题和宏大揭示。

<p align="center">
  <a href="https://frontend-harness-slides-workbench.vercel.app/?view=lab&amp;style=widescreen-title-card&amp;topic=title-card&amp;scene=1&amp;beat=0&amp;lang=zh">
    <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/title-card.webp" width="32%" alt="宽屏标题卡 — Doubao-Seed-Evolving — 宽屏片头 — Hero 最终帧" />
  </a>
  <a href="https://frontend-harness-slides-workbench.vercel.app/?view=lab&amp;style=widescreen-title-card&amp;topic=whale-fall&amp;scene=1&amp;beat=0&amp;lang=zh">
    <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/whale-fall.webp" width="32%" alt="宽屏标题卡 — GPT 5.6 Sol — 鲸落 — Hero 最终帧" />
  </a>
  <a href="https://frontend-harness-slides-workbench.vercel.app/?view=lab&amp;style=widescreen-title-card&amp;topic=chapter-zero&amp;scene=1&amp;beat=0&amp;lang=zh">
    <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/chapter-zero.webp" width="32%" alt="宽屏标题卡 — Claude Opus 4.8 — 第零章 — Hero 最终帧" />
  </a>
</p>

### 文本报告

#### [Research Memo](references/style/research-memo.md)

克制、可信、有研究感。适合研究发现、高管摘要和需要自洽阅读的证据页面。

<p align="center">
  <a href="https://frontend-harness-slides-workbench.vercel.app/?view=lab&amp;style=research-memo&amp;topic=research-memo&amp;scene=1&amp;beat=0&amp;lang=zh">
    <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/research-memo.webp" width="32%" alt="研究备忘录 — Doubao-Seed-Evolving — 研究备忘 — Hero 最终帧" />
  </a>
  <a href="https://frontend-harness-slides-workbench.vercel.app/?view=lab&amp;style=research-memo&amp;topic=impact-evidence&amp;scene=1&amp;beat=0&amp;lang=zh">
    <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/impact-evidence.webp" width="32%" alt="研究备忘录 — GPT 5.6 Sol — 撞击证据 — Hero 最终帧" />
  </a>
  <a href="https://frontend-harness-slides-workbench.vercel.app/?view=lab&amp;style=research-memo&amp;topic=why-users-churn&amp;scene=1&amp;beat=0&amp;lang=zh">
    <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/why-users-churn.webp" width="32%" alt="研究备忘录 — Claude Opus 4.8 — 用户流失 — Hero 最终帧" />
  </a>
</p>

#### [Maintainer Issue Brief](references/style/maintainer-issue-brief.md)

整洁、结构化、行动导向。灵感来自现代 issue tracker 和代码审查工具。

<p align="center">
  <a href="https://frontend-harness-slides-workbench.vercel.app/?view=lab&amp;style=maintainer-issue-brief&amp;topic=issue-brief&amp;scene=1&amp;beat=0&amp;lang=zh">
    <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/issue-brief.webp" width="32%" alt="维护者问题简报 — Doubao-Seed-Evolving — 问题简报 — Hero 最终帧" />
  </a>
  <a href="https://frontend-harness-slides-workbench.vercel.app/?view=lab&amp;style=maintainer-issue-brief&amp;topic=ozone-hole&amp;scene=1&amp;beat=0&amp;lang=zh">
    <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/ozone-hole.webp" width="32%" alt="维护者问题简报 — GPT 5.6 Sol — 臭氧洞 — Hero 最终帧" />
  </a>
  <a href="https://frontend-harness-slides-workbench.vercel.app/?view=lab&amp;style=maintainer-issue-brief&amp;topic=flaky-test-root-cause&amp;scene=1&amp;beat=0&amp;lang=zh">
    <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/flaky-test-root-cause.webp" width="32%" alt="维护者问题简报 — Claude Opus 4.8 — 不稳定测试 — Hero 最终帧" />
  </a>
</p>

#### [Decision Record](references/style/decision-record.md)

严谨、架构化。用 ADR 节奏呈现上下文、决策、权衡和验证。

<p align="center">
  <a href="https://frontend-harness-slides-workbench.vercel.app/?view=lab&amp;style=decision-record&amp;topic=decision-record&amp;scene=1&amp;beat=0&amp;lang=zh">
    <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/decision-record.webp" width="32%" alt="决策记录 — Doubao-Seed-Evolving — 决策记录 — Hero 最终帧" />
  </a>
  <a href="https://frontend-harness-slides-workbench.vercel.app/?view=lab&amp;style=decision-record&amp;topic=standard-time&amp;scene=1&amp;beat=0&amp;lang=zh">
    <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/standard-time.webp" width="32%" alt="决策记录 — GPT 5.6 Sol — 标准时 — Hero 最终帧" />
  </a>
  <a href="https://frontend-harness-slides-workbench.vercel.app/?view=lab&amp;style=decision-record&amp;topic=why-we-chose-monorepo&amp;scene=1&amp;beat=0&amp;lang=zh">
    <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/why-we-chose-monorepo.webp" width="32%" alt="决策记录 — Claude Opus 4.8 — 选单仓库 — Hero 最终帧" />
  </a>
</p>

#### [Benchmark Matrix](references/style/benchmark-matrix.md)

分析型、比较型。强调结构化证据、评估标准、指标和表格化对比。

<p align="center">
  <a href="https://frontend-harness-slides-workbench.vercel.app/?view=lab&amp;style=benchmark-matrix&amp;topic=benchmark&amp;scene=1&amp;beat=0&amp;lang=zh">
    <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/benchmark.webp" width="32%" alt="基准矩阵 — Doubao-Seed-Evolving — 基准评估 — Hero 最终帧" />
  </a>
  <a href="https://frontend-harness-slides-workbench.vercel.app/?view=lab&amp;style=benchmark-matrix&amp;topic=natural-clocks&amp;scene=1&amp;beat=0&amp;lang=zh">
    <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/natural-clocks.webp" width="32%" alt="基准矩阵 — GPT 5.6 Sol — 自然时钟 — Hero 最终帧" />
  </a>
  <a href="https://frontend-harness-slides-workbench.vercel.app/?view=lab&amp;style=benchmark-matrix&amp;topic=build-buy-borrow&amp;scene=1&amp;beat=0&amp;lang=zh">
    <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/build-buy-borrow.webp" width="32%" alt="基准矩阵 — Claude Opus 4.8 — 自建还是买 — Hero 最终帧" />
  </a>
</p>

#### [Field Notes Report](references/style/field-notes-report.md)

有纸张触感，偏观察记录。使用账簿纸、木炭墨水和卡片网格。

<p align="center">
  <a href="https://frontend-harness-slides-workbench.vercel.app/?view=lab&amp;style=field-notes-report&amp;topic=field-notes&amp;scene=1&amp;beat=0&amp;lang=zh">
    <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/field-notes.webp" width="32%" alt="田野笔记报告 — Doubao-Seed-Evolving — 田野笔记 — Hero 最终帧" />
  </a>
  <a href="https://frontend-harness-slides-workbench.vercel.app/?view=lab&amp;style=field-notes-report&amp;topic=ancient-sound&amp;scene=1&amp;beat=0&amp;lang=zh">
    <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/ancient-sound.webp" width="32%" alt="田野笔记报告 — GPT 5.6 Sol — 古代声音 — Hero 最终帧" />
  </a>
  <a href="https://frontend-harness-slides-workbench.vercel.app/?view=lab&amp;style=field-notes-report&amp;topic=shadowing-support&amp;scene=1&amp;beat=0&amp;lang=zh">
    <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/shadowing-support.webp" width="32%" alt="田野笔记报告 — Claude Opus 4.8 — 跟班客服 — Hero 最终帧" />
  </a>
</p>

#### [Operating Manual](references/style/operating-manual.md)

流程化、高对比。用工业 runbook、终端块和步骤执行来表达可重复操作。

<p align="center">
  <a href="https://frontend-harness-slides-workbench.vercel.app/?view=lab&amp;style=operating-manual&amp;topic=manual&amp;scene=1&amp;beat=0&amp;lang=zh">
    <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/manual.webp" width="32%" alt="操作手册 — Doubao-Seed-Evolving — 运行手册 — Hero 最终帧" />
  </a>
  <a href="https://frontend-harness-slides-workbench.vercel.app/?view=lab&amp;style=operating-manual&amp;topic=escapement&amp;scene=1&amp;beat=0&amp;lang=zh">
    <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/escapement.webp" width="32%" alt="操作手册 — GPT 5.6 Sol — 擒纵器 — Hero 最终帧" />
  </a>
  <a href="https://frontend-harness-slides-workbench.vercel.app/?view=lab&amp;style=operating-manual&amp;topic=rotate-the-secrets&amp;scene=1&amp;beat=0&amp;lang=zh">
    <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/rotate-the-secrets.webp" width="32%" alt="操作手册 — Claude Opus 4.8 — 轮换密钥 — Hero 最终帧" />
  </a>
</p>

#### [Checklist Ledger](references/style/checklist-ledger.md)

可靠、务实。用账簿线、紧凑行和可见 check 表达验收标准和最终准备度。

<p align="center">
  <a href="https://frontend-harness-slides-workbench.vercel.app/?view=lab&amp;style=checklist-ledger&amp;topic=checklist-ledger&amp;scene=1&amp;beat=0&amp;lang=zh">
    <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/checklist-ledger.webp" width="32%" alt="检查清单台账 — Doubao-Seed-Evolving — 检查清单 — Hero 最终帧" />
  </a>
  <a href="https://frontend-harness-slides-workbench.vercel.app/?view=lab&amp;style=checklist-ledger&amp;topic=pigment-without-touch&amp;scene=1&amp;beat=0&amp;lang=zh">
    <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/pigment-without-touch.webp" width="32%" alt="检查清单台账 — GPT 5.6 Sol — 无损识色 — Hero 最终帧" />
  </a>
  <a href="https://frontend-harness-slides-workbench.vercel.app/?view=lab&amp;style=checklist-ledger&amp;topic=close-the-quarter&amp;scene=1&amp;beat=0&amp;lang=zh">
    <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/close-the-quarter.webp" width="32%" alt="检查清单台账 — Claude Opus 4.8 — 季度结账 — Hero 最终帧" />
  </a>
</p>

#### [Annotated Source & Diff](references/style/annotated-source-and-diff.md)

可审查、强调变化。用 before/after、注释和类源码界面直接证明改动价值。

<p align="center">
  <a href="https://frontend-harness-slides-workbench.vercel.app/?view=lab&amp;style=annotated-source-diff&amp;topic=source-diff&amp;scene=1&amp;beat=0&amp;lang=zh">
    <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/source-diff.webp" width="32%" alt="注解源码与差异 — Doubao-Seed-Evolving — 源码差异 — Hero 最终帧" />
  </a>
  <a href="https://frontend-harness-slides-workbench.vercel.app/?view=lab&amp;style=annotated-source-diff&amp;topic=reading-rosetta&amp;scene=1&amp;beat=0&amp;lang=zh">
    <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/reading-rosetta.webp" width="32%" alt="注解源码与差异 — GPT 5.6 Sol — 破译罗塞塔 — Hero 最终帧" />
  </a>
  <a href="https://frontend-harness-slides-workbench.vercel.app/?view=lab&amp;style=annotated-source-diff&amp;topic=killing-a-god-object&amp;scene=1&amp;beat=0&amp;lang=zh">
    <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/killing-a-god-object.webp" width="32%" alt="注解源码与差异 — Claude Opus 4.8 — 拆解巨类 — Hero 最终帧" />
  </a>
</p>

<p align="center">
  <a href="https://frontend-harness-slides-workbench.vercel.app/"><b>🎬 动态 Demo</b></a>
</p>

## 我的更多精选 Skill

更多我长期维护、偏实战的精选 Agent Skills，见
[Awesome Skills](https://github.com/patrick-fu/awesome-skills)。
