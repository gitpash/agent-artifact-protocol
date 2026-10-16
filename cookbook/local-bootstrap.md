# Cookbook: local bootstrap (optional profile)

> **Optional profile — not required for Orientation conformance.**  
> Keeps machine GPS and session procedure out of the committed Core map.

## Split of concerns

| File | Committed? | Role |
|------|------------|------|
| `.aap/map.yaml` (or discoverable map) | Yes | **L0 topology** — workspace, self, nodes, layout |
| `map.local.yaml` | Usually **no** (gitignore) | GPS overlays + optional profile index |
| Thin orientation card | Optional / often local | Short always-on card **after** the map |
| Stream packs | Optional / often local | One task-class pack per session |
| Runtime dispatcher | Runtime-owned | Thin mandatory bootstrap if the harness needs it |

Core validation applies to the map (and optional committed overlays). Profile index keys beside GPS are **consumer convention**, not Map v2 required fields.

## map.local.yaml shapes

### GPS only (schema-compatible idea)

```yaml
# map.local.yaml — gitignored
overlays:
  nodes:
    orders-api: { path: /home/you/work/orders-api }
    edge-gateway: { path: /home/you/work/edge-gateway }
```

Overlays **navigate only**. They never grant write authority (see SPEC **Overlays**).

### GPS + optional profile index (informative)

```yaml
# map.local.yaml — gitignored; profile keys are local convention
overlays:
  nodes:
    orders-api: { path: /home/you/work/orders-api }

orientation: .aap/local/orientation.md

streams:
  disclosure: .aap/local/streams/
  default: research
  packs:
    - research
    - release-check

acceptance: .aap/local/streams/_accept-default.yaml
```

Publish a GPS-only `.example` in git if helpful; keep live absolute paths out of the shared tree.

## Thin orientation card

A short workspace card (on the order of ~10–20 lines), not a constitution dump:

- what this workspace is  
- where the map and GPS live  
- write-home / coordination fences worth knowing  
- do / don’t for first reads  
- how to pick a stream (if packs exist)

**MUST NOT** replace the map or become a mandatory essay at L0 for Core conformance.

Sample tone: [`examples/stream-packs/orientation.md`](../examples/stream-packs/orientation.md).

## Runtime dispatcher

Some harnesses inject a thin local rules file (often named like `AGENTS.md` / `AGENTS.local.md`) that says:

1. Read the map.  
2. Optionally read orientation.  
3. Open **exactly one** stream pack.  
4. Run accept bar before “done.”

That file is **runtime policy**. Soft “consider reading packs” guidance often fails under task pressure; hard bootstrap is a consumer choice. Keep it **thin** — product standing rules and tool catalogs do not belong in Core, and large dispatcher dumps recreate the preload problem AAP avoids.

## Accept-default pattern

Before claiming done / ship / PR-ready, walk a small checklist (orient, evidence for claims, honest degrade when indexes are empty, no green claim on failing checks). Sample: [`examples/stream-packs/streams/_accept-default.yaml`](../examples/stream-packs/streams/_accept-default.yaml).

## Anti-patterns

- Absolute checkout paths committed in shared `map.yaml`  
- Stream catalogs as required Core map fields  
- Orientation card that embeds full SPEC / skill catalogs  
- Dispatcher that mandates SPEC + all packs every session  
- Treating local bootstrap as universal AAP law  

## See also

- [`stream-packs.md`](./stream-packs.md)  
- [`hub-umbrella.md`](./hub-umbrella.md)  
- [`what-not-to-copy.md`](./what-not-to-copy.md)  
- [`brownfield-init.md`](./brownfield-init.md) — still ends at map-only experiment first  
