# Component Libraries — Decision Tree + Imports

## Decision tree: which library for which job
| Your need | Pick | Avoid | Install |
|---|---|---|---|
| **Icons** (actions, status, UI chrome) | Phosphor Icons (React) | Font Awesome (CSS bloat), heroicons (small set) | `npm i @phosphor-icons/react` |
| **Charts** (bars, lines, pies, areas, radar) | Recharts (React wrapper on D3) | Chart.js (DOM-heavy, SSR fussy), pure D3 (too low-level) | `npm i recharts` |
| **Code blocks / syntax highlight** (inline source) | Shiki (VSCode grammars + themes, WASM) | Prism.js (unmaintained since 2022), highlight.js (no tree-sitter) | `npm i shiki` |
| **Diagrams** (flow, sequence, class, state, gantt) | Mermaid (text→SVG) | Excalidraw embedded (non-deterministic visual tests) | `npm i mermaid` |
| **Tables** (sortable, filterable, dense data) | TanStack Table (headless) + hand-rolled CSS | Material-UI Table (weight 300KB+) | `npm i @tanstack/react-table` |

## Two-line copy-paste per library

### Phosphor Icons
```tsx
import { Rocket, ArrowRight, CheckCircle, Warning } from '@phosphor-icons/react';
// Weight: thin, light, regular, bold, fill, duotone — match your theme
<Rocket size={28} weight="duotone" />
```

### Recharts (theme-aware)
```tsx
import { BarChart, Bar, XAxis, YAxis, ResponsiveContainer, Tooltip } from 'recharts';
// Stage is 1920×1080, so charts render at REAL size. Never use pixel widths — use percentage.
<ResponsiveContainer width="100%" height={380}>
  <BarChart data={myData}>
    <XAxis dataKey="name" stroke="var(--text-muted)" />
    <YAxis stroke="var(--text-muted)" />
    <Tooltip contentStyle={{background: 'var(--bg-card)', border: '1px solid var(--border)'}} />
    <Bar dataKey="value" fill="var(--accent-primary)" radius={[6,6,0,0]} />
  </BarChart>
</ResponsiveContainer>
```

### Shiki (code highlighting)
```tsx
import { codeToHtml } from 'shiki';
// Pre-render strings at build time. NEVER run shiki inside a React render — it's synchronous and slow.
const html = await codeToHtml(source, { lang: 'ts', theme: 'github-dark-dimmed' });
<div dangerouslySetInnerHTML={{ __html: html }} className="shiki-wrapper" />
```

### Mermaid (diagrams from text)
```tsx
import mermaid from 'mermaid';
// Initialize ONCE at module scope, NOT per render
mermaid.initialize({ startOnLoad: false, theme: 'neutral', securityLevel: 'strict' });
// In component: use useEffect to render into a ref (add [data-visual-mask] if Mermaid draws with randomized IDs)
const ref = useRef<HTMLDivElement>(null);
useEffect(() => { if (ref.current) mermaid.run({ nodes: [ref.current] }); }, [diagramSource]);
<div ref={ref} className="mermaid" data-visual-mask>{diagramSource}</div>
```

## Integration notes with the harness
- All libraries render to DOM → Auditor can verify that chart titles/axis labels exist
- Mermaid and Shiki emit SVG/HTML that may contain auto-generated IDs or timestamps → mark containers with `[data-visual-mask]` so visual tests mask them
- Recharts uses WAAPI animations → freeze.mjs handles WAAPI via `document.getAnimations()`. If you see motion blur, add `animationDuration={0}` to chart props explicitly.
- Phosphor icons use `currentColor` by default → automatically theme-aware
