# Deploy

Use this when the user wants a live URL, a shareable build, or a static handoff
after the deck frames have already been checked.

## Live URL

This skill does not prefer a hosting provider. Use any static host that fits the
project and account context.

Before deploying:

- run the deck's final relevant verification gate
- build or export with the project-specific command
- open the deployed URL and inspect key frames
- confirm fonts, images, animation states, and direct frame links work

Do not use random generated project names for a deck the user may share. Prefer
a dedicated project name and a dedicated domain or domain prefix, such as the
talk name, product name, team name, or event name. Random names are acceptable
only for disposable previews that will not be shared as the final link.

## Production Smoke Test

If you provide a hosted URL, do not stop at "deployment command succeeded." Open
the production URL or alias that the user will actually share and smoke-test it:

- the URL or alias points at the latest build, not a stale preview
- the stage base size, aspect ratio, centering, and scale match the confirmed
  contract, including large-screen upscaling when allowed
- a direct frame URL opens the intended scene and beat
- at least one desktop navigation path works, such as click or keyboard next
- if touch navigation is enabled, at least one tap or swipe path works on a
  mobile/tablet viewport
- fonts, images, and static assets do not show obvious load failures or broad
  404s

Report any skipped smoke-test item explicitly.

If the deck uses query parameters for frame state, ordinary static hosting is
usually enough. If the deck uses path-based client routing, configure a fallback
to the app entry page. Do not fallback known static asset directories to HTML; a
missing font or image should fail visibly instead of returning the entry page.

Use immutable caching for fingerprinted assets when the host supports it. Avoid
aggressive caching for the app entry page unless the deployment process handles
cache busting.

## Optional PDF Handoff

PDF export is project-specific, not a built-in skill concern. If the user
explicitly needs PDF, choose the simplest path after the checked deck is correct:

- browser print/export for simple decks
- a temporary browser capture script for precise fixed-stage pages
- a hosted URL plus manual export when the user wants to review the live deck
  first

Whatever path is chosen, inspect the output before delivery. Check font loading,
page count, clipped content, and whether animated beats collapse to the intended
static frame.

## CJK Font Size

If the deck uses a heavy CJK font, format conversion alone is not enough to get
it under budget. `ttf2woff2` changes the container; it does not subset glyphs.
For a large CJK TTF, a converted WOFF2 can still be many megabytes.

Use a subsetter only when stable CI, offline presentation, or static handoff
rendering is worth the extra step. See `references/cjk-fonts.md` for the lighter
decision tree.

## CI

Add CI only when it helps the deck's workflow. A lightweight private talk may not
need hosted CI; a team-reviewed deck probably does. If CI is added, it should run
the same project-specific final gate the agent uses locally and upload useful
failure artifacts when visual or browser checks fail.
