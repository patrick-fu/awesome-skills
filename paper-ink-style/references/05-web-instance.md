# Web instance

`assets/base.css` is the worked Web instance of the vocabulary in
`02-components.md`: every token and component, as CSS custom properties and
classes. Any other carrier reproduces the same parameters in its own idiom.

Working on the Web:

- Link or inline base.css; page CSS composes with the tokens as they are. A
  new component joins base.css with a version bump.
- Deliver a single HTML file by default: inline the sheet in a `<style>`
  block; embed the font subsets (`assets/fonts/`, SIL OFL) when their size is
  acceptable, otherwise let the system Kai fallbacks carry the handwritten
  voice. Split into files only when the reader asks or the deliverable
  genuinely needs it.
- Screenshots: any headless browser works. Measure the real 390px layout (an
  iframe probe or devtools device mode): macOS headless Chrome clamps windows
  to >= 500px, so a direct 390px screenshot reports the clamped width.
- `assets/snippets/` and `assets/examples/` are Web specimens: look at them
  for the hand. On other carriers reproduce the parameters in the platform
  idiom.
