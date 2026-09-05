# Setup workflow

Use this branch only after the user explicitly asks to set up or repair local transcription.

Local setup is supported only on macOS Apple Silicon (arm64). Other hosts must not run setup. Setup downloads pinned third-party model weights; licenses are listed in [NOTICE.md](../NOTICE.md).

1. Run `scripts/manage-runtime inspect --json`.
   When the user explicitly wants persistent or external storage, first run
   `scripts/manage-runtime storage status --json`. After they choose four dedicated,
   non-overlapping directories, run `storage configure --app-root ... --cache-root ...
   --temp-root ... --transcript-root ... --json`; it persists locations only and does not
   move an existing runtime or data.
2. Explain the recommended profile, approximate download size, missing system dependencies, and whether lower quantization changes quality.
3. Total unified memory below the standard profile threshold is a recommendation for `low-memory`, not proof that inference will succeed. Ask before selecting lower quantization.
4. Run `scripts/manage-runtime setup --profile <profile>`. Setup may use the network and Homebrew, creates a versioned runtime under the user's Application Support directory, downloads pinned model revisions, and activates only after validation.
5. Run `scripts/manage-runtime doctor --json`.
6. Ask whether the user wants a stable CLI entry. The default is no installation. Inspect candidates, then run `scripts/manage-runtime install-cli --bin-dir "<directory>"` only after the user chooses.

Read `scripts/manage-runtime --help`, `scripts/manage-runtime setup --help`, and `scripts/manage-runtime install-cli --help` for the current contract. Never improvise dependency versions, model revisions, install locations, `sudo`, or cleanup commands.
