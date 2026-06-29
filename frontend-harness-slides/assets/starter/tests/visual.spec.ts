import { test, expect } from '@playwright/test';
import {
  FREEZE_CSS,
  freezePage,
  freezeImperative,
  waitForAnimationsToSettle,
  VISUAL_MASK_SELECTORS,
} from '../harness/freeze.mjs';

// Deterministic pixel regression (frozen frame). The slide list is read at runtime from
// window.__SLIDE_REGISTRY__ (single source) — never duplicated here. Chromium only: one baseline,
// less CI bandwidth; the cross-platform snapshot suffix is matched automatically.

// —— H-5 health channels: a broken page must not produce a "same-as-last-time" screenshot ——
let vPageErrors: string[] = [];
let vConsoleErrors: string[] = [];
let vFailedRequests: Array<{ url: string; error: string }> = [];
let vBadStatus: Array<{ url: string; status: number }> = [];
const vHealthErrors: string[] = [];

test.beforeEach(async ({ page }) => {
  vPageErrors = [];
  vConsoleErrors = [];
  vFailedRequests = [];
  vBadStatus = [];
  vHealthErrors.length = 0;
  page.on('pageerror', (err) => {
    vPageErrors.push(`${err.name ?? 'E'}: ${err.message}\n${err.stack ?? ''}`);
    vHealthErrors.push(`[PAGE_ERROR] ${(err.name ?? 'E')}: ${err.message}`);
  });
  page.on('console', (msg) => {
    if (msg.type() !== 'error') return;
    const t = msg.text();
    if (t.includes('[vite]') || t.includes('Download the React DevTools') || t.includes('[HMR]') ||
        /HMR|Vite|source-map|failed to fetch dynamically imported module/i.test(t)) {
      return;
    }
    vConsoleErrors.push(t);
    vHealthErrors.push(`[CONSOLE_ERROR] ${t.slice(0, 500)}`);
  });
  page.on('requestfailed', (req) => {
    const u = req.url();
    if (u.endsWith('/favicon.ico')) return;
    if (u.startsWith('data:') || u.startsWith('about:')) return;
    const err = req.failure()?.errorText ?? 'unknown';
    vFailedRequests.push({ url: u, error: err });
    vHealthErrors.push(`[REQ_FAILED] ${err} ${u.slice(0, 300)}`);
  });
  page.on('response', (res) => {
    const s = res.status();
    const u = res.url();
    if (u.endsWith('/favicon.ico')) return;
    const ct = res.headers()['content-type'] ?? '';
    if (s >= 400 && !ct.startsWith('text/event-stream')) {
      vBadStatus.push({ url: u, status: s });
      vHealthErrors.push(`[HTTP_${s}] ${res.request().method()} ${u.slice(0, 300)}`);
    }
  });
});

// Surface H-5 health errors as soft assertions at the end of every test, then hard-fail if any
// soft error accumulated. Order matters: if we only checked in test() body, beforeEach-attached
// listeners that fire after the body's final line (last-page idle network, late errors) would be
// lost to the timing gap.
test.afterEach(async ({}, testInfo) => {
  // Per-channel soft reports (one error per line = one soft failure, so triage is scannable).
  if (vHealthErrors.length > 0) {
    for (const err of vHealthErrors) {
      expect.soft(false, `[H-5 健康度通道] ${testInfo.title}: ${err}`).toBeTruthy();
    }
  }
  // CR-1 + H-5: turn any accumulated soft error into a hard failure.
  expect(
    testInfo.errors,
    `"${testInfo.title}" 存在 soft 断言失败（含 H-5 健康度通道），详情见上方日志`,
  ).toHaveLength(0);
});

test('pixel regression — every registered scene / beat', async ({ page }, testInfo) => {
  test.skip(testInfo.project.name !== 'chromium', 'Visual snapshots run on Chromium desktop only.');
  await page.setViewportSize({ width: 1920, height: 1080 });

  await page.goto('/?test=true', { waitUntil: 'networkidle' });
  const registry = await page.evaluate(() => window.__SLIDE_REGISTRY__ ?? []);
  expect(
    registry.length,
    'window.__SLIDE_REGISTRY__ is empty: call exposeRegistryForTooling() at startup',
  ).toBeGreaterThan(0);

  // CR-5 fix: every screenshot clips to [data-slide-stage]'s bounding box. This guarantees
  // visual.spec.ts and export-pdf.mjs crop from the same geometric origin, and that letterbox
  // chrome (flex-centered padding around the 1920×1080 canvas) never pollutes the baseline.
  const stageLocator = page.locator('[data-slide-stage]');
  const firstBcr = await stageLocator.boundingBox();
  if (!firstBcr) throw new Error('[data-slide-stage] has no bounding box — cannot clip screenshots');
  const clip = { x: firstBcr.x, y: firstBcr.y, width: firstBcr.width, height: firstBcr.height };

  // Canvas/iframe/video etc. can't be frozen (e.g. cross-origin <iframe> has its own event loop).
  // VISUAL_MASK_SELECTORS is the single source shared between the harness and any callers.
  const mask = VISUAL_MASK_SELECTORS.map((s) => page.locator(s));

  for (const { id, totalBeats } of registry) {
    for (let beat = 0; beat <= totalBeats; beat++) {
      await page.goto(`/?scene=${id}&beat=${beat}&test=true`, { waitUntil: 'networkidle' });
      await page.evaluate(() => document.fonts.ready);

      // The app must actually have landed on the requested frame, or the screenshot is meaningless
      // (a router that silently ignored the params would still "pass" against whatever rendered).
      const landed = await page.evaluate(() => {
        const stage = document.querySelector('[data-slide-stage]');
        return { id: stage?.getAttribute('data-slide-id'), beat: stage?.getAttribute('data-beat') };
      });
      expect
        .soft(landed, `${id} beat ${beat}: router did not honor the requested scene/beat`)
        .toEqual({ id, beat: String(beat) });

      await freezePage(page);           // CSS + WAAPI + SMIL + media (single source)
      await freezeImperative(page);     // belt-and-suspenders (idempotent even if freezePage called it)
      await waitForAnimationsToSettle(page); // wait for spring physics to fully decay

      // CR-5: clip to the stage BCR — no fullPage (1920×1080 stage == viewport).
      // Mask for non-frozen live elements is sourced from VISUAL_MASK_SELECTORS so the harness
      // and any downstream callers agree on what is "not pixel-regression-tested".
      await expect.soft(page).toHaveScreenshot(`${id}-beat-${beat}.png`, {
        clip,
        maxDiffPixelRatio: 0.0005,
        maxDiffPixels: 100,
        mask,
      });
    }
  }

  // CR-1: expect.soft() never fails the test on its own — turn accumulated errors hard.
  // NOTE: H-5 per-test failures are surfaced in test.afterEach(), this line handles soft
  // failures from the beat loop (router assertions, screenshot diffs).
  expect(test.info().errors, 'Soft assertions accumulated failures (see logs above)').toHaveLength(0);
});
