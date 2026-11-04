# Extension · device-real

Realistic device frame plus outside-the-device pencil annotation: show what the
user actually sees, then explain it in the margin.

**Load when** the page explains an app/product experience and the reader must
recognise a real screen — experience walkthroughs, feature explainers,
before/after UI comparisons, bug repros.
**Skip when** the page argues about mechanisms, data or code with no user-facing
screen; a fake device frame around abstract boxes is noise.

## What it may activate (complete allowlist)

- `.pvl-device` (300px wide, 6px `--pvl-device-border`, 2px
  `--pvl-device-frame` outline, radius 48px, `--pvl-shadow-device`) with
  `.pvl-device__status`, `.pvl-device__island`, `.pvl-device__sheet`.
  Width becomes 100% under 640px — do not override that.
- iOS token set for what lives *inside* the frame: `--pvl-ios-blue #007aff`,
  `--pvl-ios-green #34c759`, `--pvl-ios-orange #ff9500`, `--pvl-ios-red #ff3b30`,
  `--pvl-ios-card #ffffff`, `--pvl-ios-gray-bg #f2f2f7`,
  `--pvl-ios-gray-border #e5e5ea`.
- Inside the frame the voice switches to system sans
  (`--pvl-font-sans`, 13–17px): real UI does not speak in the handwritten face.
  `<html data-dense="true">` permits 10.5–13px scan type for in-device system
  UI rows.
- `.pvl-annot` for annotation cards outside the frame: rough radius, 2px pencil
  border, `--pvl-shadow-pencil` (`2.5px 3px 0 rgba(42,42,42,.85)`).
- `--pvl-pen-blue #0066cc` for arrows and connector strokes that point from an
  annotation into the frame.

## What it must never change

- The two voices stay separated: handwritten/display outside the device,
  system sans inside it. Never render the annotated UI in the display face.
- Outside the frame, ink/marker/semantic kit/radii/type floors are core.
- Keep experience detail inside the frame (real labels, real numbers); do not
  replace the screen with a wireframe and then annotate the wireframe.

## Markers it should leave on the page

Pencil annotation cards plus pen-blue arrows are the craft here; add a scribble
on the verdict sentence of the scene. Annotation without any hand-made marker
reads as a product brochure.
