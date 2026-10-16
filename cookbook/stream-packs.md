# Cookbook: stream packs (optional profile)

> **Optional profile — not required for Orientation conformance.**  
> Core L0 remains: discoverable map only.

## Problem

A map tells agents **where** things live. It does not encode **how this session should proceed** (research vs release scan vs minimal fix). Teams then either:

- dump constitutions into context, or  
- improvise procedure every turn.

## Pattern: one stream pack per session

A **stream pack** is a small YAML (or Markdown) file that names:

- when to choose it (`when:` keywords or human `stream: <id>`)
- `read_first` / `open_when_needed` paths
- preferred tools and **degrade** rules
- `process` steps
- `acceptance` and `forbid`

**Rule:** open **exactly one** pack for the session (plus optional shared accept bar). Do not preload every pack.

## Suggested layout (local, often gitignored)

```text
.aap/
  map.yaml                 # committed L0
  map.local.yaml           # gitignored: GPS + optional streams index
  local/
    orientation.md         # optional thin card
    streams/
      research.yaml
      release-check.yaml
      _accept-default.yaml
```

Committed map stays topology-only. Stream catalogs belong in **local** profile files so machine/tool preferences do not fork the shared map.

## Minimal pack shape (informative)

```yaml
id: research
summary: Domain answers from map + evidence
when: [where is, blast radius, investigate]
read_first:
  - .aap/map.yaml
open_when_needed:
  - docs/architecture/   # example only
tools:
  rules:
    - "Prefer map hops before wide repository search"
    - "If optional index or retrieval MCP is empty → degrade; say so"
process:
  - State question and candidate nodes
  - Cite paths for factual claims
acceptance:
  - Claims tied to file or git evidence
forbid:
  - Preload full constitution catalogs
```

Samples: [`examples/stream-packs/`](../examples/stream-packs/).

## Accept bar (companion)

Optional `_accept-default.yaml`: steps before claiming done / PR-ready (orient, evidence, no ship on failing checks). Encode honesty without growing the L0 map. Full pattern: [`done-bar.md`](./done-bar.md). Sample: [`examples/stream-packs/streams/_accept-default.yaml`](../examples/stream-packs/streams/_accept-default.yaml). Stub: [`templates/stream-pack.yaml`](../templates/stream-pack.yaml).

## Runtime note

Harnesses MAY inject a thin dispatcher file that **requires** reading map + one pack. That dispatcher is **runtime policy**, not AAP Core. Soft “you may read packs” wording often fails under task pressure; hard bootstrap is a consumer choice.

See [`local-bootstrap.md`](./local-bootstrap.md).

## Anti-patterns

- Putting stream catalogs into committed `map.yaml` as mandatory Core fields  
- Opening all packs “just in case” — see [`examples/invalid/anti-multi-stream-open.md`](../examples/invalid/anti-multi-stream-open.md)  
- Naming vendor-specific tool ids in shared examples as if required  
- Treating stream packs as a replacement for the map  
- Redefining Core L0 as “map + every pack”  

## See also

- [`done-bar.md`](./done-bar.md)  
- [`local-bootstrap.md`](./local-bootstrap.md)  
- [`templates/orientation.md`](../templates/orientation.md)  
- [`templates/stream-pack.yaml`](../templates/stream-pack.yaml)  
 
