# 03 Build

Use this while implementing the deck. The goal is a framework-neutral harness
that keeps every meaningful frame addressable, deterministic, interactive, and
safe to verify.

## Harness Guidance

### Stable Frame Address

Every scene should have a stable id. Every meaningful state inside that scene
should have a stable beat or equivalent frame index. A reviewer or test should
be able to open one frame directly without clicking through the whole deck.

Avoid using visible titles, file names, or array positions as the only identity.
They change during editing. Stable ids should survive copy changes, reordering,
and insertion of scenes.

### Registry Or Manifest

Tooling needs a source of truth for:

- scene order
- scene id
- human title
- number of meaningful beats or frame states
- mode/audit profile when it varies by scene
- optional metadata such as section, speaker notes, or visual baseline policy

The registry can be code, JSON, generated metadata, or an app-level route table.
Tests should enumerate frames without scraping visible text or guessing
filenames.

### Fixed Stage

Author slide content inside a fixed-ratio stage, usually 16:9. Confirm the base
stage before implementation. Prefer `1920x1080` by default, but support
`1280x720`, `2560x1440`, `4:3`, or custom ratios when the user chooses them.

The stage scales as a whole to fit the viewport. Avoid viewport breakpoints
inside the stage that rearrange slide content differently on laptop, phone,
projector, and CI.

### Mobile Fixed Stage

For a fixed 16:9 stage that should work on mobile, use a three-layer structure
by default:

```html
<div class="stage-viewport">
  <div class="stage-frame">
    <section class="stage"></section>
  </div>
</div>
```

Rules:

- `.stage` keeps the base design size such as `1920px` by `1080px`.
- `.stage` uses `transform: scale(var(--stage-scale))`.
- `transform-origin` is `top left`.
- `.stage-frame` uses the scaled width/height to participate in layout.
- The viewport centers or positions `.stage-frame`, not the unscaled stage box.

Avoid directly transforming a `1920x1080` stage and placing that unscaled layout
box inside a centered grid/flex container. On phones, that can push the visible
scaled slide outside the viewport and produce a blank-looking page.

### Navigation Contract

Support the confirmed navigation inputs. Recommended defaults:

- Space, ArrowRight, ArrowDown: next beat or next scene.
- ArrowLeft, ArrowUp: previous beat or previous scene.
- Tap/click empty slide space: next.
- Swipe left/up: next.
- Swipe right/down: previous.
- In-stage dot/marker navigator: jump to a scene.

One physical input should cause exactly one navigation step. Ignore repeated
keyboard events such as `event.repeat`. If touch and click are both listened to,
handle synthetic click double-fire, or use pointer events so one tap cannot jump
two beats.

Interactive regions should not accidentally trigger slide navigation. Buttons,
links, form controls, code editors, demos, tooltips, expandable notes, and local
interactive objects should stop or route events intentionally.

When an in-stage dot/marker navigator communicates position, do not also add
visible text counters such as `5 / 12`, `Page 5`, or `第五页 / 共十二页` on the
slide canvas. Add textual page numbers only when the user asks for them or when
making a PDF/reading/compliance variant.

Keep navigation inside the fixed stage. Every dot, button, rail, hotspot, and
hover target should belong inside the stage coordinate system.

### Frozen Mode

Tests need deterministic render mode. Frozen mode should stop or stabilize:

- entrance and exit animation
- timers and clocks
- random values
- video, canvas, embedded demos, and live widgets
- network-dependent regions when they are not the thing being tested

Frozen mode should normally render the requested beat's settled end state, not
the middle of an entrance transition.

### Audit Surface

The harness should fail loudly on:

- requested frame does not match rendered scene id or beat
- content overflows outside the stage
- stage base size or scale behavior differs from the confirmed contract
- visible content collapses to zero size
- fonts or images fail to load
- unexpected console errors or runtime exceptions
- interactive regions swallow or leak navigation keys

## Motion

Recommend a keynote/product-launch motion style unless the user asks for dense
reports or a very static handoff:

- short directional scene transitions
- beat-by-beat reveals where each beat changes the story state
- important objects entering with opacity plus small position/scale movement
- light spring emphasis for promoted cards, numbers, or decisions
- old or superseded ideas fading, dimming, being crossed out, or moving aside
- stagger only when it clarifies reading order
- a final takeaway or highlighted phrase on the last meaningful beat

Magic Move-style continuity, explicitly inspired by Keynote's Magic Move effect,
is the recommended default across deck types. It means smooth scene transitions,
objects moving continuously between related states, and progressive reveals
instead of dumping all content at once.

Tune intensity:

- Presentation, keynote, sharing, product-launch, and live speaking decks can
  use rotation, bounce, wobble, flowing arrows, and playful object movement.
- Reading-first decks should still use smooth transitions and staged reveals,
  but keep movement quieter.
- Formal reports should use continuity with restrained duration, smaller travel,
  and fewer decorative loops.

## Motion Semantics

Pick motion based on story change:

- **Reveal**: introduce a new claim, card, number, or diagram piece.
- **Promote**: make the current decision or result feel primary.
- **Replace**: show an old model losing relevance while a new model takes over.
- **Accumulate**: grow bars, counters, paths, or stacks.
- **Warn**: use shake, glitch, or spillover only for real risk moments.
- **Resolve**: settle movement and show the final takeaway.

Avoid motion that is only decorative. Beats should be reviewable story states,
not arbitrary fade timing.

## Interactive Motion

Use interaction when it clarifies the story or makes the deck feel alive:

- hover effects on meaningful cards, labels, diagrams, or emoji actors
- local click actions such as expand, pulse, rotate, reveal, or emphasize
  without advancing to the next scene
- click feedback for intentionally interactive elements
- continuous flow effects for arrows, paths, queues, or pipelines
- tooltips or small callouts for supporting notes

Frozen/test mode should render reviewable interaction states deterministically
when those states matter.

## Reveal And Layout Pitfalls

Reveal mechanisms should not change layout semantics.

Avoid:

```html
<div class="reveal">
  <div class="absolute-thing">...</div>
</div>
```

If `.reveal` has `transform`, it can create a containing block and break
absolute positioning inside a fixed stage.

Also avoid extra wrappers where grid, flex, direct-child selectors, or circular
track layouts expect the actual child element:

```html
<div class="reveal">
  <span class="track-node">Node</span>
</div>
```

Prefer applying reveal state directly to the visual/layout element:

```html
<span class="track-node reveal" data-show="2">Node</span>
```

If a wrapper is necessary, keep it layout-neutral. Opacity-only wrappers are
safer, but only when they do not affect layout, containing blocks, stacking, or
selectors.

## Other Implementation Anti-Patterns

- Rendering a whole static slide in canvas: DOM/SVG text is easier to inspect,
  copy, search, translate, and audit.
- Embedding live demos in critical frames: prefer stable screenshots plus an
  external demo link unless the live region has deterministic test mode.
- Casual stable id renames: ids are part of links, baselines, and review
  history.
- Masking main content in visual tests: masks are for nondeterministic regions,
  not broken layout.
- Adding PDF export, deployment automation, or CI before the user needs it.
