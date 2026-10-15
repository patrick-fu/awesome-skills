#!/usr/bin/env python3
"""Offline process double; never imports or invokes the real CLI."""

import json
import os
from pathlib import Path
import sys


def main() -> int:
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
    return int(os.environ.get("STUB_EXIT", "0"))


if __name__ == "__main__":
    raise SystemExit(main())
