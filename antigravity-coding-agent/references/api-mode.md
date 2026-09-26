# Antigravity API-Key Mode

Account sign-in — OAuth through the local browser, silent keyring re-auth, and
the SSH authorization-URL loop for remote hosts — is the default authentication
and needs no configuration here. Use API-key mode for headless or CI machines
without a browser, or to point the CLI at a Gemini-compatible custom endpoint.
Verified against Antigravity CLI 1.2.11; the official reference is
https://antigravity.google/docs/cli/install.

## Enable API-Key Mode

1. Set the provider in `~/.gemini/antigravity-cli/settings.json`:

   ```json
   {
     "modelProvider": "gemini"
   }
   ```

   Only lowercase `"gemini"` is accepted; an unrecognized value is ignored and
   the CLI keeps using account sign-in.

2. Export the key as `GEMINI_API_KEY`. The CLI reads only this variable from
   the environment; it does not load `.env` files, and `GOOGLE_API_KEY` alone
   has no effect. Create keys in Google AI Studio. Persist by adding the export
   to the shell profile.

3. Start the CLI. It skips sign-in, and the header shows `Gemini API key`
   instead of the account email. `/logout` is an interactive command: passing
   it to a print run fails with exit 2 rather than doing nothing, because
   there is no account session to clear.

## Custom Endpoint

```sh
export GOOGLE_GEMINI_BASE_URL="https://your-endpoint.example.com"
```

Model requests go to `<base-url>/v1beta/...`; the endpoint must speak the
Gemini API request shape and authenticate the key the way the Gemini API does.
Gemini-compatible relays commonly accept `x-goog-api-key`, `?key=`, and
`Authorization: Bearer`.

## Gotchas

- A `model` field in `settings.json` pins the default model and takes the
  display name from `<launcher> models` (for example
  `"Gemini 3.8 Flash (High)"`), not the catalog ID; ID-form values are silently
  ignored (observed on 1.2.11).
- The built-in default model can be absent from a limited or relayed catalog;
  the run then fails with `400 ... unknown provider for model ...`. Pick a
  model the endpoint actually serves and pass `--model` with `--effort`
  explicitly.
- With `modelProvider: "gemini"` but no `GEMINI_API_KEY`, the CLI exits at
  startup with an explicit message. Startup only checks that the key is
  non-empty; an invalid or revoked key surfaces on the first model request.
- Model requests go directly to the Gemini API or the custom endpoint; the
  account session and its account-level eligibility and verification checks do
  not apply in this mode.
- `settings.json` also supports custom model entries under `customModels`
  (entries require `modelName`; media support via `modelFeatures`) for
  endpoints beyond the Gemini shape. The schema evolves — check
  `<launcher> changelog` for the current fields.
