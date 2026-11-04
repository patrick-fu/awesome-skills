#!/usr/bin/env python3
"""Screenshot and measure a paper-ink-style page.
Usage: render.py <page.html> <out-dir>

macOS headless Chrome clamps --window-size to a 500px minimum, so a naive
390px run silently lays out at 500px and crops the screenshot. This script
therefore measures and shoots the mobile view through a same-origin 390px
iframe probe (file access flag on), and crops the screenshot back to 390px.
Requires headless Chrome; degrades gracefully (exit 0 with a notice) when
absent."""
import os, re, shutil, subprocess, sys
from pathlib import Path

PROBE_CSS = ("html,body{margin:0;background:#fff}"
           # macOS headless clamps windows to >=500px and sips center-crops,
           # so center the 390px iframe in the 500px window: (500-390)/2 = 55.
           "iframe{border:0;display:block;margin-left:55px}")

def chrome():
    env = os.environ.get("CHROME")
    if env and Path(env).exists(): return env
    mac = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
    if Path(mac).exists(): return mac
    return shutil.which("google-chrome") or shutil.which("chromium")

def run(bin_, args, text=False):
    return subprocess.run([bin_, "--headless=new", "--disable-gpu", "--no-first-run",
                           "--allow-file-access-from-files", *args],
                          capture_output=True, text=text, timeout=180)

def crop(src: Path, w: int, h: int):
    sips = shutil.which("sips")
    if not sips or not src.exists(): return False
    subprocess.run([sips, "--cropOffset", "0", "0", "-c", str(h), str(w), str(src)],
                   capture_output=True)
    return True

def main(page: Path, out: Path):
    out.mkdir(parents=True, exist_ok=True)
    bin_ = chrome()
    if not bin_:
        print("RENDER skipped: no headless Chrome found; do a manual 390px check")
        return 0
    url = page.resolve().as_uri()
    # desktop: direct
    dst = out / f"{page.stem}-desktop.png"
    run(bin_, [f"--user-data-dir={out / '.chrome-desktop'}", "--window-size=1440,2400",
               "--virtual-time-budget=12000", f"--screenshot={dst}", url])
    print("RENDER", dst, dst.stat().st_size if dst.exists() else "missing")
    # mobile: 390px iframe probe (true layout) + measure
    probe = page.parent / f"{page.stem}.probe.html"
    probe.write_text(
        "<!doctype html><meta charset='utf-8'><style>" + PROBE_CSS + "</style>"
        f"<iframe id='f' src='{page.name}' style='width:390px;height:2360px'></iframe>"
        "<script>window.addEventListener('load',function(){setTimeout(function(){"
        "var d=document.getElementById('f').contentDocument;"
        "document.title='PVL_SW_'+d.documentElement.scrollWidth;},600);});</script>",
        encoding="utf-8")
    dst = out / f"{page.stem}-mobile.png"
    run(bin_, [f"--user-data-dir={out / '.chrome-mobile'}", "--window-size=500,2400",
               "--virtual-time-budget=12000", f"--screenshot={dst}", probe.resolve().as_uri()])
    crop(dst, 390, 2400)
    print("RENDER", dst, dst.stat().st_size if dst.exists() else "missing")
    dom = run(bin_, [f"--user-data-dir={out / '.chrome-measure'}", "--window-size=500,1200",
                     "--virtual-time-budget=10000", "--dump-dom", probe.resolve().as_uri()],
              text=True).stdout
    m = re.search(r"PVL_SW_(\d+)", dom)
    sw = int(m.group(1)) if m else -1
    tag = "MOBILE OVERFLOW" if 0 < sw > 390 else "width ok"
    print(f"MEASURE mobile: scrollWidth={sw} viewport=390 -> {tag}")
    probe.unlink(missing_ok=True)
    return 0

if __name__ == "__main__":
    sys.exit(main(Path(sys.argv[1]), Path(sys.argv[2])))
