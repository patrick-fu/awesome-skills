#!/usr/bin/env python3
"""Zero-dependency procedural MS Paint & toddler-crayon doodle renderer.

Uses only the Python 3 standard library (zlib, struct, json, math, html) to
render a declarative JSON doodle spec into a crisp nearest-neighbor upscaled PNG
and/or a self-contained interactive HTML5 Canvas page.
"""

from __future__ import annotations

import argparse
import html as html_mod
import json
import math
import struct
import sys
import zlib
from pathlib import Path
from typing import Callable, Dict, List, Optional, Sequence, Tuple

RGB = Tuple[int, int, int]

PRESETS: Dict[str, Dict[str, object]] = {
    "clumsy": {
        "bg": "#ffffff",
        "paper_grain": 0,
        "jitter": 1.8,
        "slop": 3.0,
        "spacing": 4.6,
        "wobble": 0.12,
        "overshoot": 2.2,
        "texture": "pixel",
        "auto_double": False,
    },
    "messy": {
        "bg": "#ffffff",
        "paper_grain": 0,
        "jitter": 2.6,
        "slop": 4.8,
        "spacing": 5.2,
        "wobble": 0.19,
        "overshoot": 3.4,
        "texture": "pixel",
        "auto_double": False,
    },
    "neat-rough": {
        "bg": "#ffffff",
        "paper_grain": 0,
        "jitter": 1.1,
        "slop": 1.8,
        "spacing": 4.0,
        "wobble": 0.07,
        "overshoot": 1.2,
        "texture": "pixel",
        "auto_double": False,
    },
    "crayon": {
        "bg": "#fbf9f2",
        "paper_grain": 6,
        "jitter": 2.3,
        "slop": 4.2,
        "spacing": 4.0,
        "wobble": 0.17,
        "overshoot": 3.0,
        "texture": "crayon",
        "auto_double": False,
    },
    "cursed": {
        "bg": "#ffffff",
        "paper_grain": 0,
        "jitter": 2.4,
        "slop": 4.2,
        "spacing": 4.8,
        "wobble": 0.24,
        "overshoot": 3.8,
        "texture": "pixel",
        "auto_double": True,
    },
}

NAMED_COLORS: Dict[str, str] = {
    "black": "#111111",
    "white": "#ffffff",
    "red": "#ff2a2a",
    "blue": "#1e90ff",
    "green": "#2ecc71",
    "yellow": "#ffe066",
    "orange": "#ff922b",
    "purple": "#9b59b6",
    "pink": "#ff85c0",
    "gray": "#8f9396",
    "grey": "#8f9396",
    "brown": "#8b4513",
    "cyan": "#2eb5ff",
}

# Crisp 5x7 ASCII pixel font (rows of 5 bits, MSB on left)
FONT_5X7: Dict[str, Tuple[int, ...]] = {
    "A": (0b01110, 0b10001, 0b10001, 0b11111, 0b10001, 0b10001, 0b10001),
    "B": (0b11110, 0b10001, 0b10001, 0b11110, 0b10001, 0b10001, 0b11110),
    "C": (0b01110, 0b10001, 0b10000, 0b10000, 0b10000, 0b10001, 0b01110),
    "D": (0b11100, 0b10010, 0b10001, 0b10001, 0b10001, 0b10010, 0b11100),
    "E": (0b11111, 0b10000, 0b10000, 0b11110, 0b10000, 0b10000, 0b11111),
    "F": (0b11111, 0b10000, 0b10000, 0b11110, 0b10000, 0b10000, 0b10000),
    "G": (0b01110, 0b10001, 0b10000, 0b10111, 0b10001, 0b10001, 0b01110),
    "H": (0b10001, 0b10001, 0b10001, 0b11111, 0b10001, 0b10001, 0b10001),
    "I": (0b01110, 0b00100, 0b00100, 0b00100, 0b00100, 0b00100, 0b01110),
    "J": (0b00111, 0b00010, 0b00010, 0b00010, 0b10010, 0b10010, 0b01100),
    "K": (0b10001, 0b10010, 0b10100, 0b11000, 0b10100, 0b10010, 0b10001),
    "L": (0b10000, 0b10000, 0b10000, 0b10000, 0b10000, 0b10000, 0b11111),
    "M": (0b10001, 0b11011, 0b10101, 0b10101, 0b10001, 0b10001, 0b10001),
    "N": (0b10001, 0b11001, 0b10101, 0b10011, 0b10001, 0b10001, 0b10001),
    "O": (0b01110, 0b10001, 0b10001, 0b10001, 0b10001, 0b10001, 0b01110),
    "P": (0b11110, 0b10001, 0b10001, 0b11110, 0b10000, 0b10000, 0b10000),
    "Q": (0b01110, 0b10001, 0b10001, 0b10001, 0b10101, 0b10010, 0b01101),
    "R": (0b11110, 0b10001, 0b10001, 0b11110, 0b10100, 0b10010, 0b10001),
    "S": (0b01111, 0b10000, 0b10000, 0b01110, 0b00001, 0b00001, 0b11110),
    "T": (0b11111, 0b00100, 0b00100, 0b00100, 0b00100, 0b00100, 0b00100),
    "U": (0b10001, 0b10001, 0b10001, 0b10001, 0b10001, 0b10001, 0b01110),
    "V": (0b10001, 0b10001, 0b10001, 0b10001, 0b10001, 0b01010, 0b00100),
    "W": (0b10001, 0b10001, 0b10001, 0b10101, 0b10101, 0b11011, 0b10001),
    "X": (0b10001, 0b10001, 0b01010, 0b00100, 0b01010, 0b10001, 0b10001),
    "Y": (0b10001, 0b10001, 0b01010, 0b00100, 0b00100, 0b00100, 0b00100),
    "Z": (0b11111, 0b00001, 0b00010, 0b00100, 0b01000, 0b10000, 0b11111),
    "0": (0b01110, 0b10001, 0b10011, 0b10101, 0b11001, 0b10001, 0b01110),
    "1": (0b00100, 0b01100, 0b00100, 0b00100, 0b00100, 0b00100, 0b01110),
    "2": (0b01110, 0b10001, 0b00001, 0b00110, 0b01000, 0b10000, 0b11111),
    "3": (0b11110, 0b00001, 0b00001, 0b01110, 0b00001, 0b00001, 0b11110),
    "4": (0b00010, 0b00110, 0b01010, 0b10010, 0b11111, 0b00010, 0b00010),
    "5": (0b11111, 0b10000, 0b11110, 0b00001, 0b00001, 0b10001, 0b01110),
    "6": (0b01110, 0b10000, 0b11110, 0b10001, 0b10001, 0b10001, 0b01110),
    "7": (0b11111, 0b00001, 0b00010, 0b00100, 0b01000, 0b01000, 0b01000),
    "8": (0b01110, 0b10001, 0b10001, 0b01110, 0b10001, 0b10001, 0b01110),
    "9": (0b01110, 0b10001, 0b10001, 0b01111, 0b00001, 0b00010, 0b01100),
    " ": (0, 0, 0, 0, 0, 0, 0),
    "!": (0b00100, 0b00100, 0b00100, 0b00100, 0b00100, 0b00000, 0b00100),
    "?": (0b01110, 0b10001, 0b00001, 0b00110, 0b00100, 0b00000, 0b00100),
    ".": (0b00000, 0b00000, 0b00000, 0b00000, 0b00000, 0b01100, 0b01100),
    ",": (0b00000, 0b00000, 0b00000, 0b00000, 0b00100, 0b00100, 0b01000),
    ":": (0b00000, 0b00100, 0b00100, 0b00000, 0b00100, 0b00100, 0b00000),
    ";": (0b00000, 0b00100, 0b00100, 0b00000, 0b00100, 0b00100, 0b01000),
    "-": (0b00000, 0b00000, 0b00000, 0b11111, 0b00000, 0b00000, 0b00000),
    "+": (0b00000, 0b00100, 0b00100, 0b11111, 0b00100, 0b00100, 0b00000),
    "=": (0b00000, 0b00000, 0b11111, 0b00000, 0b11111, 0b00000, 0b00000),
    "/": (0b00001, 0b00010, 0b00010, 0b00100, 0b01000, 0b01000, 0b10000),
    "'": (0b00100, 0b00100, 0b01000, 0b00000, 0b00000, 0b00000, 0b00000),
    '"': (0b01010, 0b01010, 0b00000, 0b00000, 0b00000, 0b00000, 0b00000),
    "(": (0b00010, 0b00100, 0b01000, 0b01000, 0b01000, 0b00100, 0b00010),
    ")": (0b01000, 0b00100, 0b00010, 0b00010, 0b00010, 0b00100, 0b01000),
    "_": (0b00000, 0b00000, 0b00000, 0b00000, 0b00000, 0b00000, 0b11111),
    "#": (0b01010, 0b11111, 0b01010, 0b01010, 0b11111, 0b01010, 0b00000),
    "$": (0b00100, 0b01111, 0b10100, 0b01110, 0b00101, 0b11110, 0b00100),
    "%": (0b11001, 0b11010, 0b00010, 0b00100, 0b01000, 0b01011, 0b10011),
    "@": (0b01110, 0b10001, 0b10111, 0b10101, 0b10110, 0b10000, 0b01110),
    "&": (0b01100, 0b10010, 0b10100, 0b01000, 0b10101, 0b10010, 0b01101),
    "*": (0b00000, 0b10101, 0b01110, 0b11111, 0b01110, 0b10101, 0b00000),
    "~": (0b00000, 0b00000, 0b01001, 0b10110, 0b00000, 0b00000, 0b00000),
}


def parse_color(val: Optional[str], default: str = "#111111") -> RGB:
    s = (val or default).strip().lower()
    s = NAMED_COLORS.get(s, s)
    if s.startswith("#"):
        s = s[1:]
    if len(s) == 3:
        s = "".join(c * 2 for c in s)
    if len(s) != 6:
        raise ValueError(f"Unsupported color: {val!r}")
    return (int(s[0:2], 16), int(s[2:4], 16), int(s[4:6], 16))


def clamp_byte(v: float) -> int:
    return 0 if v < 0 else (255 if v > 255 else int(v))


class LcgRng:
    def __init__(self, seed: int) -> None:
        self.state = (int(seed) & 0xFFFFFFFF) or 1

    def next(self) -> float:
        self.state = (self.state * 1664525 + 1013904223) & 0xFFFFFFFF
        return self.state / 4294967296.0

    def rand(self, a: float, b: float) -> float:
        return a + self.next() * (b - a)


def point_in_poly(px: float, py: float, pts: Sequence[Sequence[float]]) -> bool:
    inside = False
    n = len(pts)
    j = n - 1
    for i in range(n):
        xi, yi = pts[i][0], pts[i][1]
        xj, yj = pts[j][0], pts[j][1]
        if ((yi > py) != (yj > py)) and (px < ((xj - xi) * (py - yi)) / (yj - yi + 1e-9) + xi):
            inside = not inside
        j = i
    return inside


class DoodleRenderer:
    def __init__(self, spec: Dict[str, object]) -> None:
        self.spec = spec
        self.w = int(spec.get("width", 240))
        self.h = int(spec.get("height", 240))
        preset_name = str(spec.get("preset", "clumsy"))
        self.preset = PRESETS.get(preset_name, PRESETS["clumsy"])
        self.rng = LcgRng(int(spec.get("seed", 42)))
        bg = parse_color(str(spec.get("bg") or self.preset["bg"]), "#ffffff")
        self.buf = bytearray(self.w * self.h * 3)
        grain = int(self.preset["paper_grain"])
        if grain > 0:
            idx = 0
            for _ in range(self.w * self.h):
                g = int(self.rng.rand(-grain, grain + 0.99))
                self.buf[idx] = clamp_byte(bg[0] + g)
                self.buf[idx + 1] = clamp_byte(bg[1] + g)
                self.buf[idx + 2] = clamp_byte(bg[2] + g)
                idx += 3
        else:
            row = bytes(bg) * self.w
            for y in range(self.h):
                self.buf[y * self.w * 3 : (y + 1) * self.w * 3] = row

    def set_px(self, x: int, y: int, col: RGB) -> None:
        if 0 <= x < self.w and 0 <= y < self.h:
            i = (y * self.w + x) * 3
            self.buf[i] = col[0]
            self.buf[i + 1] = col[1]
            self.buf[i + 2] = col[2]

    def dot(self, x: float, y: float, size: int, col: RGB, texture: str = "pixel") -> None:
        ix = int(round(x))
        iy = int(round(y))
        if texture == "crayon":
            r = max(1, (size + 1) // 2)
            r2 = r * r + 0.6
            for dy in range(-r, r + 1):
                for dx in range(-r, r + 1):
                    d2 = dx * dx + dy * dy
                    if d2 <= r2:
                        # Dry wax grain: skip outer/random specks so paper texture peeks through
                        keep = 0.82 if d2 <= r2 * 0.45 else 0.56
                        if self.rng.next() < keep:
                            v = int(self.rng.rand(-14, 15))
                            self.set_px(
                                ix + dx,
                                iy + dy,
                                (clamp_byte(col[0] + v), clamp_byte(col[1] + v), clamp_byte(col[2] + v)),
                            )
            return

        if size <= 1:
            self.set_px(ix, iy, col)
            return
        if size == 2:
            self.set_px(ix, iy, col)
            self.set_px(ix + 1, iy, col)
            self.set_px(ix, iy + 1, col)
            self.set_px(ix + 1, iy + 1, col)
            return
        r = size // 2
        r2 = r * r + 0.5
        for dy in range(-r, r + 1):
            for dx in range(-r, r + 1):
                if dx * dx + dy * dy <= r2:
                    self.set_px(ix + dx, iy + dy, col)

    def raw_line(self, x0: float, y0: float, x1: float, y1: float, size: int, col: RGB, texture: str) -> None:
        ix0, iy0 = int(round(x0)), int(round(y0))
        ix1, iy1 = int(round(x1)), int(round(y1))
        dx = abs(ix1 - ix0)
        dy = abs(iy1 - iy0)
        sx = 1 if ix0 < ix1 else -1
        sy = 1 if iy0 < iy1 else -1
        err = dx - dy
        while True:
            self.dot(ix0, iy0, size, col, texture)
            if ix0 == ix1 and iy0 == iy1:
                break
            e2 = 2 * err
            if e2 > -dy:
                err -= dy
                ix0 += sx
            if e2 < dx:
                err += dx
                iy0 += sy

    def shaky_line(self, pts: Sequence[Sequence[float]], op: Dict[str, object]) -> None:
        if not pts or len(pts) < 2:
            return
        col = parse_color(op.get("color"), "#111111")  # type: ignore[arg-type]
        size = int(op.get("size", 2))
        jitter = float(op.get("jitter", self.preset["jitter"]))
        step = float(op.get("step", 6.0))
        overshoot = float(op.get("overshoot", self.preset["overshoot"]))
        texture = str(op.get("texture", self.preset["texture"]))

        out: List[Tuple[float, float]] = []
        drift_x = 0.0
        drift_y = 0.0
        last_seg = len(pts) - 2
        for i in range(len(pts) - 1):
            x0, y0 = float(pts[i][0]), float(pts[i][1])
            x1, y1 = float(pts[i + 1][0]), float(pts[i + 1][1])
            seg_len = math.hypot(x1 - x0, y1 - y0) or 1.0
            if i == 0 and overshoot:
                ov = self.rng.rand(-0.8, overshoot)
                x0 -= ((x1 - x0) / seg_len) * ov
                y0 -= ((y1 - y0) / seg_len) * ov
            if i == last_seg and overshoot:
                ov = self.rng.rand(-0.8, overshoot)
                x1 += ((x1 - x0) / seg_len) * ov
                y1 += ((y1 - y0) / seg_len) * ov
            n = max(2, int(math.ceil(math.hypot(x1 - x0, y1 - y0) / step)))
            for k in range(n + 1):
                if i > 0 and k == 0:
                    continue
                t = k / n
                drift_x = drift_x * 0.65 + self.rng.rand(-jitter, jitter) * 0.55
                drift_y = drift_y * 0.65 + self.rng.rand(-jitter, jitter) * 0.55
                out.append(
                    (
                        x0 + (x1 - x0) * t + drift_x + self.rng.rand(-jitter * 0.5, jitter * 0.5),
                        y0 + (y1 - y0) * t + drift_y + self.rng.rand(-jitter * 0.5, jitter * 0.5),
                    )
                )
        for i in range(len(out) - 1):
            self.raw_line(out[i][0], out[i][1], out[i + 1][0], out[i + 1][1], size, col, texture)

    def shaky_ellipse(self, op: Dict[str, object]) -> None:
        steps = int(op.get("steps", 22))
        start = float(op.get("start", 0.0))
        end_val = op.get("end")
        end = float(end_val) if end_val is not None else (math.pi * 2.0 + self.rng.rand(-0.22, 0.34))
        wobble = float(op.get("wobble", self.preset["wobble"]))
        cx, cy = float(op["cx"]), float(op["cy"])
        rx, ry = float(op["rx"]), float(op["ry"])
        p1 = self.rng.rand(0.0, 6.28)
        p2 = self.rng.rand(0.0, 6.28)
        pts = []
        for i in range(steps + 1):
            a = start + (end - start) * (i / steps)
            mod = 1.0 + wobble * math.sin(a * 2.0 + p1) + wobble * 0.55 * math.cos(a * 3.0 + p2)
            pts.append((cx + math.cos(a) * rx * mod, cy + math.sin(a) * ry * mod))
        self.shaky_line(pts, op)

    def scribble_fill(
        self,
        bx: float,
        by: float,
        bw: float,
        bh: float,
        inside_fn: Callable[[float, float], bool],
        op: Dict[str, object],
    ) -> None:
        color = str(op.get("color", "#ffe066"))
        size = int(op.get("size", 3))
        spacing = float(op.get("spacing", self.preset["spacing"]))
        angle = float(op.get("angle", -0.45))
        slop = float(op.get("slop", self.preset["slop"]))
        texture = str(op.get("texture", self.preset["texture"]))

        cos_a, sin_a = math.cos(angle), math.sin(angle)
        cx, cy = bx + bw / 2.0, by + bh / 2.0
        diag = math.hypot(bw, bh)
        direction = 1
        prev: Optional[Tuple[float, float]] = None
        u = -diag / 2.0
        while u <= diag / 2.0:
            hits: List[Tuple[float, float]] = []
            v = -diag / 2.0
            while v <= diag / 2.0:
                px = cx + u * cos_a - v * sin_a
                py = cy + u * sin_a + v * cos_a
                if inside_fn(px, py):
                    hits.append((px, py))
                v += 2.2
            if len(hits) < 2:
                prev = None
            else:
                pa = hits[0] if direction > 0 else hits[-1]
                pb = hits[-1] if direction > 0 else hits[0]
                a = (pa[0] + self.rng.rand(-slop, slop), pa[1] + self.rng.rand(-slop, slop))
                b = (pb[0] + self.rng.rand(-slop, slop), pb[1] + self.rng.rand(-slop, slop))
                if prev is not None and math.hypot(prev[0] - a[0], prev[1] - a[1]) < 24.0 and self.rng.next() < 0.72:
                    self.shaky_line(
                        [prev, a],
                        {"color": color, "size": size, "jitter": 0.9, "step": 7, "overshoot": 0, "texture": texture},
                    )
                self.shaky_line(
                    [a, b],
                    {"color": color, "size": size, "jitter": 1.3, "step": 8, "overshoot": 1.4, "texture": texture},
                )
                prev = b
                direction *= -1
            u += max(1.5, spacing + self.rng.rand(-0.9, 1.1))

    def draw_label(self, op: Dict[str, object]) -> None:
        text = str(op.get("text", "")).upper()
        x0 = int(round(float(op.get("x", 0))))
        y0 = int(round(float(op.get("y", 0))))
        scale = max(1, int(op.get("scale", 2)))
        jitter = float(op.get("jitter", 1.0))
        col = parse_color(op.get("color"), "#111111")  # type: ignore[arg-type]
        texture = str(op.get("texture", self.preset["texture"]))

        cursor_x = x0
        for ch in text:
            glyph = FONT_5X7.get(ch, FONT_5X7["?"])
            dy_j = int(round(self.rng.rand(-jitter, jitter))) if jitter > 0 else 0
            for row_idx, bits in enumerate(glyph):
                for col_idx in range(5):
                    if bits & (1 << (4 - col_idx)):
                        for sy in range(scale):
                            for sx in range(scale):
                                px = cursor_x + col_idx * scale + sx
                                py = y0 + row_idx * scale + sy + dy_j
                                if texture == "crayon" and self.rng.next() < 0.14:
                                    continue
                                self.set_px(px, py, col)
            cursor_x += 6 * scale

    def render(self) -> None:
        auto_double = bool(self.preset["auto_double"])
        for op in self.spec.get("ops", []):  # type: ignore[attr-defined]
            kind = op.get("op")
            passes = 2 if (op.get("double") or (auto_double and kind in ("rect", "ellipse", "line"))) else 1
            if kind == "fillRect":
                x, y, w, h = float(op["x"]), float(op["y"]), float(op["w"]), float(op["h"])
                self.scribble_fill(x, y, w, h, lambda px, py, x=x, y=y, w=w, h=h: x <= px <= x + w and y <= py <= y + h, op)
            elif kind == "fillEllipse":
                cx, cy = float(op["cx"]), float(op["cy"])
                rx, ry = float(op["rx"]) or 1.0, float(op["ry"]) or 1.0
                self.scribble_fill(
                    cx - rx,
                    cy - ry,
                    rx * 2.0,
                    ry * 2.0,
                    lambda px, py, cx=cx, cy=cy, rx=rx, ry=ry: ((px - cx) / rx) ** 2 + ((py - cy) / ry) ** 2 <= 1.0,
                    op,
                )
            elif kind == "fillPoly":
                pts = op["points"]
                xs = [float(p[0]) for p in pts]
                ys = [float(p[1]) for p in pts]
                min_x, min_y = min(xs), min(ys)
                self.scribble_fill(
                    min_x,
                    min_y,
                    max(xs) - min_x,
                    max(ys) - min_y,
                    lambda px, py, pts=pts: point_in_poly(px, py, pts),
                    op,
                )
            elif kind == "line":
                for _ in range(passes):
                    self.shaky_line(op["points"], op)
            elif kind == "rect":
                x, y, w, h = float(op["x"]), float(op["y"]), float(op["w"]), float(op["h"])
                pts = [(x, y), (x + w, y), (x + w, y + h), (x, y + h), (x, y)]
                for _ in range(passes):
                    self.shaky_line(pts, op)
            elif kind == "ellipse":
                for _ in range(passes):
                    self.shaky_ellipse(op)
            elif kind == "arrow":
                pts = op["points"]
                self.shaky_line(pts, op)
                if len(pts) >= 2:
                    x0, y0 = float(pts[-2][0]), float(pts[-2][1])
                    x1, y1 = float(pts[-1][0]), float(pts[-1][1])
                    ang = math.atan2(y1 - y0, x1 - x0)
                    hl = float(op.get("head", 10.0))
                    head_pts = [
                        (x1 - math.cos(ang - 0.55) * hl, y1 - math.sin(ang - 0.55) * hl),
                        (x1, y1),
                        (x1 - math.cos(ang + 0.55) * hl, y1 - math.sin(ang + 0.55) * hl),
                    ]
                    self.shaky_line(head_pts, {**op, "overshoot": 0.6})
            elif kind == "dot":
                col = parse_color(op.get("color"), "#111111")
                self.dot(
                    float(op["x"]),
                    float(op["y"]),
                    int(op.get("size", 3)),
                    col,
                    str(op.get("texture", self.preset["texture"])),
                )
            elif kind == "label":
                self.draw_label(op)
            elif kind == "bubble":
                x, y, w, h = float(op["x"]), float(op["y"]), float(op["w"]), float(op["h"])
                fill_col = str(op.get("fill", "#ffffff"))
                stroke_col = str(op.get("color", "#111111"))
                self.scribble_fill(
                    x,
                    y,
                    w,
                    h,
                    lambda px, py, x=x, y=y, w=w, h=h: x <= px <= x + w and y <= py <= y + h,
                    {**op, "color": fill_col, "angle": 0.08, "spacing": float(op.get("spacing", 3.6)), "slop": 1.8},
                )
                box_pts = [(x, y), (x + w, y), (x + w, y + h), (x, y + h), (x, y)]
                self.shaky_line(box_pts, {**op, "color": stroke_col, "size": int(op.get("size", 2))})
                tail = op.get("tail")
                if tail and len(tail) == 2:
                    tx, ty = float(tail[0]), float(tail[1])
                    anchor_x = max(x + 8.0, min(x + w - 8.0, tx))
                    anchor_y = y + h if ty >= y + h / 2.0 else y
                    self.shaky_line(
                        [(anchor_x - 5.0, anchor_y), (tx, ty), (anchor_x + 5.0, anchor_y)],
                        {**op, "color": stroke_col, "size": int(op.get("size", 2)), "overshoot": 0.6},
                    )
                text = str(op.get("text", ""))
                if text:
                    sc = max(1, int(op.get("scale", 1)))
                    tw = max(0, len(text) * 6 * sc - sc)
                    th = 7 * sc
                    self.draw_label(
                        {
                            "x": x + max(4.0, (w - tw) / 2.0),
                            "y": y + max(4.0, (h - th) / 2.0),
                            "text": text,
                            "scale": sc,
                            "color": str(op.get("textColor", stroke_col)),
                            "jitter": float(op.get("jitter", 0.8)),
                            "texture": str(op.get("texture", self.preset["texture"])),
                        }
                    )

    def to_png_bytes(self, scale: int = 4) -> bytes:
        scale = max(1, int(scale))
        out_w = self.w * scale
        out_h = self.h * scale
        raw = bytearray()
        for y in range(self.h):
            row_start = y * self.w * 3
            if scale == 1:
                scaled_row = bytes(self.buf[row_start : row_start + self.w * 3])
            else:
                line = bytearray(out_w * 3)
                dst = 0
                for x in range(self.w):
                    src = row_start + x * 3
                    r, g, b = self.buf[src], self.buf[src + 1], self.buf[src + 2]
                    for _ in range(scale):
                        line[dst] = r
                        line[dst + 1] = g
                        line[dst + 2] = b
                        dst += 3
                scaled_row = bytes(line)
            for _ in range(scale):
                raw.append(0)  # PNG filter type 0 (None)
                raw.extend(scaled_row)

        def chunk(tag: bytes, data: bytes) -> bytes:
            return (
                struct.pack("!I", len(data))
                + tag
                + data
                + struct.pack("!I", zlib.crc32(tag + data) & 0xFFFFFFFF)
            )

        ihdr = struct.pack("!IIBBBBB", out_w, out_h, 8, 2, 0, 0, 0)
        idat = zlib.compress(bytes(raw), level=6)
        return b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", ihdr) + chunk(b"IDAT", idat) + chunk(b"IEND", b"")


def build_standalone_html(spec: Dict[str, object], title: str = "Clumsy Doodle") -> str:
    w = int(spec.get("width", 240))
    h = int(spec.get("height", 240))
    spec_json = json.dumps(spec, ensure_ascii=False, indent=2).replace("</", "<\\/")
    safe_title = html_mod.escape(title)
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width,initial-scale=1" />
<title>{safe_title}</title>
<style>
  * {{ box-sizing: border-box; }}
  body {{
    margin: 0; padding: 20px; background: #f6f4ef; color: #222;
    font-family: ui-monospace, SFMono-Regular, Menlo, monospace;
    display: flex; flex-direction: column; align-items: center; gap: 12px;
  }}
  .frame {{
    width: min(100%, 480px); background: #fff; border: 2px solid #222;
    border-radius: 10px; overflow: hidden; box-shadow: 4px 5px 0 rgba(0,0,0,.14);
  }}
  canvas {{
    display: block; width: 100%; height: auto;
    image-rendering: pixelated; image-rendering: crisp-edges;
  }}
  .bar {{ display: flex; gap: 8px; flex-wrap: wrap; justify-content: center; }}
  button {{
    font: 700 12px/1 ui-monospace, Menlo, monospace; padding: 8px 14px;
    border: 2px solid #222; border-radius: 999px; background: #fff; cursor: pointer;
    box-shadow: 2px 2px 0 rgba(0,0,0,.12);
  }}
  button:active {{ transform: translate(1px, 1px); }}
</style>
</head>
<body>
  <div class="frame"><canvas id="doodle" width="{w}" height="{h}"></canvas></div>
  <div class="bar">
    <button id="reroll">Reroll Seed</button>
    <button id="save">Download PNG</button>
  </div>
<script id="doodle-spec" type="application/json">
{spec_json}
</script>
<script>
(() => {{
  const PRESETS = {{
    clumsy:       {{ bg:'#ffffff', paper_grain:0, jitter:1.8, slop:3.0, spacing:4.6, wobble:0.12, overshoot:2.2, texture:'pixel', auto_double:false }},
    messy:        {{ bg:'#ffffff', paper_grain:0, jitter:2.6, slop:4.8, spacing:5.2, wobble:0.19, overshoot:3.4, texture:'pixel', auto_double:false }},
    'neat-rough': {{ bg:'#ffffff', paper_grain:0, jitter:1.1, slop:1.8, spacing:4.0, wobble:0.07, overshoot:1.2, texture:'pixel', auto_double:false }},
    crayon:       {{ bg:'#fbf9f2', paper_grain:6, jitter:2.3, slop:4.2, spacing:4.0, wobble:0.17, overshoot:3.0, texture:'crayon', auto_double:false }},
    cursed:       {{ bg:'#ffffff', paper_grain:0, jitter:2.4, slop:4.2, spacing:4.8, wobble:0.24, overshoot:3.8, texture:'pixel', auto_double:true }},
  }};
  const makeRng = (seed) => {{ let s = (seed >>> 0) || 1; return () => ((s = (s * 1664525 + 1013904223) >>> 0) / 4294967296); }};
  const inPoly = (px, py, pts) => {{
    let inside = false;
    for (let i = 0, j = pts.length - 1; i < pts.length; j = i++) {{
      const [xi, yi] = pts[i], [xj, yj] = pts[j];
      if (((yi > py) !== (yj > py)) && (px < ((xj - xi) * (py - yi)) / (yj - yi + 1e-9) + xi)) inside = !inside;
    }}
    return inside;
  }};
  function render(canvas, spec) {{
    const ctx = canvas.getContext('2d');
    const w = canvas.width, h = canvas.height;
    const preset = PRESETS[spec.preset] || PRESETS.clumsy;
    const rng = makeRng(spec.seed ?? 42);
    const rand = (a, b) => a + rng() * (b - a);
    ctx.fillStyle = spec.bg || preset.bg;
    ctx.fillRect(0, 0, w, h);
    function dot(x, y, size, color, texture) {{
      const ix = Math.round(x), iy = Math.round(y);
      ctx.fillStyle = color;
      if (texture === 'crayon') {{
        const r = Math.max(1, Math.floor((size + 1) / 2)), r2 = r * r + 0.6;
        for (let dy = -r; dy <= r; dy++) for (let dx = -r; dx <= r; dx++) {{
          const d2 = dx * dx + dy * dy;
          if (d2 <= r2 && rng() < (d2 <= r2 * 0.45 ? 0.82 : 0.56)) ctx.fillRect(ix + dx, iy + dy, 1, 1);
        }}
        return;
      }}
      if (size <= 1) {{ ctx.fillRect(ix, iy, 1, 1); return; }}
      if (size === 2) {{ ctx.fillRect(ix, iy, 2, 2); return; }}
      const r = Math.floor(size / 2);
      for (let dy = -r; dy <= r; dy++) for (let dx = -r; dx <= r; dx++) if (dx*dx + dy*dy <= r*r + 0.5) ctx.fillRect(ix+dx, iy+dy, 1, 1);
    }}
    function rawLine(x0, y0, x1, y1, size, color, texture) {{
      x0 = Math.round(x0); y0 = Math.round(y0); x1 = Math.round(x1); y1 = Math.round(y1);
      const dx = Math.abs(x1 - x0), dy = Math.abs(y1 - y0), sx = x0 < x1 ? 1 : -1, sy = y0 < y1 ? 1 : -1;
      let err = dx - dy;
      while (true) {{
        dot(x0, y0, size, color, texture);
        if (x0 === x1 && y0 === y1) break;
        const e2 = 2 * err;
        if (e2 > -dy) {{ err -= dy; x0 += sx; }}
        if (e2 < dx) {{ err += dx; y0 += sy; }}
      }}
    }}
    function shakyLine(pts, op = {{}}) {{
      if (!pts || pts.length < 2) return;
      const color = op.color || '#111111', size = op.size ?? 2, jitter = op.jitter ?? preset.jitter;
      const step = op.step ?? 6, overshoot = op.overshoot ?? preset.overshoot, texture = op.texture || preset.texture;
      const out = []; let dx = 0, dy = 0;
      for (let i = 0; i < pts.length - 1; i++) {{
        let [x0, y0] = pts[i], [x1, y1] = pts[i + 1];
        const len = Math.hypot(x1 - x0, y1 - y0) || 1;
        if (i === 0 && overshoot) {{ const ov = rand(-0.8, overshoot); x0 -= ((x1-x0)/len)*ov; y0 -= ((y1-y0)/len)*ov; }}
        if (i === pts.length - 2 && overshoot) {{ const ov = rand(-0.8, overshoot); x1 += ((x1-x0)/len)*ov; y1 += ((y1-y0)/len)*ov; }}
        const n = Math.max(2, Math.ceil(Math.hypot(x1 - x0, y1 - y0) / step));
        for (let k = 0; k <= n; k++) {{
          if (i > 0 && k === 0) continue;
          const t = k / n;
          dx = dx * 0.65 + rand(-jitter, jitter) * 0.55; dy = dy * 0.65 + rand(-jitter, jitter) * 0.55;
          out.push([x0 + (x1 - x0) * t + dx + rand(-jitter*0.5, jitter*0.5), y0 + (y1 - y0) * t + dy + rand(-jitter*0.5, jitter*0.5)]);
        }}
      }}
      for (let i = 0; i < out.length - 1; i++) rawLine(out[i][0], out[i][1], out[i+1][0], out[i+1][1], size, color, texture);
    }}
    function shakyEllipse(op) {{
      const steps = op.steps ?? 22, start = op.start ?? 0, end = op.end ?? (Math.PI * 2 + rand(-0.22, 0.34));
      const wobble = op.wobble ?? preset.wobble, p1 = rand(0, 6.28), p2 = rand(0, 6.28), pts = [];
      for (let i = 0; i <= steps; i++) {{
        const a = start + (end - start) * (i / steps);
        const mod = 1 + wobble * Math.sin(a * 2 + p1) + wobble * 0.55 * Math.cos(a * 3 + p2);
        pts.push([op.cx + Math.cos(a) * op.rx * mod, op.cy + Math.sin(a) * op.ry * mod]);
      }}
      shakyLine(pts, op);
    }}
    function scribbleFill(b, insideFn, op) {{
      const color = op.color || '#ffe066', size = op.size ?? 3, spacing = op.spacing ?? preset.spacing;
      const angle = op.angle ?? -0.45, slop = op.slop ?? preset.slop, texture = op.texture || preset.texture;
      const cos = Math.cos(angle), sin = Math.sin(angle), cx = b.x + b.w / 2, cy = b.y + b.h / 2, diag = Math.hypot(b.w, b.h);
      let dir = 1, prev = null;
      for (let u = -diag / 2; u <= diag / 2; u += Math.max(1.5, spacing + rand(-0.9, 1.1))) {{
        const hits = [];
        for (let v = -diag / 2; v <= diag / 2; v += 2.2) {{
          const px = cx + u * cos - v * sin, py = cy + u * sin + v * cos;
          if (insideFn(px, py)) hits.push([px, py]);
        }}
        if (hits.length < 2) {{ prev = null; continue; }}
        const pA = dir > 0 ? hits[0] : hits[hits.length - 1], pB = dir > 0 ? hits[hits.length - 1] : hits[0];
        const a = [pA[0] + rand(-slop, slop), pA[1] + rand(-slop, slop)], bb = [pB[0] + rand(-slop, slop), pB[1] + rand(-slop, slop)];
        if (prev && Math.hypot(prev[0]-a[0], prev[1]-a[1]) < 24 && rng() < 0.72) shakyLine([prev, a], {{ color, size, jitter:0.9, step:7, overshoot:0, texture }});
        shakyLine([a, bb], {{ color, size, jitter:1.3, step:8, overshoot:1.4, texture }});
        prev = bb; dir *= -1;
      }}
    }}
    for (const op of spec.ops || []) {{
      const passes = (op.double || (preset.auto_double && ['rect','ellipse','line'].includes(op.op))) ? 2 : 1;
      if (op.op === 'fillRect') scribbleFill(op, (px, py) => px >= op.x && px <= op.x + op.w && py >= op.y && py <= op.y + op.h, op);
      else if (op.op === 'fillEllipse') scribbleFill({{ x:op.cx-op.rx, y:op.cy-op.ry, w:op.rx*2, h:op.ry*2 }}, (px, py) => ((px-op.cx)/(op.rx||1))**2 + ((py-op.cy)/(op.ry||1))**2 <= 1, op);
      else if (op.op === 'fillPoly') {{
        const xs = op.points.map(p=>p[0]), ys = op.points.map(p=>p[1]), mx = Math.min(...xs), my = Math.min(...ys);
        scribbleFill({{ x:mx, y:my, w:Math.max(...xs)-mx, h:Math.max(...ys)-my }}, (px, py) => inPoly(px, py, op.points), op);
      }}
      else if (op.op === 'line') {{ for (let k = 0; k < passes; k++) shakyLine(op.points, op); }}
      else if (op.op === 'rect') {{
        const pts = [[op.x,op.y],[op.x+op.w,op.y],[op.x+op.w,op.y+op.h],[op.x,op.y+op.h],[op.x,op.y]];
        for (let k = 0; k < passes; k++) shakyLine(pts, op);
      }}
      else if (op.op === 'ellipse') {{ for (let k = 0; k < passes; k++) shakyEllipse(op); }}
      else if (op.op === 'arrow') {{
        shakyLine(op.points, op);
        if (op.points.length >= 2) {{
          const [x0, y0] = op.points[op.points.length - 2], [x1, y1] = op.points[op.points.length - 1];
          const a = Math.atan2(y1 - y0, x1 - x0), hl = op.head ?? 10;
          shakyLine([[x1-Math.cos(a-0.55)*hl,y1-Math.sin(a-0.55)*hl],[x1,y1],[x1-Math.cos(a+0.55)*hl,y1-Math.sin(a+0.55)*hl]], {{ ...op, overshoot:0.6 }});
        }}
      }}
      else if (op.op === 'dot') dot(op.x, op.y, op.size ?? 3, op.color || '#111111', op.texture || preset.texture);
      else if (op.op === 'label') {{
        ctx.fillStyle = op.color || '#111111';
        ctx.font = `700 ${{(op.scale ?? 2) * 7}}px "Comic Sans MS","Chalkboard SE",monospace`;
        ctx.fillText(String(op.text || ''), Math.round(op.x), Math.round(op.y) + (op.scale ?? 2) * 6);
      }}
      else if (op.op === 'bubble') {{
        const fill = op.fill || '#ffffff', stroke = op.color || '#111111';
        scribbleFill(op, (px, py) => px >= op.x && px <= op.x + op.w && py >= op.y && py <= op.y + op.h, {{ ...op, color:fill, angle:0.08, spacing:3.6, slop:1.8 }});
        shakyLine([[op.x,op.y],[op.x+op.w,op.y],[op.x+op.w,op.y+op.h],[op.x,op.y+op.h],[op.x,op.y]], {{ ...op, color:stroke, size:op.size ?? 2 }});
        if (op.tail && op.tail.length === 2) {{
          const [tx, ty] = op.tail, ax = Math.max(op.x+8, Math.min(op.x+op.w-8, tx)), ay = ty >= op.y+op.h/2 ? op.y+op.h : op.y;
          shakyLine([[ax-5, ay], [tx, ty], [ax+5, ay]], {{ ...op, color:stroke, size:op.size ?? 2, overshoot:0.6 }});
        }}
        if (op.text) {{
          ctx.fillStyle = op.textColor || stroke;
          const fs = Math.max(10, (op.scale ?? 1) * 11);
          ctx.font = `700 ${{fs}}px "Comic Sans MS","Chalkboard SE",monospace`;
          ctx.textAlign = 'center'; ctx.textBaseline = 'middle';
          ctx.fillText(String(op.text), Math.round(op.x + op.w / 2), Math.round(op.y + op.h / 2));
          ctx.textAlign = 'start'; ctx.textBaseline = 'alphabetic';
        }}
      }}
    }}
  }}
  const baseSpec = JSON.parse(document.getElementById('doodle-spec').textContent);
  const canvas = document.getElementById('doodle');
  let seed = baseSpec.seed ?? 42;
  const draw = () => render(canvas, {{ ...baseSpec, seed }});
  draw();
  document.getElementById('reroll').onclick = () => {{ seed = (seed * 31 + 17) % 99991; draw(); }};
  document.getElementById('save').onclick = () => {{
    const out = document.createElement('canvas');
    const sc = baseSpec.scale ?? 4;
    out.width = canvas.width * sc; out.height = canvas.height * sc;
    const octx = out.getContext('2d');
    octx.imageSmoothingEnabled = false;
    octx.drawImage(canvas, 0, 0, out.width, out.height);
    const a = document.createElement('a'); a.download = 'clumsy-doodle.png'; a.href = out.toDataURL('image/png'); a.click();
  }};
}})();
</script>
</body>
</html>
"""


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = argparse.ArgumentParser(
        description="Render a clumsy MS Paint or toddler-crayon doodle JSON spec to PNG / HTML (zero dependencies)."
    )
    parser.add_argument("spec", help="Path to JSON spec file, or '-' to read from stdin.")
    parser.add_argument("-o", "--output", help="Output PNG file path.")
    parser.add_argument("--html", help="Optional standalone interactive HTML output path.")
    parser.add_argument("--preset", choices=sorted(PRESETS.keys()), help="Override spec preset.")
    parser.add_argument("--seed", type=int, help="Override random seed.")
    parser.add_argument("--scale", type=int, help="Override integer PNG upscale factor (default: 4).")
    args = parser.parse_args(argv)

    if not args.output and not args.html:
        parser.error("Provide at least one of -o/--output (PNG) or --html (HTML).")

    raw_text = sys.stdin.read() if args.spec == "-" else Path(args.spec).read_text(encoding="utf-8")
    spec = json.loads(raw_text)
    if args.preset is not None:
        spec["preset"] = args.preset
    if args.seed is not None:
        spec["seed"] = args.seed
    if args.scale is not None:
        spec["scale"] = args.scale

    if args.output:
        renderer = DoodleRenderer(spec)
        renderer.render()
        out_path = Path(args.output)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        scale = int(spec.get("scale", 4))
        out_path.write_bytes(renderer.to_png_bytes(scale=scale))
        print(f"Wrote PNG: {out_path} ({renderer.w * scale}x{renderer.h * scale}, preset={spec.get('preset', 'clumsy')}, seed={spec.get('seed', 42)})")

    if args.html:
        html_path = Path(args.html)
        html_path.parent.mkdir(parents=True, exist_ok=True)
        html_path.write_text(build_standalone_html(spec, title=html_path.stem), encoding="utf-8")
        print(f"Wrote HTML: {html_path}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
