# Theming

Use this during visual discovery and theme implementation.

Read `references/style-presets.md` when the user asks for preset inspiration,
gives only a vague style direction, or needs a few contrasting visual directions
before implementation.

## Discover By Eye

Most users cannot name the exact style they want; they recognize it when they see
it. When visual direction is unclear, show a small number of real deck-like
previews instead of asking the user to choose abstract adjectives.

Offer three meaningfully different directions:

- **Safe**: restrained, legible, hard to dislike.
- **Bold**: a committed look with one strong narrative or graphic device.
- **Wildcard**: context-specific and clearly different from the other two.

Use style presets as inspiration, not as locked templates. Explain the
recommendation in chat and ask the user to confirm, adjust, or reject it before
turning it into the deck's theme.

The preview itself should look like an actual first slide from the user's deck.
Do not render option labels, workflow notes, file paths, theme slugs, or internal
requirements on the slide surface. Explain the options in the chat, not inside
the deck.

## Theme Tokens

Keep recurring visual decisions in a theme layer rather than scattering one-off
values across slides:

- display font
- body font
- background
- text
- accent
- borders
- radii
- shadows
- chart colors

How those tokens are implemented depends on the stack: CSS variables, design
tokens, a context provider, a global stylesheet, or generated theme data are all
acceptable. The important part is that a theme change does not require editing
many unrelated scenes.

## Preview Authenticity

Use the user's real title, product, story, screenshots, or data. A preview that
looks like a diagnostic card is not useful. The user should be reacting to the
deck's likely final feel, not to an implementation demo.

## Commit The Direction

After the user chooses a direction:

- remove temporary preview-only controls or routes
- commit the selected theme into the deck's normal theme mechanism
- rerun the relevant visual checks
- update baselines only after inspecting the changed frames
