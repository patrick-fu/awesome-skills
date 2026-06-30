import { test, expect } from '@playwright/test';
import type {
  ConsoleMessage,
  Page,
  Request,
  Response,
  TestInfo,
} from '@playwright/test';

// Deterministic pixel regression (frozen frame). The slide list is read at runtime from
// window.__SLIDE_REGISTRY__ (single source) — never duplicated here. Chromium only: one baseline,
// less CI bandwidth; the cross-platform snapshot suffix is matched automatically.
//
// Keep the freeze helper local to the Playwright spec. Importing a shared .mjs module from a
// Playwright test can hang during `playwright test --list` in some environments, which means
// preflight cannot tell whether the harness is usable.

const FREEZE_CSS = `
*, *::before, *::after {
  animation-play-state: paused !important;
  animation: none !important;
  transition: none !important;
  transition-duration: 0s !important;
  transition-property: none !important;
  animation-fill-mode: both !important;
}
video, lottie-player, canvas, iframe {
  animation-play-state: paused !important;
}
html { scroll-behavior: auto !important; }
svg :is(animate, animateTransform, animateMotion, animateColor, set) {
  display: none !important;
}
`;

const VISUAL_MASK_SELECTORS = [
  'canvas',
  'iframe',
  'video',
  '.non-deterministic',
  '[data-visual-mask]',
];

async function freezeImperative(page: Page) {
  await page.evaluate(() => {
    try {
      const docAny = document as Document & {
        getAnimations?: (opts?: { subtree?: boolean }) => Animation[];
        pauseAnimations?: () => void;
      };
      const allAnims = typeof docAny.getAnimations === 'function'
        ? docAny.getAnimations({ subtree: true })
        : [];
      for (const anim of allAnims) {
        try { anim.pause(); } catch {
          try { anim.cancel(); } catch { /* swallow */ }
        }
      }
    } catch { /* CSS freeze still covers normal animations */ }

    try {
      const smilNodes = document.querySelectorAll('animate, animateTransform, animateMotion, animateColor, set');
      for (const node of Array.from(smilNodes)) {
        const n = node as SVGElement & { endElement?: () => void; pauseAnimations?: () => void };
        try { n.endElement?.(); } catch { /* ignore */ }
        try { n.pauseAnimations?.(); } catch { /* ignore */ }
      }
      for (const svg of Array.from(document.querySelectorAll('svg'))) {
        const s = svg as SVGSVGElement & { pauseAnimations?: () => void };
        try { s.pauseAnimations?.(); } catch { /* ignore */ }
      }
      const docAny = document as Document & { pauseAnimations?: () => void };
      try { docAny.pauseAnimations?.(); } catch { /* ignore */ }
    } catch { /* ignore */ }

    try {
      const medias = document.querySelectorAll('video, audio');
      for (const media of Array.from(medias)) {
        const m = media as HTMLMediaElement;
        try { if (!m.paused) m.pause(); } catch { /* ignore */ }
        try { m.currentTime = 0; } catch { /* ignore */ }
      }
    } catch { /* ignore */ }
  });
}

async function waitForAnimationsToSettle(page: Page, opts?: { samples?: number; intervalMs?: number; stableRounds?: number }) {
  const samples = opts?.samples ?? 30;
  const intervalMs = opts?.intervalMs ?? 50;
  const stableRounds = opts?.stableRounds ?? 3;
  const selector = [
    'div','span','p','a','strong','em',
    'h1','h2','h3','h4','h5','h6',
    'img','li','button','input','select','textarea','label',
    'section','article','nav','header','footer','aside','main',
    'svg','path','circle','rect','g','text','use',
    'polygon','polyline','line','ellipse','canvas',
    'code','pre','kbd','samp',
    'table','thead','tbody','tfoot','tr','th','td',
    'video','audio','iframe','picture','figure','figcaption',
    'ul','ol','dl','dt','dd',
    'small','sub','sup','abbr','blockquote','hr',
  ].join(',');

  const history: string[] = [];
  for (let i = 0; i < samples; i += 1) {
    const current = await page.evaluate((sel) => {
      const els = document.querySelectorAll(sel);
      const parts = new Array(els.length);
      for (let j = 0; j < els.length; j += 1) {
        const el = els[j]!;
        const r = el.getBoundingClientRect();
        const s = window.getComputedStyle(el);
        parts[j] = [
          r.top, r.left, r.width, r.height,
          s.opacity, s.transform, s.filter,
          s.strokeDashoffset, s.strokeDasharray,
        ].join(',');
      }
      return parts.join('|');
    }, selector);

    history.push(current);
    if (history.length > stableRounds) history.shift();
    if (history.length === stableRounds && history.every((value) => value === history[0])) {
      return;
    }
    await page.waitForTimeout(intervalMs);
  }
}

async function freezePage(page: Page) {
  try {
    await page.addStyleTag({ content: FREEZE_CSS });
  } catch { /* page may be in a bad state; continue to imperative freeze */ }
  await freezeImperative(page);
  await waitForAnimationsToSettle(page);
}

// —— H-5 health channels: a broken page must not produce a "same-as-last-time" screenshot ——
// P0-6 FIXED: single vHealthErrors array aggregates 4 error channels; legacy per-channel
// arrays were retired to avoid drift between parallel collectors.
const vHealthErrors: string[] = [];

test.beforeEach(async ({ page }: { page: Page }) => {
  vHealthErrors.length = 0;
  page.on('pageerror', (err: Error) => {
    vHealthErrors.push(`[PAGE_ERROR] ${(err.name ?? 'E')}: ${err.message}\n${(err.stack ?? '').slice(0, 500)}`);
  });
  page.on('console', (msg: ConsoleMessage) => {
    if (msg.type() !== 'error') return;
    const t = msg.text();
    if (t.includes('[vite]') || t.includes('Download the React DevTools') || t.includes('[HMR]') ||
        /HMR|Vite|source-map|failed to fetch dynamically imported module/i.test(t)) {
      return;
    }
    vHealthErrors.push(`[CONSOLE_ERROR] ${t.slice(0, 500)}`);
  });
  page.on('requestfailed', (req: Request) => {
    const u = req.url();
    if (u.endsWith('/favicon.ico')) return;
    if (u.startsWith('data:') || u.startsWith('about:')) return;
    const err = req.failure()?.errorText ?? 'unknown';
    vHealthErrors.push(`[REQ_FAILED] ${err} ${u.slice(0, 300)}`);
  });
  page.on('response', (res: Response) => {
    const s = res.status();
    const u = res.url();
    if (u.endsWith('/favicon.ico')) return;
    const ct = res.headers()['content-type'] ?? '';
    if (s >= 400 && !ct.startsWith('text/event-stream')) {
      vHealthErrors.push(`[HTTP_${s}] ${res.request().method()} ${u.slice(0, 300)}`);
    }
  });
});

// Surface H-5 health errors as soft assertions at the end of every test, then hard-fail if any
// soft error accumulated. Order matters: if we only checked in test() body, beforeEach-attached
// listeners that fire after the body's final line (last-page idle network, late errors) would be
// lost to the timing gap.
test.afterEach(async ({}, testInfo: TestInfo) => {
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

test('pixel regression — every registered scene / beat',
  { tag: ['@visual', '@slow', '@screenshot'] },
  async ({ page }: { page: Page }, testInfo: TestInfo) => {
    test.skip(testInfo.project.name !== 'chromium', 'Visual snapshots run on Chromium desktop only.');
    await page.setViewportSize({ width: 1920, height: 1080 });

    await page.goto('/?test=true', { waitUntil: 'networkidle' });
    const registry = await page.evaluate(() => window.__SLIDE_REGISTRY__ ?? []);
    expect(
      registry.length,
      'window.__SLIDE_REGISTRY__ is empty: call exposeRegistryForTooling() at startup',
    ).toBeGreaterThan(0);

    // CR-5 fix: every screenshot clips to [data-slide-stage]'s bounding box, so letterbox chrome
    // around the 1920×1080 canvas never pollutes the baseline.
    const stageLocator = page.locator('[data-slide-stage]');
    const firstBcr = await stageLocator.boundingBox();
    if (!firstBcr) throw new Error('[data-slide-stage] has no bounding box — cannot clip screenshots');
    const clip = { x: firstBcr.x, y: firstBcr.y, width: firstBcr.width, height: firstBcr.height };

    // Canvas/iframe/video etc. can't be frozen (e.g. cross-origin <iframe> has its own event loop).
    const mask = VISUAL_MASK_SELECTORS.map((s: string) => page.locator(s));

    for (const { id, totalBeats } of registry) {
      for (let beat = 0; beat <= totalBeats; beat++) {
        // P1-4: SPA nav via __deck.gotoBeat() — same rationale as auditor.spec.
        await page.evaluate(
          ([sid, b]) => (window as any).__deck?.gotoBeat(sid, b),
          [id, beat] as const,
        );
        await page.waitForFunction(
          ([sid, b]) => {
            const stage = document.querySelector('[data-slide-stage]');
            return stage?.getAttribute('data-slide-id') === sid
              && stage?.getAttribute('data-beat') === String(b);
          },
          [id, beat] as const,
          { timeout: 8000 },
        );
        await page.evaluate(() => document.fonts.ready);

        // Defense-in-depth: landed assertion. Technically waitForFunction above already
        // proves this, but we keep the soft assert so a framework regression is explicit.
        const landed = await page.evaluate(() => {
          const stage = document.querySelector('[data-slide-stage]');
          return { id: stage?.getAttribute('data-slide-id'), beat: stage?.getAttribute('data-beat') };
        });
        expect
          .soft(landed, `${id} beat ${beat}: router did not honor the requested scene/beat`)
          .toEqual({ id, beat: String(beat) });

        await freezePage(page); // CSS + WAAPI + SMIL + media, then wait for spring physics.

        // CR-5: clip to the stage BCR — no fullPage (1920×1080 stage == viewport).
        // Mask non-frozen live elements so stable surrounding layout remains regression-tested.
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
