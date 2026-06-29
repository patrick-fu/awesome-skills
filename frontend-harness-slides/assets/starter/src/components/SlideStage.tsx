import { useEffect, useRef, useState, type ReactNode } from 'react';

// Absolute 16:9 stage: lock all content inside a virtual 1920x1080 canvas, then scale the whole
// stage to fit the viewport (letterbox / pillarbox the leftover). Every screen shows the exact same
// layout — no responsive breakpoints rearranging content per device.
//
// Contract for the harness: the frame carries `data-slide-stage` (stable bounds anchor) plus
// `data-slide-id` / `data-beat` (so a test can assert the app actually landed on the requested
// frame). Anchor on these attributes, never on class chains — classes drift, attributes don't.
interface SlideStageProps {
  children: ReactNode;
  slideId: string;
  beat: number;
  themeBg?: string;
}

// H-6: clamp the scale so zoom never exceeds 1 (prevents upscaling blur on large monitors) and
// never drops below 0.05 (prevents divide-by-near-zero in derived metrics).
function clampScale(raw: number): number {
  return Math.max(0.05, Math.min(1, raw));
}

export function SlideStage({ children, slideId, beat, themeBg = '#000000' }: SlideStageProps) {
  const [scale, setScale] = useState(1);
  const ref = useRef<HTMLDivElement>(null);
  const rafRef = useRef<number | null>(null);

  useEffect(() => {
    const calculate = () => {
      // H-6: double-rAF debounce. ResizeObserver firing → first rAF commits layout → second rAF
      // we read the post-layout size. Avoids the "setScale → triggers reflow → observer fires
      // again" infinite re-trigger on some browsers.
      if (rafRef.current != null) cancelAnimationFrame(rafRef.current);
      rafRef.current = requestAnimationFrame(() => {
        rafRef.current = requestAnimationFrame(() => {
          const scaleX = window.innerWidth / 1920;
          const scaleY = window.innerHeight / 1080;
          setScale(clampScale(Math.min(scaleX, scaleY)));
        });
      });
    };
    const observer = new ResizeObserver(calculate);
    observer.observe(document.documentElement);
    calculate();
    return () => {
      if (rafRef.current != null) cancelAnimationFrame(rafRef.current);
      observer.disconnect();
    };
  }, []);

  return (
    <div
      className="w-screen h-screen overflow-hidden flex items-center justify-center select-none relative"
      style={{ backgroundColor: themeBg }}
    >
      <div
        ref={ref}
        data-slide-stage
        data-slide-id={slideId}
        data-beat={beat}
        style={{
          width: '1920px',
          height: '1080px',
          transform: `scale(${scale})`,
          transformOrigin: 'center center',
          flex: 'none', // stop the flex parent from squeezing the canvas and distorting 16:9
        }}
        // H-6: no transition on transform. A 75ms ease-out means a screenshot taken immediately
        // after a resize captures an in-between frame and the visual baseline drifts. Instant
        // transforms are fine — scale changes happen on window resize which is already animated
        // by the OS compositor, not the slide runtime.
        // H-7 P0-3: lock the stage chrome to effects tokens so theme.effects.shadow drives the
        // drop shadow instead of a hard-coded Tailwind preset — a swap to a "flat" theme will zero it out.
        className="relative overflow-hidden shadow-card transition-none"
      >
        {children}
      </div>
    </div>
  );
}
