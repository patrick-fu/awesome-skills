# Harness Pattern

This is reference, not a starter and not a template. Use it to design the
mechanisms inside the user's chosen stack.

## Goal

A slide deck should be safe to revise after the first draft. The harness exists
to make every meaningful rendered frame discoverable, deterministic, and
checkable before delivery.

## Required Mechanisms

### Stable Frame Address

Every scene needs a stable id. Every meaningful state inside that scene needs a
stable beat or equivalent frame index. A tester or reviewer must be able to open
one frame directly without manually clicking through the whole deck.

Do not use visible titles, file names, or array positions as the only identity.
They change during editing. Stable ids should survive copy changes, reordering,
and insertion of new scenes.

### Registry Or Manifest

Tooling needs a source of truth for:

- scene order
- scene id
- human title
- number of meaningful beats or frame states
- optional metadata such as section, speaker notes, or visual baseline policy

The registry can be code, JSON, generated metadata, or an app-level route table.
The important part is that tests can enumerate frames without scraping the DOM
or guessing from filenames.

### Fixed Stage

Author slide content inside a fixed-ratio stage, usually 16:9. Confirm the base
stage size before implementation. Prefer `1920x1080` by default, but support
`1280x720`, `2560x1440`, or another explicit project ratio when that better
matches the talk, reference deck, or deployment surface.

The stage scales as a whole to fit the viewport. The normal scale rule is the
smaller of viewport width/base width and viewport height/base height. This means
scale may be greater than `1` on large displays. Do not cap scale at `1` by
default. If the user wants to avoid upscaling, make that an explicit opt-in such
as "max scale 1" and document the tradeoff.

Inside the stage, avoid viewport responsive breakpoints that rearrange slide
content differently on laptop, phone, or CI.

Responsive layout can exist outside the stage for controls, presenter tools, or
debug panels. It should not change the slide composition itself.

### Navigation And Touch

Keyboard navigation is not enough when the deck may be opened on a phone, tablet,
or touchscreen. Confirm whether touch navigation is required. When enabled, the
expected behavior is:

- tap/click empty slide space: next beat or next scene
- swipe left or up: next
- swipe right or down: previous
- interactive regions: do not accidentally trigger slide navigation

Recommend a small in-stage scene navigator by default, then confirm with the
user. It can be a horizontal row near the lower edge, a vertical rail near the
side edge, or another style-matched form. It should feel embedded in the slide
design: glowing dots for a tech deck, sketch marks for a hand-drawn deck, small
tabs for an editorial deck, etc. The active scene marker should be visible but
subtle.

Do not place navigation outside the fixed stage. If the base stage is
`1920x1080`, every dot, button, rail, hotspot, and hover target belongs inside
that coordinate system. No navigation, controls, or decorative interaction
element may overflow beyond the slide stage.

Frozen or test mode should disable or stabilize pointer/touch navigation if it
could make automated checks nondeterministic.

### Frozen Mode

Tests need a deterministic render mode. Frozen mode should stop or stabilize:

- entrance and exit animation
- timers and clocks
- random values
- video, canvas, embedded demos, and live widgets
- network-dependent regions when they are not the thing being tested

Frozen mode does not mean the deck has no animation. It means each animation
state can be inspected as a known frame. For a beat-driven deck, frozen mode
should normally render the requested beat's settled end state, not the middle of
an entrance transition.

### Audit Surface

The harness should fail loudly on problems that a build step usually misses:

- requested frame does not match the rendered scene id or beat
- content overflow outside the stage
- stage base size or scale behavior differs from the confirmed contract
- visible content collapses to zero size
- fonts or images fail to load
- unexpected console errors or runtime exceptions
- interactive regions swallow or leak navigation keys

The exact implementation depends on the project. The behavior should not.

### Visual Baseline

Use visual screenshots or an equivalent rendered-frame comparison when visual
drift matters. Keep baselines tied to stable frame ids, not file positions.

Only update a baseline after inspecting the new image and confirming the change
is intentional. A green visual test only means "matches the baseline"; it does
not prove the baseline was good.

### Interaction Check

If the deck supports click, tap, swipe, or interactive regions, add an
interaction check. It should cover at least:

- a desktop viewport where the stage may be scaled up
- a small/mobile viewport where the stage is scaled down
- click or tap advances only when the target is non-interactive slide space
- swipe next and previous paths when touch navigation is enabled
- form controls, links, code editors, demos, or other interactive regions do not
  trigger accidental navigation

Interaction checks can use Playwright, another browser automation tool, or the
project's existing UI test system.

## Verification Tiers

Use the smallest check that matches the risk:

- **Preflight**: environment, dependencies, server, browser, and obvious config.
- **Structural audit**: registry, addressability, geometry, overflow, collapsed
  content, and runtime errors.
- **Visual check**: deterministic screenshot comparison for frames likely to
  drift.
- **Full gate**: all relevant checks before delivery or baseline acceptance.

Do not require one universal command name. Name the commands to fit the chosen
toolchain, then document them in the deck project.

## Implementation Notes

- Start by adapting an existing project if the user already has one.
- For a new project, choose the lightest stack that can satisfy the mechanisms.
- Keep harness code close to the deck so future edits run the same checks.
- Avoid adding PDF export, deployment automation, or CI until the user needs it.
- If a check is skipped, report that explicitly instead of implying safety.
