# Cookbook: schema pinning

> **Profile status:** used in practice

> **Consumer ops guidance — not a new Core schema feature.**  
> Keeps validators honest when upstream evolves.

## Problem

Map validation drifts when consumers:

- validate against a **floating branch tip** (`main`, `latest`)  
- mix a **Gist raw URL** editor hint with a **different** in-repo schema revision  
- upgrade schema, lock file, and fixtures on different days  

Agents then “pass” maps that other clones reject — or the reverse.

## Rules of thumb

1. **Pin by immutable tag or commit** when validating or vendoring schemas.  
2. **MUST NOT** treat `main` / floating raw URLs as the live runtime contract during ordinary agent turns.  
3. Optional **contract file** in the consumer MAY record revision + content hash for deterministic checks.  
4. Be **honest** about dual sources of truth (e.g. editor `$schema` Gist URL vs `schemas/map.schema.json` in this repo).

## Pin styles (pick one and document it)

| Style | Example | Notes |
|-------|---------|--------|
| **Git tag** | `v0.2.1-prototype` | Preferred for humans; matches CHANGELOG language with `v` prefix on tags |
| **Commit SHA** | full or abbreviated immutable SHA | Best when tags lag |
| **Vendored file** | copy `schemas/map.schema.json` into consumer | Offline CI; bump deliberately |
| **Contract sidecar** | e.g. `.aap/aap-contract.yaml` with `revision` + `sha256` | Optional; consumer convention |

Conceptual pin (no fetch during normal sessions):

```bash
# git clone --depth 1 --branch v0.2.1-prototype \
#   https://github.com/gitpash/agent-artifact-protocol.git /tmp/aap
# cp /tmp/aap/schemas/map.schema.json path/to/consumer-tools/
```

One-line consumer note (example):

```text
# .aap/VERSION  (or equivalent local note)
v0.2.1-prototype
https://github.com/gitpash/agent-artifact-protocol
```

## Optional contract file (informative)

```yaml
# Consumer-local — not required by Map v2 Core
schema:
  name: map.schema.json
  pin: v0.2.1-prototype      # or commit SHA
  # sha256: <hex of pinned bytes>
source: https://github.com/gitpash/agent-artifact-protocol
```

Upgrade **schema revision, lock/contract, validator, and compatibility fixtures together**. Partial upgrades are how tip-drift returns.

## Dual gist vs in-repo honesty

This seed’s minimal map template may carry a `yaml-language-server: $schema=…` comment pointing at a **revision-pinned** raw URL for editor UX. The **repository** also ships `schemas/map.schema.json`.

| Surface | Role |
|---------|------|
| In-repo `schemas/` | CI and `scripts/validate.py` SoT for this seed |
| Pinned remote URL in a comment | Editor convenience — **must** name an immutable revision, not tip |
| Consumer contract file | Local lock for *their* validators |

**MUST NOT** silently validate against Gist or GitHub **tip**. If Gist and git diverge, say so and pick one pin for automation until they match.

Validation is **never** required for L0 orientation. Schema checks are for editors, CI, and conformance claims — not session start preload.

## Anti-patterns

- `raw/.../main/map.schema.json` as the only pin  
- Different SHAs in CI vs laptop “because both green yesterday”  
- Expanding Core schema to encode stream packs “so we can validate profiles” without multi-consumer evidence  
- Fetching upstream on every agent turn to “stay current”  

## See also

- [`brownfield-init.md`](./brownfield-init.md) — pin step during init  
- [`README.md`](../README.md) — pin language in 60-second start  
- [`CONTRIBUTING.md`](../CONTRIBUTING.md) — Core vs profile; L0 budget  
