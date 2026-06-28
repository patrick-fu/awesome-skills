import { useCallback, useEffect, useMemo, useState } from 'react';
import { SLIDE_REGISTRY, getSlideNavigation } from './SlideRegistry';
import { SlideStage } from './components/SlideStage';
import { ThemeProvider } from './theme/ThemeProvider';
import { defaultTheme } from './theme/themes';

// The beat controller: slide state lives in the URL (?scene=<id>&beat=<n>), so any frame is a
// shareable, reloadable deep link. With ?test=true the deck locks to that exact scene+beat and skips
// live keyboard navigation — that determinism is what lets the harness freeze a frame.

function readFrameFromUrl() {
  const params = new URLSearchParams(window.location.search);
  const isTest = params.get('test') === 'true';

  const requested = params.get('scene') ?? SLIDE_REGISTRY[0].id;
  const sceneId = SLIDE_REGISTRY.some((s) => s.id === requested) ? requested : SLIDE_REGISTRY[0].id;
  const entry = SLIDE_REGISTRY.find((s) => s.id === sceneId)!;

  const rawBeat = Number(params.get('beat') ?? '0');
  const beat = Number.isFinite(rawBeat)
    ? Math.min(Math.max(0, Math.trunc(rawBeat)), entry.totalBeats)
    : 0;

  return { sceneId, beat, isTest };
}

export function SlideDeck() {
  const initial = useMemo(readFrameFromUrl, []);
  const [sceneId, setSceneId] = useState(initial.sceneId);
  const [beat, setBeat] = useState(initial.beat);
  const isTest = initial.isTest;

  const nav = getSlideNavigation(sceneId);
  const entry = nav.current;

  // keep the URL in sync so a reload restores the exact frame
  useEffect(() => {
    const params = new URLSearchParams(window.location.search);
    params.set('scene', sceneId);
    params.set('beat', String(beat));
    if (isTest) params.set('test', 'true');
    window.history.replaceState(null, '', `${window.location.pathname}?${params.toString()}`);
  }, [sceneId, beat, isTest]);

  const advance = useCallback(
    (direction: 1 | -1) => {
      const nextBeat = beat + direction;
      if (nextBeat >= 0 && nextBeat <= entry.totalBeats) {
        setBeat(nextBeat);
        return;
      }
      const sibling = direction === 1 ? nav.next : nav.prev;
      if (!sibling) return; // clamp at the deck edges
      setSceneId(sibling.id);
      setBeat(direction === 1 ? 0 : sibling.totalBeats);
    },
    [beat, entry.totalBeats, nav.next, nav.prev],
  );

  // live keyboard navigation — disabled in test mode so the frame stays frozen
  useEffect(() => {
    if (isTest) return;
    const onKey = (e: KeyboardEvent) => {
      if (e.key === 'ArrowRight' || e.key === ' ' || e.key === 'PageDown') {
        e.preventDefault();
        advance(1);
      } else if (e.key === 'ArrowLeft' || e.key === 'PageUp') {
        e.preventDefault();
        advance(-1);
      }
    };
    window.addEventListener('keydown', onKey);
    return () => window.removeEventListener('keydown', onKey);
  }, [isTest, advance]);

  const Scene = entry.component;

  return (
    <ThemeProvider theme={defaultTheme}>
      <SlideStage slideId={entry.id} beat={beat} themeBg={defaultTheme.colors.background}>
        <Scene currentBeat={beat} isTestMode={isTest} />
      </SlideStage>
    </ThemeProvider>
  );
}
