# Photo-to-Doodle Distillation Guide

The comedy of the viral "Scribblification / MSPaintify" look comes from
**recognizability under extreme degradation**: the drawing looks hilariously
clumsy, yet anyone who saw the photo immediately recognizes the exact person,
pet, or scene.

Because this skill does not use an image-generation model, **your multimodal
vision analysis is the secret sauce**. Follow this 4-step loop.

## Step 1: Extract 4–6 Unmistakable Identity Anchors

Inspect the source image and list only the visual anchors that carry identity:

1. **Signature silhouette / framing** — head tilt, posture, crop (close-up selfie vs full-body landmark shot).
2. **Loudest color & accessory anchor** — rainbow ski goggles, yellow buttons on a dark coat, striped bow tie, bright shirt, glasses frame shape.
3. **Key facial / fur markers** — eye color, hair texture/parting, orange-and-white fur patches, beard stubble, tongue sticking out.
4. **1–2 simplified background cues** — passenger seat, window, Eiffel Tower, laptop with logo, horizon grass. Drop 80% of background clutter to plain white.
5. **Optional kid-style naive embellishment** — a tiny smiling sun in a window, a blue scribble sea, or a floating heart/sweat drop when it boosts the joke.

## Step 2: Plan Proportional Exaggeration

Do **not** trace realistic anatomy:
- Enlarge heads and eyes (`1.2×–1.5×`), shrink bodies or turn full-body people into stick figures when a big landmark dominates the frame.
- Replace complex textures (leather seats, fur, iron lattice, sunlit water) with 1–2 crude zigzag `fillPoly`/`fillRect` passes plus a few crooked lines.
- Preserve **exact relative positions and signature colors** of the 4–6 anchors (e.g., goggles slightly tilted, blue eyes centered under them, seat on the right, window far right).

## Step 3: Author the Layered JSON Spec

Follow the strict 4-layer order from `references/dsl.md`:
1. **Background hints** (plain white canvas; 3–6 sparse lines + 1 colored window/ground patch).
2. **Color scribble fills** (`fillEllipse`, `fillRect`, `fillPoly` with varied angles and `slop: 2.5–4.0`).
3. **Shaky black outlines** (`double: true` on 1–2 hero features like glasses or body silhouette).
4. **Eyes, nose, crooked mouth, and tiny details** (whiskers, coat buttons, hand/paw lines).

## Step 4: Render, Visually Inspect, and Iterate

Run `scripts/render_doodle.py` and **open the rendered PNG** to critique it
against the original photo:

- **Too generic / unrecognizable?** Strengthen the 2 loudest anchors (e.g., make glasses thicker, add exact fur patches or clothing collar/buttons, fix hair silhouette).
- **Too neat / looks like clip art?** Switch `preset` to `"messy"` or `"crayon"`, increase `spacing` (`4.8–5.5`) and `slop` (`3.5–5.0`), and un-align the eyes by 2–3px.
- **Cluttered / muddy?** Remove secondary lines and open up more pure white background space.
- Stop after 1–2 focused iterations once the before/after punchline hits.
