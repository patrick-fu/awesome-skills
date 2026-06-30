# Frontend Harness Slides

**[English](README.md)**

让 Agent 做一套可以反复修改、但不容易静默改坏其他页面的 HTML slides。

单体 HTML 很适合快速出第一版。真正麻烦的是第一版之后：用户会要求改某页文案、加一个章节、删一页、调动画、替换截图、把某个信息密度过高的页面改得更清楚。单体文件里，一个小小的 CSS 或动画改动可能会意外影响别的页面，而且往往到 review 时才发现。

`frontend-harness-slides` 解决的是这个反复改造阶段的问题。它不提供 starter
工程，也不要求 React、Vite、Tailwind、Playwright 或任何固定框架。它提供的是一套框架无关的 harness 思路：稳定帧地址、registry、固定舞台、可冻结渲染、结构审计，以及必要时的视觉检查。

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

1. 先和用户对齐 slides 风格、信息密度、动画方向、stage 尺寸、触屏导航、素材来源和交付方式。
2. 根据用户现有项目和偏好选择项目目录与技术栈。
3. 在该技术栈里实现 harness 机制。
4. 把 deck 做成稳定 scene 和有意义的 beat。
5. 迭代时跑最小有用检查，交付前跑最终 gate。
6. 最终画面符合预期后再部署，或按当前项目需要做交付导出。

用户不需要亲自操作前端工具链。关键是 Agent 有足够结构把多轮改造控制住。

## 什么时候适合

当 slides 不是很小的一次性静态页面，后续可能会收反馈、调动画、改结构、用到截图/图表，或者需要在交付前确认每一帧没有被改坏时，用它。

如果只是非常小的静态一次性页面，单体 HTML 已经足够，而且不需要任何回归 harness，那就没必要上这套工程。

## 更多 Skills

更多可复用的 agent skills，见
[Awesome Skills](https://github.com/patrick-fu/awesome-skills)。
