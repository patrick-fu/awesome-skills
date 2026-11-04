# Eval 03 - mobile overflow

Purpose: the style must survive 390px.

1. Render any produced page with `scripts/render.py`.
2. Pass criteria: no horizontal scrollbar at 390px (inspect the mobile
   screenshot; grids collapse to one column, tables scroll inside their card
   or reflow), stickers and notes remain inside the canvas.

Note: macOS headless Chrome clamps `--window-size` to a 500px minimum, so a
naive 390px run lays out at 500px and crops the PNG. `scripts/render.py`
measures and shoots the mobile view through a same-origin 390px iframe probe
and reports `MEASURE mobile: scrollWidth=...`; treat that line, not the raw
PNG width, as the overflow gate.
