# Visual Drift Triage

Use this before accepting new snapshots when visual regression fails.

## First Question

Is the diff an intended design change, or did the rendering environment drift?

Do not immediately run `--update-snapshots` just to make red tests green.

## Common Patterns

| Pattern | Likely cause | Response |
|---|---|---|
| Text edges changed across many slides | Font fallback, font hinting, browser/runtime change | Check font loading and baseline environment before rebasing. |
| One scene moved or resized | Real layout change | Review the scene and update only if intended. |
| Animated/live region differs each run | Unfrozen animation, video, canvas, iframe | Freeze, mask, or make the region deterministic. |
| Old scene snapshot remains after registry change | Orphan baseline | Delete the stale snapshot after confirming the scene id was removed. |
| Screenshot is blank or wrong scene | Router/test landing issue | Check `data-slide-id`, `data-beat`, and registry exposure. |

## Minimal Triage Steps

1. Run `npm run auditor` to catch structural errors first.
2. Open a few changed snapshots or Playwright diff images.
3. Decide whether the change is local to edited scenes or global.
4. If global text drift appears, inspect font strategy before increasing
   thresholds.
5. Rebaseline only intentional changes:

```bash
npm run visual:update
npm run test:full
```

Report any skipped or unresolved visual risk explicitly.
