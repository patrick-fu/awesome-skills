// Single source of the freeze mechanism. Imported by tests/visual.spec.ts (the pixel harness) and
// scripts/export-pdf.mjs (the exporter) so both freeze frames identically — change it once, here.
//
// CRITICAL: this file is a plain .mjs consumed both by Playwright (evaluate(...)) and by Node
// (scripts/export-pdf.mjs imports it). Do NOT use TypeScript syntax anywhere (no `as`, no `: Type`,
// no generics, no `satisfies`). Keep it runtime-valid in both engines.

// H-7 FIXED:
//   • Drop `animation-delay: 0s !important` — clobbers negative phase pins
//     (e.g. `animation-delay: -1.2s` to start mid-marquee). force-fill/playState still freezes.
//   • Use single `transition: none !important` instead of duration/delay = 0 — cleaner.
//   • Expanded selector set: SVG leaves (path/rect/circle/.../g/text), media, tables, form
//     controls. Pairs with the H-6 sampler expansion in waitForAnimationsToSettle below.
export const FREEZE_CSS = `
*,
*::before,
*::after,
div, span, p, h1, h2, h3, h4, h5, h6, img, li, button, a, label,
table, thead, tbody, tr, th, td, caption, colgroup,
video, audio, canvas, iframe, picture, source,
input, select, option, textarea, optgroup, fieldset, legend,
svg, path, rect, circle, ellipse, polygon, polyline, line, g, text, tspan, textPath,
defs, mask, clipPath, pattern, linearGradient, radialGradient, stop,
use, symbol, switch, foreignObject, image {
  transition: none !important;
  animation-play-state: paused !important;
  animation-fill-mode: both !important;
}
html { scroll-behavior: auto !important; }
`;

// H-8: mask selectors — always co-masked in visual.spec.ts and export-pdf.mjs. Keeping the
// constants here means callers never drift apart on what counts as non-deterministic.
export const VISUAL_MASK_SELECTORS = [
  'canvas',          // rAF-driven paint loops
  'video',           // poster / currentTime is network-timing dependent
  'iframe',          // cross-origin content is out of our control
  'lottie-player',   // 3rd-party animation player
  'model-viewer',    // WebGL 3D renders are GPU/driver dependent
  '[data-visual-mask]', // escape hatch: authors can mark any element explicitly
];

// Imperative freeze — covers what CSS can't reach:
//   1) Web Animations API (framer-motion on the JS pipeline, element.animate())
//   2) SVG SMIL <animate>/<animateTransform>/<animateMotion>/<set>
//   3) Media playback (video/audio currentTime advance)
export async function freezeImperative(page) {
  await page.evaluate(() => {
    // 1) WAAPI / CSSOM animations. Pause at currentTime, NOT endTime — a "pin to phase"
    //    animation is authored to look exactly where it is.
    try {
      var docAny = document;
      var allAnims = typeof docAny.getAnimations === 'function'
        ? docAny.getAnimations()
        : [];
      for (var i = 0; i < allAnims.length; i++) {
        try { allAnims[i].pause(); } catch (_) { /* ignore */ }
      }
    } catch (_) { /* old browser / no getAnimations — CSS rule above still covers CSS anims */ }

    // 2) SMIL / SVG time-based animations. endElement() + pauseAnimations() freeze at current state.
    try {
      var smilSel = 'animate, animateTransform, animateMotion, animateColor, set, animateMotion';
      var smilNodes = document.querySelectorAll(smilSel);
      for (var j = 0; j < smilNodes.length; j++) {
        var n = smilNodes[j];
        try { if (typeof n.endElement === 'function') n.endElement(); } catch (_) {}
        try { if (typeof n.pauseAnimations === 'function') n.pauseAnimations(); } catch (_) {}
      }
      var svgs = document.querySelectorAll('svg');
      for (var k = 0; k < svgs.length; k++) {
        try { if (typeof svgs[k].pauseAnimations === 'function') svgs[k].pauseAnimations(); } catch (_) {}
      }
    } catch (_) { /* SVG 1.1 Full API unavailable — ignore */ }

    // 3) Media — pause at whatever the current playback head is, so poster matches between runs.
    try {
      var medias = document.querySelectorAll('video, audio');
      for (var m = 0; m < medias.length; m++) {
        var media = medias[m];
        if (!media.paused) { try { media.pause(); } catch (_) {} }
      }
    } catch (_) { /* CORS media / blocked autoplay — ignore */ }
  });
}

// H-7: N consecutive identical visual samples → page is physically at rest.
// H-8 FIXED: stableRounds = 3 (not 1). Springs can cross zero velocity mid-travel and produce
// a coincident "equal sample"; three rounds at 50ms = 150ms of identical visuals means settled.
// Also: H-6 expanded selector set, broader sampled attrs (transform/filter/strokeDash*).
export async function waitForAnimationsToSettle(page, opts) {
  var samples = opts && opts.samples != null ? opts.samples : 30;
  var intervalMs = opts && opts.intervalMs != null ? opts.intervalMs : 50;
  var stableRounds = opts && opts.stableRounds != null ? opts.stableRounds : 3;
  var SELECTOR =
    'div, span, p, h1, h2, h3, h4, h5, h6, img, li, button, a, label, ' +
    'svg, path, rect, circle, ellipse, polygon, polyline, line, g, text, tspan, ' +
    'table, thead, tbody, tr, th, td, video, audio, canvas, iframe, input, select, ' +
    'textarea, fieldset, form, picture, figure, figcaption, section, article, aside, ' +
    'header, footer, nav, main';

  var history = [];
  for (var i = 0; i < samples; i++) {
    var current = await page.evaluate(function (sel) {
      var els = document.querySelectorAll(sel);
      var parts = new Array(els.length);
      for (var j = 0; j < els.length; j++) {
        var el = els[j];
        var r = el.getBoundingClientRect();
        var s = window.getComputedStyle(el);
        parts[j] =
          r.top + ',' + r.left + ',' + r.width + ',' + r.height + ',' +
          s.opacity + ',' + s.transform + ',' + s.filter + ',' +
          s.strokeDashoffset + ',' + s.strokeDasharray;
      }
      return parts.join('|');
    }, SELECTOR);
    history.push(current);
    if (history.length > stableRounds) history.shift();
    if (history.length === stableRounds) {
      var allEqual = true;
      for (var h = 1; h < history.length && allEqual; h++) {
        if (history[h] !== history[0]) allEqual = false;
      }
      if (allEqual) return { ok: true, polls: i + 1, stableForMs: stableRounds * intervalMs };
    }
    await page.waitForTimeout(intervalMs);
  }
  return { ok: false, polls: samples, stableForMs: 0, reason: 'exceeded sample budget' };
}

// Orchestration wrapper used by export-pdf.mjs (and a shorthand for visual.spec.ts).
// Returns summary so callers can decide whether to warn / fail on non-settle.
export async function freezePage(page, opts) {
  // 1. Inject CSS freeze. addStyleTag({ content }) is synchronous on commit.
  try {
    await page.addStyleTag({ content: FREEZE_CSS });
  } catch (_) { /* page might have no head yet — fall through to imperatives below */ }

  // 2. WAAPI / SMIL / media imperative freeze.
  await freezeImperative(page);

  // 3. Wait for N consecutive identical samples. If the starter has no animations, this
  //    returns in ~3 × intervalMs (~150ms) — essentially free.
  var settle = await waitForAnimationsToSettle(page, opts || {});
  return settle;
}

// Page.addInitScript() form — dumped as a pre-stringified IIFE so export-pdf.mjs / CI code
// can dump it into a new page context without re-assembling the CSS constant.
export const STYLE_INJECT_SCRIPT =
  "(function(){var s=document.createElement('style');s.setAttribute('data-freeze','true');s.textContent=" +
  JSON.stringify(FREEZE_CSS) +
  ";var a=function(){(document.head||document.documentElement).appendChild(s);};if(document.head)a();else document.addEventListener('DOMContentLoaded',a,{once:true});})();";
