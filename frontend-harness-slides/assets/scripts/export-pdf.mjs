#!/usr/bin/env node
// ==========================================
// 💡 export-pdf.mjs — export the whole deck to a PDF (one page per slide, final-beat frozen frame)
// ==========================================
//
// Reads window.__SLIDE_REGISTRY__ from the running app as the single source of truth, so it covers
// every slide automatically — no separate slide list to maintain. Each page is captured with
// ?test=true (a frozen frame), so the exported PDF matches what the harness verifies.
//
// Usage:
//   node assets/scripts/export-pdf.mjs --base http://localhost:4173 --out deck.pdf [--compact]
//
// Prereq: build and serve the deck first (e.g. `npm run build && npm run preview`),
// and install Playwright's chromium (`npx playwright install chromium`).

import { chromium } from '@playwright/test';

function arg(name, fallback) {
  const i = process.argv.indexOf(`--${name}`);
  return i !== -1 && process.argv[i + 1] ? process.argv[i + 1] : fallback;
}

const BASE = arg('base', 'http://localhost:4173').replace(/\/$/, '');
const OUT = arg('out', 'deck.pdf');
const COMPACT = process.argv.includes('--compact');
const W = COMPACT ? 1280 : 1920;
const H = COMPACT ? 720 : 1080;

// Same freeze as visual.spec: pause continuous animations, zero transitions, lock the first frame.
const FREEZE_CSS = `
  *, *::before, *::after {
    animation-play-state: paused !important;
    transition-delay: 0s !important;
    transition-duration: 0s !important;
  }
`;

const browser = await chromium.launch();
const page = await browser.newPage({ viewport: { width: W, height: H } });

// 1) read the registry from the running app (single source of truth)
await page.goto(`${BASE}/?test=true`, { waitUntil: 'networkidle' });
const registry = await page.evaluate(() => window.__SLIDE_REGISTRY__ ?? []);
if (!registry.length) {
  console.error('No window.__SLIDE_REGISTRY__ found. Call exposeRegistryForTooling() and start the preview server first.');
  await browser.close();
  process.exit(1);
}

// 2) capture each slide's final beat as a frozen frame
const shots = [];
for (const { id, totalBeats } of registry) {
  await page.goto(`${BASE}/?scene=${id}&beat=${totalBeats}&test=true`, { waitUntil: 'networkidle' });
  await page.evaluate(() => document.fonts.ready);
  await page.addStyleTag({ content: FREEZE_CSS });
  await page.waitForTimeout(150); // let Framer Motion spring physics settle
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
