# Frontend Harness Slides

**[English](README.md)**

让 Agent 做一套可以反复修改、但不容易静默改坏其他页面的 HTML
slides。

单体 HTML 很适合快速出第一版。真正麻烦的是第一版之后：用户会要求改某页文案、加一个章节、删一页、调动画、替换截图、把某个信息密度过高的页面改得更清楚。单体文件里，一个小小的 CSS 或动画改动可能会意外影响别的页面，而且往往到 review 时才发现。

`frontend-harness-slides` 解决的是这个反复改造阶段的问题。它从一个
React/Vite slides 工程开始，并配套 Playwright harness：审计结构、冻结动画、逐帧视觉回归。Agent 可以在交付前先确认每一帧没有被改坏，再按项目需要选择浏览器演示、部署或临时导出方式。

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
- **布局固定**：每页都在 1920x1080 stage 内编排，整体缩放，不按 viewport 重新排版。
- **动画可 review**：test mode 会冻结帧，让像素 diff 代表真实变化，而不是动画时序抖动。
- **交付前先确认画面**：最终采用浏览器演示、部署还是项目特定导出，都先以已检查的帧为准。

## Agent 怎么使用

1. 先和用户对齐受众、信息密度、素材来源、视觉方向。
2. 复制内置 starter。
3. 把每页做成 React scene，并用稳定 id 注册。
4. 迭代时按风险选择测试层级，交付前跑 full gate。
5. 只有确认是有意变化时才更新视觉基线。
6. 最终画面符合预期后再部署，或按当前项目需要做临时交付导出。

用户不需要亲自操作前端工具链。关键是 Agent 有一套 harness，能把多轮改造控制住。

## 快速开始

```bash
cp -r ~/.agents/skills/frontend-harness-slides/assets/starter ./my-deck
cd ./my-deck
npm install
npx playwright install chromium
npm run doctor
npm run dev
```

第一次生成基线并验证：

```bash
npm run visual:update
npm run test:full
```

## 什么时候适合

当 slides 不是很小的一次性静态页面，后续可能会收反馈、调动画、改结构、用到截图/图表，或者需要在交付前确认每一帧没有被改坏时，用它。

如果只是非常小的静态一次性页面，单体 HTML 已经足够，而且不需要任何回归 harness，那就没必要上这套工程。

## 更多 Skills

更多可复用的 agent skills，见
[Awesome Skills](https://github.com/patrick-fu/awesome-skills)。
