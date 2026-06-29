# frontend-harness-slides Anti-Pattern Catalog（完整 10 条扩展版）

本文档对应 SKILL.md **§VII Anti-patterns** 的完整扩展版。每条包含：触发条件、为什么是反模式、代码/工程反例、正确修复方式。

---

## #1 用 canvas 渲染整页静态内容

**触发场景**：嫌布局麻烦、想用「画笔画一张图」的方式做幻灯片；或用第三方图表库默认渲染 canvas 整张 poster。

**为什么是反模式**：
- Canvas 文本不可选中、不可复制、不可被无障碍读屏。
- 导出 PDF 时整张幻灯片变成位图，放大即糊。
- auditor 的 `hasOwnText` / `0×0 折叠检查` 对 canvas 内容完全失效。
- 响应 `textContent` / DOM 查询的第三方工具（翻译、对比、搜索）全部失效。

**反例**：
```jsx
// ❌ 整张 slide 用 canvas 画
<canvas width={1920} height={1080} ref={paintAll}/>
```

**正确做法**：
- 静态文本 → DOM；
- 图表只在真正的动态数据区域（柱状、折线）使用 canvas / SVG，标题和标签保留 DOM；
- 必须位图化的区域，上叠加一层透明 `aria-label` 文本容器。

---

## #2 <10 页、一次性交付还启用本 Skill

**触发场景**：用户说「做一个 8 页的分享会 PPT」，嫌切换 Skill 麻烦就直接用了 harness-slides。

**为什么是反模式**：
- Vite + React + Playwright + 两个 spec + CI + 路由 + beat 控制器这一套在 <10 页一次性场景下是**纯负担**。
- `npm install` 比写 8 页 HTML 还慢。
- 8 页内容本来就不会「以后改 20 次」，像素回归测试完全浪费。

**正确做法**：
- <10 页一次性 → `frontend-slides`（单文件 HTML + deck-stage.js，2 分钟启动）；
- 10–14 页看生命周期：有 git + CI + 会改 ≥3 次才用 harness；否则还是 `frontend-slides`。

---

## #3 beat 仅用于淡入淡出文字

**触发场景**：把 beat 当成「CSS transition 触发器」——每出现一行文字就是一个新 beat。

**为什么是反模式**：
- 每个 beat 都会生成一份 Playwright 视觉基线（`{id}-beat-{n}.png`），10 个空 beat = 10 张无用截图 + 10 倍 CI 磁盘。
- 讲述者按 10 次 Space 只是看文字一行一行蹦出来，观众感知不到「故事推进」。

**正确做法**：
- 一个 beat = 一个**故事单元**（新论点、新图表、新对比）；
- 同一论点内部的文字淡入 → 用 framer-motion 的 `staggerChildren`，不拆 beat。

---

## #4 Stage 内用 responsive breakpoints（md:/lg:）

**触发场景**：作者习惯了 Tailwind 响应式，看到舞台缩在小手机上就写 `md:text-9xl text-4xl`。

**为什么是反模式**：
- Stage 内部坐标系永远是 1920×1080。`md:` 断点看的是**视口宽度**，1920×1080 画布在 375px 手机上显示时，`md:` 已经触发，文字变得巨大溢出 stage；
- 反过来在 34 寸宽屏上，视口超过 `lg:`，但 stage 仍是 1920×1080，样式完全错乱。

**正确做法**：
- 所有尺寸用**绝对像素**（stage 里的 32px 永远是 32px）；
- 真的需要"手机上缩小"——在 stage 外层缩放的基础上，自己按 `window.devicePixelRatio` 或父容器 scale 调整 meta 容器。

---

## #5 Stage 内嵌 iframe 做可交互 Demo

**触发场景**：想在幻灯片里嵌入一个 CodeSandbox / CodePen / Storybook 演示。

**为什么是反模式**：
- iOS Safari 对 iframe 内部 layout 的缩放与桌面不一致，一个看起来正常的 iframe 在 iPhone 上会横向溢出 stage；
- `[data-slide-stage]` 的 overflow 检查对 iframe 内部没有用；
- Playwright 截图时，跨域 iframe 内容常是空白（需要额外 `waitForLoadState("networkidle")`，CI 里常常卡住）；
- 导出 PDF 时 iframe 内容要么空、要么是第一帧位图。

**正确做法**：
- Demo 做成**外链** + 一张高保真截图作为封面；
- 演讲时切到新 Tab 演示，讲完再切回 deck。

---

## #6 用 CSS zoom 做舞台缩放

**触发场景**：觉得 `transform: scale()` 太繁琐，就一句 `zoom: 0.875` 解决。

**为什么是反模式**：
- `zoom` 是非标准属性（W3C 没收录），Firefox 不认；
- zoom 缩放后 `getBoundingClientRect()` 在 Chromium 和 WebKit 里返回的坐标不一致——**导致 auditor 的「不溢出 stage」检查给出假阳性/假阴性**；
- 子元素的 `position: fixed` 相对谁的问题在各引擎上有不同实现。

**正确做法**：
- `transform: scale(var(--scale))` + `transform-origin: top left`。
- 所有 BCR 计算都基于 stage 原始坐标系 → auditor 与导出 PDF 共享几何源。

---

## #7 Registry 里同一张图引用超过 3 次

**触发场景**：比如 deck 里每张 slide 右上角都有 "产品 logo + 吉祥物" 小图块，作者就 `import logo from './logo.svg'` 然后到处粘贴 `<img src={logo} className=...>`。

**为什么是反模式**：
- 每次改动 logo 的尺寸 / 外边距 / alt 文案，要在 N 个 scene 文件里同步改。容易漏 → 回归；
- Playwright 视觉快照对比时，任何一个 logo 的偏差都会产生 N 张失败的截图。

**正确做法**：
- 提取成 shared component（`<ProductLogoChip />`），所有 scene 引用同一个组件；
- 真的只想改其中 1 张，再在那一张里单独覆盖 props。

---

## #8 默认引入完整 CJK 字体（20MB+ WOFF2）

**触发场景**：幻灯片里有中文，直接 `<link href='google fonts Noto Sans SC'>` 引入全量 Noto。

**为什么是反模式**：
- Noto Sans SC 全量 WOFF2 约 10–20MB；**auditor 的 H-5 requestfailed + HTTP 4xx 健康度通道不会报字体错（它是正常 200 OK），但首屏加载慢到让所有 Playwright 截图 `waitUntil: 'networkidle'` 超时**；
- CI 环境下载 Google Fonts 失败率不低（网络波动），导致 snapshot baseline 用 fallback 字体然后全红。
- PDF 导出时字体加载顺序不稳定，造成文字轻微错位。

**正确做法**：
- 用 `glyphhanger` + `pyftsubset` 只子集化 deck 里实际出现的字；目标是每个 CJK 字体 <1MB；
- 字体文件 **check-in 到 public/fonts/**，不要外链 CDN；
- auditor 里用 `document.fonts.ready` + 检查实际渲染 fontFamily 是否真切换到目标字体。

---

## #9 全写 expect.soft 忘记兜底 hard 断言

**触发场景**：作者想一次看到所有失败（而不是第一个就退出），就把所有断言改成 `.soft()`。

**为什么是反模式**：
- `expect.soft()` **本身不会让测试 fail**。CI 报告会显示绿色（pass），虽然 console 里有一堆红字；
- 审计失败完全被隐藏，harness 变成「看日志看运气」。

**反例**：
```ts
for (const beat of ...) {
  expect.soft(landed.beat).toBe(String(beat)); // ❌ soft 不会让测试变红
  expect.soft(page).toHaveScreenshot(/*...*/); // ❌ 同上
}
// 没有 hard 兜底 → 全部失败也 green
```

**正确做法**：
- 每段 soft 后面紧跟着一条硬断言：
  ```ts
  expect(test.info().errors, 'Soft assertions accumulated failures').toHaveLength(0);
  ```
- 跨生命周期的（如 beforeEach 监听的 pageerror）放在 `test.afterEach()` 里统一兜底（starter 的 visual.spec.ts 已内置此模式）。

---

## #10 build 通过就跳过 harness

**触发场景**："我只是改了一个 CSS 颜色值，`npm run build` 已经过了，harness 跑起来要 2 分钟——先 commit 再说"。

**为什么是反模式**：
- TypeScript 通过 ≠ 渲染正确：一个 Tailwind 类名拼错（`bg-primery`），类型完全没问题但整张幻灯片背景变白；
- 文本多了几个字导致某个卡片 0×0 折叠或溢出 stage，**build 过程也完全不会报错**；
- 真正"跳过 harness 不会出问题"的改动只有：注释、README.md、纯文档——其他任何能触达 src/ 的改动都必须跑。

**正确做法**：
- CI 配置里 `test:ci` 作为必过 gate（starter 的 `.github/workflows/harness.yml.example` 已启用）；
- 本地快速验证时可以只跑 auditor（`npm run test:audit`，大约 15 秒），它比 visual baseline 快 10 倍。
