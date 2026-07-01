# Frontend Harness Slides

**[中文说明](README.zh-CN.md)**

Build HTML slides with a **rigorous frontend engineering mindset**. Treat your presentation as a high-standard, fully testable Web Application backed by a robust automated testing harness.

> 🖥️ **Live Interactive Demo**: Explore all 24 visual styles and density levels in our [Live Style Preview Workbench](https://harness-slides-24-styles.vercel.app/).

A single HTML file is fine for a quick draft. The nightmare begins during iteration: the user asks to rewrite a page, adjust an animation, update a chart, or restructure a layout. In a monolithic file, a small CSS or script change can accidentally break another slide, and the regression remains completely invisible until the live presentation.

`frontend-harness-slides` turns slide creation into a **checked, bulletproof workflow**. It provides a framework-neutral harness contract: stable frame addresses, a centralized registry, fixed stage geometry, deterministic frozen mode, and automated layout/interaction assertions.

---

## Key Engineering Pillars (Never Breaks)

*   **Harness-Backed Testing**: Built-in automated regression tests (e.g., Playwright/Vitest) run locally or in CI/CD to ensure **zero silent regressions** during edits.
*   **Stable Frame Addresses**: Every scene and beat is an addressable, isolated route. Modifying one slide has absolutely zero side-effects on others.
*   **Fixed Stage Geometry**: The entire slide deck renders inside a fixed-ratio stage (e.g., 16:9) that scales proportionally. This completely eliminates text overflows, overlapping elements, or layout reflow collapses across different screen sizes.
*   **Deterministic Frozen Mode**: A global flag that freezes all entrance/exit animations, CSS transitions, timers, and random values, enabling 100% stable visual regression testing (Snapshot Testing).
*   **Event-Isolated Interactivity**: Custom interactive components (like draggable knobs or text inputs) are strictly isolated. User inputs stop propagation and never leak to trigger accidental slide navigation.

---

## 🛡️ Harness & Testing Suite (Minimal Assertions)

Every deck built with this skill is a testable Web App. Below is a minimal, high-value Playwright assertion that automatically catches layout breaks, text overflows, and runtime exceptions across all slides:

```javascript
// test/slides.spec.ts
import { test, expect } from '@playwright/test';

test('verify all scenes render with zero overflows and console errors', async ({ page }) => {
  // 1. Fetch the centralized slide registry
  const scenes = await page.evaluate(() => window.SLIDE_REGISTRY);

  for (const scene of scenes) {
    // 2. Navigate to the isolated frame in deterministic frozen mode
    await page.goto(`/frame/${scene.id}?frozen=true`);

    // 3. Assert no unhandled console errors occurred
    expect(page.errors).toHaveLength(0);

    // 4. Assert no content overflowed the fixed 16:9 stage boundary
    const hasOverflow = await page.evaluate(() => {
      const stage = document.getElementById('stage');
      return stage.scrollHeight > stage.clientHeight || stage.scrollWidth > stage.clientWidth;
    });
    expect(hasOverflow).toBe(false);
  }
});
```

### Terminal Output
```text
$ npm run test:slides

  ✓ [Scene 01: Intro] Passed (No overflow, 0 console errors)
  ✓ [Scene 02: Architecture] Passed (No overflow, 0 console errors)
  ✓ [Scene 03: Performance Table] Passed (No overflow, 0 console errors)

  Test Suites: 1 passed, 1 total
  Tests:       24 passed, 24 total
  Snapshots:   24 matched, 24 total
  Time:        4.82 s
  Active filters: stage-boundary, event-isolation, frozen-determinism
```

---

## 📺 Visual Style Gallery

Instead of repeating a rigid template, this skill advocates **Single Style System, Multi-Layout Composition**. The layout is driven entirely by the semantic structure of your content, scaling fluidly across three density levels (Low, Medium, High).

Here are 6 curated representative styles from our catalog. Click any style to see its detailed design recipe, or explore the full catalog.

### 🟢 Minimal Keynote (Speaker-Led & Highly Expressive)

#### [Style 06: Blackboard Chalk Talk](references/style/minimal-keynote.md#style-06-blackboard-chalk-talk)
*Handmade, educational, and reasoning-first. Uses chalk-drawn lines and formulas on a deep green board.*
*   **Topic**: *The First Principles of Quantum Computing*
<p align="center">
  <img src="references/style/screenshots/style-06-low.webp" width="32%" alt="Low Density: Hero Formula" />
  <img src="references/style/screenshots/style-06-med.webp" width="32%" alt="Medium Density: Routed Proof" />
  <img src="references/style/screenshots/style-06-high.webp" width="32%" alt="High Density: Qubit Bento" />
</p>

#### [Style 02: Sketch Board Emoji](references/style/minimal-keynote.md#style-02-sketch-board-emoji)
*Warm, approachable, and human-in-the-loop. Emphasizes sticky notes, tape, and emoji actors.*
*   **Topic**: *Offline-First Sync Engine Design*
<p align="center">
  <img src="references/style/screenshots/style-02-low.webp" width="32%" alt="Low Density: Why Offline-First" />
  <img src="references/style/screenshots/style-02-med.webp" width="32%" alt="Medium Density: Sync Timeline" />
  <img src="references/style/screenshots/style-02-high.webp" width="32%" alt="High Density: Strategy Bento" />
</p>

---

### 🟡 Balanced Hybrid (Roadshows & Hybrid Reading)

#### [Style 13: Subway Map of Intent](references/style/balanced-hybrid.md#style-13-transit-flow-subway-map)
*Systematic, clean, and highly structured. Represents converging workflows as subway lines and transfer stations.*
*   **Topic**: *The Lifecycle of a Distributed Request*
<p align="center">
  <img src="references/style/screenshots/style-13-low.webp" width="32%" alt="Low Density: Packet Journey" />
  <img src="references/style/screenshots/style-13-med.webp" width="32%" alt="Medium Density: Transit Map" />
  <img src="references/style/screenshots/style-13-high.webp" width="32%" alt="High Density: Schedule Bento" />
</p>

#### [Style 16: Debug Reaction Board](references/style/balanced-hybrid.md#style-16-diagnostic-kanban-board)
*Developer-native, diagnostic, and actionable. Uses glowing neon badges and monospace terminal layouts.*
*   **Topic**: *Microservices Health Self-Check*
<p align="center">
  <img src="references/style/screenshots/style-16-low.webp" width="32%" alt="Low Density: System Ready" />
  <img src="references/style/screenshots/style-16-med.webp" width="32%" alt="Medium Density: Self-Check Flow" />
  <img src="references/style/screenshots/style-16-high.webp" width="32%" alt="High Density: Risk Kanban" />
</p>

---

### 🔵 Text Report (Asynchronous Reading & High Density)

#### [Style 18: Maintainer Issue Brief](references/style/text-report.md#style-18-developer-ticket-brief)
*Clean, structured, and action-oriented. Inspired by modern open-source issue trackers and code review tools.*
*   **Topic**: *Post-Mortem: Connection Pool Exhaustion*
<p align="center">
  <img src="references/style/screenshots/style-18-low.webp" width="32%" alt="Low Density: Issue Header" />
  <img src="references/style/screenshots/style-18-med.webp" width="32%" alt="Medium Density: Incident Timeline" />
  <img src="references/style/screenshots/style-18-high.webp" width="32%" alt="High Density: Code Review Diff" />
</p>

#### [Style 21: Field Notes Report](references/style/text-report.md#style-21-field-notes-report)
*Tactile, observational, and literary. Uses warm ledger paper, charcoal ink, and polaroid-like card grids.*
*   **Topic**: *Smart Home UX Field Research*
<p align="center">
  <img src="references/style/screenshots/style-21-low.webp" width="32%" alt="Low Density: Research Cover" />
  <img src="references/style/screenshots/style-21-med.webp" width="32%" alt="Medium Density: User Journey Map" />
  <img src="references/style/screenshots/style-21-high.webp" width="32%" alt="High Density: Observation Grid" />
</p>

<p align="center">
  <a href="references/style/preview.md"><b>👉 Explore All 24 Styles in the Full Style Preview Guide →</b></a>
  <br />
  <a href="https://harness-slides-24-styles.vercel.app/"><b>🖥️ Try the Live Style Preview Workbench →</b></a>
</p>

---

## Install

```bash
npx skills add patrick-fu/frontend-harness-slides
```

Update later:

```bash
npx skills update
```

---

## How An Agent Uses It

1.  **Plan**: Align with the user on content, presentation format, technology stack, and delivery. Establish the Pre-Build Alignment Gate and record decisions in a context document.
2.  **Design**: Propose 2-3 contrasting styles from our 24-style catalog. Build interactive previews, capture screenshots, and record the selected theme notes.
3.  **Build**: Implement stable scenes, registry, fixed stage scaling, frozen mode, and event-isolated interactive components.
4.  **Verify and Ship**: Run automated layout/interaction tests, perform visual smoke checks, and deploy to a live URL or export to PDF.

---

## Stage References

For non-trivial deck work, agents must read these references in order:

| File | Purpose |
|---|---|
| `references/01-plan.md` | Intake gate, technology choice, context tracking, and content registry. |
| `references/style/index.md` | Style Index, 24 style directions, and semantic-to-visual mapping. |
| `references/style/preview.md` | **Full Style Preview Guide** (All 24 styles with 3-image progressions). |
| `references/02-design.md` | Style previews, layout variations, navigation design, fonts/CJK, and assets. |
| `references/03-build.md` | Stable frames, registry, fixed stage, frozen mode, and event isolation. |
| `references/04-verify-and-ship.md` | Audit profiles, visual smoke, viewport stress checks, and PDF/static handoff. |

---

## When It Fits

Use this skill when the deck is non-trivial, expected to receive feedback, has animation or state, uses screenshots/charts, or needs checked frames before handoff.

Skip it when you only need a tiny static one-off where a single HTML file is enough and no regression harness is useful.

---

## More Skills

For more reusable agent skills, see [Awesome Skills](https://github.com/patrick-fu/awesome-skills).
