import { defineConfig, devices } from '@playwright/test';

// Port is overridable (PORT env, default 4173) and shared with vite.config.ts's preview server, so a
// busy port is escapable with `PORT=4180 npm test`. reuseExistingServer is off on purpose: reusing a
// foreign process already on the port would silently test the wrong app; with strictPort a busy port
// instead fails fast with a clear "Port is in use" error.
const PORT = Number(process.env.PORT) || 4173;
const ORIGIN = `http://localhost:${PORT}`;

export default defineConfig({
  testDir: './tests',
  fullyParallel: false, // Slide tests share a single browser + URL state
  // CI: serial workers so a single browser process is reused; local: let playwright choose
  ...(process.env.CI ? { workers: 1 } : {}),
  forbidOnly: !!process.env.CI,
  // H-3 (P0-5): tolerate flaky network on CI; local runs keep strict to surface flake to the author.
  retries: process.env.CI ? 2 : 0,
  // H-3: overall test budget. One scene/beat pair is ~2s (networkidle + fonts + screenshot); with the
  // starter's 2 scenes × 3 beats this fits comfortably; raising to 45s leaves headroom for a real deck.
  timeout: 45_000,
  expect: {
    timeout: 15_000,
    // Absorb sub-pixel anti-aliasing / font-hinting jitter (approx. 1/2000 of pixels)
    // without letting real regressions slip through.
    toHaveScreenshot: {
      maxDiffPixelRatio: 0.0005,
      maxDiffPixels: 100,
    },
  },
  // H-3 (P0-5): CI emits list + html + junit (junit is the machine-readable artifact gate); local keeps
  // list only unless a test actually fails, in which case the html report opens.
  reporter: process.env.CI
    ? [
        ['list'],
        ['html', { open: 'never' }],
        ['junit', { outputFile: 'test-results/playwright-junit.xml' }],
      ]
    : [['list'], ['html', { open: 'on-failure' }]],
  // P0-1 FIXED: drop the default `{platform}-` prefix so baselines are byte-comparable between
  // developer darwin laptops and linux CI runners. Snapshot contents still differ slightly between
  // Chromium builds (antialiasing); that's what maxDiffPixelRatio is for.
  // 必须在 defineConfig 顶层（不是 use: 里），对所有项目生效。
  snapshotPathTemplate: '{testDir}/{testFileDir}/snapshots/{arg}{ext}',
  use: {
    baseURL: ORIGIN,
    // CR-4 fix: lock every project to a canonical 1920×1080 @ DPR=1 so visual snapshots and
    // layout audits are byte-comparable across developer laptops and CI. playwright's
    // Desktop Chrome profile inherits these; project-level `use` overrides are additive.
    viewport: { width: 1920, height: 1080 },
    deviceScaleFactor: 1,
    ignoreHTTPSErrors: true,
    trace: 'retain-on-failure',
  },
  projects: [
    {
      name: 'chromium',
      use: {
        ...devices['Desktop Chrome'],
        // Explicitly repeat the locks at the project level so merging with the Desktop Chrome
        // preset can never accidentally override viewport / DPR.
        viewport: { width: 1920, height: 1080 },
        deviceScaleFactor: 1,
      },
    },
  ],
  webServer: {
    command: 'npm run build && npm run preview',
    url: ORIGIN,
    reuseExistingServer: false,
    timeout: 120_000,
  },
});
