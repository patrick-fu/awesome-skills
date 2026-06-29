import { createContext, useContext, useEffect, type ReactNode } from 'react';

export interface ThemeConfig {
  id: string;
  name: string;
  fonts: {
    display: string; // headline font stack
    body: string; // copy font stack
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

const ThemeContext = createContext<ThemeConfig | null>(null);

export function useTheme(): ThemeConfig {
  const ctx = useContext(ThemeContext);
  if (!ctx) throw new Error('useTheme must be used within <ThemeProvider>');
  return ctx;
}

// Map theme tokens to CSS variables so slides use clean classes (bg-background, text-primary,
// font-display) and a live theme swap is just a variable update — no re-render of every slide.
export function ThemeProvider({ theme, children }: { theme: ThemeConfig; children: ReactNode }) {
  useEffect(() => {
    const root = document.documentElement;
    root.style.setProperty('--font-display', theme.fonts.display);
    root.style.setProperty('--font-body', theme.fonts.body);
    root.style.setProperty('--color-background', theme.colors.background);
    root.style.setProperty('--color-text', theme.colors.text);
    root.style.setProperty('--color-primary', theme.colors.primary);
    root.style.setProperty('--color-border', theme.colors.border);
    // H-2 fix: tailwind/themes.ts declare effects tokens; without writing them as CSS variables
    // here, any `rounded-border-radius` / `shadow-shadow` / `border-w-border-width` utility
    // resolves to `var(--effect-*)` with no value and silently falls back to the UA default.
    root.style.setProperty('--effect-border-radius', theme.effects.borderRadius);
    root.style.setProperty('--effect-border-width', theme.effects.borderWidth);
    root.style.setProperty('--effect-shadow', theme.effects.shadow);

    // P0-5 FIXED: Effects tokens — derived variants (sm/lg/xl) + Tailwind DEFAULT aliases.
    // 把 borderRadius/shadow 解析成数值 + 单位，派生出 sm/lg/xl 变量，供 rounded / shadow 工具类使用。
    {
      const parseLen = (v: string) => {
        const m = v.match(/^([\d.]+)([a-zA-Z%]*)$/);
        if (!m) return { num: 0, unit: 'px' };
        return { num: Number(m[1]), unit: m[2] || 'px' };
      };
      const { num: rNum, unit: rUnit } = parseLen(theme.effects.borderRadius);
      if (rNum > 0) {
        const mk = (n: number) => `${Number(n.toFixed(2))}${rUnit}`;
        root.style.setProperty('--effect-border-radius-sm', mk(Math.max(2, rNum * 0.5)));
        root.style.setProperty('--effect-border-radius-lg', mk(rNum * 1.5));
        root.style.setProperty('--effect-border-radius-xl', mk(rNum * 2.2));
        // 同时设置为 DEFAULT，这样普通 rounded() 也能吃到主题圆角
        root.style.setProperty('--slide-radius', mk(rNum));
      }
      // shadow-sm：把 shadow 里的 offset/blur 减半
      const shadow = theme.effects.shadow;
      if (shadow) {
        try {
          const reduced = shadow.replace(/(-?\d+(?:\.\d+)?)px\s+(-?\d+(?:\.\d+)?)px/g, (_, x, y) =>
            `${Math.floor(Number(x) / 2)}px ${Math.floor(Number(y) / 2)}px`,
          );
          root.style.setProperty('--effect-shadow-sm', reduced);
        } catch {
          root.style.setProperty('--effect-shadow-sm', shadow);
        }
        root.style.setProperty('--slide-shadow', shadow);
      }
    }
  }, [theme]);

  return <ThemeContext.Provider value={theme}>{children}</ThemeContext.Provider>;
}
