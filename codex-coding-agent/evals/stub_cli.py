#!/usr/bin/env python3
"""A local observable process, not a model invocation."""
import json
import os
from pathlib import Path
import signal
import subprocess
import sys
import time

arguments = sys.argv[1:]
prompt = sys.stdin.read()
with open(os.environ["STUB_OBSERVED"], "a", encoding="utf-8") as target:
    target.write(json.dumps({"argv": arguments, "cwd": os.getcwd(), "home": os.environ["HOME"], "prompt": prompt}) + "\n")
sys.stderr.write(os.environ.get("STUB_STDERR", ""))
sys.stderr.flush()
payload = Path(os.environ["STUB_STREAM"]).read_bytes()
if os.environ.get("STUB_EARLY_STREAM"):
    sys.stdout.buffer.write(payload)
    sys.stdout.buffer.flush()
if os.environ.get("STUB_TERM") == "zero":
    signal.signal(signal.SIGTERM, lambda *_: sys.exit(0))
if os.environ.get("STUB_WORKER"):
    worker = subprocess.Popen([sys.executable, "-c", "import signal,sys,time; from pathlib import Path; signal.signal(signal.SIGTERM, signal.SIG_IGN); Path(sys.argv[1]).touch(); time.sleep(120)", os.environ["STUB_WORKER"] + ".ready"])
    while not Path(os.environ["STUB_WORKER"] + ".ready").exists():
        time.sleep(0.01)
    Path(os.environ["STUB_WORKER"] + ".pid").write_text(str(worker.pid))
    Path(os.environ["STUB_WORKER"]).touch()
if os.environ.get("STUB_RELEASE"):
    while not Path(os.environ["STUB_RELEASE"]).exists():
        time.sleep(0.01)
time.sleep(float(os.environ.get("STUB_SLEEP", "0")))
if not os.environ.get("STUB_EARLY_STREAM"):
    sys.stdout.buffer.write(payload)
    sys.stdout.buffer.flush()
sys.exit(int(os.environ.get("STUB_EXIT", "0")))
