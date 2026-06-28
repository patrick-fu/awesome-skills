import { motion } from 'framer-motion';
import type { SceneProps } from '../SlideRegistry';

// Demo scene. Replace with your own, but keep the contract:
//  - read `currentBeat` to decide what is revealed
//  - when `isTestMode`, jump straight to the final state (no entrance stagger) so frames are freezable
export function CoverScene({ currentBeat, isTestMode }: SceneProps) {
  const instant = isTestMode === true;

  return (
    <div className="w-full h-full flex flex-col items-center justify-center gap-8 bg-background px-32 text-center">
      <motion.h1
        className="font-display font-bold text-text tracking-tight"
        style={{ fontSize: '128px', lineHeight: 1.05 }}
        initial={instant ? false : { opacity: 0, y: 24 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: instant ? 0 : 0.5 }}
      >
        Frontend Harness Slides
      </motion.h1>
      <motion.p
        className="font-body text-text"
        style={{ fontSize: '40px' }}
        initial={instant ? false : { opacity: 0 }}
        animate={{ opacity: currentBeat >= 1 ? 1 : 0 }}
        transition={{ duration: instant ? 0 : 0.4 }}
      >
        Build slide decks like production software.
      </motion.p>
    </div>
  );
}
