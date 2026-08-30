# Online transcription

This branch uploads a converted copy of the supplied media to Doubao/Volcengine. Converted audio leaves the machine. Do not enter this branch for media that must remain local. Enter it only when the user explicitly asks for online/cloud/Doubao transcription, explicitly permits upload, or asks for a local-versus-online comparison.

- “双模型”“并行”“交叉验证” alone mean the two local models and do not authorize upload.
- “只用豆包/只用在线” runs only the online worker.
- “本地和在线对比” runs local Qwen plus MOSS and Doubao independently.
- A local-only or no-upload instruction always wins.

Read `scripts/online-transcribe --help` before execution. Pass `--online-consent` only after the request satisfies the rule above. Credentials stay in environment variables; never print, persist, request, or copy their values.

When changing or diagnosing provider behavior, read [doubao-asr-2.0-api.md](doubao-asr-2.0-api.md) instead of reconstructing the protocol from memory.

Online output remains independent. Do not use it as a prompt for either local model and do not silently merge it into a canonical transcript.
