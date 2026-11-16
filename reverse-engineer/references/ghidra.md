# Deep Ghidra pseudocode workflow

Use this workflow only after Layer 3 has been escalated and `rea doctor --provider ghidra --json` confirms Ghidra and JDK 21+ are available.

## JDK 21+ and provider readiness

Ghidra requires JDK 21+ and `GHIDRA_INSTALL_DIR`. On macOS, agent shells may default to JDK 17, and `/usr/libexec/java_home -v 21` without `-F` can silently fall back to 17. Check readiness with `rea doctor --provider ghidra --json` and select JDK 21+ with `/usr/libexec/java_home -F -v 21+` or an explicit JDK 21+ path; report a missing JDK 21+ explicitly instead of falling back to 17.

## Thin universal binaries

Ghidra refuses fat binaries. Before any analysis, check architecture and split:

```sh
lipo -info T
lipo -thin arm64 -o T1 T
```

## Build the analysis snapshot

The first Ghidra-backed command builds a local snapshot keyed by SHA-256; subsequent calls reuse the cache instantly. The snapshot lives in REA's own data directory (not in the target tree).

Find the current command names with `rea --llms | rg -i "ghidra|analyze|decompile"`.

## Decompile a single function

Use the pseudocode / decompile command for a single symbol or address. Static decompilation is inferred logic, not observed execution.

## Cross-references

Follow call edges with the cross-reference command after you have an anchor address. This tells you who calls the function and what it calls, which is often the answer to "what does this do" without reading every instruction.

## Cache and raw-binary edge cases

- If the target path contains a space or a dot folder (like `.re-cache`), Ghidra's project cache may refuse it; check `rea <cmd> --schema` for a snapshot or cache override flag.
- For headerless raw binaries, check `--target-format` and `--architecture` in `rea <cmd> --schema`.
