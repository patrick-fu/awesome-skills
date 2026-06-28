import type { ThemeConfig } from './ThemeProvider';

// One committed look. Swap fonts/colors here (and install the faces per references/fonts.md);
// the dual-preview flow in references/theming.md is how you discover the right one with the user.
export const defaultTheme: ThemeConfig = {
  id: 'midnight-lime',
  name: 'Midnight Lime',
  fonts: {
    display: "'Cabinet Grotesk', system-ui, sans-serif",
    body: "'Plus Jakarta Sans', system-ui, sans-serif",
  },
  colors: {
    background: '#0b0b0f',
    text: '#f5f5f4',
    primary: '#c7f284',
    border: '#2a2a32',
  },
  effects: {
    borderRadius: '1.5rem',
    borderWidth: '1px',
    shadow: '0 30px 80px -20px rgba(0, 0, 0, 0.6)',
  },
};
