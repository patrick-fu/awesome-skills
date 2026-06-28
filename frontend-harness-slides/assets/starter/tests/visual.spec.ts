import { test, expect } from '@playwright/test';
import { FREEZE_CSS, waitForAnimationsToSettle } from '../harness/freeze.mjs';

// Deterministic pixel regression (frozen frame). The slide list is read at runtime from
// window.__SLIDE_REGISTRY__ (single source) — never duplicated here. Chromium only: one baseline,
// less CI bandwidth; the cross-platform snapshot suffix is matched automatically.

test('pixel regression — every registered scene / beat', async ({ page }, testInfo) => {
  test.skip(testInfo.project.name !== 'chromium', 'Visual snapshots run on Chromium desktop only.');
  await page.setViewportSize({ width: 1920, height: 1080 });

  await page.goto('/?test=true', { waitUntil: 'networkidle' });
  const registry = await page.evaluate(() => window.__SLIDE_REGISTRY__ ?? []);
  expect(
    registry.length,
    'window.__SLIDE_REGISTRY__ is empty: call exposeRegistryForTooling() at startup',
  ).toBeGreaterThan(0);

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

      await page.addStyleTag({ content: FREEZE_CSS }); // freeze continuous motion
      await waitForAnimationsToSettle(page); // wait for spring physics to settle

      // expect.soft: audit the whole deck and aggregate failures; one diff won't abort the rest
      await expect.soft(page).toHaveScreenshot(`${id}-beat-${beat}.png`, {
        maxDiffPixelRatio: 0.01, // absorb sub-pixel antialiasing across platforms
        fullPage: true,
        mask: [page.locator('[data-live-region]'), page.locator('iframe')], // can't freeze these
      });
    }
  }
});
