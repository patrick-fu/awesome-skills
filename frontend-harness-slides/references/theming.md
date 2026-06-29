# Theming — config, context, dual-preview

How to declare themes, inject them, and let the user pick one **by eye** (not by verbal description). Read this during theme discovery (Phase 1).

## 1. ThemeConfig shape

Declare every theme as a plain config object; never hardcode color/font inside a slide — slides read tokens from context.

```typescript
export interface ThemeConfig {
  id: string;
  name: string;
  fonts: {
    display: string; // headline font, e.g. 'Cabinet Grotesk'
    body: string;    // copy font, e.g. 'Plus Jakarta Sans'
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

Inject via a React Context (`ThemeProvider` + `useTheme`, implemented in the starter's `src/theme/`). Map each token to a CSS variable so slides use clean classes (`bg-background`, `text-primary`) instead of inline hex, while keeping IDE autocomplete. Avoid Tailwind's `/<alpha>` opacity modifier on these var-backed colors — it produces invalid CSS.

## 2. Dual-preview — discover themes visually

Most people can't name what they want; they recognize it on sight. Offer two complementary preview modes:

1. **Three-pane grid** — render the *same* title slide three times, each wrapped in a different `ThemeProvider`, scaled down to 16:9 thumbnails side by side. Instant static comparison.
2. **Single-page hot-swap** — once a direction is chosen, go fullscreen and keep a small floating theme switcher (dev only, gate behind `?dev=true`). Clicking a theme swaps the context live — CSS variables and web fonts update in place, no reload. Lets the user feel the type and color in motion before committing.

## 3. Which three to show (the mix)

Show three genuinely different options so the user reacts to contrast, not nuance:

- **1 safe** — restrained, high-legibility, hard to dislike.
- **1 bold** — a committed, narrative-specific look with one strong atmospheric or graphic device.
- **1 wildcard** — adventurous and context-specific; clearly different from the other two.

Map the occasion's mood to candidates:

| Mood | Lean toward |
| :--- | :--- |
| confident / authoritative | sharp grotesk, dark canvas, one accent color |
| energetic / playful | high-contrast color, expressive display type |
| calm / editorial | serif, generous whitespace, paper tones |

## 4. Preview authenticity (non-negotiable)

A preview must look like a **real first slide of this deck**, never a diagnostic card. On the preview slide itself, never render:

- option labels — "Option A", "Safe", "Bold", "Wildcard"
- workflow / meta text — "preview", "generated", file names, paths, theme slugs
- the user's requirement notes — "for internal sharing", "audience: execs", "sharp and provocative"

Theme names and the safe/bold/wildcard framing belong only in your message to the user, not on the slide. If the slide needs chrome, use real deck chrome: deck title, section, date, author, page number, or a genuine line from the user's content. Before showing previews, scan the visible text and strip anything internal.

---

## 5. 🚧 Planned features (NOT YET IMPLEMENTED)

> ⚠️ **The following are planned features, not current behavior.** Do not instruct users to rely on them yet. They are documented here to show the roadmap and prevent wasted PR effort on already-scheduled work.

- **Floating theme switcher (in-progress, target Q3 2026).** A small floating component (bottom-left corner, opacity 80%) with 3 preset theme buttons that calls `setTheme()` live. Currently requires manual code in `App.tsx`; official component ships when token API v2 stabilizes.
- **Live hot-swap with Tweaks protocol (planned, Q4 2026).** Integration with baoyu-design's Tweaks Host Protocol: `postMessage({type: '__edit_mode_set_keys', keys: {...}})` → ThemeProvider applies delta tokens in real time without reload. Currently you need to edit `theme.ts` and recompile.

## 6. Dual-preview skeleton (implementable today)

While the official switcher is in progress, use this pattern to build a 2-column comparison page in your OWN deck. It uses two `ThemeProvider` instances with `targetRef` instead of `document.documentElement`:

```tsx
function DualThemePreview({ leftTheme, rightTheme, children }) {
  const leftRef = useRef<HTMLDivElement>(null);
  const rightRef = useRef<HTMLDivElement>(null);
  return (
    <div className="grid grid-cols-2 gap-4">
      <div ref={leftRef}>
        <ThemeProvider theme={leftTheme} targetRef={leftRef}>
          {children}
        </ThemeProvider>
      </div>
      <div ref={rightRef}>
        <ThemeProvider theme={rightTheme} targetRef={rightRef}>
          {children}
        </ThemeProvider>
      </div>
    </div>
  );
}
```

⚠️ **Critical**: `targetRef` must point to a container that is NOT `document.documentElement`. Two ThemeProviders writing to `documentElement` would overwrite each other's CSS variables. This pattern is ONLY for side-by-side previews; the default `App.tsx` always writes to `documentElement`.

> **Starter compatibility**: Requires ThemeProvider v1.2+ which accepts an optional `targetRef: RefObject<HTMLElement>`. If `targetRef` is null/undefined, the provider writes to `documentElement` (current behavior). If your current ThemeProvider doesn't support it, add the prop first.

## 7. Known limitations

1. **Tailwind theme tokens are var() lookups, not values.** `borderRadius: 'var(--effect-border-radius)'` in `tailwind.config.ts` means Tailwind IntelliSense shows the `var()` string, not the actual pixel value. Fix: document expected values in the `ThemeConfig` type comment.
2. **`--slide-*` legacy tokens are deprecated but kept.** v1 starter shipped `--slide-bg`, `--slide-fg`, etc. v2 replaced with `--surface-*` and `--text-*`. Legacy names are written BOTH for 6 months to avoid breaking custom user CSS. Remove legacy writes after Q4 2026.
3. **ThemeProvider writes to documentElement synchronously.** In a deck with 100+ token derivations, first render adds ~2ms. Not an issue for production but shows up in React DevTools Profiler as a long synchronous block.
4. **`prefers-color-scheme: dark` auto-detect is opt-in.** By default, ThemeProvider uses `theme.preferred` and ignores system preference. To enable: pass `auto: true` in theme config (requires v1.2+ starter).
