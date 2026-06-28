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
  }, [theme]);

  return <ThemeContext.Provider value={theme}>{children}</ThemeContext.Provider>;
}
