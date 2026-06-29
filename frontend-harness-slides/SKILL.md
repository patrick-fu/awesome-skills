---
name: frontend-harness-slides
description: >-
  Build an HTML slide deck as a real engineering project — a complete,
  maintainable presentation that stays visually consistent and won't silently
  break as it grows or gets edited, a sturdier step up from single-file HTML
  slides. Use when the user wants to create, extend, refactor, or harden HTML
  slides (a talk or pitch deck) into something built to last, or wants slide
  work with automated visual checks and PDF export — not a quick one-off.
  适用于 ≥15 页、需要多轮迭代、CI 视觉回归测试或团队协作 review 的幻灯片项目；<10 页一次性交付请用 frontend-slides，需要飞书原生编辑/分享请用 lark-slides。
version: 1.0.0
updated: 2026-06-29
# publish_targets: ["awesome-skills"]  # 如需对外发布取消注释
---

# Frontend Harness Slides

Build slide decks like production software: a Playwright **harness** guards every frame, a **registry** decouples order from filenames, and an absolute 16:9 **stage** keeps layout identical on any screen. The bundled `assets/starter/` is a runnable project that already wires all of this together — copy it first, then make it yours.

Each section below is a rule plus a pointer to the file that implements it. Read the pointed file when you reach that piece — keep this file lean.

## Core Principles

1. **Harness over eyeballing** — Never trust "looks fine" by eye. The Playwright harness audits structure and compares pixels every run; a change is done only when the harness is green (§II).
2. **Resilience by architecture** — A central **registry** kills re-indexing hell; the **stage** locks a 1920×1080 canvas and scales as a whole, so you never reflow per device.
3. **Anti-slop aesthetics** — Reject generic AI-slop (no Inter, no default purple-on-white gradient). Commit to one bold, narrative-specific look (§III).

## Trigger Boundaries — 三 Skill 触发边界表

选择技能前对照下表，边界不清时向用户提问确认。**选错 Skill 的代价比选错模板大得多。**

| 维度 | frontend-slides | frontend-harness-slides | lark-slides |
| :--- | :--- | :--- | :--- |
| **页数触发** | < 10 页，一次性 | ≥ 15 页，或 <15 但长期维护 | 任意页数，要求飞书原生 |
| **生命周期** | 一次性交付、修改极少 | 多轮迭代、版本化、多人协作 | 持续编辑、多人评论、权限控制 |
| **交付形态** | 单 HTML 文件 → 链接 / PDF | Vite+React 仓库 + CI 截图基线 + PDF 导出 | 飞书文档 / 飞书演示稿 |
| **测试 & 回归** | 无，手工目视 | Playwright auditor + visual baseline，**每次提交跑** | 飞书版本历史 + 评论 |
| **动画保真** | CSS transition / WAAPI，目视检查 | 每个 beat 冻结截图 + 3 轮稳定采样，像素级一致 | 飞书原生动画，有限可控 |
| **典型用户故事** | 小项目分享、面试 8 页自我介绍、周会一次性展示 | 产品季度 pitch、开源 conference talk、需要 PR review 的团队 deck、设计规范展示 | 公司内部方案评审、跨部门同步、需要 @人 评论、权限分级的分享 |

> **灰色地带 10–14 页**：如果 ≥2 个「是」（有 git、有 CI、要 PR review、未来会改 ≥3 次）→ 用 harness-slides；否则 → frontend-slides。

## 0. Start from the starter

Don't hand-assemble the project. The repeated engineering — Vite + React + Tailwind, the router/beat-controller, the theme provider, `playwright.config`, the two specs, the PDF exporter, an optional CI — is bundled in `assets/starter/` and already green:

1. Copy `assets/starter/` to the project root.
2. `npm install`, then `npx playwright install chromium` (the package ships
   without a browser binary — required for tests and PDF export). After that,
   `npm run dev` to author and `npm test` to run the harness.
3. Replace the two demo scenes in `src/scenes/` with real content, registered through the array (§I.1).

Everything below explains the pieces you'll touch inside that starter.

## I. Architecture

### 1. Registry — one array owns order
Inserting a slide must not rename files or break snapshots ("re-indexing hell"). Decouple order from filenames:
- Name components semantically (`CoverScene.tsx`, not `Scene7.tsx`).
- One central array (`src/SlideRegistry.tsx`) owns order; routing, page numbers, and tests all derive from array position plus each entry's stable `id` (which also names snapshots). Keep `id`s stable once set.
- → `assets/starter/src/SlideRegistry.tsx` — the registry shape, `getSlideNavigation`, and `exposeRegistryForTooling` (publishes a slim list to `window.__SLIDE_REGISTRY__` for the harness and PDF export).

### 2. Stage — absolute 16:9, no reflow
To look identical on ultra-wide, projector, and phone, never use responsive breakpoints to rearrange slide content. Lock content in a virtual 1920×1080 canvas and scale the whole stage to fit (letterbox/pillarbox).
- Contract: the stage frame carries `data-slide-stage` (bounds anchor) plus `data-slide-id` / `data-beat` (so a test can assert the app landed on the right frame). The harness keys on these attributes, never on class chains — they drift.
- → `assets/starter/src/components/SlideStage.tsx`.

### 3. Theming — config + context, picked by eye
Declare each theme as a config and inject it via React Context (slides read tokens, never hardcode color/font). Discover themes visually, not verbally.
- → `references/theming.md` — the `ThemeConfig` shape, the dual-preview (three-pane + live hot-swap), and the preview-authenticity rules. Read it during theme discovery. The provider itself lives in `assets/starter/src/theme/`.
- Fonts → `references/fonts.md` (open-source only, downloaded into `public/fonts/`).

### 4. Sandbox — 双层键盘/滚动/点击隔离

在幻灯片里嵌入 `<input>`、终端、可交互 Demo、嵌入式编辑器时，**绝对不能让它的事件冒泡到 SlideDeck 的键盘导航**，否则打一个空格就翻页、方向键就跳 beat。

这里是**双层隔离模型**，两层同时生效——任何一层漏掉，另一层兜底：

- **Layer 1（SlideDeck 层 —— 被动白名单）**：`SlideDeck.tsx` 在处理 `keydown` 时先调 `isEditableEventTarget(e.target)`。如果目标是 `<input>` / `<textarea>` / `contenteditable` / `role="textbox"` / `<select>`，**直接返回不拦截**。这保证了「没有被 SandboxIsolator 包裹的可编辑元素」也不会被翻页键盘吃掉文字输入。
- **Layer 2（SandboxIsolator 组件 —— 主动拦截）**：`SandboxIsolator.tsx` 是一个 wrapper，在**原生 capture 阶段**用 `addEventListener(..., { capture: true })` + `stopImmediatePropagation()` 吞掉：Space、方向键、PageUp/PageDown、Home/End、`F`/`Esc`/`?` 等 slide 快捷键，以及 wheel（内部滚动不导致整页滑动）、contextmenu（防止与自定义右键菜单冲突）。它**不吞**普通字母/数字输入，且 `isEditable=true` / `isInteractive=true` 的子元素会跳过拦截。两层同时通过时，输入区与导航区完全解耦。

典型用法：把一个代码编辑器、交互式 playground、嵌入式原型 Demo 包进 `<SandboxIsolator>`，就可以专注演示而不用担心意外翻页。

- → `assets/starter/src/components/SandboxIsolator.tsx`（Layer 2，主动拦截，原生 capture 阶段）。
- → `assets/starter/src/SlideDeck.tsx` 中的 `isEditableEventTarget()`（Layer 1，被动白名单）。

> **注意**：v1.0.0 起 SandboxIsolator **仍然作为组件存在**（已重写为原生 capture 阶段 + `stopImmediatePropagation`，共 146 行）。老文档里说「已删除」是错误描述——见 §VIII Q3。

## II. The Harness

The harness exists to make every screenshot a **frozen frame**: the same render every run, so a pixel diff means a real regression, not animation jitter.

### §II.1 Keyboard Shortcuts

在幻灯片舞台（未聚焦任何 input 时）以下快捷键生效：

| Key | Action |
|-----|--------|
| `→` / `Space` / `PageDown` / `N` | 下一页 |
| `←` / `PageUp` / `P` | 上一页 |
| `Home` | 第 1 页 |
| `End` | 最后 1 页 |
| `0-9` + `Enter` | 跳转到第 N 页 |
| `F` / `F11` | 全屏 |
| `Esc` | 退出全屏 / 关闭 present 模式 |
| `?` / `H` | 显示快捷键帮助 |

> 注：聚焦在 `<input>`/`<textarea>`/可编辑区域内，以上快捷键**不拦截**（见「键盘事件模型」）。

### 1. Beat controller — state lives in the URL
Bind slide state to query params (`?scene=<id>&beat=<n>`). With `?test=true` the deck locks scene+beat and components jump straight to that beat's final state (no stagger timers, no live keyboard nav). That determinism is what makes a frame freezable, and it makes every frame a shareable deep link.
- → `assets/starter/src/SlideDeck.tsx` parses the query, clamps the beat, syncs the URL on navigation, and emits `data-slide-id` / `data-beat` so the specs can assert the frame actually rendered.

### 2. Freeze — kill continuous motion in test mode
Infinite/looping animations (spinning gears, pulsing gradients) shift by milliseconds and break visual diffs. In test mode, **freeze** them: pause animation play-states, zero transition durations, then wait for the DOM to settle before the shot. Mask truly live regions (canvas, third-party iframes).
- → `assets/starter/harness/freeze.mjs` is the single source of the freeze (the CSS + `waitForAnimationsToSettle`). Both `tests/visual.spec.ts` and `scripts/export-pdf.mjs` import it — change freeze once, here.

### 3. Audit — structure, not just pixels
Alongside snapshots, `assets/starter/tests/auditor.spec.ts` walks every scene/beat and checks, with near-zero false positives:
- **Beat honored** — the rendered `data-slide-id` / `data-beat` match the requested URL, so a snapshot can't silently pass on the wrong frame.
- **No collapse** — an element that should be visible (its own text, or media with a `src`) must not render 0×0. Opt a known-empty node out with `data-allow-empty`.
- **No overflow** — nothing escapes `data-slide-stage`; opt a deliberate bleed out with `data-allow-overflow`.

Element-vs-element collision is deliberately *not* a DOM assertion — real decks layer on purpose, so a generic check only cries wolf. Whether things *look* wrong is owned by the visual baseline (§II.2), not the auditor.

## III. Aesthetics & humanizer

- **Anti-slop** — one committed palette, distinctive type, one strong atmospheric device. No generic dashboard-card look, no Inter, no default purple gradient.
- **Legible type** — prefer large, confident type; tiny text reads as slop and is unreadable on a projector. This is guidance, not a gate — if the user wants small type for a dense handout, honor it.
- **humanizer mode** — when the user asks for humanizer (`speak-like-human: true`), strip corporate hype and AI symmetry; keep on-slide text to keywords/metrics/one direct takeaway, and speaker notes in first-person practitioner voice. → Contrastive examples and rules in `references/humanizer-slides.md`.

## IV. Content Density

Ask once whether the deck is speaker-led or reading-first, then let the answer drive the design:

| Mode | Best for | Behavior |
| :--- | :--- | :--- |
| **Low / speaker-led** | live talks, keynotes | one idea per slide, big type, 1–3 lines, more slides |
| **High / reading-first** | handouts, async review | self-contained slides, grids/tables/annotations, 4–8 points |

When a dense slide would force hard-to-read type or push content past `data-slide-stage`, split it into more slides rather than shrink past legibility — overflow is a hard fail (§II.3), and cramped type undercuts the deck.

## V. Workflow

### Phase 0 — Detect mode (first)
- **New deck** → scaffold from the starter (§0), then Phase 1.
- **Convert** (user has a PPT / markdown / outline) → extract content, confirm the outline, scaffold, then Phase 1.
- **Enhance an existing deck** → the high-frequency case for a multi-session deck. Before editing:
  1. Run the existing harness once to capture a green baseline (`npx playwright test`).
  2. Insert/edit slides through the **registry** (append or reorder the array; never rename files).
  3. Before adding content to a slide, check it against the density guidance (§IV); if it would overflow, split instead.
  4. Re-run the harness. Done only per the Phase 3 criterion, with every snapshot diff intended and re-baselined (`--update-snapshots`).

For any deck under git, keep a root `CONTEXT.md` as the single source of decisions/backlog, and prune it during big restructures so it stays high-density.

### §V.0 Import: Convert PPTX / Markdown / Keynote → Slides Project

**PPTX 导入（最常见）**：
```bash
# 1) Keynote / WPS 先导出为 PPTX
# 2) 用 frontend-slides 的 extract-pptx.py 抽取文本和图片
python ~/.agents/skills/frontend-slides/scripts/extract-pptx.py \
  --input ./source.pptx --output ./tmp-extracted \
  --images ./assets/images/
# 3) 生成的每一页文本对应到 SlideEntry.registry 的 content 字段
```

**Markdown 导入**：
```
每一级 `#` 代表一张新的 slide，`---` 分隔页。
抽取每个页面后：
  1) 生成 SlideEntry.id（slug 化 title）
  2) 放入 registry 数组
  3) 图片从 `![alt](path)` 拷贝到 assets/images/ 并改相对路径
```

**规则**：
- 导入后**必须**按 §Phase II 重做布局（纯文本位置不做保留）
- 字体方案、主题色按 §Theme 重新配置
- 图片需走 §Phase I Asset Prep（裁切、去底、WebP 压缩）

### Phase 1 — Discover (ask together)
Ask in one batch: **purpose · audience · length · density** (speaker-led vs reading-first). Then:
- Propose three themes via the dual-preview (`references/theming.md`); let the user pick by eye.
- If the user supplied images/logo/screenshots: judge each (usable? what it shows) and design the outline *around* them (3 screenshots → 3 feature slides, logo → cover/closing). Put assets in `public/`.
- Seed the `SLIDE_REGISTRY` array from the agreed outline.

### §Phase I.1 Asset Prep: Standard Operating Procedure

**Logo 处理**：
```bash
# 去白底 → PNG transparent
python -c "from PIL import Image; ..."
# 或用 vector magic / super vectorizer 转 SVG
# 最终要求：SVG 优先，200×200 px 边界，居中
```

**截图裁切 16:9 背景图**：
```bash
# 固定 1920×1080，WebP 质量 82，1200px 最大维度
convert input.jpg -resize 1920x1080^ -gravity center -extent 1920x1080 \
  -quality 82 output.webp
```

**SVG 优化**：
```bash
npx svgo input.svg --enable=removeUselessStrokeAndFill,prefixIds -o output.svg
```

**规范**：所有 assets 文件命名 `{slug}-{desc}-{dim}.{ext}`，如 `hero-app-mockup-1242x2688.webp`。

### Phase 2 — Build
- Author each registry component in `src/scenes/`. Done when every registry entry resolves to a real component (no placeholders).
- Bind each internal state to a `beat`, reachable via `?scene=&beat=` and identical on reload.
- Wrap every interactive widget in `<SandboxIsolator>`; verify key/scroll/click don't leak into navigation.
- Honor `prefers-reduced-motion` for real viewers — gate decorative/continuous motion behind it. (Distinct from test-mode **freeze**, which only stabilizes snapshots.)
- The starter already calls `exposeRegistryForTooling()` in `main.tsx`; keep it so the harness and PDF export can read the deck.

### Phase 3 — Verify & ship
Done only when **all** of these hold:
1. `npm run build` passes (types + production build).
2. `npx playwright test` exits clean.
3. The auditor spec is green — every frame honors its URL, nothing collapses to 0×0, nothing escapes `data-slide-stage`.
4. The visual spec is green for every registry scene at every beat, with any diff intended and re-baselined (`--update-snapshots`).
5. The visual run is not silently skipped — the registry is non-empty (the specs assert this).

Then ship → `references/deploy.md`: Vercel `vercel.json` rewrite for `?scene=&beat=` deep links, plus PDF export via `assets/starter/scripts/export-pdf.mjs`.

### §Phase III.1 Humanizer & Stop-Slop Gate

完成所有页面后，**必须**跑两轮质量 Gate：

1. **调用 `humanizer` skill**（或 `humanizer-zh` 中文版本），输入：
   ```
   请把以下幻灯片文案进行 humanize：（粘贴所有 SlideEntry 文本内容）
   要求：保留专业度、去除 AI 味、统一语调、减少重复词、保留所有数据事实。
   ```

2. **调用 `stop-slop` skill**，跑「Slop check on slide deck」模式，检查：
   - 空泛形容词（"seamless"、"robust"、"state-of-the-art"）
   - 动词堆叠（"enable and empower"）
   - 缺乏具体数字的 claims
   - 每条 slide 的标题是否能单独表意（3 秒测试）

Gate 不通过**不能发布**。

## VI. Supporting Files

| File | Read / use when |
| :--- | :--- |
| `assets/starter/` | **start here** — copy this runnable project; it wires registry, stage, beat controller, theme, sandbox, harness, specs, PDF export, and optional CI |
| `assets/starter/src/SlideRegistry.tsx` | wiring the registry / routing |
| `assets/starter/src/SlideDeck.tsx` | the beat controller (URL → frame, test-mode lock) |
| `assets/starter/src/components/SlideStage.tsx` | building the 16:9 stage |
| `assets/starter/harness/freeze.mjs` | the single freeze mechanism |
| `assets/starter/tests/` | the auditor + visual specs |
| `references/theming.md` | theme discovery, dual-preview, preview rules |
| `references/fonts.md` | choosing / installing fonts |
| `references/humanizer-slides.md` | the user asks for humanizer copy |
| `references/deploy.md` | deploying to Vercel or exporting PDF |
| `references/anti-patterns.md` | full 10-entry anti-pattern catalog (§VII expansion, 含每条触发场景 & 反例) |
| `references/troubleshooting.md` | full 9-entry troubleshooting catalog (§VIII expansion, 含根因 + 精确修复命令) |

## §VII Anti-patterns — 绝对不要做的事

> 完整扩展版（10 条，含每条触发场景 & 反例）见 [`references/anti-patterns.md`](./references/anti-patterns.md)。以下是**必须记住的快速清单**，生成或审查幻灯片时逐项对照。

1. **不要用 canvas 渲染整页静态内容**。Canvas 文字不可选中、不可拷贝、破坏无障碍、导出 PDF 是位图。只在图表/动画帧时用。
2. **< 10 页、一次性交付的幻灯片，不要使用本 skill**。用 frontend-slides（单文件 HTML），工程化 setup 成本不值得。
3. **不要把 beat 仅用于做动画/视觉效果**。每个 beat 对应一个「故事单元」，如果只是淡入淡出文字，合并为一个 beat。
4. **不要在 [data-slide-stage] 内使用 responsive breakpoints (md:/lg:)**。舞台永远是 1920×1080 像素坐标，Tailwind 的屏幕断点基于 viewport，不适用。
5. **不要在 Stage 内放 <iframe> 做可交互 Demo**。iOS Safari 缩放 iframe 会改变内部 layout；导出 PDF/截图 iframe 内容丢失。将交互 Demo 作为链接外链。
6. **不要用 CSS `zoom:` 属性做舞台缩放**。它是非标准的，`transform: scale()` + `transform-origin: top left` 更可靠且可预测。
7. **不要在 registry 中引用同一张图超过 3 次**。先考虑做成 shared component（如通用 App Mockup 组件），减少重复维护。
8. **不要默认引入完整 CJK 字体 (20MB+)**。必须走 glyphhanger/pyftsubset 子集化到 < 1MB。
9. **不要把测试断言全部写成 expect.soft 后忘记兜底 hard**。soft 本身不会让测试变红——**必须在每段后加 `expect(test.info().errors).toHaveLength(0)`**。
10. **不要在 `npm run build` 成功的基础上跳过 harness**。类型通过≠渲染正确；一个 CSS 拼写错误只影响视觉。

## §VIII Troubleshooting — 高频问题速查

> 完整扩展版（9 条，含每条根因分析 + 精确修复命令）见 [`references/troubleshooting.md`](./references/troubleshooting.md)。

**Q1: Playwright visual 快照第一次全红？**
> 正常。先跑 `npx playwright test visual.spec --update-snapshots` 生成基线，再提交。后续 CI 会对比。

**Q2: 导出 PDF 文字错位？**
> 99% 是本地字体与 CI 字体不匹配。确保：1) fonts 用子集化 WOFF2 上传到 assets/fonts；2) auditor.spec 里有 @font-face loaded 检查；3) 加 `--font-render-hinting=none` 启动参数。

**Q3: SandboxIsolator 和 SlideDeck 的键盘隔离是怎么配合的？**
> 见「§I.4 Sandbox」下的**双层隔离模型**。Layer 1（SlideDeck 层白名单 `isEditableEventTarget()`）+ Layer 2（`SandboxIsolator` 原生 capture 阶段 `stopImmediatePropagation`）双层同时工作。**注意：v1.0.0 起 SandboxIsolator 仍然作为组件存在**（已重写为原生 capture + stopImmediatePropagation，含 editable / interactive 判断）。老文档里说「已删除」是错误——如果你在老项目中看到了这个说法，请升级 starter 后重新阅读 §I.4。

**Q4: 图片在 Safari 里被自动放大？**
> `<ImageSlot>` 默认 fit=cover 会裁切。设 `fit="contain"` 或加 `--image-slot-position`。双击图片进入 reframe 模式手动裁切。

**Q5: npm run test 卡在 chromium 下载？**
> `@playwright/test` 是 driver + 浏览器分离架构，Chromium binary 默认在 `~/.cache/ms-playwright/`，**首次需要单独下载**。§0 已显式提醒：`npx playwright install chromium`。离线环境下，在另一台能上网的机器打包 `~/.cache/ms-playwright/` 后复制过去，然后 `export PLAYWRIGHT_SKIP_BROWSER_DOWNLOAD=1`。CI 环境：starter 的 `.github/workflows/harness.yml.example` 已内置 Playwright browser cache（key 基于 lockfile hash），首次下载后命中缓存。

**Q6: 幻灯片舞台缩放时，fixed 定位元素位置错？**
> `position: fixed` 基于 viewport，缩放后会漂移。全部改为 `position: absolute`，父容器用 `position: relative`。

**Q7: presenter 模式下按 space 无法翻页？**
> 确认没有任何 textarea/input 聚焦。如果 TweaksPanel 打开着，其内部 TweakNumber 横向 scrub 会吃掉 space（这是预期行为）。先点击舞台空白处失焦。

**Q8: auditor「0×0 折叠检查」在 CJK 单字/双字标题上漏检？**
> 旧版 `hasOwnText` 使用 `.trim().length > 2`，CJK 单字（「一」length=1）、双字（「你好」length=2）全部误判为空节点，跳过 0×0 检查。**P0 修复后改用 Unicode code-point 计数 `[...raw].length > 0` + 过滤纯标点/空白正则**。如仍出现漏检，检查节点是否只含纯标点（如只有「。」）——可在父容器上补 `data-allow-empty=false`（强制检查）或拆分文本节点。

**Q9: 视觉快照抖动（同代码两次跑 maxDiffPixels > 100 仍红）？**
> 常见根因按概率：① **字体加载不稳定**——未在 `document.fonts.ready` 后截图（修复：visual.spec.ts 已内置 `await page.evaluate(() => document.fonts.ready)`，请确认你的 fork 未删除）；② **sub-pixel 抗锯齿抖动**——CI 没设 `--font-render-hinting=none` + DPR=1（修复：playwright.config 已内置）；③ **framer-motion 弹簧未衰减**——`waitForAnimationsToSettle` 默认 3 轮×50ms 采样，超慢动画需手动加 `stableRounds: 5` 或 `intervalMs: 80`；④ **canvas / video / lottie-player 内容不冻结**——已在 `VISUAL_MASK_SELECTORS` 里统一遮罩，如缺失请在元素上补 `data-visual-mask` 属性；⑤ **Live Reload 资源未完成**——截图前必须 `waitUntil: 'networkidle'`（已内置）。
