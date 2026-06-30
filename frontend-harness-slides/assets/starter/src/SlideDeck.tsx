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

  const requested = params.get('scene') ?? SLIDE_REGISTRY[0]!.id;
  const sceneId = SLIDE_REGISTRY.some((s) => s.id === requested) ? requested : SLIDE_REGISTRY[0]!.id;
  const entry = SLIDE_REGISTRY.find((s) => s.id === sceneId)!;

  const rawBeat = Number(params.get('beat') ?? '0');
  const beat = Number.isFinite(rawBeat)
    ? Math.min(Math.max(0, Math.trunc(rawBeat)), entry.totalBeats)
    : 0;

  return { sceneId, beat, isTest };
}

/** Returns true if the event originates from inside an editable element. */
function isEditableEventTarget(e: KeyboardEvent): boolean {
  const target = e.target as HTMLElement | null;
  if (!target) return false;
  // Walk up the tree so a <span> inside contenteditable still counts
  let cur: HTMLElement | null = target;
  while (cur) {
    if (cur.isContentEditable) return true;
    const tag = cur.tagName;
    if (
      tag === 'INPUT' ||
      tag === 'TEXTAREA' ||
      tag === 'SELECT'
    ) {
      // For INPUT, skip only the "actually editable" types (not button/checkbox/radio)
      if (tag === 'INPUT') {
        const type = (cur as HTMLInputElement).type;
        const editableTypes = [
          'text', 'password', 'email', 'search', 'tel', 'url',
          'number', 'date', 'datetime-local', 'time', 'week',
          'month', 'color', 'file',
        ];
        if (editableTypes.includes(type)) return true;
      } else {
        return true; // TEXTAREA / SELECT
      }
    }
    cur = cur.parentElement;
  }
  return false;
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
    // H-7: use replaceState so a single deck session doesn't pollute browser history with every
    // beat advance. Use only when the URL would actually change to avoid thrashing history state.
    const next = `${window.location.pathname}?${params.toString()}`;
    if (next !== window.location.pathname + window.location.search) {
      window.history.replaceState(null, '', next);
    }
  }, [sceneId, beat, isTest]);

  // H-7 (P1): listen for URL changes initiated by the browser (Back / Forward buttons, sharing a deep
  // link inside a SPA host). Without this the displayed frame and the URL get out of sync the moment
  // the user uses browser navigation.
  useEffect(() => {
    const onPop = () => {
      const { sceneId: nextScene, beat: nextBeat } = readFrameFromUrl();
      setSceneId(nextScene);
      setBeat(nextBeat);
    };
    window.addEventListener('popstate', onPop);
    return () => window.removeEventListener('popstate', onPop);
  }, []);

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

  // H-7: imperative API for hosts and integration tests.
  // Exposes window.__deck with a stable surface; never access internal React state directly from
  // outside.
  useEffect(() => {
    const api = {
      /** Go to a specific scene + beat. Unknown ids clamp to first slide. */
      gotoBeat(targetSceneId: string, targetBeat: number): void {
        const safeScene = SLIDE_REGISTRY.some((s) => s.id === targetSceneId)
          ? targetSceneId
          : SLIDE_REGISTRY[0]!.id;
        const safeEntry = SLIDE_REGISTRY.find((s) => s.id === safeScene)!;
        const safeBeat = Math.min(
          Math.max(0, Number.isFinite(targetBeat) ? Math.trunc(targetBeat) : 0),
          safeEntry.totalBeats,
        );
        setSceneId(safeScene);
        setBeat(safeBeat);
      },
      nextBeat(): void { advance(1); },
      prevBeat(): void { advance(-1); },
      goToStart(): void {
        setSceneId(SLIDE_REGISTRY[0]!.id);
        setBeat(0);
      },
      goToEnd(): void {
        const last = SLIDE_REGISTRY[SLIDE_REGISTRY.length - 1]!;
        setSceneId(last.id);
        setBeat(last.totalBeats);
      },
      setTheme(_themeId: string): void {
        // Reserved: currently the starter ships one theme; extend here when theming expands.
        // Intentionally no-op so the surface doesn't throw when a host calls it.
      },
      /** Read-only snapshot of the current frame. */
      getCurrentFrame() {
        return { sceneId, beat, totalBeats: entry.totalBeats };
      },
      /** Pass-through from the registry so hosts enumerate once. */
      getRegistry() {
        return SLIDE_REGISTRY.map((r) => ({ id: r.id, totalBeats: r.totalBeats }));
      },
    };
    const win = window as typeof window & { __deck?: typeof api };
    win.__deck = api;
    return () => {
      if (win.__deck === api) delete win.__deck;
    };
  }, [advance, beat, entry.totalBeats, sceneId]);

  // live keyboard navigation — disabled in test mode so the frame stays frozen
  useEffect(() => {
    if (isTest) return;
    const onKey = (e: KeyboardEvent) => {
      // H-7 (P1): if another handler (e.g. an input's preventDefault inside a Sandbox-like
      // container) has already claimed this event, don't re-handle it.
      if (e.defaultPrevented) return;
      // H-7: the correct input guard — editable fields get all keys back, focus-trapped content
      // inside the slide can respond without flipping pages.
      if (isEditableEventTarget(e)) return;

      switch (e.key) {
        case 'ArrowRight':
        case ' ':
        case 'PageDown':
        case 'Enter':
        case 'j':  // vim-style next
          e.preventDefault();
          advance(1);
          break;
        case 'ArrowDown':
          e.preventDefault();
          advance(1);
          break;
        case 'k':  // vim-style prev
          e.preventDefault();
          advance(-1);
          break;
        case 'ArrowLeft':
        case 'PageUp':
        case 'Backspace':
        case 'ArrowUp':
          e.preventDefault();
          advance(-1);
          break;
        case 'Home':
          e.preventDefault();
          setSceneId(SLIDE_REGISTRY[0]!.id);
          setBeat(0);
          break;
        case 'End':
          e.preventDefault(); {
            const last = SLIDE_REGISTRY[SLIDE_REGISTRY.length - 1]!;
            setSceneId(last.id);
            setBeat(last.totalBeats);
          }
          break;
        case 'f':
        case 'F': {
          e.preventDefault();
          // Fullscreen toggle — wrap in try/catch so iframe contexts fail silently.
          const docEl = document.documentElement as HTMLElement & {
            webkitRequestFullscreen?: () => Promise<void>;
          };
          try {
            if (!document.fullscreenElement) {
              (docEl.requestFullscreen ?? docEl.webkitRequestFullscreen)?.call(docEl);
            } else {
              document.exitFullscreen?.();
            }
          } catch {
            /* ignore fullscreen rejection (iframe / permissions / user gesture policy) */
          }
          break;
        }
        default:
          // Digits 1-9 jump to the 1st..9th slide; 0 jumps to 10th.
          if (/^[0-9]$/.test(e.key)) {
            const idx = e.key === '0' ? 9 : Number(e.key) - 1;
            if (idx < SLIDE_REGISTRY.length) {
              e.preventDefault();
              setSceneId(SLIDE_REGISTRY[idx]!.id);
              setBeat(0);
            }
          }
          break;
      }
    };
    window.addEventListener('keydown', onKey);
    return () => window.removeEventListener('keydown', onKey);
  }, [isTest, advance]);

  // Block pinch-zoom / ctrl-wheel only when it would zoom the page while the user is interacting
  // with the stage. React synthetic stopPropagation is ineffective at this layer, so we capture on
  // document directly with passive:false to keep preventDefault() working.
  useEffect(() => {
    const onWheel = (e: WheelEvent) => {
      if (e.ctrlKey || e.metaKey) {
        // Prevent browser page zoom from pinch/ctrl-wheel so the stage stays pixel-true.
        e.preventDefault();
      }
    };
    document.addEventListener('wheel', onWheel, { passive: false } as AddEventListenerOptions);
    return () => document.removeEventListener('wheel', onWheel);
  }, []);

  const Scene = entry.component;

  return (
    <ThemeProvider theme={defaultTheme}>
      <SlideStage slideId={entry.id} beat={beat} themeBg={defaultTheme.colors.background}>
        <Scene currentBeat={beat} isTestMode={isTest} />
      </SlideStage>
    </ThemeProvider>
  );
}
