# Changelog

## 0.1.1-draft — 2026-09-08

### Added

- `scripts/validate.py` + GitHub Actions workflow (schema, maps, envelopes, invalid fixtures)  
- `examples/invalid/*` negative cases  
- `CONTRIBUTING.md`  
- Explicit: layout keys ≠ NL intent router; `write` ≠ security; default mode = no write grant  
- Init no-overwrite rule in cookbook  
- `updated` field semantics (material change, not verification)  
- Core schema posture: envelope shape permissive on extension `type`  

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
