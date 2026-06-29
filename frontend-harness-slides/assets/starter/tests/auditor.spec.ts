import { test, expect } from '@playwright/test';
import type {
  ConsoleMessage,
  Page,
  Request,
  Response,
  TestInfo,
} from '@playwright/test';

// Structural & layout safety audit (not pixels). Reads the slide list at runtime from
// window.__SLIDE_REGISTRY__ (single source). Per scene / beat it runs three checks, each mapping
// 1:1 to a line in the skill's completion criterion — and each kept near-zero-false-positive:
//   1) beat-honored: the app actually rendered the requested scene + beat.
//   2) zero-size: an element that declares intent to be visible (own direct text, or media with a
//      src) must not collapse to 0x0 — the canonical "rendered to nothing" silent break.
//   3) overflow: no visible element escapes [data-slide-stage]; deliberate bleed opts out with
//      data-allow-overflow.
//   4) health channels (H-5 P0-6): page JS errors, console.error, failed HTTP requests, 4xx/5xx
//      responses — a React crash must NOT still let the auditor go green.
// Element collision is intentionally NOT asserted here: real decks layer on purpose (text over
// imagery, badges on cards), so a generic DOM collision check is a false-positive machine. "Does it
// look wrong" is owned by the visual baseline in visual.spec.ts, not a brittle DOM heuristic.

// —— H-5 health collectors: set up in beforeEach, asserted once after the scene/beat loop ——
// P0-6 FIXED: 单一数组聚合 4 类错误（pageerror/console.error/HTTP 4xx/requestfailed），
// 避免多个 per-channel 数组不同步导致的漏报错。
const healthErrors: string[] = [];

test.beforeEach(async ({ page }: { page: Page }, _testInfo: TestInfo) => {
  // P0-6: 每次测试前清空统一健康度数组
  healthErrors.length = 0;

  // P0-6 FIXED: pageerror 写入统一 healthErrors 单数组，四通道格式统一
  page.on('pageerror', (err: Error) => {
    healthErrors.push(`[PAGE_ERROR] ${err.name ?? 'Error'}: ${err.message}\n${(err.stack ?? '').slice(0, 500)}`);
  });

  // 2. console.error / failed console.assert — catches React warnings, resource load failures,
  //    failed prop-type checks, and any `console.error(...)` the author dropped during debugging.
  page.on('console', (msg: ConsoleMessage) => {
    if (msg.type() !== 'error') return;
    const text = msg.text();
    // Noise suppression: Vite HMR handshakes, React DevTools promo, Playwright's own frames.
    if (
      text.includes('[vite] connecting') ||
      text.includes('[vite] connected') ||
      text.includes('[vite] hot updated') ||
      text.includes('Download the React DevTools') ||
      text.includes('[HMR]') ||
      /HMR|Vite|source-map|failed to fetch dynamically imported module/i.test(text)
    ) {
      return;
    }
    // P0-6: 同步写入统一健康度数组
    healthErrors.push(`[CONSOLE_ERROR] ${text.slice(0, 500)}`);
  });

  // 3. Network-level failures (DNS, CORS, net::ERR_*, TLS, aborted). 404 on a missing asset is
  //    NOT caught here — it's a valid HTTP response with status 404, caught in the next handler.
  page.on('requestfailed', (req: Request) => {
    const url = req.url();
    if (url.endsWith('/favicon.ico')) return; // dev-server favicon 404 is expected noise
    if (url.startsWith('data:') || url.startsWith('about:')) return;
    const err = req.failure()?.errorText ?? 'unknown';
    // P0-6: 同步写入统一健康度数组
    healthErrors.push(`[REQ_FAILED] ${err} ${url.slice(0, 300)}`);
  });

  // 4. HTTP 4xx / 5xx responses. Missing JS/CSS/assets, broken API endpoints.
  page.on('response', (res: Response) => {
    const status = res.status();
    const url = res.url();
    if (url.endsWith('/favicon.ico')) return;
    const ct = res.headers()['content-type'] ?? '';
    if (status >= 400 && !ct.startsWith('text/event-stream')) {
      // P0-6: 同步写入统一健康度数组
      healthErrors.push(`[HTTP_${status}] ${res.request().method()} ${url.slice(0, 300)}`);
    }
  });
});


// P0-6 + P0-7 FIXED: afterEach 健康度通道 soft 断言 + soft 兜底 hard 失败
test.afterEach(async ({}, testInfo: TestInfo) => {
  // P0-6: 先 soft 断言每个健康度错误（一次性全部打出）
  if (healthErrors.length > 0) {
    for (const err of healthErrors) {
      expect.soft(false, `[健康度通道] ${testInfo.title}: ${err}`).toBeTruthy();
    }
  }
  // P0-7: soft 断言兜底 —— 任何 soft 失败都必须转成 hard 失败
  expect(
    testInfo.errors,
    `"${testInfo.title}" 存在断言失败（含 soft），详情见上方错误日志`,
  ).toHaveLength(0);
});

test('layout audit — every registered scene / beat', async ({ page }: { page: Page }) => {
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
      // CR-2 fix: isEffectivelyHidden walks the ancestor chain + checks BCR size, so a parent
      // display:none doesn't cause a "should be visible but is 0x0" false-negative or, worse,
      // a parent overflow:hidden clipping the child to 0x0 doesn't either.
      const zeroSize = await page.evaluate<string[]>(() => {
        // P0-8 FIXED: 递归 isHidden() 替代原来的 while 迭代，
        // 给出独立的 isEffectivelyHidden() 做 BCR 0x0 兜底。
        // 覆盖：aria-hidden / data-allow-empty closest、display:none、visibility:hidden、
        // opacity:0、HTML hidden 属性、offsetParent null + 非 fixed/sticky 0x0、递归祖先链。
        function isHidden(el: Element): boolean {
          if (!el || el === document.documentElement) return false; // base case
          if (el.closest && el.closest('[aria-hidden="true"], [data-allow-empty]') !== null) return true;
          const cs = getComputedStyle(el);
          if (cs.display === 'none') return true;
          if (cs.visibility === 'hidden') return true;
          if (Number(cs.opacity) === 0) return true;
          if ((el as HTMLElement).hasAttribute('hidden')) return true;
          // offsetParent 为 null + 0x0 + 非 fixed/sticky 时判定隐藏
          const htmlEl = el as HTMLElement;
          if (
            htmlEl.offsetParent === null &&
            cs.position !== 'fixed' &&
            cs.position !== 'sticky'
          ) {
            if (htmlEl.offsetWidth === 0 && htmlEl.offsetHeight === 0) return true;
          }
          if (el.parentElement) return isHidden(el.parentElement); // 递归
          return false;
        }
        const isEffectivelyHidden = (el: Element): boolean => {
          if (isHidden(el)) return true;
          const bcr = (el as HTMLElement).getBoundingClientRect();
          return bcr.width === 0 && bcr.height === 0; // BCR 0x0 fallback
        };
        const hidden = (el: Element) => isEffectivelyHidden(el);
        const offenders: string[] = [];
        const nodes = document.querySelectorAll('[data-slide-stage] *');
        for (const el of Array.from(nodes)) {
          const hasOwnText = Array.from(el.childNodes).some(
            (n) => n.nodeType === Node.TEXT_NODE && (n.textContent ?? '').trim().length > 0,
          );
          const isMedia =
            ['IMG', 'VIDEO', 'CANVAS', 'IFRAME'].includes((el as HTMLElement).tagName) &&
            el.hasAttribute('src');
          if ((hasOwnText || isMedia) && hidden(el)) {
            const tag = (el as HTMLElement).tagName.toLowerCase();
            const cls = (el as HTMLElement).className
              ? `.${String((el as HTMLElement).className).split(/\s+/).slice(0, 3).join('.')}`
              : '';
            offenders.push(`<${tag}${cls}>`);
            if (offenders.length >= 15) break;
          }
        }
        return offenders;
      });
      expect.soft(zeroSize, `${where}: elements declared visible but collapsed to 0x0`).toEqual([]);

      // —— Check 3: overflow beyond the stage bounds ——
      // `data-allow-overflow` opt-out handles intentional bleed (e.g. a header strip on top).
      const overflow = await page.evaluate<string[]>(() => {
        const stage = document.querySelector('[data-slide-stage]') as HTMLElement | null;
        if (!stage) return ['[data-slide-stage] not found'];
        const sbox = stage.getBoundingClientRect();
        const offenders: string[] = [];
        const all = stage.querySelectorAll<HTMLElement>('*');
        for (const el of Array.from(all)) {
          // Allow descendants to opt out of the overflow check individually.
          let optOut = false;
          for (let n: Element | null = el; n && n !== stage; n = n.parentElement) {
            if (n.hasAttribute('data-allow-overflow')) { optOut = true; break; }
          }
          if (optOut) continue;
          const r = el.getBoundingClientRect();
          if (r.width === 0 && r.height === 0) continue; // hidden nodes aren't overflow
          const outsideLeft = sbox.left - r.left;
          const outsideRight = r.right - sbox.right;
          const outsideTop = sbox.top - r.top;
          const outsideBottom = r.bottom - sbox.bottom;
          const maxOutside = Math.max(0, outsideLeft, outsideRight, outsideTop, outsideBottom);
          if (maxOutside > 2) {
            const tag = el.tagName.toLowerCase();
            const cls = el.className
              ? `.${String(el.className).split(/\s+/).slice(0, 3).join('.')}`
              : '';
            offenders.push(`<${tag}${cls}> overflows by ${Math.round(maxOutside)}px`);
            if (offenders.length >= 15) break;
          }
        }
        return offenders;
      });
      expect.soft(overflow, `${where}: elements escape the stage bounds`).toEqual([]);
    }
  }

  // —— Aggregate: any per-frame soft failure flips the whole test red ——
  expect(test.info().errors, `soft assertion failures above (see per-frame diffs)`).toHaveLength(0);
});
