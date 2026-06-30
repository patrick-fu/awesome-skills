# frontend-harness-slides Troubleshooting（完整 9 条扩展版）

本文档对应 SKILL.md **§VIII Troubleshooting** 的完整扩展版。每条包含：根因分类、定位步骤、精确修复命令、如何在未来避免再次踩坑。

---

## Q1: Playwright visual 快照第一次全红

### 根因
Playwright 的 `toHaveScreenshot()` 是「对比模式」——**第一次跑没有基线**，每个截图都会被标记为失败（因为它不知道「正确的」应该长什么样）。

### 定位
日志里会出现类似文字：
```
Error: A snapshot doesn't exist at tests/snapshots/cover-beat-0.png, writing actual.
```
这**不是 bug**。

### 修复命令
```bash
# 第一次生成基线
npx playwright test visual.spec.ts --update-snapshots

# （或 npm 脚本）
npm run visual:update
```
生成后把 `tests/snapshots/*.png` 全部加入 git 并提交。**后续 CI 会对比这些基线**。

### 避坑
- 第一次生成基线时，一定要**在本地肉眼看一遍每一张截图**（至少抽查 20%），CI 只会和基线比较——基线本身错了 CI 永远会给你假绿。

---

## Q2: 视觉快照文字错位

### 根因（按概率排序）
1. **本地字体 vs CI 字体不一致**（99%）：本地系统装了 `Noto Sans SC`，CI 容器里没有，文本 fallback 到 Liberation Sans → 字符宽度差异 → 换行点不同 → 错位；
2. **字体加载 race**：Chromium 截图时字体还没加载完，第一帧用 fallback 字体；
3. **font-render-hinting 差异**：不同平台的 hinting 参数让 baseline 偏移 1–2px，逐字累加后整行错位。

### 定位
- 打开错位的截图或 handoff 产物，对比 CI 产物与本地产物；
- Playwright trace 文件里检查 `document.fonts.status` 是否 `loaded`。

### 修复
```bash
# 1) 字体永远子集化 WOFF2 + 本地放置（不要 CDN）
glyphhanger --subset=./raw-fonts/NotoSansSC.ttf \
  --LATIN --formats=woff2 --css \
  --whitelist=./deck-text-corpus.txt \
  --outDir=starter/public/fonts

# 2) auditor 里加 @font-face loaded 检查（starter 已内置）
# （auditor.spec.ts: await page.evaluate(() => document.fonts.ready);）

# 3) playwright.config 的 chromium 启动参数加
#    '--font-render-hinting=none'
```

### 避坑
- 永远不要让 deck 使用「系统可能有也可能没有」的字体。**所有使用的 display/body 字体必须在 starter/public/fonts 里有一份 WOFF2**。

---

## Q3: SandboxIsolator 和 SlideDeck 的键盘隔离是怎么配合的？（老项目迁移必读）

### 背景：v1.0.0 之前的错误文档
v1.0.0 有一批早期文档写「SandboxIsolator 已删除，功能合并到 SlideDeck 白名单」——**这个说法是错误的**。实际实现是：

**SandboxIsolator 仍然作为组件存在**（146 行，`src/components/SandboxIsolator.tsx`），并**新增**了 SlideDeck 层的白名单检查，形成**双层隔离模型**。

### 双层的职责划分

| 层 | 机制 | 覆盖的情况 | 不覆盖的情况 |
| :--- | :--- | :--- | :--- |
| Layer 1：SlideDeck 的 `isEditableEventTarget()` | keydown 处理函数开头先判断目标是否是 `<input>`/`<textarea>`/`<select>`/`contenteditable`/`role="textbox"`；是则直接 return | 所有没被 SandboxIsolator 包裹的可编辑元素；原生标签 | 自定义 Web Component、React 自定义 Input 组件（真实 DOM 可能不含这些标签） |
| Layer 2：SandboxIsolator wrapper | 原生 `addEventListener('keydown', handler, { capture: true })` + `stopImmediatePropagation()` 吞掉 Space/Enter/方向键/PageUp/PageDown/Home/End/Backspace 和 vim 风格导航键 | 自定义组件、嵌入式编辑器、iframe 外部容器、滚轮/contextmenu、任何无法被 Layer1 白名单识别的交互 | 包裹范围之外的元素（必须显式套一层） |

### 老项目迁移
如果你的老项目确实看到了「SandboxIsolator 被删除」的提示：
```bash
# 1. 升级 starter（把 src/components/SandboxIsolator.tsx 覆盖为最新版）
cp -r NEW_STARTER/src/components/SandboxIsolator.tsx YOUR_PROJECT/src/components/

# 2. 恢复所有被删除的 <SandboxIsolator> 包裹
# （搜索 "SandboxIsolator" 看 git diff 里删了哪些地方）
git log -p --all -S 'SandboxIsolator' | head -200
```

### 避坑
- 简单可编辑元素（单 `<input>` / `<textarea>`）只靠 Layer 1 就能工作；
- **嵌入式代码编辑器、Playground、iframe Demo、自定义交互组件 → 必须加 Layer 2**。

---

## Q4: 图片裁切或比例不符合预期

### 根因
常见原因是 scene 中直接使用了 `object-fit: cover`、固定宽高或绝对定位，但没有明确图片的裁切焦点。浏览器会按容器比例裁掉图片边缘，这在产品截图、人物照片、logo 上尤其明显。

### 修复
```css
.screenshot {
  object-fit: contain;   /* 完整显示，适合 logo / UI 截图 */
}

.hero-photo {
  object-fit: cover;     /* 允许裁切，适合氛围图 */
  object-position: 50% 35%;
}
```

如果图片是页面核心证据，优先 `contain`，不要为了填满版面裁掉关键信息。

---

## Q5: Playwright Chromium 缺失或下载慢

### 根因
`@playwright/test` 是 **driver + 浏览器分离**架构：`node_modules` 里只有 driver，真正的 Chromium/Firefox/WebKit 在 `~/.cache/ms-playwright/`，第一次需要下载。离线环境或国内网络环境下，下载会卡住 5–10 分钟甚至超时。

### 修复
```bash
# 方案 A：正常下载（推荐）
npx playwright install chromium

# 方案 B：只下载 chrome / msedge（复用系统 Chromium，体积小 30%）
npx playwright install chrome

# 方案 C：离线环境
# 1) 另一台能上网的机器打包：
npx playwright install chromium
tar czf ms-playwright-cache.tgz -C ~ .cache/ms-playwright
# 2) 离线机器解压：
tar xzf ms-playwright-cache.tgz -C ~
# 3) 设置 PLAYWRIGHT_BROWSERS_PATH 跳过自动下载检查
export PLAYWRIGHT_SKIP_BROWSER_DOWNLOAD=1
```

### 避坑
`npm install` 只安装 Playwright driver，不保证 Chromium binary 已经存在。新环境下总是显式运行：

```bash
npx playwright install chromium
```

---

## Q6: 舞台缩放时，fixed 定位元素位置错

### 根因
`position: fixed` 相对**视口**定位；`transform: scale()` 作用在 stage 上，但它不会改变 fixed 元素的参考坐标系（只有 transform 祖先会影响**非 fixed** 的绝对定位参考）。所以缩放后：
- 原来 `right: 80px; top: 80px` 的 logo —— 实际跑到视口右上角（stage 外面）；
- viewport 比 stage 宽时，fixed 元素距离 stage 右边越来越远；

### 修复
```diff
- position: fixed;
+ position: absolute;
```
父容器（一般是 `[data-slide-stage]`）已经是 `position: relative`，所以 `absolute` 就是相对 stage 1920×1080 的正确坐标，缩放后自然对齐。

### 避坑
- **在 Slide Stage 内部永远不用 `position: fixed`**。这是 auditor 将来会加的一条新规则（目前需要人工检查）。

---

## Q7: 按 Space / 方向键无法翻页

### 根因（按概率）
1. 焦点在 `<textarea>` 或 `<input>` 里（Layer 1 白名单把 Space 让给它们了）；
2. 某个自定义交互组件主动 `preventDefault()` 或被 `SandboxIsolator` 包裹；
3. SandboxIsolator 包裹了整页（包括舞台空白处）——极少见，属于错误使用。

### 修复
1. **点击舞台空白处失焦**（最快解）；
2. 检查当前焦点元素：`document.activeElement`；
3. 检查 SandboxIsolator 的包裹范围是否过大：
   ```diff
   - <SandboxIsolator><SlideStage>...</SlideStage></SandboxIsolator>  ❌
   + <SlideStage>
   +   <SandboxIsolator><CodePlayground /></SandboxIsolator>  ✅  只包真的需要隔离的部分
   + </SlideStage>
   ```

---

## Q8: Auditor「0×0 折叠检查」在 CJK 单字/双字标题上漏检

### 根因
旧版 `hasOwnText`（v1.0.0 P0 修复前）：
```ts
const hasOwnText = (el) =>
  Array.from(el.childNodes).some(
    n => n.nodeType === Node.TEXT_NODE && (n.textContent ?? '').trim().length > 2,
  );
```
问题：
1. 用 `String.length` 不是 Unicode code-point 计数——`'🧑🏽‍🚀'.length = 7` 实际 1 个字；CJK 的 surrogate pair 也会被误算；
2. 阈值 `>2` 是英文语感写的：「Hi」（2）、「OK」（2）被当空节点跳过。但 CJK 的**单字标题**（「一」`length=1`）、**双字**（「你好」`length=2`）全部被误判为空。
3. 纯标点节点（只有「。，、」）被算成「有内容」→ 一个只含句号的空节点如果被 display:none 掉，也不会触发折叠警告。

### P0 修复后
starter 的 auditor.spec.ts 已经切换为：
```ts
const PUNCT_RE = /^[\p{P}\p{Z}\s]+$/u;
const hasOwnText = (el) =>
  Array.from(el.childNodes).some(n => {
    if (n.nodeType !== Node.TEXT_NODE) return false;
    const raw = (n.textContent ?? '').trim();
    if (!raw) return false;
    if (PUNCT_RE.test(raw)) return false;     // 纯标点 → 不算内容
    return [...raw].length > 0;               // Unicode code-point 计数（spreads code units）
  });
```

### 如果你 fork 了旧 starter
```bash
# 定位：哪些 selector 在 auditor 里被调用
grep -n 'hasOwnText\|childNodes.*TEXT_NODE' YOUR_PROJECT/tests/auditor.spec.ts

# 替换：把 hasOwnText 的实现完整替换为上面 P0 修复后的版本
```

### 避坑
- 需要跳过折叠检查的节点（例如装饰性空 div）→ 加 `data-allow-empty`（已内置）；
- 强制要求被检查（哪怕 hasOwnText 返回 false）→ 目前没内置，可临时给元素加一个零宽空格 + `data-audit-force`。

---

## Q9: 视觉快照抖动（maxDiffPixels > 100 但代码没变）

### 根因概率表 + 排查顺序

| 优先级 | 根因 | 诊断方式 | 修复 |
|:---:|:---|:---|:---|
| 1 | **字体加载不完整** | 截图前 `document.fonts.status !== 'loaded'`；trace 里看到 @font-face 资源在 screenshot 之后才 complete | visual.spec.ts 已内置 `await page.evaluate(() => document.fonts.ready)`，请检查 fork 是否删除；字体走 WOFF2 + 本地放置（见 Q2） |
| 2 | **Sub-pixel 抗锯齿抖动** | 同截图在 Mac x86 / Mac ARM / Linux CI 上有差异；字符 baseline 偏移 0.5–1px | Chromium 启动参数加 `--font-render-hinting=none`；DPR=1（playwright.config 已内置 deviceScaleFactor） |
| 3 | **Spring 动画未完全衰减** | `framer-motion` spring type=spring / inertia，虽然视觉停了但 WAAPI 动画还在微步长推进 | `waitForAnimationsToSettle` 默认 3×50ms，超慢动画加 `{ stableRounds: 5, intervalMs: 80 }`；或在 `?test=true` 模式下主动让组件设置 spring stiffness=0 |
| 4 | **canvas / video / lottie 内容不冻结** | diff 集中在 canvas 区域（视频帧不同、rAF 绘制循环不同帧） | 已在 `VISUAL_MASK_SELECTORS` 共源遮罩（canvas/video/iframe/lottie-player/model-viewer）；自定义元素补 `data-visual-mask` 属性 |
| 5 | **Live reload / HMR** | diff 显示 "Hot Module Replacement" 浮层；或 screenshot 里出现 Vite HMR 错误框 | visual.spec 已过滤 `[HMR]`/`[vite]`/`source-map` console.error；确保 URL 用 `?test=true`（会禁用 dev 模式下的部分动画） |
| 6 | **自定义 cursor 或选区闪烁** | diff 是 1px×几像素的小方块（cursor caret 或选区 highlight） | Playwright viewport 设为 1920×1080 已减少 caret 出现概率；必要时加 CSS `caret-color: transparent !important` 在 FREEZE_CSS 里 |

### 修复命令（最常见 #3 的快速 workaround）
```diff
// 在 visual.spec.ts 的截图循环里，把：
await waitForAnimationsToSettle(page);
// 改成（对超慢动画更宽容）：
await waitForAnimationsToSettle(page, { samples: 50, intervalMs: 80, stableRounds: 5 });
```

### 避坑
- 动画一律用 framer-motion 的 `transition={{ type: 'tween' }}` 或者写精确 `duration: N`，避免无限 spring / inertia；
- 真正需要 live 的区域，**主动加 `data-visual-mask`**，而不是等 CI 抖动了才排查。
