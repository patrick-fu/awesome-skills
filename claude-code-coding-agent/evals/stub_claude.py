#!/usr/bin/env python3
"""Offline Claude process double for observed startup and stream contracts."""

import json
import os
from pathlib import Path
import signal
import sys
import time
import subprocess


def main():
    if os.environ.get("STUB_TERM") == "zero":
        signal.signal(signal.SIGTERM, lambda signum, frame: sys.exit(0))
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
    arguments = sys.argv[1:]
    prompt = sys.stdin.read()
    observed = Path(os.environ["STUB_OBSERVED"])
    with observed.open("a", encoding="utf-8") as output:
        output.write(json.dumps(dict(argv=arguments, prompt=prompt, cwd=os.getcwd(),
                                    home=os.environ.get("HOME"))) + "\n")
    if not prompt.strip():
        print("Error: Input must be provided either through stdin or as a prompt argument when using --print", file=sys.stderr)
        return 1
    if "--verbose" not in arguments:
        print("Error: When using --print, --output-format=stream-json requires --verbose", file=sys.stderr)
        return 1
    if "--restricted" in arguments and os.environ.get("STUB_BYPASS"):
        print("Error: bypassPermissions not supported in restricted mode", file=sys.stderr)
        return 1
    if os.environ.get("STUB_EARLY_STREAM"):
        sys.stdout.buffer.write(Path(os.environ["STUB_STREAM"]).read_bytes())
        sys.stdout.flush()
    if os.environ.get("STUB_SLEEP"):
        time.sleep(float(os.environ["STUB_SLEEP"]))
    if os.environ.get("STUB_RELEASE"):
        deadline = time.monotonic() + 20
        while not Path(os.environ["STUB_RELEASE"]).exists() and time.monotonic() < deadline:
            time.sleep(0.01)
    if os.environ.get("STUB_SIGNAL"):
        os.kill(os.getpid(), signal.SIGTERM)
    if not os.environ.get("STUB_EARLY_STREAM"):
        sys.stdout.buffer.write(Path(os.environ["STUB_STREAM"]).read_bytes())
    sys.stderr.write(os.environ.get("STUB_STDERR", ""))
    return int(os.environ.get("STUB_EXIT", "0"))


if __name__ == "__main__":
    raise SystemExit(main())
