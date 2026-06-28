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
