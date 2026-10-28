# Changelog

## Unreleased

- `llms.txt`: agent-readable entry point (what AAP is, what to open first, `access` rules, links).
- `skills/aap-map/`: portable agent skill that drafts and validates a minimal map, with `scripts/validate_map.py` and a bundled copy of the Map v2 schema.
- `.claude-plugin/` manifests and a README section "Use with your agent". Nothing is published to any registry.
- `scripts/validate.py` checks that the bundled schema copy matches `schemas/map.schema.json` and that plugin manifests parse.

## 0.2.1-prototype — 2026-10-16

**Docs / cookbook prototype label.** Map v2 **Core schema and required fields are unchanged** from `0.2.0-draft`. This release makes optional profiles and teaching materials legible. It is **not** a finished interoperability standard and does **not** mark Core stable.

### Added

- Cookbook: `hub-umbrella.md`, `stream-packs.md`, `local-bootstrap.md` (optional profiles / teaching patterns)
- Cookbook: `done-bar.md`, `schema-pinning.md`, `glass-box-factory.md` (pattern only), `orchestrator-session.md` (harness-agnostic manager/worker shape)
- Examples: `examples/hub-umbrella/` (synthetic multi-node shell + child map), `examples/stream-packs/` (orientation, local index example, research / release-check / accept-default samples)
- Examples: `examples/invalid/anti-multi-stream-open.md`, `anti-recursive-preload.md` (disclosure anti-patterns); `examples/shell/README.md` cross-link to hub-umbrella
- Templates: `templates/orientation.md`, `templates/stream-pack.yaml` stubs
- README: Core vs profile table; progressive disclosure footnote that profile bootstrap is not Core L0; links to new cookbook pages and templates; optional **Disclosure profile** conformance row
- SPEC: overlays, extension layout keys, optional `profiles` block, non-normative optional local files (schema-preexisting surfaces; prose only)
- MOTIVATION: experiment metrics sketch (wrong-home, index degrade honesty, accept-bar catches)
- CONTRIBUTING: stream packs / accept bars / orientation templates are **profile PRs**, not Core MUST; L0 budget reminder for profile bootstrap

### Clarified

- Core L0 remains map-only for Orientation conformance
- Dogfood-inspired profiles (stream packs, thin orientation, accept bar, thin runtime dispatcher, done bar) are **optional**; no specific agent harness or multi-agent runtime is required
- Status narrative: working-prototype **docs** alongside experimental Map v2 Core
- Glass-box factory and orchestrator session are **patterns** documented in cookbook — this repo does **not** ship conductor CLI
- `what-not-to-copy.md`: factory/orchestrator/status-macro/dispatcher/index anti-copies; copy stream-pack, done-bar, and hub-umbrella **ideas**
- Schema pinning: immutable tag/commit; MUST NOT validate against tip; dual gist vs in-repo honesty

### Not changed

- Map v2 required fields and `resourceRef` semantics
- Core size goals (profiles stay out of mandatory L0)
- `schemas/map.schema.json` document shape (still the v2 contract introduced in `0.2.0-draft`)

### Git tag

- Documents / CHANGELOG: `0.2.1-prototype` (no `v`)
- Git tag: `v0.2.1-prototype` (with `v`)

## 0.2.0-draft — 2026-09-11

Map v2 introduction (historical). Prefer pinning **`v0.2.1-prototype`** (or later) for docs+schema teaching set; Core map rules below still apply.

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

Initial public draft (v1 zones map). Superseded by Map v2; see `legacy/v1/`.
