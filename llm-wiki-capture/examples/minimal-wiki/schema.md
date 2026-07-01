# Schema

This is a small starter schema. Keep it simple until the knowledge base needs
more structure.

## Page Types

- `wiki/index.md`: top-level navigation and owner-page map.
- `wiki/log.md`: chronological record of meaningful knowledge updates.
- `wiki/<topic>.md`: canonical owner page for a reusable topic.
- `sources/<source-id>.md`: optional source note for an external source.

## Owner Pages

Each durable claim should have one canonical owner page. Update that page instead
of creating a duplicate topic.

Use a new owner page only when:

- the topic will be reused independently
- no existing page would make the knowledge discoverable
- the page can be named clearly

## Provenance

For session captures, note the session or task context briefly enough that a
future reader can understand the evidence.

For source ingest, record:

- source title or label
- canonical URL or file path when available
- access date when useful
- whether the source is original, translation, interpretation, or reference

## Links

Use relative Markdown links for local files. Update `wiki/index.md` when adding
or renaming owner pages.
