# Massive Electron / ASAR evidence slicing

Use this workflow when the target JavaScript/Electron application is large enough that a single REA command would produce hundreds of megabytes of Evidence JSON, or when you need to page through extracted modules rather than reading them all into context.

## Extract the ASAR

```sh
npx -y @electron/asar extract app.asar X
```

For patched or repackaged apps, check integrity before running the structured command; look for the `--integrityPolicy` flag in `rea <cmd> --schema`.

## Dump the full Evidence to disk (never read it raw)

```sh
rea analyze-javascript-application /abs/path --json > /tmp/rea_ev.json
```

## Discover the Evidence shape

```sh
jq 'keys' /tmp/rea_ev.json
```

## Slice the Evidence into a view

Build a compact view JSON and ask REA to project it:

```sh
jq -c '{source:{kind:"inline",evidence:.},view:{kind:"summary"}}' /tmp/rea_ev.json > /tmp/view.json
rea inspect-analysis-view /tmp/view.json
```

Swap the view kind to `{"kind":"page","collection":"modules","offset":0,"limit":32}` to page through modules, then call trace commands once a seed is found.
