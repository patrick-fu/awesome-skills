# Frontend Harness Slides

**[English](README.md)**

让 Agent 做一套可以反复修改、但不容易静默改坏其他页面的 HTML slides。

单体 HTML 很适合快速出第一版。真正麻烦的是第一版之后：用户会要求改某页文案、加一个章节、删一页、调动画、替换截图、把某个信息密度过高的页面改得更清楚。单体文件里，一个小小的 CSS 或动画改动可能会意外影响别的页面，而且往往到 review 时才发现。

`frontend-harness-slides` 解决的是这个反复改造阶段的问题。它不提供 starter
工程，也不要求 React、Vite、Tailwind、Playwright 或任何固定框架。它提供的是一套框架无关的 harness 思路：稳定帧地址、registry、固定舞台、可冻结渲染、结构审计，以及必要时的视觉检查。

主 Skill 文档保持精简，避免误触发时浪费上下文。一旦确认用户真的要制作或大改
slides，Agent 必须先阅读四个阶段 reference：规划、设计、实现、验证与交付。

## 安装

```bash
npx skills add patrick-fu/frontend-harness-slides
```

后续更新：

```bash
npx skills update
```

## 它解决什么问题

- **反复修改时不静默牵连别的页**：scene 和 beat 都是可打开、可测试的稳定帧，而不是藏在一个大文件里的隐式状态。
- **安全插页、删页、重排**：中心 registry 管理顺序，scene id 和视觉基线保持稳定。
- **布局固定**：每页都在固定比例 stage 内编排，整体缩放，不按 viewport 重新排版。
- **动画可 review**：冻结模式让帧检查变得确定。
- **交付前先确认画面**：最终采用浏览器演示、部署还是项目特定导出，都先以已检查的帧为准。

## Agent 怎么使用

1. **规划**：和用户对齐内容取向、演讲形式、时长、内容占比、风格、信息密度、动画、stage、导航、技术栈和交付方式。给推荐值，也给备选项；风格不明确时，默认建议先做 1-2 张真实 slides 预览。
2. **设计**：确定视觉方向、字体、素材、文案边界和组件选择。内部对齐信息不能默认写到 slide 画布上。
3. **实现**：在选定技术栈里实现稳定 scene、meaningful beats、固定/移动端 stage、冻结模式、键盘/触摸导航和互动动效。
4. **验证与交付**：跑结构审计、视觉 smoke、交互/移动端检查；如部署上线，还要跑 production smoke；最后交付线上 URL、PDF/静态导出，或二者兼顾。

用户不需要亲自操作前端工具链。关键是 Agent 有足够结构把多轮改造控制住。

## 阶段 Reference

确认是非小型 deck 制作或大改后，Agent 应按顺序阅读：

- `references/01-plan.md`：前置对齐、推荐值和备选项、风格预览、技术栈、内容 registry、可见文案边界。
- `references/02-design.md`：视觉风格、风格预设、手绘 emoji 方向、字体、CJK、素材、组件、文案质量。
- `references/03-build.md`：harness contract、移动端固定舞台、导航、冻结模式、动效、交互和实现陷阱。
- `references/04-verify-and-ship.md`：audit profile、视觉 smoke、production smoke、移动端/WebKit 覆盖、部署、PDF/静态交付和最终报告。

## 什么时候适合

当 slides 不是很小的一次性静态页面，后续可能会收反馈、调动画、改结构、用到截图/图表，或者需要在交付前确认每一帧没有被改坏时，用它。

如果只是非常小的静态一次性页面，单体 HTML 已经足够，而且不需要任何回归 harness，那就没必要上这套工程。

## 更多 Skills

更多可复用的 agent skills，见
[Awesome Skills](https://github.com/patrick-fu/awesome-skills)。
