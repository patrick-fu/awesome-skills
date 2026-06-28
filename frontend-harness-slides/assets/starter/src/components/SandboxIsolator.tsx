import type { ReactNode } from 'react';

// Wrap any embedded interactive demo (input, terminal, clickable mini-game) with this. Otherwise a
// space / arrow key, a scroll, or a click inside the demo bubbles up to the deck's global listeners
// and flips the slide while the user is mid-interaction. It does exactly one thing: stop
// key / wheel / click events from bubbling out of the demo.
export function SandboxIsolator({ children }: { children: ReactNode }) {
  return (
    <div
      onKeyDown={(e) => e.stopPropagation()}
      onWheel={(e) => e.stopPropagation()}
      onClick={(e) => e.stopPropagation()}
      className="w-full h-full"
    >
      {children}
    </div>
  );
}
