# Eval 02 - token drift

Purpose: content edits must not move the visual system.

1. Take `assets/examples/canonical.html`, replace all copy with a different
   topic, keep structure.
2. audit.py must PASS with zero fails; diff of `<style>`/inline style blocks
   against the original must be empty (no new colors, radii, shadows).
3. Fail if any token literal appears outside base.css.
