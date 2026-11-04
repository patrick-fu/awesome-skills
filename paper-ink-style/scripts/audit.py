#!/usr/bin/env python3
"""Static audit for paper-ink-style pages. Usage: audit.py <page.html>"""
import re, sys
from pathlib import Path

ALLOWED_RADIUS = {"var(--pvl-radius-rough)", "var(--pvl-radius-note)", "var(--pvl-radius-pill)",
                  "0", "12px", "50%", "3px 8px 4px 6px", "2px 15px", "999px",
                  "0 12px 12px 0", "255px 15px 225px/15px 225px 15px 255px",
                  "14px 6px 14px 6px/6px 14px 6px 14px", "16px", "20px", "11px", "48px"}
ALLOWED_SHADOW = {"var(--pvl-shadow-card)", "var(--pvl-shadow-note)", "var(--pvl-shadow-soft)",
                  "none", "2px 2px rgba(42,42,42,.05)", "3px 5px 12px rgba(0,0,0,.08)",
                  "var(--pvl-shadow-hard)", "var(--pvl-shadow-lift)", "var(--pvl-shadow-pencil)", "var(--pvl-shadow-device)",
                  "3px 4px 0 rgba(32,39,35,.12)", "7px 8px 0 rgba(32,39,35,.12)", "2.5px 3px 0 rgba(42,42,42,.85)"}
EMOJI_OK_CONTEXT = ("pvl-sticker", "pvl-note", "pvl-badge", "pvl-callout", "pvl-takeaway")
# hand-made markers: the craft layer that keeps a page from reading as a generic
# report. Stickers and plain .pvl-highlight are core identity, not counted here.
MARKER_PATTERNS = (("scribble", r"pvl-scribble"), ("tape", r"pvl-tape"),
                   ("sticky-note", r"pvl-note"), ("band-highlight", r"pvl-highlight--band"),
                   ("pencil-annot", r"pvl-annot"))
fails, warns, info = [], [], []


def identity_markers(markup: str):
    """Distinct hand-made marker kinds present in markup (style/script already stripped)."""
    kinds = {name for name, pat in MARKER_PATTERNS if re.search(pat, markup)}
    for m in re.finditer(r'class\s*=\s*["\']([^"\']*)["\']', markup):
        toks = m.group(1).split()
        if "pvl-card" in toks and not {"pvl-card--clean", "pvl-card--board"} & set(toks):
            kinds.add("rough-card")
            break
    return sorted(kinds)


def chunks_by(html, tag="section"):
    parts = re.split(rf"<{tag}\b", html)
    return parts[1:] if len(parts) > 1 else []


def count_highlights(markup):
    """Count elements carrying a highlight class; modifiers (--band, --lime) do
    not add a second highlight to the same element."""
    n = 0
    for m in re.finditer(r'class\s*=\s*["\']([^"\']*)["\']', markup):
        if any(t.startswith("pvl-highlight") for t in m.group(1).split()):
            n += 1
    return n

def main(path: Path):
    s = path.read_text(errors="replace")
    style = " ".join(re.findall(r"<style[^>]*>([\s\S]*?)</style>", s, re.I))
    linked = ('base.css' in s) or ("--pvl-pencil-line" in s)
    if not linked:
        fails.append("base.css not linked and tokens not inlined")
    for m in re.finditer(r":hover[^{]*\{([^}]*)\}", style):
        if re.search(r"display\s*:|max-height|grid-template-rows|height\s*:", m.group(1)):
            fails.append("hover-driven layout reveal found")
    # per-section caps: sections if the page has them, otherwise h2 blocks
    chunks = chunks_by(s, "section") + chunks_by(s, "h2") or [s]
    for chunk in chunks:
        n = count_highlights(chunk)
        if n > 3:
            fails.append(f"section with {n} highlights (>3)")
    for card in re.findall(r'class="[^"]*pvl-card[^"]*"[\s\S]{0,2000}?(?=<div class="[^"]*pvl-card|</section>|</main>|$)', s):
        if count_highlights(card) > 1:
            fails.append("card with >1 highlight")
            break
    for decl in re.findall(r"border-radius\s*:\s*([^;\"}]+)", style):
        v = decl.strip()
        if v and v not in ALLOWED_RADIUS and not v.startswith("var(--pvl"):
            fails.append(f"radius outside allowlist: {v}")
    for decl in re.findall(r"box-shadow\s*:\s*([^;\"}]+)", style):
        v = decl.strip()
        if v and v not in ALLOWED_SHADOW and not v.startswith("var(--pvl"):
            fails.append(f"shadow outside allowlist: {v}")
    if re.search(r"color\s*:\s*(#000\b|#000000\b|black\b)", style, re.I):
        fails.append("pure black ink used")
    body = re.sub(r"<(style|script)[^>]*>[\s\S]*?</\1>", " ", s, flags=re.I)
    for m in re.finditer(r"<(p|li|td|span)[^>]*>([\s\S]{0,220}?)</\1>", body):
        attrs, inner = m.group(0)[:120], m.group(2)
        if any(c in attrs for c in EMOJI_OK_CONTEXT):
            continue
        if re.search(r"[\U0001F300-\U0001FAFF\u2600-\u27BF]", inner):
            fails.append(f"floating emoji in prose: {re.sub(r'<[^>]+>','',inner)[:60]}")
    markers = identity_markers(body)
    if len(markers) < 2:
        fails.append(f"only {len(markers)} distinct hand-made marker(s) {markers}; need >=2 of "
                     "scribble / tape / sticky-note / rough-card / band-highlight / pencil-annot")
    else:
        info.append(f"hand-made markers ({len(markers)}): {', '.join(markers)}")
    dense = 'data-dense="true"' in s or "data-dense='true'" in s
    floor_warn = 14 if not dense else 10.5
    for m in re.finditer(r"font-size\s*:\s*(\d+(?:\.\d+)?)px", style):
        v = float(m.group(1))
        if v < 10.5:
            fails.append(f"type below floor: {v}px")
        elif v < floor_warn and "mono" not in style[max(0, m.start()-260):m.start()]:
            warns.append(f"small non-mono type: {v}px (set html data-dense=\"true\" for workbench/in-device density)")
    stage = "data-stage" in s  # fixed-stage decks are exempt from width warnings by design
    scan = "" if stage else re.sub(r"@media\s*\([^)]*\)", " ", style) + " " + " ".join(re.findall(r'style="([^"]+)"', s))
    for m in re.finditer(r"(?<![\w-])(?:width|min-width)\s*:\s*(\d{3,})px", scan):
        if int(m.group(1)) > 390:
            warns.append(f"fixed width {m.group(1)}px may overflow 390px viewport")
    if re.search(r"https?://", re.sub(r"<a\b[\s\S]*?</a>", " ", body)):
        warns.append("page references external URLs (skill itself must stay self-contained)")
    print(f"AUDIT {path.name}: {'FAIL' if fails else 'PASS'} ({len(fails)} fail, {len(warns)} warn)")
    for i in info: print("  ", i)
    for f in fails: print("  FAIL", f)
    for w in warns: print("  warn", w)
    return 1 if fails else 0

if __name__ == "__main__":
    sys.exit(main(Path(sys.argv[1])))
