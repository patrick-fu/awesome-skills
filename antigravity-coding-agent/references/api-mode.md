# Antigravity API-Key Mode

Use for Gemini API-key setup, compatible relays, or route verification.
Account authentication is the default. See [installation and auth](https://antigravity.google/docs/cli/install).
Display-name behavior was observed on 1.2.11; launch-context mismatch on 1.2.12.

## Configure one launch context

1. Merge `"modelProvider": "gemini"` into the intended HOME's
   `.gemini/antigravity-cli/settings.json`. Preserve unrelated settings.
   Only lowercase `gemini` selects API mode; other values can silently leave
   account authentication active.
2. Supply the Google AI Studio key as `GEMINI_API_KEY` in that process's
   environment. `.env` is not loaded; `GOOGLE_API_KEY` is ineffective.
   Persist to the intended shell profile only when requested. Keep keys out
   of repositories, synced files and captures.
3. For a relay, supply `GOOGLE_GEMINI_BASE_URL="https://your-endpoint.example.com"`
   in the same process. Verify Gemini `<base-url>/v1beta/...` request and auth
   compatibility; relays may support `x-goog-api-key`, query `key`, or Bearer.
4. Use an explicitly served `--model` catalog ID; tiered IDs carry effort.
   For settings `model`, use the exact `models` display name: catalog IDs
   there were silently ignored on 1.2.11. Add `--effort` only when required.

Headless runs inherit the host environment, not necessarily an interactive
shell profile. Use the requested opaque wrapper or scoped configuration.
Isolating HOME requires its settings and intended auth, not a copy of the
real profile. Record credential source, never values; redact auth headers
and secret query parameters. Avoid environment dumps and wrapper inspection.

## Verify generation and route

Startup checks only key nonemptiness. The interactive `Gemini API key` header
identifies mode; successful `models` does not establish generation access.
Run a minimal request, e.g. `-p "reply ok"`, with the selected model; verify
result and exit using [monitoring](monitoring.md).

| Claim | Evidence |
| --- | --- |
| Client API mode/configuration | Provider and actual launch context's key source, endpoint, model; header/diagnostics when available |
| Request destination | Redacted diagnostics or correlated proxy log |
| Relay's upstream credential | Correlated relay selection log; client settings cannot prove it |

Report unverified layers. The client has no Google account session; a relay
can independently use its own upstream credentials.

## Diagnose the failed stage

| Symptom | Check/action |
| --- | --- |
| Account sign-in | Provider spelling and settings loaded by this HOME |
| Missing-key startup | Actual process's `GEMINI_API_KEY` |
| First generation fails | Key validity/model access, verified route and response error |
| `400 unknown provider for model` | Explicitly select a relay-served model and compatible effort |
| Models works, `503 auth_unavailable` | Client key/endpoint mismatch versus unavailable relay upstream credentials |

HTTP 401/503 alone cannot identify the cause. Separate auxiliary-model errors
from main requests when logs expose them; main success does not prove
auxiliary feature health.

`/logout` is interactive with no API-mode account session; print use was
observed to exit 2. For non-Gemini providers, inspect current `customModels`
schema in `changelog` (earlier entries used `modelName`, `modelFeatures`).
