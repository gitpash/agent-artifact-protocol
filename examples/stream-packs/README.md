# Example: stream packs (optional profile)

**Not Core maps.** These files illustrate an optional disclosure profile:

| Path | Role |
|------|------|
| `orientation.md` | Thin workspace card (after the map) |
| `map.local.yaml.example` | GPS + optional streams index (gitignored in real use) |
| `streams/research.yaml` | Research / locus pack |
| `streams/release-check.yaml` | Release / ship-scan pack |
| `streams/_accept-default.yaml` | Shared accept bar before “done” |

Core Orientation still needs only a discoverable map. Open **exactly one** stream pack per session.

Cookbook: [`../../cookbook/stream-packs.md`](../../cookbook/stream-packs.md), [`../../cookbook/local-bootstrap.md`](../../cookbook/local-bootstrap.md).

These YAMLs are **not** validated as Map v2 documents by `scripts/validate.py`.
