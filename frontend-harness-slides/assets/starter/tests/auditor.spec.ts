import { test, expect } from '@playwright/test';

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
let pageErrors: string[] = [];
let consoleErrors: string[] = [];
let failedRequests: Array<{ url: string; error: string }> = [];
let badStatusResponses: Array<{ url: string; status: number }> = [];
// P0-6 FIXED: 健康度通道 —— 统一单数组聚合 4 类错误（pageerror/console.error/HTTP 4xx/requestfailed）
const healthErrors: string[] = [];

test.beforeEach(async ({ page }, testInfo) => {
  pageErrors = [];
  consoleErrors = [];
  failedRequests = [];
  badStatusResponses = [];
  // P0-6: 每次测试前清空统一健康度数组
  healthErrors.length = 0;

  // 1. Uncaught JS exceptions on the page (React render crashes / runtime TypeErrors / etc.)
  page.on('pageerror', (err) => {
    pageErrors.push(`${err.name ?? 'Error'}: ${err.message}\n${err.stack ?? ''}`);
  });

  // 2. console.error / failed console.assert — catches React warnings, resource load failures,
  //    failed prop-type checks, and any `console.error(...)` the author dropped during debugging.
  page.on('console', (msg) => {
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
    consoleErrors.push(text);
    // P0-6: 同步写入统一健康度数组
    healthErrors.push(`[CONSOLE_ERROR] ${text.slice(0, 500)}`);
  });

  // 3. Network-level failures (DNS, CORS, net::ERR_*, TLS, aborted). 404 on a missing asset is
  //    NOT caught here — it's a valid HTTP response with status 404, caught in the next handler.
  page.on('requestfailed', (req) => {
    const url = req.url();
    if (url.endsWith('/favicon.ico')) return; // dev-server favicon 404 is expected noise
    if (url.startsWith('data:') || url.startsWith('about:')) return;
    const err = req.failure()?.errorText ?? 'unknown';
    failedRequests.push({ url, error: err });
    // P0-6: 同步写入统一健康度数组
    healthErrors.push(`[REQ_FAILED] ${err} ${url.slice(0, 300)}`);
  });

  // 4. HTTP 4xx / 5xx responses. Missing JS/CSS/assets, broken API endpoints.
  page.on('response', (res) => {
    const status = res.status();
    const url = res.url();
    if (url.endsWith('/favicon.ico')) return;
    const ct = res.headers()['content-type'] ?? '';
    if (status >= 400 && !ct.startsWith('text/event-stream')) {
      badStatusResponses.push({ url, status });
      // P0-6: 同步写入统一健康度数组
      healthErrors.push(`[HTTP_${status}] ${res.request().method()} ${url.slice(0, 300)}`);
    }
  });
});


// P0-6 + P0-7 FIXED: afterEach 健康度通道 soft 断言 + soft 兜底 hard 失败
test.afterEach(async ({}, testInfo) => {
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
      // CR-2 fix: isEffectivelyHidden walks the ancestor chain + checks BCR size, so a parent
      // display:none doesn't cause a "should be visible but is 0x0" false-negative or, worse,
      // a false-positive zero-size report on an element the renderer never measured.
      const zeroSize = await page.evaluate(() => {
        const offenders: string[] = [];
        // P0-8 FIXED: 递归祖先检查（替代原来的 while 迭代），防止 wrapper display:none 导致误判
        function isHidden(el: Element): boolean {
          if (!el || el === document.documentElement) return false;
          // 显式跳过：aria-hidden 真正隐藏、或用户标注的 data-allow-empty
          if (el.parentElement == null && el !== document.body) {
            // 已到达顶层，document.body 之上不再递归
          }
          if (el.closest && el.closest('[aria-hidden="true"], [data-allow-empty]') !== null) return true;
          const cs = getComputedStyle(el);
          if (cs.display === 'none') return true;
          if (cs.visibility === 'hidden') return true;
          if (Number(cs.opacity) === 0) return true;
          if ((el as HTMLElement).hasAttribute && (el as HTMLElement).hasAttribute('hidden')) return true;
          // offsetParent check（非 fixed/sticky 元素没 offsetParent + 0 尺寸 = 真被藏了）
          const htmlEl = el as HTMLElement;
          if (htmlEl.offsetParent === null &&
              cs.position !== 'fixed' &&
              cs.position !== 'sticky') {
            const w = htmlEl.offsetWidth, h = htmlEl.offsetHeight;
            if (w === 0 && h === 0) return true;
          }
          // 递归到父级
          if (el.parentElement) return isHidden(el.parentElement);
          return false;
        }
        // BCR 尺寸兜底（递归检查完祖先后再量一次当前元素大小）
        const isEffectivelyHidden = (el: Element): boolean => {
          if (isHidden(el)) return true;
          const bcr = (el as HTMLElement).getBoundingClientRect();
          if (bcr.width === 0 && bcr.height === 0) return true;
          return false;
        };
        // M-2 FIXED: use Unicode code-point-aware length `[...raw].length` and require >0
        // (not >2). `>2` was written for English ("Hi" = 2 chars, skipped), but a CJK single
        // character like "一" or two-character word like "你好" was wrongly treated as empty
        // and skipped the 0×0 check. Also strip pure punctuation/whitespace so a node whose
        // own text is only "，。、 " doesn't count as "has content".
        const PUNCT_RE = /^[\p{P}\p{Z}\s]+$/u;
        const hasOwnText = (el: Element) =>
          Array.from(el.childNodes).some((n) => {
            if (n.nodeType !== Node.TEXT_NODE) return false;
            const raw = (n.textContent ?? '').trim();
            if (!raw) return false;
            if (PUNCT_RE.test(raw)) return false; // 纯标点：不算内容文本
            return [...raw].length > 0;
          });
        const isMedia = (el: Element) =>
          (el.tagName === 'IMG' || el.tagName === 'VIDEO') && !!el.getAttribute('src');

        for (const el of document.querySelectorAll('[data-slide-stage] *')) {
          if (isEffectivelyHidden(el)) continue;
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

  // CR-1 fix: expect.soft() never fails the test on its own. This line turns accumulated
  // soft errors into a hard failure so the spec actually goes red.
  expect(test.info().errors, 'Soft assertions accumulated failures (see logs above)').toHaveLength(0);

  // H-5 (P0-6): four-channel health check — a React crash or a 404 must not let the audit pass.
  // Using expect.soft so all four channels are reported in one run.
  expect.soft(pageErrors, 'PAGE ERRORS: uncaught JS exceptions on the page (React crash / runtime TypeError)').toEqual([]);
  expect.soft(consoleErrors, 'CONSOLE ERRORS: console.error() was printed (React warning / resource load fail / debugging residue)').toEqual([]);
  expect.soft(failedRequests, 'REQUEST FAILURES: network-level request failures (DNS / CORS / net::ERR_* / TLS)').toEqual([]);
  expect.soft(badStatusResponses, 'BAD HTTP STATUS: received a 4xx/5xx response (missing asset / broken endpoint)').toEqual([]);

  // Turn the four-channel soft errors into a hard failure.
  expect(test.info().errors, 'Health channels accumulated failures (see logs above)').toHaveLength(0);
});
