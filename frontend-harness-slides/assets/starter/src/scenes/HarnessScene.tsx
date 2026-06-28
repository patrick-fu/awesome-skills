import { motion, useReducedMotion } from 'framer-motion';
import type { SceneProps } from '../SlideRegistry';

const STEPS = ['Registry owns order', 'Stage locks 16:9', 'Harness freezes every frame'];

// Demo scene with 3 beats. The blurred pulse is a continuous animation on purpose: it shows how the
// harness handles motion — gated behind prefers-reduced-motion for real viewers, and stopped in test
// mode (instant) plus frozen by FREEZE_CSS so the pixel diff is stable.
export function HarnessScene({ currentBeat, isTestMode }: SceneProps) {
  const instant = isTestMode === true;
  const reduceMotion = useReducedMotion();
  const animatePulse = instant || reduceMotion;

  return (
    <div className="w-full h-full flex flex-col justify-center gap-12 bg-background text-text px-40">
      <h2 className="font-display font-bold" style={{ fontSize: '88px' }}>
        How it stays solid
      </h2>
      <ul className="flex flex-col gap-8">
        {STEPS.map((step, i) => (
          <motion.li
            key={step}
            className="flex items-center gap-6 font-body"
            style={{ fontSize: '46px' }}
            initial={instant ? false : { opacity: 0, x: -24 }}
            animate={{ opacity: currentBeat >= i + 1 ? 1 : 0.15, x: 0 }}
            transition={{ duration: instant ? 0 : 0.4 }}
          >
            <span
              className="inline-block rounded-full"
              style={{ width: 22, height: 22, background: 'var(--color-primary)' }}
            />
            {step}
          </motion.li>
        ))}
      </ul>

      <motion.div
        aria-hidden
        className="absolute rounded-full"
        style={{
          right: 140,
          bottom: 140,
          width: 140,
          height: 140,
          background: 'var(--color-primary)',
          filter: 'blur(10px)',
        }}
        animate={animatePulse ? undefined : { scale: [1, 1.25, 1], opacity: [0.45, 0.8, 0.45] }}
        transition={animatePulse ? undefined : { duration: 2, repeat: Infinity }}
      />
    </div>
  );
}
