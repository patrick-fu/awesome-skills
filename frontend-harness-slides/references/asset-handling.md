# Asset Handling

Use the project's existing asset convention if one exists. For a new deck, keep
assets named by content and grouped by scene or shared use.

## Suggested Organization

```text
assets/
├── shared/          # logos, brand marks, favicon, universal icons
├── scene-intro/     # per-scene images and diagrams
├── scene-demo/
└── fonts/           # checked-in web fonts when needed
```

If the framework has a specific `public/`, `static/`, or import-based asset
pipeline, use it. The important part is that tests and deployment resolve the
same files.

## Rules

- Use content-based names, not raw export names such as `image001.png`.
- Optimize large photos before committing or deploying.
- Prefer WebP/AVIF for photos when browser support is acceptable.
- Keep logos and diagrams as SVG when they need sharp scaling.
- SVGs that must change color with theme should use `currentColor` or theme
  tokens instead of hardcoded hex values.
- Do not put slide assets inside test artifact folders.
- Do not rely on remote assets for anything critical to the talk unless the
  delivery context explicitly allows network dependence.
- If an asset is visually central, verify it in the browser, not just in the file
  tree.
