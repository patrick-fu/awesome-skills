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

export function SlideStage({ children, slideId, beat, themeBg = '#000000' }: SlideStageProps) {
  const [scale, setScale] = useState(1);
  const ref = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const calculate = () => {
      const scaleX = window.innerWidth / 1920;
      const scaleY = window.innerHeight / 1080;
      setScale(Math.min(scaleX, scaleY)); // take the smaller ratio so the whole stage stays visible
    };
    const observer = new ResizeObserver(calculate);
    observer.observe(document.documentElement);
    calculate();
    return () => observer.disconnect();
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
        className="relative overflow-hidden shadow-2xl transition-transform duration-75 ease-out"
      >
        {children}
      </div>
    </div>
  );
}
