import type React from 'react';
import { CoverScene } from './scenes/CoverScene';
import { HarnessScene } from './scenes/HarnessScene';

// One central array owns slide order. Name scene components semantically (CoverScene, HarnessScene),
// never with ordinals (Scene1, Scene7). Inserting/reordering a slide is just editing this array —
// physical filenames never change, so Playwright snapshot paths (keyed on `id`) never break.

export interface SceneProps {
  currentBeat: number;
  isTestMode?: boolean;
}

export interface SlideEntry {
  id: string; // stable id — used in routes and as the Playwright snapshot filename; don't change casually
  title: string;
  component: React.ComponentType<SceneProps>;
  totalBeats: number; // beats inside this slide, excluding beat 0
}

export const SLIDE_REGISTRY: SlideEntry[] = [
  { id: 'cover', title: 'Frontend Harness Slides', component: CoverScene, totalBeats: 1 },
  { id: 'harness', title: 'The harness guards every frame', component: HarnessScene, totalBeats: 3 },
];

export function getSlideNavigation(currentId: string) {
  const found = SLIDE_REGISTRY.findIndex((s) => s.id === currentId);
  const index = found === -1 ? 0 : found;
  return {
    current: SLIDE_REGISTRY[index]!,
    index,
    total: SLIDE_REGISTRY.length,
    prev: index > 0 ? SLIDE_REGISTRY[index - 1]! : null,
    next: index < SLIDE_REGISTRY.length - 1 ? SLIDE_REGISTRY[index + 1]! : null,
  };
}

declare global {
  interface Window {
    __SLIDE_REGISTRY__?: { id: string; title: string; totalBeats: number }[];
  }
}

// Call once at startup (see main.tsx). The visual / auditor specs read this instead of hardcoding
// their own slide list, so SLIDE_REGISTRY stays the single source of truth.
export function exposeRegistryForTooling() {
  if (typeof window !== 'undefined') {
    window.__SLIDE_REGISTRY__ = SLIDE_REGISTRY.map((s) => ({
      id: s.id,
      title: s.title,
      totalBeats: s.totalBeats,
    }));
  }
}
