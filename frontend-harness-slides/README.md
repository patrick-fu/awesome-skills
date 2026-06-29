# Frontend Harness Slides Starter

> Production-ready slide deck harness with Playwright audit, visual regression, and PDF export.

---

## ⏱ 5-minute quick start

```bash
# 1. Copy starter folder from the skill asset
cp -r ~/.agents/skills/frontend-harness-slides/assets/starter ./my-deck
cd ./my-deck

# 2. Install dependencies (includes Playwright)
npm install

# 3. Install Chromium for Playwright (first time)
npx playwright install chromium

# 4. Launch dev server (http://localhost:5173)
npm run dev

# 5. Build + verify — run before every commit
npm test
```

**That's it.** Edit `src/slides/AllScenes.tsx` (or `src/SlideRegistry.tsx` in older starters) to add your content.

---

## 🆚 Keynote / PPTX comparison

| Feature | Harness Slides | Keynote / PPTX |
|---|---|---|
| **Content as code** | ✅ Git-tracked TSX, diffable | ❌ Binary blobs, impossible to diff |
| **Interactive demos** | ✅ Full React app inside slides | ❌ Static screenshots + GIFs only |
| **Visual regression CI** | ✅ Pixel-perfect diff per slide | ❌ Manual review only |
| **Overflow / structure audit** | ✅ Automatic: finds off-canvas text, missing headings | ❌ Human review, misses edge cases |
| **Theming system** | ✅ CSS variables + typed ThemeConfig, swappable | ❌ Theme editor, limited tokens |
| **Custom components** | ✅ Any npm package (Recharts, Mermaid, Shiki, ...) | ❌ Limited built-in shapes |
| **URL deep links** | ✅ `?scene=id&beat=k` permanent | ❌ Slide numbers only, breaks on reorder |
| **Setup cost** | ~30 min (npm install, first snapshot) | 0 min |
| **One-shot <5 slides** | ❌ Overkill | ✅ Perfect fit |

---

## File tree

```
starter/
├── playwright.config.ts     # Playwright: viewport (1920×1080), DPR=1, snapshot path template
├── src/
│   ├── App.tsx              # Root: ThemeProvider + SlideDeck
│   ├── slides/
│   │   └── AllScenes.tsx    # 👉 YOUR CONTENT HERE. Builds registry[]
│   ├── components/
│   │   ├── SlideDeck.tsx    # Stage + nav + registry + URL state
│   │   ├── SlideStage.tsx   # Fixed 1920×1080 scaler
│   │   ├── SandboxIsolator.tsx  # Capture-phase event isolation
│   │   └── PresenterView.tsx    # F key → present mode
│   ├── theme/
│   │   ├── ThemeProvider.tsx    # CSS variable writer
│   │   └── themes.ts            # 👉 Your themes go here
│   └── assets/              # Per-scene images, SVGs, fonts
├── tests/
│   ├── auditor.spec.ts      # Health: text, overflow, structure, console errors
│   └── visual.spec.ts       # Snapshot comparison (per beat)
├── harness/
│   └── freeze.mjs           # Animation freeze + VISUAL_MASK_SELECTORS
├── scripts/
│   └── export-pdf.mjs       # CLI: per-beat PDF export
├── .github/workflows/
│   └── harness.yml          # CI: cache + build + test + artifacts
└── package.json             # Scripts (see below)
```

---

## Common commands

| Command | What it does | When to run |
|---|---|---|
| `npm run dev` | Vite dev server, hot reload at `:5173` | Authoring content |
| `npm run build` | Type-check + production bundle to `dist/` | Before commit, before deploy |
| `npm run preview` | Serve `dist/` locally at `:4173` | Verify production build |
| `npm run auditor` | Playwright → auditor.spec only | Fast structural check |
| `npm run visual` | Playwright → visual.spec only (screenshots vs baseline) | After theme/content changes |
| `npm run test` | auditor + visual — the full gate | **Before every commit** (CI runs this) |
| `npm run test:update` | Regenerate all visual baseline snapshots | Intentional visual change only |
| `npm run pdf` | `node scripts/export-pdf.mjs` → `deck.pdf` | Share deck with non-technical reviewers |
| `npm run deploy` | Upload `dist/` → Goofy preview (requires `bytedcli` + auth) | Share live link with stakeholders |

Starters may also include aliases: `test:audit`/`test:visual`/`export:pdf` are the long-form equivalents of `auditor`/`visual`/`pdf`.

---

## Keyboard shortcuts

| Key | Action | Context |
|---|---|---|
| `→` / `Space` / `PageDown` / `Enter` / `j` | Next beat | Everywhere |
| `←` / `PageUp` / `Backspace` / `k` | Previous beat | Everywhere |
| `Home` | Jump to first slide | Everywhere |
| `End` | Jump to last slide | Everywhere |
| `0-9` + `Enter` | Jump to Nth slide | Everywhere |
| `g` | Prompt for scene id to jump to | Everywhere |
| `F` / `Esc` / `F11` | Toggle presenter mode (next-scene preview + notes + timer) | Everywhere |
| `t` | Toggle theme (if multi-theme configured) | Everywhere |
| `r` | Reload current scene (hard URL reset) | Everywhere |
| `?` / `H` | Show this cheat sheet | Everywhere |

Navigation keys are **blocked inside INPUT/TEXTAREA/SELECT/[contenteditable]** and interactive elements (`button`, `a[href]`, role=button/link/tab) — embedded demos work without fighting presenter nav.

Browser **Back / Forward** buttons work — the deck URL state changes per beat via `replaceState`, and a `popstate` listener restores the correct scene/beat.

---

## FAQ

**Q: How do I add a new slide?**
A: Add a component in `src/slides/` → export it as a scene entry → push `{id, title, scene, beats?}` into the `registry` array in `AllScenes.tsx`.

**Q: Can I use vanilla HTML/CSS instead of React?**
A: For <10 slides and a one-shot output, yes! Switch to the `frontend-slides` skill. It outputs a single HTML file with no build step. For larger decks, decks with interactive demos, or decks that need CI regression — React componentization is what makes the harness (tests, theming, registry) work.

**Q: Where do speaker notes go?**
A: `registry[i].notes = "Markdown-ish text.\nSecond line."`. Show them with `F` (presenter mode). They also get exported alongside PDF pages if you pass `--with-notes` to export-pdf.mjs.

**Q: Can I have two decks in one repo?**
A: Each deck is its own starter copy with its own `package.json`. Keep them in separate folders (e.g., `decks/2026-Q1-eng-all-hands/`) — no cross-deck import sharing unless you explicitly build a shared components package.

**Q: Which npm packages are recommended for common slide needs?**
A: See [`references/component-libraries.md`](./references/component-libraries.md). Quick cheat: Icons → Phosphor, Charts → Recharts, Code → Shiki, Diagrams → Mermaid.

---

## Troubleshooting

See [`references/troubleshooting.md`](./references/troubleshooting.md) in the skill folder, or §VIII of the SKILL.md. 9 most common issues are documented step-by-step with exact commands.

### Top 3 quick fixes

1. **Visual snapshot failures on first run** → Run `npm run test:update` to generate baselines, then commit the `tests/snapshots/` folder.
2. **`Executable doesn't exist at .../chrome-*`** → Run `npx playwright install chromium` (npm installs the driver, not the browser).
3. **CJK text in PDF shows boxes (□□□)** → Install CJK fonts (`sudo apt install fonts-noto-cjk` on CI) or force Google Fonts via ThemeConfig so Chromium downloads webfonts.
