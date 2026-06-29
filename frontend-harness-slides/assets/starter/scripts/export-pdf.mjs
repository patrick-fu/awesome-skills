#!/usr/bin/env node
// Export the whole deck to a PDF — one page per slide, captured at its final beat as a frozen frame.
// Reads window.__SLIDE_REGISTRY__ from the running app (single source of truth) and reuses the same
// freeze as the visual harness (../harness/freeze.mjs), so the PDF matches what the harness verifies.
//
// Usage:
//   npm run build && npm run preview            # serve the deck (default http://localhost:4173)
//   node scripts/export-pdf.mjs [baseUrl] [-b http://...] [-o deck.pdf] [-c] [-h]
//
// Prereq: install Playwright's chromium (`npx playwright install chromium`).

import { chromium } from '@playwright/test';
import { freezePage, waitForAnimationsToSettle, VISUAL_MASK_SELECTORS } from '../harness/freeze.mjs';

// Robust CLI arg parser (accepts --out=foo.pdf, -o foo.pdf, positional baseUrl, --help, ...).
function parseArgs(argv) {
  const result = {
    base: `http://localhost:${process.env.PORT || 4173}`,
    out: 'deck.pdf',
    compact: false,
    withNotes: false,
    help: false,
  };
  for (let i = 0; i < argv.length; i++) {
    const arg = argv[i];
    if (arg === '--out' || arg === '-o') {
      const v = argv[i + 1];
      if (!v || v.startsWith('-')) throw new Error(`CLI error: ${arg} requires a value`);
      result.out = v;
      i++;
    } else if (arg.startsWith('--out=')) {
      result.out = arg.slice('--out='.length);
    } else if (arg.startsWith('-o') && arg.length > 2) {
      result.out = arg.slice(2);
    } else if (arg === '--base' || arg === '-b') {
      const v = argv[i + 1];
      if (!v || v.startsWith('-')) throw new Error(`CLI error: ${arg} requires a value`);
      result.base = v;
      i++;
    } else if (arg.startsWith('--base=')) {
      result.base = arg.slice('--base='.length);
    } else if (arg === '--url' || arg === '-u') {
      result.base = argv[i + 1];
      i++;
    } else if (arg.startsWith('--url=')) {
      result.base = arg.slice('--url='.length);
    } else if (arg === '--compact' || arg === '-c') {
      result.compact = true;
    } else if (arg === '--with-notes' || arg === '-n') {
      result.withNotes = true;
    } else if (arg === '--help' || arg === '-h') {
      result.help = true;
    } else if (!arg.startsWith('-')) {
      // Positional: treated as the base URL
      result.base = arg;
    } else {
      console.warn(`[warn] unknown CLI argument: ${arg}`);
    }
  }
  return result;
}

const args = parseArgs(process.argv.slice(2));
if (args.help) {
  console.log(`Usage: node scripts/export-pdf.mjs [baseUrl] [options]

Options:
  -b, --base <URL>     Preview server URL (default http://localhost:4173)
  -o, --out <file>     Output PDF path (default deck.pdf)
  -c, --compact        Export at 1280x720 instead of 1920x1080 (~50–70% smaller file)
  -n, --with-notes     Reserved: render speaker notes alongside slides
  -h, --help           Show this help message

Examples:
  npm run build && npm run preview
  node scripts/export-pdf.mjs
  node scripts/export-pdf.mjs --base=http://localhost:4173 --out=slides.pdf --compact`);
  process.exit(0);
}

const BASE = args.base.replace(/\/$/, '');
const OUT = args.out;
const COMPACT = args.compact;
const W = COMPACT ? 1280 : 1920;
const H = COMPACT ? 720 : 1080;

// try/finally over the entire browser lifecycle so an early-throw doesn't leave a zombie
// Chromium process chewing CPU after the script exits.
let browser = null;
try {
  browser = await chromium.launch();
  const context = await browser.newContext({
    viewport: { width: W, height: H },
    // CR-5: match playwright.config's DPR=1 so PDF screenshot matches the visual baseline
    // pixel-for-pixel (no HiDPI upscaling producing a different clip rectangle).
    deviceScaleFactor: 1,
  });
  const page = await context.newPage();

  // 1) read the registry from the running app (single source of truth).
  // Separate the two failure modes: an unreachable server throws here, a missing registry is handled below.
  try {
    await page.goto(`${BASE}/?test=true`, { waitUntil: 'networkidle' });
  } catch {
    throw new Error(`Could not reach the preview server at ${BASE}. Start it first: npm run build && npm run preview (or pass --base/PORT).`);
  }
  const registry = await page.evaluate(() => window.__SLIDE_REGISTRY__ ?? []);
  if (!registry.length) {
    throw new Error('Reached the server but found no window.__SLIDE_REGISTRY__. Call exposeRegistryForTooling() in the app entry.');
  }

  // CR-5: compute the stage clip ONCE (same exact geometry the visual baselines use).
  // Clipping to [data-slide-stage]'s BCR — not the viewport, not fullPage — means:
  //   - letterbox chrome never appears in the PDF (same as the snapshot)
  //   - moving the stage on screen (e.g. a debug banner) doesn't shift the crop
  //   - the export rectangle shares its origin with visual.spec.ts's clip
  const stageLocator = page.locator('[data-slide-stage]');
  const firstBcr = await stageLocator.boundingBox();
  if (!firstBcr) {
    throw new Error('[data-slide-stage] has no bounding box — SlideStage may be missing its data attribute.');
  }
  const clip = { x: firstBcr.x, y: firstBcr.y, width: firstBcr.width, height: firstBcr.height };

  // 2) capture each slide's final beat as a frozen frame
  const shots = [];
  for (const { id, totalBeats } of registry) {
    await page.goto(`${BASE}/?scene=${id}&beat=${totalBeats}&test=true`, { waitUntil: 'networkidle' });
    await page.evaluate(() => document.fonts.ready);
    await freezePage(page);               // CSS + WAAPI + SMIL + media freeze (single source)
    await waitForAnimationsToSettle(page); // wait for spring physics to fully decay
    // CR-5: clip to the same BCR as visual.spec.ts. No fullPage, no mask — clip is the
    // single source of geometric truth.
    const buf = await page.screenshot({ clip });
    shots.push(`data:image/png;base64,${buf.toString('base64')}`);
    console.log(`captured ${id} (beat ${totalBeats})`);
  }

  // 3) put each shot on its own page and print to a multi-page PDF.
  //    The img size matches the clipped stage so there is no stretch, and @page size matches
  //    exactly so printers don't add margins.
  const html = `<!doctype html><meta charset="utf-8"><style>
    @page { size: ${clip.width}px ${clip.height}px; margin: 0; }
    html, body { margin: 0; padding: 0; }
    img { display: block; width: ${clip.width}px; height: ${clip.height}px; page-break-after: always; }
  </style>${shots.map((src) => `<img src="${src}">`).join('')}`;

  await page.setContent(html, { waitUntil: 'networkidle' });
  await page.pdf({ path: OUT, width: `${clip.width}px`, height: `${clip.height}px`, printBackground: true });

  console.log(`wrote ${OUT} (${shots.length} slides)`);
} catch (err) {
  console.error('[export-pdf] ERROR:', err?.message ?? String(err));
  process.exit(1);
} finally {
  if (browser) {
    try { await browser.close(); } catch (_) { /* ignore close errors */ }
  }
}
