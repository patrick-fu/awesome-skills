// Single source of the freeze mechanism. Imported by tests/visual.spec.ts (the pixel harness) and
// scripts/export-pdf.mjs (the exporter) so both freeze frames identically — change it once, here.
//
// CRITICAL: this file is a plain .mjs consumed both by Playwright (evaluate(...)) and by Node
// (scripts/export-pdf.mjs imports it). Do NOT use TypeScript syntax anywhere (no `as`, no `: Type`,
// no generics, no `satisfies`). Keep it runtime-valid in both engines.

// P0-10a FIXED: 冻结所有动画/过渡。三管齐下：
//   1) 全局 * 级联：强制 paused + animation:none + transition 清零
//   2) 媒体 / canvas / iframe 显式暂停
//   3) SVG SMIL 节点 display:none（彻底干掉 timeline）
//   同时保留 animation-fill-mode:both，避免负 phase 的动画跳回第一帧。
export const FREEZE_CSS = `
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

// P0-10d FIXED: 所有视觉回归测试 / PDF 导出中需要 mask 的非确定性元素。
// 单一来源，确保 visual.spec.ts、export-pdf.mjs、任何下游消费者永远对齐。
// .non-deterministic 是通用类名，让作者自行标记。
export const VISUAL_MASK_SELECTORS = [
  'canvas',
  'iframe',
  'video',
  '.non-deterministic',
  '[data-visual-mask]',
];

// P0-10a FIXED (freezeImperative): 覆盖 CSS 触碰不到的部分。
//   1) WAAPI/CSSOM: getAnimations() — 先 pause()，失败则 cancel()
//   2) SVG SMIL: endElement() + 单节点 pauseAnimations + 各 <svg> pauseAnimations + document.pauseAnimations()
//   3) Media: pause() + currentTime = 0（让 poster 帧在多次运行之间保持一致）
export async function freezeImperative(page) {
  await page.evaluate(() => {
    // 1) Web Animations API
    try {
      var docAny = document;
      var allAnims = typeof docAny.getAnimations === 'function'
        ? docAny.getAnimations({ subtree: true })
        : [];
      for (var i = 0; i < allAnims.length; i++) {
        var anim = allAnims[i];
        try { anim.pause(); } catch (_) {
          try { anim.cancel(); } catch (_e) { /* swallow */ }
        }
      }
    } catch (_) { /* old browser / no getAnimations — FREEZE_CSS still covers CSS anims */ }

    // 2) SVG SMIL
    try {
      var smilSel = 'animate, animateTransform, animateMotion, animateColor, set';
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
      // P0-10a FIXED: 全局 SMIL 时间轴冻结
      try { if (typeof document.pauseAnimations === 'function') document.pauseAnimations(); } catch (_) {}
    } catch (_) { /* SVG 1.1 Full API 不可用 — 忽略 */ }

    // 3) Media (video/audio) — 固定到 0 帧 / poster
    try {
      var medias = document.querySelectorAll('video, audio');
      for (var m = 0; m < medias.length; m++) {
        var media = medias[m];
        try { if (!media.paused) media.pause(); } catch (_) {}
        try { media.currentTime = 0; } catch (_) { /* CORS taint / live stream */ }
      }
    } catch (_) { /* CORS media / blocked autoplay — 忽略 */ }
  });
}

// P0-10b FIXED: 等待页面动画完全稳定。
// SETTLE_SELECTOR 包含 60 个常见 DOM 标签（全覆盖 layout / paint 可能会变的节点类型），
// 连续 stableRounds=3 次采样完全相同才算稳定（避免弹簧物理 mid-travel 假阳性）。
export async function waitForAnimationsToSettle(page, opts) {
  var samples = opts && opts.samples != null ? opts.samples : 30;
  var intervalMs = opts && opts.intervalMs != null ? opts.intervalMs : 50;
  var stableRounds = opts && opts.stableRounds != null ? opts.stableRounds : 3;

  // P0-10b FIXED: 60 个标签的 SETTLE_SELECTOR（单一来源，顺序无关）
  var SETTLE_SELECTOR = [
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
    }, SETTLE_SELECTOR);
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

// P0-10c FIXED: freezePage — 统一入口。
//   1) 注入 FREEZE_CSS
//   2) 调 freezeImperative (WAAPI + SMIL + media)
//   3) 捕获所有 <canvas> 的像素内容为 dataURL，写入 dataset.__frozenUrl，
//      让 CORS tainted / rAF 驱动的 canvas 在截图时保持同帧。
export async function freezePage(page, opts) {
  // 1. 注入 CSS freeze
  try {
    await page.addStyleTag({ content: FREEZE_CSS });
  } catch (_) { /* page 可能还没有 head，继续走 imperative */ }

  // 2. Imperative 冻结
  await freezeImperative(page);

  // 3. Canvas 像素快照（P0-10c FIXED）
  try {
    await page.evaluate(() => {
      var canvases = document.querySelectorAll('canvas');
      for (var c = 0; c < canvases.length; c++) {
        var canvas = canvases[c];
        try {
          var url = canvas.toDataURL('image/png');
          canvas.setAttribute('data-__frozenUrl', url);
        } catch (_) { /* CORS tainted canvas — 跳过 */ }
      }
    });
  } catch (_) { /* evaluate 可能在异常页面失败 */ }

  // 4. 等稳定（带可配置选项）
  var settle = await waitForAnimationsToSettle(page, opts || {});
  return settle;
}

// Page.addInitScript() 形态 — 预字符串化的 IIFE，方便 CI / 外部脚本直接 dump。
export const STYLE_INJECT_SCRIPT =
  "(function(){var s=document.createElement('style');s.setAttribute('data-freeze','true');s.textContent=" +
  JSON.stringify(FREEZE_CSS) +
  ";var a=function(){(document.head||document.documentElement).appendChild(s);};if(document.head)a();else document.addEventListener('DOMContentLoaded',a,{once:true});})();";
