#!/usr/bin/env python3
"""Offline process double; never imports or invokes the real CLI."""

import json
import os
from pathlib import Path
import sys
import time
import signal
import subprocess


def main() -> int:
    if os.environ.get("STUB_TERM") == "zero":
        signal.signal(signal.SIGTERM, lambda signum, frame: sys.exit(0))
    elif os.environ.get("STUB_TERM") == "ignore":
        signal.signal(signal.SIGTERM, signal.SIG_IGN)
    worker_path = os.environ.get("STUB_WORKER")
    if worker_path:
        worker = subprocess.Popen([sys.executable, "-c", '''
import signal, sys, time
from pathlib import Path
signal.signal(signal.SIGTERM, signal.SIG_IGN)
target = Path(sys.argv[1])
for index in range(400):
    target.write_text(str(index))
    time.sleep(0.05)
''', worker_path])
        Path(worker_path + ".pid").write_text(str(worker.pid))
    Path("invoked.json").write_text(json.dumps({
        "args": sys.argv[1:], "cwd": os.getcwd(), "home": os.environ.get("HOME")
    }), encoding="utf-8")
    fixture = os.environ.get("STUB_STREAM")
    if fixture:
        sys.stdout.buffer.write(Path(fixture).read_bytes())
    else:
        print(json.dumps({"event": "init", "init": {
            "model": "stub-model", "cwd": os.getcwd()
        }}))
        print(json.dumps({"event": "result", "result": {
            "status": "SUCCESS", "response": "完成", "denied_actions": []
        }}))
    sys.stderr.write(os.environ.get("STUB_STDERR", "ordinary warning\n"))
    sys.stdout.flush()
    sys.stderr.flush()
    if os.environ.get("STUB_SLEEP"):
        time.sleep(float(os.environ["STUB_SLEEP"]))
    if os.environ.get("STUB_RELEASE"):
        deadline = time.monotonic() + 20
        while not Path(os.environ["STUB_RELEASE"]).exists() and time.monotonic() < deadline:
            time.sleep(0.01)
    return int(os.environ.get("STUB_EXIT", "0"))


if __name__ == "__main__":
    raise SystemExit(main())
