# Changelog

## Unreleased

### Deprecated

- Archived the 0.1.1-draft material as a non-normative legacy trial. It remains reproducible for historical reference, but is not the AnyTag v2 map contract or validator.

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
