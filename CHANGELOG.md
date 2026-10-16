# Changelog

## Unreleased

### Added

- Cookbook: `hub-umbrella.md`, `stream-packs.md`, `local-bootstrap.md` (optional profiles / teaching patterns)
- Examples: `examples/hub-umbrella/` (synthetic multi-node shell + child map), `examples/stream-packs/` (orientation, local index example, research / release-check / accept-default samples)
- README: Core vs profile table; progressive disclosure footnote that profile bootstrap is not Core L0; links to new cookbook pages; optional **Disclosure profile** conformance row
- SPEC: overlays, extension layout keys, optional `profiles` block, non-normative optional local files (schema-preexisting surfaces; prose only)

### Clarified

- Core L0 remains map-only for Orientation conformance
- Dogfood-inspired profiles (stream packs, thin orientation, accept bar, thin runtime dispatcher) are **optional**; no specific agent harness is required
- Status narrative: working-prototype cookbook alongside experimental Map v2 — still not a finished interop standard
- `what-not-to-copy.md`: factory/orchestrator/status-macro/dispatcher/index anti-copies; copy stream-pack and hub-umbrella **ideas**

### Not changed

- Map v2 required fields and `resourceRef` semantics
- Schema document version / git tag (`0.2.0-draft` / `v0.2.0-draft`)
- Core size goals (profiles stay out of mandatory L0)

## 0.2.0-draft — Unreleased

### Changed

- Replaced the v1 `zones` map with the repository-oriented v2 `workspace` / `self` / `nodes` map.
- Added `resourceRef` layout values: backward-compatible strings or `{ path, access?, description? }` objects.
- Defined deterministic write-home selection: first reference whose normalized access is not `read-only`.
- Added a generic optional `brownfield-artifacts` profile for one writable artifact home and migrate-on-touch pointers.
- Moved v1 schemas and examples to historical `legacy/v1/` material; v1 is not v2-compatible.

### Kept out of Core

- Repository-specific external-node restrictions, path-name rules, CI workflows, IAM, and agent runtimes remain local policy or adapters.

## 0.1.1-draft — 2026-09-08

### Added

- `scripts/validate.py` + GitHub Actions workflow (schema, maps, envelopes, invalid fixtures)  
- `examples/invalid/*` negative cases  
- `CONTRIBUTING.md`  
- Explicit: layout keys ≠ NL intent router; `write` ≠ security; default mode = no write grant  
- Init no-overwrite rule in cookbook  
- `updated` field semantics (material change, not verification)  
- Core schema posture: envelope shape permissive on extension `type`
- Deployment-defined write mode labels; deployment-specific role names are no longer Core vocabulary
- Clarified `artifacts` layout key and recommended namespace-like artifact ids
- Renamed `WHITE-PAPER.md` to `MOTIVATION.md`

### Clarified

- Project framed as filesystem **convention** + schemas, not finished interop standard  
- Document version without `v`; Git tags with `v`  

## 0.1.0-draft — 2026-09-08

### Added

- Initial public seed: README, SPEC, white paper outline, MIT license  
- JSON Schemas: map + artifact envelope  
- Templates: minimal map, capability + decision artifacts  
- Examples: single-repo and multi-zone maps  
- Cookbook: brownfield init, what not to copy from incubators  

### Design stance

- Progressive disclosure (L0 = map only)  
- Zone = placement/coordination scope (ownership not implied)  
- `write` allow-list may be empty; optional `access`  
- External zones: schema-compatible, provisional, not required for Core orientation  
