import { defineConfig, devices } from '@playwright/test';

// Port is overridable (PORT env, default 4173) and shared with vite.config.ts's preview server, so a
// busy port is escapable with `PORT=4180 npm test`. reuseExistingServer is off on purpose: reusing a
// foreign process already on the port would silently test the wrong app; with strictPort a busy port
// instead fails fast with a clear "Port is in use" error.
const PORT = Number(process.env.PORT) || 4173;
const ORIGIN = `http://localhost:${PORT}`;

export default defineConfig({
  testDir: './tests',
  fullyParallel: true,
  forbidOnly: !!process.env.CI,
  reporter: 'list',
  use: {
    baseURL: ORIGIN,
  },
  projects: [{ name: 'chromium', use: { ...devices['Desktop Chrome'] } }],
  webServer: {
    command: 'npm run build && npm run preview',
    url: ORIGIN,
    reuseExistingServer: false,
    timeout: 120_000,
  },
});
