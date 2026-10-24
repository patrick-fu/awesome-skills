---
name: reverse-engineer
description: Reverse-engineer shipped software with native Unix tools and the local REA CLI when source is absent.
---

# Reverse engineer

Three layers, zero MCP daemon, no client config changes. Start at Layer 1; escalate only when Layer 1 cannot answer.

## Hard invariants

- Resolve targets with `realpath <target>`.
- Work on a copy under `$TMPDIR/re/$(basename $T)`; use `cp -c` on APFS.
- Cap verbose output: native tools pipe to `head`, REA commands carry `--token-limit 8000`.
- Cite findings as **seen / inferred / unknown**; absence is unknown. Static reading is not execution.

## Layer 1 — Native recon

First moves:
- Mach-O:  `file T; lipo -info T; otool -L T; nm -gU T | head; nm -u T | head; strings -a -n 6 T | head -400`
- Electron: `npx @electron/asar extract app.asar X; rg -uu -l 'ipcMain\.|contextBridge' X --glob '!node_modules'`
- Go:      `go version -m T`
- Search:  `rg -uu -o '.{0,200}NEEDLE.{0,200}' X | head`

Route by magic:
| Target | Command |
|---|---|
| Mach-O | `otool -L`, `nm -gU` / `nm -u`, `strings` |
| ELF | `readelf -dW`, `nm -D`, `objdump -d -M intel` |
| Go buildinf | `go version -m T` |
| Rust `.dep-v0` | `cargo audit bin T` |
| WASM `\0asm` | `wasm-objdump -x`, `wasm2wat` |
| SQLite | `sqlite3 file:C?mode=ro '.schema'` |
| Firmware / pcap | `binwalk -e`, `tshark -r C -q -z conv,tcp` |

## Layer 2 — REA structured

Escalate when Layer 1 cannot produce structured Evidence, cannot parse a niche format, or when downstream logic needs `--format json`.

Discovery protocol (version-agnostic):
- Surface:  `rea --llms | rg -i "<keyword>"`
- Contract: `rea <cmd> --schema`
- Health:   `rea doctor --json`

Every potentially verbose REA command carries `--token-limit 8000`; page with `--token-offset`.
For patched Electron apps, check `--integrityPolicy` in `rea <cmd> --schema` before running.

## Layer 3 — Ghidra pseudocode

Escalate when the question is a function's logic, not its surface. Confirm Ghidra with `rea doctor --json`; thin universal binaries first (`lipo -thin arm64 -o T1 T`).
Workflow (find commands via `rea --llms | rg -i "ghidra|decompile|analyze|xrefs"`):
1. Build analysis snapshot (cached per SHA-256).
2. Decompile one function or symbol.
3. Trace cross-references for call edges.

## Disclosed workflows

- Massive Electron/ASAR evidence slicing: read [references/slicing.md](references/slicing.md).
- Layer 3 deep Ghidra specifics (cache quirks, raw-binary edge cases): read [references/ghidra.md](references/ghidra.md).
- Installing missing tools: read [references/install-tools.md](references/install-tools.md).
