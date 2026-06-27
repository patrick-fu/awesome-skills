---
name: frontend-harness-slides
description: Create and manage high-quality, production-grade, and test-driven React + Vite + Framer Motion slide presentations. Use this skill when the user wants to build professional slide decks as positive-engineering frontend projects, when they mention Framer Motion animations, Playwright visual regression testing, or query-based Vercel deployments, or when they want to refactor an existing deck into a resilient, pixel-perfect, and highly-maintainable presentation.
---

# Frontend Harness Slides

Create high-end React-based slide presentations as professional software engineering projects, protected by comprehensive visual regression testing, absolute 16:9 stage layout preservation, and resilient state-management workflows.

---

## Core Principles

1. **Slides as Software Engineering** — Treat slides with the same rigor as production code: type safety (TypeScript), code quality (ESLint), automation (CI/CD), and regression protection.
2. **Resilience & Defensiveness** — Use robust architecture (SlideRegistry) to prevent maintenance headaches, and absolute layout scaling (SlideStage) to guarantee visual consistency on any screen size.
3. **Aesthetic Conviction (Anti-Slop)** — Reject flat, generic "AI slop" designs (no Inter font, no default purple-on-white gradients). Commit to bold, distinctive aesthetics tailored specifically to the presentation's narrative.
4. **Harness-Driven Loop** — Never trust visual design to verbal assertions. Use Playwright to automatically audit layouts, catch overlaps, verify minimum font thresholds, and compare pixel-level snapshots.

---

## I. Architectural Foundations

### 1. SlideRegistry & Centralized Deck Routing
To eliminate **"Re-indexing Hell"** (where inserting a slide forces renaming dozens of physical files, rewriting imports, and breaking visual snapshot Baselines), you MUST decouple slide order from filenames.

* **The Pattern**: Author slide components using semantic, descriptive names (`CoverSlide.tsx`, `HarnessConveyorSlide.tsx`).
* **The Registry**: Register and order slide components in a centralized `SlideRegistry.ts` array.
* **The Route**: Derive the active index and page numbering dynamically from the array position.

#### Implementation Contract (`SlideRegistry.ts`)
```typescript
import React from 'react';
import { CoverSlide } from '../scenes/CoverSlide';
import { HarnessConveyorSlide } from '../scenes/HarnessConveyorSlide';
import { CompactionVortexSlide } from '../scenes/CompactionVortexSlide';

export interface SlideEntry {
  id: string; // Persistent ID used for routing and snapshot filenames
  component: React.ComponentType<{ currentBeat: number }>;
  totalBeats: number;
}

export const SLIDE_REGISTRY: SlideEntry[] = [
  { id: 'cover', component: CoverSlide, totalBeats: 1 },
  { id: 'harness-conveyor', component: HarnessConveyorSlide, totalBeats: 3 },
  { id: 'compaction-vortex', component: CompactionVortexSlide, totalBeats: 4 },
];
```

In your main `SlideDeck.tsx` framework:
* Resolve navigation (prev/next) and route parameters (e.g., `?scene=harness-conveyor&beat=2`) based on the array `id` matching. This ensures inserting a new slide simply requires adding an entry to the registry array—zero file renaming, zero broken routing.

---

### 2. Absolute 16:9 Stage Scaling (No-Reflow)
To guarantee your slides look identical on ultra-wide monitors, projectors, and mobile split-screens, **NEVER** use standard responsive breakpoints to reflow text or rearrange grids. 
Lock the slide inside a virtual **1920×1080 canvas** and scale the entire stage uniformly to fit the viewport (Letterboxing/Pillarboxing).

#### The Stage Component (`SlideStage.tsx`)
```tsx
import React, { useState, useEffect, useRef } from 'react';

interface SlideStageProps {
  children: React.ReactNode;
  themeBg?: string; // Automatically matches slide backgrounds to avoid jarring borders
}

export const SlideStage: React.FC<SlideStageProps> = ({ children, themeBg = '#000000' }) => {
  const [scale, setScale] = useState(1);
  const containerRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const calculateScale = () => {
      if (!containerRef.current) return;
      
      const targetWidth = 1920;
      const targetHeight = 1080;
      const viewportWidth = window.innerWidth;
      const viewportHeight = window.innerHeight;

      // Fit-to-screen scale factor
      const scaleX = viewportWidth / targetWidth;
      const scaleY = viewportHeight / targetHeight;
      const newScale = Math.min(scaleX, scaleY);

      setScale(newScale);
    };

    const resizeObserver = new ResizeObserver(() => calculateScale());
    resizeObserver.observe(document.documentElement);
    calculateScale();

    return () => resizeObserver.disconnect();
  }, []);

  return (
    <div 
      className="w-screen h-screen overflow-hidden flex items-center justify-center select-none relative"
      style={{ backgroundColor: themeBg }}
    >
      <div
        ref={containerRef}
        style={{
          width: '1920px',
          height: '1080px',
          transform: `scale(${scale})`,
          transformOrigin: 'center center',
          flex: 'none', // Critical: prevent flex child self-collapse
        }}
        className="relative overflow-hidden shadow-2xl transition-transform duration-75 ease-out"
      >
        {children}
      </div>
    </div>
  );
};
```

---

### 3. Integrated Theme Context & Dual Preview Interaction
Rather than duplicating pages, declare style tokens in separate config files and inject them using a React Context. This enables both static and dynamic visual comparison.

#### Theme Interface (`ThemeConfig.ts`)
```typescript
export interface ThemeConfig {
  id: string;
  name: string;
  fonts: {
    display: string; // Header font (e.g., 'Cabinet Grotesk')
    body: string;    // Copy font (e.g., 'Plus Jakarta Sans')
  };
  colors: {
    background: string;
    text: string;
    primary: string;
    border: string;
  };
  effects: {
    borderRadius: string;
    borderWidth: string;
    shadow: string;
  };
}
```

#### Dual-Preview Selector Design
1. **Three-Pane Grid Preview**: Render a grid with three 16:9 scaled-down thumbnails of the Title Slide, each wrapped in a different `ThemeProvider`. This allows instant static side-by-side comparison of the design options.
2. **Single-Page Hot-Swap**: Once an option is chosen, expand to fullscreen. Keep a small, floating theme-selector overlay available in local development mode (`?dev=true`). Clicking styles dynamically updates the `ThemeContext` state, instantly hot-swapping CSS variables and WebFonts live in the browser.

---

### 4. Interactive Sandbox Isolator
When embedding interactive demos (such as text input fields, terminals, or clickable games) inside your 16:9 slides, stop events from bubbling up and causing accidental slide changes while the user interacts with the demo.

```tsx
export const SandboxIsolator: React.FC<{ children: React.ReactNode }> = ({ children }) => (
  <div 
    onKeyDown={(e) => e.stopPropagation()} // Stop space, arrows, enter from triggering slide transitions
    onWheel={(e) => e.stopPropagation()}   // Stop scroll from accidental navigation
    onClick={(e) => e.stopPropagation()}   // Prevent click-to-next triggers
    className="w-full h-full"
  >
    {children}
  </div>
);
```

---

## II. Harness & Quality Safeguards

To maintain 100% deterministic visual and structural quality, integrate a dual-mode test suite in Playwright.

### 1. The Global Beat Controller (Harness-Friendly Testing)
Instead of letting components run free-flowing animations, bind slide states directly to the route query parameters (`?scene=harness-conveyor&beat=2`).
* When Playwright runs tests with `?test=true`, the central router immediately locks the active scene and beat.
* Components render their final state for that beat without waiting for staggered delay timers, creating a 100% stable frame for screenshot comparison.

### 2. Eliminating Visual Flakiness (Continuous Motion Suspender)
Continuous fluid animations (like rotating background gears or pulsing gradients) will fail visual regression checks because their exact rendering position varies by milliseconds.
* **The Directive**: In test mode, freeze all infinite or continuous CSS / Framer Motion animations.
* **The Rule**: Inject a global stylesheet or append a `.test-mode` CSS class that forces standard animation play states to pause:
```css
.test-mode *, .test-mode *::before, .test-mode *::after {
  animation-play-state: paused !important;
  transition-duration: 0s !important;
}
```
* **Masking**: Use Playwright's `mask` property in your screenshots to blank out high-variance dynamic regions (like a live canvas or third-party web preview).

### 3. Layout and Typography Auditing
Run a physical DOM audit alongside visual checks:
* Verify that no element has zero height/width if it is visible.
* **Font-Size Floor**: Audit all visible text elements. Fail the build if any readable copy or annotations fall below **16px** (which is `text-sm` or `text-base` scaled, scaled proportional to the 1920×1080 design dimensions). Tiny fonts are an AI slop tell; keep design elements legible and punchy.
* **Overlap Check**: Check bounding client rects of adjacent components (such as Slide Title vs Card Headers) to programmatically ensure nothing collides.

---

## III. Writing Style & "说人话" Mode

When the user requests **"说人话" (Speak Like Human) Mode** (or `speak-like-human: true`), strictly filter out bloated corporate hype and mechanical AI symmetries. Replace them with specific, concrete, and conversational human verbs.

### 1. Contrastive Few-Shot Guidelines

| Scenario | ❌ AI-Slop/Corporate Slop Template | ✅ Speak-Like-Human (Alternative) |
| :--- | :--- | :--- |
| **Login Overhaul** | "通过重构鉴权管线，我们对底层会话生命周期提供了全链路的安全闭环保障，赋能高弹性的登录持久化体验。" | "登录态过期时，要先保住用户正在编辑的内容。别直接跳转踢人，保留现场，让用户刷新完还能回来继续写。" |
| **Harness Introduction** | "建设高密度的测试 Harness 承接底层执行质量，闭环收敛技术债务，从而最大化地释放开发提效产能。" | "没有测试的 Loop 只是自动试错。Harness 就像地基，地基稳了，改东西才不怕改坏别的，你才敢放手让 Agent 自己跑。" |
| **Context Overload** | "针对长程任务导致的会话高熵饱和及上下文拥堵痛点，我们设计了物理级别会话隔离的编排机制。" | "任务变长之后，上下文足迹会直接压垮智商。要解决这个拥堵，要么把任务拆出去走编排，要么在主线上把日志压缩熔炼。一个往外拆，一个往里压。" |

### 2. Formatting Rules
* **No Slogans on Screen**: Except for the Title and final conclusion slides, never output generic, high-sounding marketing slogans. Keep text on the slide limited to keywords, tags, physical metrics, or brief, direct takeaways.
* **First-Person Authenticity**: When providing speaker notes or explanations, speak from a first-person practitioner perspective: *"My experience shows that..."* or *"I tried this, and it didn't work because..."* instead of presenting assumptions as universal laws.

---

## IV. Font & Copyright Guidelines

To prevent licensing or copyright issues while retaining beautiful typography, **NEVER** hardcode or bundle commercial font files directly inside the skill package.

### 1. Font Recommendations & Off-the-shelf Links
When initiating a theme, recommend and link to established copyright-free and open-source font platforms:
*   **Sans-Serif / Display**:
    *   *Syne* (Bold, Brutalist) — [Google Fonts](https://fonts.google.com/specimen/Syne)
    *   *Cabinet Grotesk* (Sharp, Modern) — [Fontshare](https://www.fontshare.com/fonts/cabinet-grotesk)
    *   *Plus Jakarta Sans* (Clean, Professional) — [Google Fonts](https://fonts.google.com/specimen/Plus+Jakarta+Sans)
*   **Serif / Editorial**:
    *   *Cormorant Garamond* (High-contrast Serif) — [Google Fonts](https://fonts.google.com/specimen/Cormorant+Garamond)
    *   *Playfair Display* (Editorial Classic) — [Google Fonts](https://fonts.google.com/specimen/Playfair+Display)
*   **Chinese / Handdrawn**:
    *   *LXGW WenKai Lite* (霞鹜文楷 Lite - Clean Handdrawn/Sketch) — [GitHub Official Release](https://github.com/lxgw/LxgwWenKai-Lite)
    *   *Noto Serif SC* (思源宋体) — [Google Fonts](https://fonts.google.com/specimen/Noto+Serif+SC)

### 2. Setup Guidance
Instruct the developer/Agent to download the `.ttf` or `.woff2` files from these official sources, place them in the project's local directory (`public/fonts/`), and reference them locally in `index.css`. This ensures:
1. **Zero copyright liability** for the template creator.
2. **100% offline-safe presentation** (slides don't need active internet to fetch remote WebFonts).

---

## V. Deployment & Version Control

To prevent state drift in long-term multi-session collaboration, establish a rigorous version control and deployment workflow.

### 1. Out-of-band Context Maintenance
Keep a central tracking document (typically `CONTEXT.md` in the root folder) as the single source of truth for historical decisions, architectural choices, and the current iteration backlog.
*   **Dynamic Pruning (Garbage Collection)**: During major restructures (e.g. adding scenes or changing routes), the Agent MUST actively review the `CONTEXT.md` and prune away stale implementation history, obsolete drafts, and old debug notes. Keep the context file clean, compact, and high-density to avoid wasting prompt token budgets.

### 2. Vercel Deployment Instructions
Always recommend **Vercel** for hosting the slide presentation due to its generous free tier and superb SPA capabilities.
*   To enable seamless routing (`?scene=X&beat=Y`) on static hosting platforms, configure a custom `vercel.json` in the project root. This ensures that any deep links or manual browser refreshes gracefully fall back to `index.html` without throwing a 404 error:

```json
{
  "rewrites": [
    {
      "source": "/(.*)",
      "destination": "/index.html"
    }
  ]
}
```

---

## VI. Workflow: Bootstrap and Run

When starting a new slide project, always execute the following sequential phases:

### Phase 0: Environment & Version Control Setup
1. **Git Initialization**: Check if the current directory is a Git repository. If it's a blank directory, explain in plain words why local version control is crucial (safeguarding changes, allowing easy rollback of visual iterations) and initialize it: `git init`.
2. **Remote Disaster Recovery**: Inquire if they want to create a private remote GitHub repository. If they have `gh` (GitHub CLI) installed, help them configure a private repo in a semi-automatic way: `gh repo create --private`. If they are not comfortable with advanced remote setup, gracefully degrade and rely solely on local Git.
3. **Context Choice**: Ask if they have an existing context document to pass on historical decisions. If not, bootstrap a clean `CONTEXT.md` at the root.

### Phase 1: Structure and Theme Discovery
1. Ask purpose, audience, and density preferences (Speaker-led vs Reading-first).
2. Propose three custom Theme configs matching the tone. Enable the developers' theme-switcher overlay for side-by-side browser exploration.
3. Establish the `SlideRegistry.ts` array to map the initial outline scenes.

### Phase 2: Implementation and Refinement
1. Write TSX components inside `src/scenes/` aligned with the registry.
2. Bind internal states to query parameters for 100% repeatable beat positioning.
3. Wrap interactive zones with `<SandboxIsolator>` to protect transition triggers.

### Phase 3: Verification and Deployment
1. Write and run Playwright tests locally to confirm layout and visual safety.
2. Commit changes and push to trigger remote GitHub Actions CI checks (fully configured to compile LXGW WenKai fallback and ttf2woff2 on the fly).
3. Execute `npx vercel --prod` to deploy live. Provide the final production URL to the user.
