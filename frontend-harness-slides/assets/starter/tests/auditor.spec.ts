import { test, expect } from '@playwright/test';

// Structural & layout safety audit (not pixels). Reads the slide list at runtime from
// window.__SLIDE_REGISTRY__ (single source). Per scene / beat it runs three checks, each mapping
// 1:1 to a line in the skill's completion criterion — and each kept near-zero-false-positive:
//   1) beat-honored: the app actually rendered the requested scene + beat.
//   2) zero-size: an element that declares intent to be visible (own direct text, or media with a
//      src) must not collapse to 0x0 — the canonical "rendered to nothing" silent break.
//   3) overflow: no visible element escapes [data-slide-stage]; deliberate bleed opts out with
//      data-allow-overflow.
// Element collision is intentionally NOT asserted here: real decks layer on purpose (text over
// imagery, badges on cards), so a generic DOM collision check is a false-positive machine. "Does it
// look wrong" is owned by the visual baseline in visual.spec.ts, not a brittle DOM heuristic.

test('layout audit — every registered scene / beat', async ({ page }) => {
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
      const where = `${id} beat ${beat}`;

      // —— Check 1: the router honored the requested frame ——
      const landed = await page.evaluate(() => {
        const stage = document.querySelector('[data-slide-stage]');
        return { id: stage?.getAttribute('data-slide-id'), beat: stage?.getAttribute('data-beat') };
      });
      expect.soft(landed, `${where}: router did not honor the requested scene/beat`).toEqual({
        id,
        beat: String(beat),
      });

      // —— Check 2: should-be-visible elements that rendered 0x0 ——
      const zeroSize = await page.evaluate(() => {
        const offenders: string[] = [];
        const isHidden = (el: Element) => {
          const s = getComputedStyle(el);
          return (
            s.display === 'none' ||
            s.visibility === 'hidden' ||
            s.opacity === '0' ||
            el.closest('[aria-hidden="true"], [data-allow-empty]') !== null
          );
        };
        const hasOwnText = (el: Element) =>
          Array.from(el.childNodes).some(
            (n) => n.nodeType === Node.TEXT_NODE && (n.textContent ?? '').trim().length > 2,
          );
        const isMedia = (el: Element) =>
          (el.tagName === 'IMG' || el.tagName === 'VIDEO') && !!el.getAttribute('src');

        for (const el of document.querySelectorAll('[data-slide-stage] *')) {
          if (isHidden(el)) continue;
          if (!hasOwnText(el) && !isMedia(el)) continue;
          const r = el.getBoundingClientRect();
          if (r.width === 0 || r.height === 0) {
            offenders.push(`<${el.tagName.toLowerCase()}> "${(el.textContent ?? '').trim().slice(0, 30)}"`);
          }
        }
        return offenders;
      });
      expect.soft(zeroSize, `${where}: element should be visible but rendered 0x0`).toEqual([]);

      // —— Check 3: elements escaping [data-slide-stage] ——
      const escaped = await page.evaluate(() => {
        const stage = document.querySelector('[data-slide-stage]');
        if (!stage) return ['[data-slide-stage] not found (does SlideStage carry the attribute?)'];
        const s = stage.getBoundingClientRect();
        const offenders: string[] = [];
        for (const el of document.querySelectorAll('[data-slide-stage] *')) {
          if ((el as HTMLElement).closest('[data-allow-overflow]')) continue; // deliberate bleed
          const r = el.getBoundingClientRect();
          if (r.width === 0 || r.height === 0) continue;
          if (
            r.left < s.left - 0.5 ||
            r.top < s.top - 0.5 ||
            r.right > s.right + 0.5 ||
            r.bottom > s.bottom + 0.5
          ) {
            offenders.push(`<${el.tagName.toLowerCase()}> "${(el.textContent ?? '').trim().slice(0, 30)}"`);
          }
        }
        return offenders;
      });
      expect.soft(escaped, `${where}: element escapes the stage`).toEqual([]);
    }
  }
});
