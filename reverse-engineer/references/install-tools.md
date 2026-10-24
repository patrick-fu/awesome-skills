# Install missing dependencies

Read this when a command in `SKILL.md` reports `command not found`, or when `rea doctor --json` reports a missing engine.

## Layer requirements

| Layer | Required | Optional |
|---|---|---|
| 1 (Native recon) | `otool`, `nm`, `strings`, `file` (macOS built-in); `readelf`, `objdump` (Linux binutils) | `jq`, `rg` |
| 2 (REA structured) | `rea` on PATH or `npx -y rea-agents` | `jadx` (APK), `apktool` (resources) |
| 3 (Ghidra pseudocode) | `ghidra` + JDK 21+ | `ilspycmd` (.NET) |

## Quick install

macOS (Homebrew):
```sh
brew install jadx apktool binwalk wabt wireshark
brew install --cask temurin@21        # JDK 21 for Ghidra / jadx
brew install --cask ghidra             # or download from https://ghidra-sre.org
```

Linux (Debian/Ubuntu):
```sh
sudo apt install openjdk-21-jdk binutils file jq ripgrep
# Ghidra, jadx, binwalk, wabt: use the official releases or distro packages
```

## REA CLI

If `rea` is not on `PATH`, pin the version to avoid future breakage:

```sh
npm install --global rea-agents
```

Check which engines are ready (version-agnostic):

```sh
rea doctor --json
```

The doctor report lists what is installed, what is missing, and which REA commands are unavailable without them. Install only what your current task needs; skip the rest.
