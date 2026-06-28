// Single source of the freeze mechanism. Imported by tests/visual.spec.ts (the pixel harness) and
// scripts/export-pdf.mjs (the exporter) so both freeze frames identically — change it once, here.

// Pause every continuous / infinite animation, zero out transitions, and lock the first frame.
export const FREEZE_CSS = `
  *, *::before, *::after {
    animation-play-state: paused !important;
    animation-delay: 0s !important;
    transition-delay: 0s !important;
    transition-duration: 0s !important;
  }
`;

// Settle poller: when two consecutive samples show no change in element box / opacity, the page is
// physically at rest and safe to screenshot. Replaces brittle fixed waits.
export async function waitForAnimationsToSettle(page, { samples = 20, intervalMs = 50 } = {}) {
  let previous = '';
  for (let i = 0; i < samples; i++) {
    const current = await page.evaluate(() =>
      Array.from(document.querySelectorAll('div, span, p, h1, h2, h3, img, li, button'))
        .map((el) => {
          const r = el.getBoundingClientRect();
          return `${r.top},${r.left},${r.width},${r.height},${getComputedStyle(el).opacity}`;
        })
        .join('|'),
    );
    if (current === previous) return;
    previous = current;
    await page.waitForTimeout(intervalMs);
  }
}
