# Changelog

## Unreleased

### Added

- Cookbook: `hub-umbrella.md`, `stream-packs.md`, `local-bootstrap.md` (optional profiles / teaching patterns)
- Cookbook: `done-bar.md`, `schema-pinning.md`, `glass-box-factory.md` (pattern only), `orchestrator-session.md` (harness-agnostic manager/worker shape)
- Examples: `examples/hub-umbrella/` (synthetic multi-node shell + child map), `examples/stream-packs/` (orientation, local index example, research / release-check / accept-default samples)
- Examples: `examples/invalid/anti-multi-stream-open.md`, `anti-recursive-preload.md` (disclosure anti-patterns); `examples/shell/README.md` cross-link to hub-umbrella
- Templates: `templates/orientation.md`, `templates/stream-pack.yaml` stubs
- README: Core vs profile table; progressive disclosure footnote that profile bootstrap is not Core L0; links to new cookbook pages and templates; optional **Disclosure profile** conformance row; prototype-narrative note (unreleased)
- SPEC: overlays, extension layout keys, optional `profiles` block, non-normative optional local files (schema-preexisting surfaces; prose only)
- MOTIVATION: experiment metrics sketch (wrong-home, index degrade honesty, accept-bar catches)
- CONTRIBUTING: stream packs / accept bars / orientation templates are **profile PRs**, not Core MUST; L0 budget reminder for profile bootstrap

### Clarified

- Core L0 remains map-only for Orientation conformance
- Dogfood-inspired profiles (stream packs, thin orientation, accept bar, thin runtime dispatcher, done bar) are **optional**; no specific agent harness or multi-agent runtime is required
- Status narrative: working-prototype cookbook alongside experimental Map v2 — still not a finished interop standard
- Glass-box factory and orchestrator session are **patterns** documented in cookbook — this repo does **not** ship conductor CLI
- `what-not-to-copy.md`: factory/orchestrator/status-macro/dispatcher/index anti-copies; copy stream-pack, done-bar, and hub-umbrella **ideas**
- Schema pinning: immutable tag/commit; MUST NOT validate against tip; dual gist vs in-repo honesty

### Not changed

- Map v2 required fields and `resourceRef` semantics
- Schema document version / git tag (`0.2.0-draft` / `v0.2.0-draft`)
- Core size goals (profiles stay out of mandatory L0)

### Unreleased candidate notes (not tagged)

Draft text for a possible future **docs-only** `0.2.1-prototype` label — **candidate only**. Do **not** treat as released; **no** git tag from this changelog alone; Core remains experimental.

```text
## 0.2.1-prototype — (date TBD; unreleased candidate)

### Added
- Cookbook: hub umbrella, stream packs, local bootstrap, done-bar, schema-pinning,
  glass-box-factory (pattern), orchestrator-session (optional profiles / patterns)
- Examples: hub-umbrella, stream-packs samples; invalid disclosure anti-pattern notes
- Templates: orientation.md, stream-pack.yaml stubs
- SPEC clarifications: overlays, extension layout keys, profiles block (schema-preexisting)

### Clarified
- Core L0 remains map-only for Orientation conformance
- Dogfood-inspired profiles are optional; multi-agent runtimes not required
- Status: working-prototype docs; still not a finished interop standard

### Not changed
- Map v2 required fields / resourceRef semantics
```

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
