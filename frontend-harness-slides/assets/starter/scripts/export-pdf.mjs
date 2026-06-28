#!/usr/bin/env node
// Export the whole deck to a PDF — one page per slide, captured at its final beat as a frozen frame.
// Reads window.__SLIDE_REGISTRY__ from the running app (single source of truth) and reuses the same
// freeze as the visual harness (../harness/freeze.mjs), so the PDF matches what the harness verifies.
//
// Usage:
//   npm run build && npm run preview            # serve the deck (default http://localhost:4173)
//   node scripts/export-pdf.mjs --base http://localhost:4173 --out deck.pdf [--compact]
//
// Prereq: install Playwright's chromium (`npx playwright install chromium`).

import { chromium } from '@playwright/test';
import { FREEZE_CSS, waitForAnimationsToSettle } from '../harness/freeze.mjs';

function arg(name, fallback) {
  const i = process.argv.indexOf(`--${name}`);
  return i !== -1 && process.argv[i + 1] ? process.argv[i + 1] : fallback;
}

const BASE = arg('base', `http://localhost:${process.env.PORT || 4173}`).replace(/\/$/, '');
const OUT = arg('out', 'deck.pdf');
const COMPACT = process.argv.includes('--compact');
const W = COMPACT ? 1280 : 1920;
const H = COMPACT ? 720 : 1080;

const browser = await chromium.launch();
const page = await browser.newPage({ viewport: { width: W, height: H } });

// 1) read the registry from the running app (single source of truth).
// Separate the two failure modes: an unreachable server throws here, a missing registry is handled below.
try {
  await page.goto(`${BASE}/?test=true`, { waitUntil: 'networkidle' });
} catch {
  console.error(`Could not reach the preview server at ${BASE}. Start it first: npm run build && npm run preview (or pass --base/PORT).`);
  await browser.close();
  process.exit(1);
}
const registry = await page.evaluate(() => window.__SLIDE_REGISTRY__ ?? []);
if (!registry.length) {
  console.error('Reached the server but found no window.__SLIDE_REGISTRY__. Call exposeRegistryForTooling() in the app entry.');
  await browser.close();
  process.exit(1);
}

// 2) capture each slide's final beat as a frozen frame
const shots = [];
for (const { id, totalBeats } of registry) {
  await page.goto(`${BASE}/?scene=${id}&beat=${totalBeats}&test=true`, { waitUntil: 'networkidle' });
  await page.evaluate(() => document.fonts.ready);
  await page.addStyleTag({ content: FREEZE_CSS });
  await waitForAnimationsToSettle(page);
  const buf = await page.screenshot({ fullPage: false });
  shots.push(`data:image/png;base64,${buf.toString('base64')}`);
  console.log(`captured ${id} (beat ${totalBeats})`);
}

// 3) put each shot on its own page and print to a multi-page PDF
const html = `<!doctype html><meta charset="utf-8"><style>
  @page { size: ${W}px ${H}px; margin: 0; }
  html, body { margin: 0; padding: 0; }
  img { display: block; width: ${W}px; height: ${H}px; page-break-after: always; }
</style>${shots.map((src) => `<img src="${src}">`).join('')}`;

await page.setContent(html, { waitUntil: 'networkidle' });
await page.pdf({ path: OUT, width: `${W}px`, height: `${H}px`, printBackground: true });

await browser.close();
console.log(`wrote ${OUT} (${shots.length} slides)`);
