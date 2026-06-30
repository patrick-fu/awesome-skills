# Animation Style

Use this when the user asks for polished slide motion, gives an animation
reference, or leaves animation direction vague during intake.

## Recommended Default

Recommend a keynote/product-launch motion style unless the user asks for a dense
report deck or a very static handoff:

- short directional scene transitions, around `250-350ms`
- beat-by-beat reveals where each beat changes the story state
- new important objects entering with opacity plus small position or scale
  movement
- light spring emphasis for promoted cards, numbers, or decisions
- old or superseded ideas fading, dimming, being crossed out, or moving aside
- small staggered delays only when they clarify reading order
- a final takeaway or highlighted phrase on the last meaningful beat

Magic Move-style continuity is the recommended default across deck types: smooth
scene transitions, objects moving continuously between related states, and
progressive reveals instead of dumping all content at once. Tune the intensity
to the deck:

- presentation, keynote, product-launch, sharing, and live speaking decks can
  use more energetic motion, including rotation, bounce, wobble, flowing arrows,
  and playful object movement
- reading-first decks should still use smooth transitions and staged reveals,
  but keep movement quieter so dense material remains easy to scan
- formal reports should use the same continuity principle with restrained
  duration, smaller travel, and fewer decorative loops

Describe it in plain text as: "similar to a modern product-launch keynote: each
click advances the argument, not just another bullet. New ideas appear with a
small confident motion; old ideas visibly lose importance; the final beat lands
the takeaway."

## Confirm The Default

Do not silently adopt the recommended animation style. Explain the default in
plain text, then ask whether the user agrees, wants a livelier direction, wants a
more restrained report style, or has another reference.

Confirm style words such as "playful", "lively", "cinematic", "restrained", or
"static" before implementation. These words materially change motion, density,
interaction, and visual tone.

## Intake Prompt

When animation direction is not confirmed, ask in ordinary chat before building:

"For animation, I recommend a keynote-like progressive reveal: short directional
transitions, Magic Move-style continuity between related objects, beat-by-beat
state changes, light spring/scale emphasis, old ideas fading or being crossed
out, and a final takeaway highlight. Do you want that, a livelier version with
more bounce/flow/rotation, a more restrained report style, or a different
reference?"

This is a recommendation, not a forced choice. If the user gives a reference
deck or URL, inspect it and extract concrete behavior before deciding: base stage
size, whether scale can exceed `1`, scene transition style, beat reveal style,
takeaway behavior, and click/touch navigation.

## Report-Style Alternative

For formal reports, executive reviews, or reading-first decks, keep motion
quieter:

- use shorter fades or small vertical shifts
- minimize spring and large movement
- avoid continuous ambient motion unless it explains a concept
- prioritize stable scanning over theatrical reveals
- keep dense tables, charts, and code blocks fully legible at every beat

## Motion Semantics

Pick animation based on what changed in the story:

- **Reveal**: introduce a new claim, card, number, or diagram piece.
- **Promote**: make the current decision or key result feel primary.
- **Replace**: show an old model losing relevance while a new model takes over.
- **Accumulate**: grow bars, counters, paths, or stacks to show build-up.
- **Warn**: use color, shake, glitch, or spillover only for real risk moments.
- **Resolve**: settle movement and show the final takeaway.

Avoid motion that is only decorative. Beats should be reviewable story states,
not arbitrary fade timing.

## Interactive Motion

Use interaction when it clarifies the story or makes the deck feel alive:

- hover effects on meaningful cards, labels, diagrams, or emoji actors
- local click actions such as expand, pulse, rotate, reveal, or emphasize
  without advancing to the next scene
- click feedback for intentionally interactive elements
- continuous flow effects for arrows, paths, queues, or pipelines when they
  explain movement through a system

Interactive regions must not accidentally trigger slide navigation. Frozen or
test mode should render any reviewable interaction state deterministically.

## Determinism

Animation must not make the harness flaky:

- every animated state should have a stable scene/beat address
- frozen or test mode should render the requested beat's settled end state
- long-running loops should be disabled, stabilized, or excluded from visual
  checks when they are not the subject
- layout should not depend on animation timing
