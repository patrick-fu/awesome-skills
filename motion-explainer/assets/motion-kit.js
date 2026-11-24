// Motion Explainer Shared Deterministic Motion Kit (inlined via motion-explainer-kit placeholder)
(function initMotionKit(global) {
  'use strict';

  const STAGE_WIDTH = 1280;
  const STAGE_HEIGHT = 720;

  function clamp(value, min = 0, max = 1) {
    if (!Number.isFinite(value)) return min;
    return Math.max(min, Math.min(max, value));
  }

  function mix(a, b, t) {
    return a + (b - a) * t;
  }

  function easeOutCubic(t) {
    const x = clamp(t);
    return 1 - (1 - x) ** 3;
  }

  function easeInOutCubic(t) {
    const x = clamp(t);
    return x < 0.5 ? 4 * x * x * x : 1 - ((-2 * x + 2) ** 3) / 2;
  }

  function element(tag, className, text) {
    const node = document.createElement(tag);
    if (className) node.className = className;
    if (text !== undefined) node.textContent = text;
    return node;
  }

  /**
   * Closed-form harmonic spring (underdamped, critically damped, or overdamped).
   * Pure function of elapsed `age` in seconds; safe for forward and reverse seek().
   */
  function springState(age, options = {}) {
    const {
      stiffness = 220,
      damping = 18,
      mass = 1,
      velocity = 0,
      from = 0,
      to = 1,
      settled = false,
      restDelta = 1e-4,
    } = options;
    const span = to - from;
    if (settled) return { value: to, velocity: 0, done: true };
    if (!Number.isFinite(age) || age <= 0) return { value: from, velocity, done: false };
    if (span === 0) return { value: to, velocity: 0, done: true };

    const k = Math.max(1e-3, stiffness);
    const m = Math.max(1e-3, mass);
    const c = Math.max(0, damping);
    const w0 = Math.sqrt(k / m);
    const zeta = c / (2 * Math.sqrt(k * m));
    const x0 = -1;
    const v0 = velocity / span;

    let x;
    let dx;
    if (zeta < 1 - 1e-6) {
      const wd = w0 * Math.sqrt(1 - zeta * zeta);
      const decay = Math.exp(-zeta * w0 * age);
      if (decay < restDelta) return { value: to, velocity: 0, done: true };
      const cos = Math.cos(wd * age);
      const sin = Math.sin(wd * age);
      const b = (v0 + zeta * w0 * x0) / wd;
      x = decay * (x0 * cos + b * sin);
      dx = decay * ((-zeta * w0 * x0 + wd * b) * cos - (zeta * w0 * b + wd * x0) * sin);
    } else if (zeta <= 1 + 1e-6) {
      const decay = Math.exp(-w0 * age);
      if (decay * (1 + w0 * age) < restDelta) return { value: to, velocity: 0, done: true };
      const b = v0 + w0 * x0;
      x = decay * (x0 + b * age);
      dx = decay * (b - w0 * (x0 + b * age));
    } else {
      const root = Math.sqrt(zeta * zeta - 1);
      const r1 = -w0 * (zeta - root);
      const r2 = -w0 * (zeta + root);
      const c1 = (v0 - r2 * x0) / (r1 - r2);
      const c2 = x0 - c1;
      const e1 = Math.exp(r1 * age);
      const e2 = Math.exp(r2 * age);
      x = c1 * e1 + c2 * e2;
      dx = c1 * r1 * e1 + c2 * r2 * e2;
      if (Math.abs(x) < restDelta && Math.abs(dx) < restDelta) {
        return { value: to, velocity: 0, done: true };
      }
    }

    const progress = 1 + x;
    return { value: from + span * progress, velocity: span * dx, done: false };
  }

  function spring(age, options = {}) {
    return springState(age, options).value;
  }

  /**
   * Volume-preserving impact squash-and-stretch recoil.
   */
  function impact(age, options = {}) {
    const {
      intensity = 0.22,
      frequency = 16,
      damping = 7.5,
      axis = 'y',
      offset = 8,
      settled = false,
    } = options;
    if (settled || !Number.isFinite(age) || age <= 0) {
      return { scaleX: 1, scaleY: 1, offsetX: 0, offsetY: 0, energy: 0, transform: 'scale(1, 1)' };
    }
    const env = Math.exp(-damping * age);
    if (env < 1e-4) {
      return { scaleX: 1, scaleY: 1, offsetX: 0, offsetY: 0, energy: 0, transform: 'scale(1, 1)' };
    }
    const amp = clamp(intensity, 0, 0.48);
    const wave = amp * env * Math.sin(frequency * age);
    let scaleX = 1;
    let scaleY = 1;
    let offsetX = 0;
    let offsetY = 0;
    if (axis === 'x') {
      scaleX = clamp(1 - wave, 0.55, 1.55);
      scaleY = 1 / scaleX;
      offsetX = wave * offset;
    } else {
      scaleY = clamp(1 - wave, 0.55, 1.55);
      scaleX = 1 / scaleY;
      offsetY = wave * offset;
    }
    return {
      scaleX,
      scaleY,
      offsetX,
      offsetY,
      energy: Math.abs(wave),
      transform: `translate(${offsetX.toFixed(2)}px, ${offsetY.toFixed(2)}px) scale(${scaleX.toFixed(4)}, ${scaleY.toFixed(4)})`,
    };
  }

  /**
   * Velocity-aligned directional smear / capsule stretch.
   */
  function smear(vx, vy, options = {}) {
    const {
      strength = 0.00045,
      maxStretch = 0.55,
      settled = false,
    } = options;
    const speed = settled || !Number.isFinite(vx) || !Number.isFinite(vy) ? 0 : Math.hypot(vx, vy);
    if (speed < 1e-3) {
      return { angle: 0, stretch: 1, squash: 1, speed: 0, transform: '', capsuleTransform: '' };
    }
    const amount = Math.min(Math.max(0, maxStretch), speed * Math.max(0, strength));
    const stretch = 1 + amount;
    const squash = 1 / Math.sqrt(stretch);
    const angle = Math.atan2(vy, vx) * (180 / Math.PI);
    const a = angle.toFixed(2);
    const sx = stretch.toFixed(4);
    const sy = squash.toFixed(4);
    return {
      angle,
      stretch,
      squash,
      speed,
      transform: `rotate(${a}deg) scale(${sx}, ${sy}) rotate(${(-angle).toFixed(2)}deg)`,
      capsuleTransform: `rotate(${a}deg) scale(${sx}, ${sy})`,
    };
  }

  /**
   * 2.5D orthographic spherical eye/gaze projection (opt-in vitality for any subject).
   */
  function sphereEyes(yaw = 0, pitch = 0, options = {}) {
    const {
      radius = 40,
      eyeSpacing = 22,
      eyeY = -4,
      maxAngle = 55,
      radians = false,
    } = options;
    const toRad = radians ? 1 : Math.PI / 180;
    const limit = maxAngle * toRad;
    const theta = clamp(yaw * toRad, -limit, limit);
    const phi = clamp(pitch * toRad, -limit * 0.75, limit * 0.75);
    const delta = Math.asin(clamp(eyeSpacing / (2 * Math.max(1, radius)), 0, 0.85));
    const phiBase = Math.asin(clamp(eyeY / Math.max(1, radius), -0.7, 0.7));
    const phiTotal = clamp(phiBase + phi, -Math.PI * 0.45, Math.PI * 0.45);

    function project(angleOffset) {
      const alpha = theta + angleOffset;
      const cosPhi = Math.cos(phiTotal);
      const x = radius * cosPhi * Math.sin(alpha);
      const y = radius * Math.sin(phiTotal);
      const z = cosPhi * Math.cos(alpha);
      return {
        x,
        y,
        z,
        scaleX: Math.max(0.2, Math.cos(alpha)),
        scaleY: Math.max(0.35, Math.cos(phiTotal)),
        visible: z > 0.05,
      };
    }

    return {
      left: project(-delta),
      right: project(delta),
      center: {
        x: radius * Math.cos(phi) * Math.sin(theta),
        y: radius * Math.sin(phi),
        z: Math.cos(phi) * Math.cos(theta),
      },
    };
  }

  /**
   * Living-sentence inline elastic slot expansion that pushes sibling words apart.
   */
  function inlineSlot(age, options = {}) {
    const {
      targetWidth = 120,
      pad = 0,
      duration = 0.45,
      stiffness = 240,
      damping = 19,
      settled = false,
    } = options;
    const raw = settled ? 1 : (age <= 0 ? 0 : spring(age, { stiffness, damping, settled: false }));
    const width = Math.max(0, raw * (targetWidth + pad));
    const opacity = settled ? 1 : clamp(age / Math.max(0.05, duration * 0.45));
    const scale = Math.max(0.01, raw);
    return {
      progress: raw,
      width,
      opacity,
      scale,
      style: {
        width: `${width.toFixed(2)}px`,
        opacity: opacity.toFixed(3),
        transform: `scale(${scale.toFixed(4)})`,
      },
    };
  }

  /**
   * Directional CSS clip-path mask wipe for in-place content swaps.
   */
  function wipeClip(age, options = {}) {
    const {
      duration = 0.42,
      direction = 'left-to-right',
      ease = easeInOutCubic,
      settled = false,
    } = options;
    const p = settled ? 1 : ease(clamp(age / Math.max(1e-3, duration)));
    const rem = ((1 - p) * 100).toFixed(2);
    const done = (p * 100).toFixed(2);
    let incomingClip;
    let outgoingClip;
    if (direction === 'right-to-left') {
      incomingClip = `inset(0 0 0 ${rem}%)`;
      outgoingClip = `inset(0 ${done}% 0 0)`;
    } else if (direction === 'top-to-bottom') {
      incomingClip = `inset(0 0 ${rem}% 0)`;
      outgoingClip = `inset(${done}% 0 0 0)`;
    } else if (direction === 'bottom-to-top') {
      incomingClip = `inset(${rem}% 0 0 0)`;
      outgoingClip = `inset(0 0 ${done}% 0)`;
    } else {
      incomingClip = `inset(0 ${rem}% 0 0)`;
      outgoingClip = `inset(0 0 0 ${done}%)`;
    }
    return { progress: p, clipPath: incomingClip, incomingClip, outgoingClip };
  }

  /**
   * Single-edge anchored pill / bubble morph (e.g. tool call or chat stream expansion).
   */
  function pillMorph(age, options = {}) {
    const {
      fromWidth = 48,
      toWidth = 280,
      fromHeight,
      toHeight,
      anchor = 'left',
      stiffness = 220,
      damping = 20,
      settled = false,
    } = options;
    const p = spring(age, { stiffness, damping, settled });
    const width = Math.max(1, mix(fromWidth, toWidth, p));
    const height = fromHeight !== undefined && toHeight !== undefined
      ? Math.max(1, mix(fromHeight, toHeight, p))
      : undefined;
    const contentOpacity = settled ? 1 : clamp((p - 0.35) / 0.55);
    const transformOrigin = anchor === 'right'
      ? 'right center'
      : anchor === 'center'
        ? 'center center'
        : 'left center';
    return { progress: p, width, height, contentOpacity, transformOrigin };
  }

  /**
   * Virtual 2D camera push/pan/rotate over a 1280x720 stage.
   */
  function camera(keyframes, seconds, options = {}) {
    const {
      stageWidth = STAGE_WIDTH,
      stageHeight = STAGE_HEIGHT,
      settled = false,
    } = options;
    const cx = stageWidth / 2;
    const cy = stageHeight / 2;
    const fallback = { x: cx, y: cy, zoom: 1, rotate: 0 };
    if (!Array.isArray(keyframes) || !keyframes.length) {
      return { ...fallback, transform: 'translate(0px, 0px) scale(1)', transformOrigin: '0 0' };
    }
    const frames = keyframes
      .map(kf => ({
        t: Number(kf.t ?? 0),
        x: kf.x ?? cx,
        y: kf.y ?? cy,
        zoom: kf.zoom ?? 1,
        rotate: kf.rotate ?? 0,
        ease: kf.ease,
        spring: kf.spring,
      }))
      .sort((a, b) => a.t - b.t);

    let state;
    if (seconds <= frames[0].t) {
      state = frames[0];
    } else if (seconds >= frames.at(-1).t) {
      state = frames.at(-1);
    } else {
      let idx = 0;
      for (let i = 0; i < frames.length - 1; i++) {
        if (seconds >= frames[i].t && seconds < frames[i + 1].t) {
          idx = i;
          break;
        }
      }
      const prev = frames[idx];
      const next = frames[idx + 1];
      if (settled) {
        state = prev;
      } else {
        const span = Math.max(1e-6, next.t - prev.t);
        const local = seconds - prev.t;
        const t = next.spring
          ? spring(local, typeof next.spring === 'object' ? { ...next.spring, settled: false } : {})
          : (next.ease || easeInOutCubic)(clamp(local / span));
        state = {
          x: mix(prev.x, next.x, t),
          y: mix(prev.y, next.y, t),
          zoom: Math.max(0.05, mix(prev.zoom, next.zoom, t)),
          rotate: mix(prev.rotate, next.rotate, t),
        };
      }
    }

    const rot = Math.abs(state.rotate) > 1e-4 ? ` rotate(${state.rotate.toFixed(3)}deg)` : '';
    const transform = `translate(${cx.toFixed(2)}px, ${cy.toFixed(2)}px) scale(${state.zoom.toFixed(4)})${rot} translate(${(-state.x).toFixed(2)}px, ${(-state.y).toFixed(2)}px)`;
    return {
      x: state.x,
      y: state.y,
      zoom: state.zoom,
      rotate: state.rotate,
      transform,
      transformOrigin: '0 0',
    };
  }

  /**
   * Deterministic blink & subtle breathing oscillation (zero Math.random()).
   */
  function deterministicBlink(seconds, options = {}) {
    const {
      interval = 3.6,
      blinkDuration = 0.14,
      seed = 0,
      doubleBlinkEvery = 3,
      breathPeriod = 2.8,
      settled = false,
    } = options;
    if (settled || !Number.isFinite(seconds)) {
      return { open: 1, scaleY: 1, closed: false, breath: 0, bobY: 0 };
    }
    const safeInterval = Math.max(0.5, interval);
    const dur = clamp(blinkDuration, 0.04, safeInterval * 0.4);
    const shifted = Math.max(0, seconds + seed);
    const cycle = Math.floor(shifted / safeInterval);
    const phase = shifted - cycle * safeInterval;
    const hash = Math.sin((cycle + 1 + seed * 13.37) * 78.233) * 43758.5453;
    const jitter = hash - Math.floor(hash);
    const firstStart = safeInterval * (0.28 + jitter * 0.44);

    function blinkEnvelope(start) {
      if (phase < start || phase > start + dur) return 1;
      const u = (phase - start) / dur;
      return 1 - 0.92 * Math.sin(u * Math.PI);
    }

    let open = blinkEnvelope(firstStart);
    if (doubleBlinkEvery > 0 && cycle % doubleBlinkEvery === 0) {
      const secondStart = firstStart + dur + 0.09;
      if (secondStart + dur < safeInterval) {
        open = Math.min(open, blinkEnvelope(secondStart));
      }
    }
    const breath = Math.sin((shifted / Math.max(0.2, breathPeriod)) * Math.PI * 2);
    return { open, scaleY: open, closed: open < 0.25, breath, bobY: breath * 2.5 };
  }

  function resolveNode(target, fallbackSelector) {
    if (target instanceof Element) return target;
    if (typeof target === 'string') return document.querySelector(target);
    return fallbackSelector ? document.querySelector(fallbackSelector) : null;
  }

  /**
   * Engineering shell encapsulating 1280x720 scaling, karaoke word-synced caption
   * pagination (sentence/punctuation priority + font-load reflow), progress bar,
   * and multi-page audit() overflow/clipping/caption-overlap guardrails.
   */
  function createPlayerShell(config = {}) {
    const stage = resolveNode(config.stage, '#stage');
    const caption = resolveNode(config.caption, '#caption');
    const progressEl = resolveNode(config.progress, '#progress');
    const auditSelector = config.auditSelector ?? 'h1,.support,.node,.code-line,[data-audit]';
    const titleSelector = config.titleSelector ?? 'h1,[data-title]';
    const requireTitle = config.requireTitle !== false;
    const captionClearance = config.captionClearance ?? 16;

    let storyboard = null;
    let timeline = [];
    let scenes = [];
    let visualTracks = [];
    let cueTracks = [];
    let captionBeat = -1;
    let captionNodes = [];
    let captionPages = [];
    let captionPage = -1;

    function resolveAuditRoot() {
      if (config.auditRoot) return resolveNode(config.auditRoot);
      return document.querySelector('#front') || stage;
    }

    function paginateCaption(beatIndex, beat, words) {
      if (!caption) return;
      caption.replaceChildren();
      captionPages = [];
      captionPage = -1;
      if (words?.length) {
        captionNodes = words.map(word => element('span', 'caption-word', word.text));
        const limit = parseFloat(getComputedStyle(caption).maxHeight);
        const hasLimit = Number.isFinite(limit) && limit > 0;
        let start = 0;
        captionNodes.forEach((node, i) => {
          caption.append(node);
          while (hasLimit && i > start && caption.scrollHeight > limit + 1) {
            const candidates = captionNodes.slice(start, i);
            let boundary = candidates.findLastIndex(
              previous => /[。！？!?；;][”’」』）)\]]*\s*$|\.\s+$/.test(previous.textContent)
            );
            if (boundary < 0) {
              boundary = candidates.findLastIndex(
                previous => /[，,、：:]\s*$/.test(previous.textContent)
              );
            }
            const end = boundary < 0 ? i : start + boundary + 1;
            captionPages.push([start, end]);
            caption.replaceChildren(...captionNodes.slice(end, i + 1));
            start = end;
          }
        });
        captionPages.push([start, words.length]);
      } else {
        captionNodes = [];
        caption.textContent = beat.narration;
      }
      captionBeat = beatIndex;
    }

    function updateCaption(beatIndex, beat, words, time, settled) {
      if (!caption) return;
      if (captionBeat !== beatIndex) {
        paginateCaption(beatIndex, beat, words);
      }
      if (words?.length) {
        const local = time - beat.start;
        const page = settled
          ? captionPages.length - 1
          : Math.max(0, captionPages.findLastIndex(([start]) => local >= words[start].start));
        const [start, end] = captionPages[page];
        if (captionPage !== page) {
          caption.replaceChildren(...captionNodes.slice(start, end));
          captionPage = page;
        }
        for (let i = start; i < end; i++) {
          captionNodes[i].classList.toggle('said', settled || local >= words[i].end);
          captionNodes[i].classList.toggle('now', !settled && local >= words[i].start && local < words[i].end);
        }
      }
    }

    const controller = {
      load(data) {
        storyboard = data.storyboard;
        timeline = data.timeline;
        visualTracks = timeline.map(beat => {
          const source = storyboard.scenes[beat.scene].beats[beat.beat];
          const track = [{ start: beat.start, focus: beat.focus || [], show: beat.show }];
          for (const cue of source.cues || []) {
            if (cue.focus !== undefined || cue.show !== undefined) {
              track.push({ ...track.at(-1), ...cue, start: beat.start + cue.start });
            }
          }
          return track;
        });
        cueTracks = timeline.map(beat => {
          const source = storyboard.scenes[beat.scene].beats[beat.beat];
          const base = {
            start: beat.start,
            end: beat.start,
            focus: beat.focus || [],
            show: beat.show,
            cue: null,
          };
          const track = [base];
          for (const cue of source.cues || []) {
            const absStart = beat.start + cue.start;
            const absEnd = beat.start + cue.end;
            track.push({
              ...track.at(-1),
              ...cue,
              start: absStart,
              end: absEnd,
              cue: { ...cue, start: absStart, end: absEnd, localStart: cue.start, localEnd: cue.end },
            });
          }
          return track;
        });
        captionBeat = -1;
        scenes = storyboard.scenes.map((scene, i) => {
          const beats = timeline.filter(beat => beat.scene === i);
          return { index: i, id: scene.id, start: beats[0].start, end: beats.at(-1).end, beats };
        });
        document.title = storyboard.title;
        document.documentElement.lang = storyboard.language || 'zh-CN';
        if (stage) {
          stage.style.transform = `scale(${data.width / STAGE_WIDTH})`;
        }
        if (typeof config.onLoad === 'function') {
          config.onLoad({ storyboard, timeline, scenes, visualTracks, cueTracks, width: data.width, stage, caption });
        }
        controller.seek(0, true);
        captionBeat = -1;
      },

      seek(seconds, settled = false) {
        const total = timeline.at(-1).end;
        const time = Math.max(0, Math.min(seconds, total));
        const found = timeline.findIndex(beat => time < beat.end);
        const beatIndex = found < 0 ? timeline.length - 1 : found;
        const beat = timeline[beatIndex];
        const scene = storyboard.scenes[beat.scene];
        const beatSource = scene.beats[beat.beat];
        const sceneMeta = scenes[beat.scene];
        const vTrack = visualTracks[beatIndex];
        const cTrack = cueTracks[beatIndex];
        const cueIndex = settled
          ? cTrack.length - 1
          : Math.max(0, cTrack.findLastIndex(entry => time >= entry.start));
        const activeState = cTrack[cueIndex];
        const triggeredCues = cTrack.slice(1, cueIndex + 1).map(entry => entry.cue);

        if (typeof config.onSeek === 'function') {
          config.onSeek({
            seconds,
            time,
            settled,
            beatIndex,
            beat,
            beatSource,
            sceneIndex: beat.scene,
            scene,
            sceneMeta,
            sceneAge: Math.max(0, time - sceneMeta.start),
            beatAge: Math.max(0, time - beat.start),
            visualTrack: vTrack,
            visualTracks,
            cueTrack: cTrack,
            cueTracks,
            cueIndex,
            activeCue: activeState.cue,
            activeState,
            triggeredCues,
            storyboard,
            timeline,
            scenes,
            stage,
            caption,
          });
        }

        updateCaption(beatIndex, beat, beatSource.words, time, settled);
        if (progressEl) {
          progressEl.style.transform = `scaleX(${total > 0 ? time / total : 0})`;
        }
      },

      audit() {
        const errors = [];
        if (!stage) return ['missing #stage'];
        const limits = stage.getBoundingClientRect();
        const scale = limits.width / STAGE_WIDTH;
        const root = resolveAuditRoot();
        const rootStyle = root && root !== stage ? getComputedStyle(root) : null;
        const rootLimits = rootStyle && (rootStyle.overflowX !== 'visible' || rootStyle.overflowY !== 'visible')
          ? root.getBoundingClientRect()
          : null;
        const queried = typeof config.getAuditNodes === 'function'
          ? [...config.getAuditNodes({ root, stage, caption, storyboard, timeline })]
          : (root && auditSelector ? [...root.querySelectorAll(auditSelector)] : []);
        const nodes = caption ? [...queried, caption] : queried;
        const current = caption ? [...caption.childNodes] : [];
        const pages = caption
          ? (captionPages.length ? captionPages.map(([start, end]) => captionNodes.slice(start, end)) : [current])
          : [[]];

        for (const contents of pages) {
          if (caption) caption.replaceChildren(...contents);
          const captionRect = caption ? caption.getBoundingClientRect() : null;
          for (const node of nodes) {
            if (!node) continue;
            const style = getComputedStyle(node);
            if (node !== caption && style.display === 'none') continue;
            const rect = node.getBoundingClientRect();
            if (node !== caption && rect.width === 0 && rect.height === 0) continue;
            const label = node.dataset?.auditLabel || node.className || node.id || node.tagName.toLowerCase();
            const bottom = rect.top + Math.max(rect.height, node.scrollHeight * scale);
            if (rect.right > limits.right + 1 || bottom > limits.bottom + 1 || rect.left < limits.left - 1) {
              errors.push(`${label}: stage overflow`);
            }
            if (rootLimits && node !== caption && (
              rect.right > rootLimits.right + 1
              || rect.bottom > rootLimits.bottom + 1
              || rect.left < rootLimits.left - 1
              || rect.top < rootLimits.top - 1
            )) {
              errors.push(`${label}: clipped by viewport`);
            }
            const limited = node.classList.contains('node')
              || style.maxHeight !== 'none'
              || style.overflowY !== 'visible';
            if (node.scrollWidth > node.clientWidth + 1 || (limited && node.scrollHeight > node.clientHeight + 1)) {
              errors.push(`${label}: clipped text`);
            }
            if (caption && node !== caption && rect.bottom > captionRect.top - captionClearance * scale) {
              errors.push(`${label}: overlaps captions`);
            }
          }
        }
        if (caption) caption.replaceChildren(...current);

        const missingTitle = requireTitle && (!root || !root.querySelector(titleSelector)?.textContent.trim());
        const missingNarration = Boolean(caption) && !caption.textContent.trim();
        if (missingTitle || missingNarration) {
          errors.push('missing title or narration');
        }
        if (typeof config.onAudit === 'function') {
          const extra = config.onAudit({ root, stage, caption, storyboard, timeline, scale, limits });
          if (Array.isArray(extra)) errors.push(...extra);
        }
        return [...new Set(errors)];
      },
    };

    if (document.fonts && typeof document.fonts.addEventListener === 'function') {
      document.fonts.addEventListener('loadingdone', () => {
        captionBeat = -1;
      });
    }

    if (config.register !== false) {
      global.motionExplainer = controller;
      global.animatic = controller;
    }
    return controller;
  }

  global.MotionKit = {
    STAGE_WIDTH,
    STAGE_HEIGHT,
    clamp,
    mix,
    easeOutCubic,
    easeInOutCubic,
    element,
    springState,
    spring,
    impact,
    smear,
    sphereEyes,
    inlineSlot,
    wipeClip,
    pillMorph,
    camera,
    deterministicBlink,
    createPlayerShell,
  };
})(typeof window !== 'undefined' ? window : globalThis);
