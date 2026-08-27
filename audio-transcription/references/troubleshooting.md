# Troubleshooting

First run the failed command with `--json`, follow `next_actions`, then run `scripts/local-transcribe help errors` or `scripts/manage-runtime doctor --json`.

Escalate here only when those actions are insufficient:

- Repeated model-load or Metal failures: capture the stable error code, active profile, model revision, macOS version, unified memory, and the last bounded stderr excerpt. Do not switch online automatically.
- Apparent out-of-memory failure: recommend the explicitly installed low-memory profile or shorter chunks; never silently change quantization.
- Long MOSS output with inconsistent speakers: verify chunk boundaries and preserve chunk-qualified speaker IDs.
- Runtime activation failure: keep the previous active runtime. A staging directory is not a valid runtime.
- Online failure: preserve the non-secret task ID and status code. Do not expose credentials or retry by changing upload authorization.

Do not delete models, runtimes, caches, or CLI entries while diagnosing. Cleanup is a separate explicit workflow described by `scripts/manage-runtime cleanup --help` and `scripts/local-transcribe help cache`.
