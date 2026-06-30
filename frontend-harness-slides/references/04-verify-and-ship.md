# 04 Verify And Ship

Use this before delivery and whenever layout, animation, fonts, assets,
navigation, harness code, or deployment changes. The goal is to prove that the
deck works, then deliver the confirmed output instead of stopping at a local dev
server.

## Verification Tiers

Use project-specific commands. Do not run the heaviest suite after every tiny
copy edit, but do not ship without the relevant final gate.

| Tier | Purpose | Use when |
|---|---|---|
| Preflight | Dependencies, server, browser engines, obvious config. | Setup, moving deck, suspicious environment. |
| Structural audit | Registry, direct frame routes, stage geometry, overflow, collapsed content, assets, console errors. | Ordinary scene/content/layout edits. |
| Visual smoke | Screenshots plus human scan of representative frames. | After visual, layout, animation, theme, font, or shared component changes. |
| Production smoke | Hosted URL, production alias, mobile visibility, navigation, assets. | After live deployment. |
| Full gate | Relevant build, audit, visual, interaction, and production checks. | Final delivery or baseline acceptance. |

Report skipped checks explicitly. A skipped check is not a pass.

## Audit Profiles

Bind the audit profile to the confirmed information density.

### Speaker-Led

Use for live talks, sparse slides, demos, and presenter-driven decks.

- Each beat needs at least one visible story element.
- Do not require long text or multiple reveal elements.
- Allow large whitespace.
- Check that the title, primary visual object, and beat intent exist.
- Rely more heavily on visual smoke because machines cannot judge "sparse but
  effective" well.

### Reading-First

Use for reports, research readouts, and self-contained decks.

- Each page should explain itself.
- Check hierarchy, font size, table/chart readability, and annotations.
- Do not rely on the speaker to fill in core facts.
- Dense content should be split instead of shrunk.

### Hybrid

Mark profile by scene or section. Demo/keynote scenes can use speaker-led
checks; evidence, data, or report sections should use reading-first checks.

## Interaction Checks

If the deck supports keyboard, click, tap, swipe, or local interactive regions,
verify at least:

- Space once advances exactly one beat/scene.
- ArrowRight or ArrowDown once advances exactly one beat/scene.
- ArrowLeft or ArrowUp once moves back exactly one beat/scene.
- Mobile tap once advances exactly one beat/scene.
- Swipe next/previous advances exactly one step in the expected direction.
- Long key repeat does not accidentally skip multiple beats unless intentionally
  supported.
- Clicking controls, links, tooltips, expandable notes, demos, or other
  interactive regions does not leak into slide navigation.
- Direct frame URLs render the intended scene/beat.
- Frozen mode renders settled states.

## Mobile Visibility

When mobile/touch support is part of delivery, structural checks are not enough.
Add mobile viewport checks:

- capture at least one mobile screenshot
- confirm the stage has real intersection with the viewport
- confirm the stage is not pushed outside the visible area
- confirm stage width is close to viewport width in portrait scale mode when
  that is the intended behavior
- confirm the viewport center or stage center hits slide content
- confirm the screenshot is not mostly blank background

## Visual Smoke

After structural audit passes, manually scan representative screenshots. Minimum
set for non-trivial decks:

- opening page
- core thesis or turning-point page
- complex motion page
- grid/flex/track layout page
- screenshot/product/tool comparison page
- final takeaway page
- mobile viewport page when touch/mobile is supported

Look for overlaps, missing nodes, wrong visual hierarchy, layout drift, clipped
assets, unreadable text, and whether the page matches the intended style.

## Browser Coverage

Preflight should identify available browser engines when mobile support matters:

- Playwright package availability
- Chromium availability
- WebKit availability when Safari/iOS coverage is relevant

Chromium mobile emulation is useful, but it is not the same as real iOS Safari.
If WebKit is unavailable or not run, say so in the final report. If the deck is
Safari-critical, ask whether to install/run WebKit or test on a real device.

## Visual Drift Triage

When screenshots fail:

1. Inspect the new screenshot before accepting any baseline.
2. Decide whether the change is expected, environment drift, or a real
   regression.
3. Suspect fonts first when text edges move across machines.
4. Suspect animation timing when elements are between states.
5. Suspect responsive leakage when stage geometry changes by viewport.
6. Update baselines only after confirming the new image is intentional.

Common causes:

- font fallback or missing local font
- screenshots before fonts finish loading
- non-frozen animations
- timers/random values/live widgets
- browser or OS rendering differences
- viewport scale or DPR changes

## Delivery Target

Before building, confirm whether the final handoff is:

- deployed online URL
- PDF/static export
- both

A local dev server is only a preview unless the user explicitly asks for
local-only work.

## Live Deployment

Follow the user's deployment habit when they have one. If not, recommend Vercel
for a Vite/React or static web deck. GitHub Pages and Cloudflare Pages are good
static alternatives. Check current provider docs before exact commands.

Deploy hygiene for new deck projects:

- ignore `node_modules/`
- ignore local check output such as `artifacts/`
- ignore `.vercel/` unless the project intentionally commits provider metadata
- ignore `.DS_Store`
- do not recommend deprecated Vercel CLI flags such as `--name`
- prefer existing project binding or provider config after first setup

Before deploying:

- run the final relevant local gate
- build the static output
- verify local preview from the built output when possible
- confirm fonts, images, animation states, and direct frame links work

After deploying:

- smoke test the production URL, not only a preview URL
- verify direct frame links on the hosted URL
- verify mobile visibility and navigation when mobile/touch is supported
- record the production URL, deploy command, and smoke status in README or a
  handoff note

## PDF Or Static Handoff

If the user wants PDF export, confirm whether the PDF is:

- speaker handout
- reading-first version
- archival record
- client/shareable artifact

PDF may need different choices than the live deck: page numbers, fewer
interactive-only explanations, expanded notes, or static versions of animated
states.

## Mobile Viewing Note

For 16:9 decks, distinguish "phone can open it" from "phone is the ideal
watching surface":

- mobile portrait should be usable for preview and navigation
- mobile landscape is usually better for watching
- formal presentation is best on desktop, projector, or shared screen
- if the user expects phone-first consumption, confirm whether to design a
  separate phone-first layout instead of only scaling 16:9 slides

## Troubleshooting

- Wrong direct frame: compare URL params, registry id/beat, and rendered
  `data-scene-id`/`data-beat`.
- Overflow/collapse: inspect element boxes inside the fixed stage and check that
  reveals do not remove layout unexpectedly.
- Navigation keys fail: ensure focus is not trapped by an input/editor; global
  navigation should respect editable elements.
- Static host shows HTML for missing assets: check base path, asset URLs, and
  fallback rewrites.
- Hosted deck works locally but fails online: inspect network errors, base path,
  asset case sensitivity, font paths, and provider caching.

## Final Report

Final delivery should state:

- where the deck lives
- chosen delivery target and production URL/PDF path
- commands or checks run
- audit profile used
- visual smoke coverage
- mobile/touch coverage
- WebKit/Safari coverage status when relevant
- skipped checks and residual risk
