# Cookbook: CI validation

> **Consumer ops guidance — not a new Core schema feature.**  
> Optional automation for maps you already maintain. Validation is **never** required for L0 orientation.

## Goal

Run a **deterministic** map check in CI so every consumer `.aap/map.yaml` (or equivalent) is judged against a **pinned** protocol revision — not against whatever `main` or a Gist tip happens to be today.

Pin details and dual-source honesty: [`schema-pinning.md`](./schema-pinning.md).

## Why pin in CI

| Pin | Effect |
|-----|--------|
| **Git tag** (e.g. `v0.2.1-prototype`) | Human-readable; matches release notes |
| **Commit SHA** | Immutable when tags lag or you need a one-off revision |
| Floating `main` / branch tip | **Silent drift** — yesterday’s green job can fail (or worse, pass a map that other clones reject) without any intentional upgrade |
| Mutable Gist / `raw/.../main/...` URL | Same problem: remote bytes change under the same URL |

> **Warning:** Validating against a **mutable Gist URL** or an **unpinned `main` (or any branch tip)** can **silently change CI behavior** when upstream moves. Treat that as a supply-chain footgun, not “staying current.” Upgrade pins deliberately (schema + lock/contract + fixtures together — see schema-pinning).

## What this seed validates

In **this** repository, CI runs:

```bash
pip install pyyaml jsonschema
python scripts/validate.py
```

[`scripts/validate.py`](../scripts/validate.py) checks in-repo `schemas/`, positive maps under `templates/` + `examples/` (except `examples/invalid/`), invalid fixtures that must fail, and artifact envelope templates. That is the seed’s own conformance job — not a universal multi-repo linter.

## Consumer maps (every checkout that ships a map)

Consumers typically want: **fail the PR if our map no longer matches the schema we pinned.**

Pick one approach and document the pin in-repo (tag or SHA):

1. **Vendored schema** — copy `schemas/map.schema.json` at a known pin into the consumer; validate `.aap/map.yaml` with `jsonschema` (or any Draft 7 validator). Offline-friendly.
2. **Pinned checkout** — shallow-clone or submodule **this** protocol repo at a **tag or commit**; point the job at that tree’s schema (and optionally adapt/run a thin check). Never `git clone … main` without pinning the ref.
3. **Contract sidecar** — optional local file recording `revision` + content hash (see schema-pinning); CI asserts the schema bytes match the lock.

Validation remains **CI / editor / conformance** tooling. Do **not** fetch upstream on every agent turn “to stay current.”

### Minimal generic CI step (example)

Vendor-neutral shape — map the `run:` body onto GitHub Actions, GitLab CI, Buildkite, etc. **Example only; not locked to one product.**

```yaml
# EXAMPLE — illustrative job fragment (any CI product)
# Pin MUST be a tag or commit SHA, never a floating branch name alone.
env:
  AAP_PIN: v0.2.1-prototype   # or full commit SHA
steps:
  - name: checkout-consumer
    run: # your normal workspace checkout

  - name: fetch-pinned-aap-schema
    run: |
      set -e
      git clone --depth 1 --branch "${AAP_PIN}" \
        https://github.com/gitpash/agent-artifact-protocol.git /tmp/aap
      # Prefer the in-repo schema at that pin — not a Gist tip URL
      test -f /tmp/aap/schemas/map.schema.json

  - name: install-validator-deps
    run: pip install pyyaml jsonschema

  - name: validate-consumer-map
    run: |
      set -e
      python - <<'PY'
      import json, sys
      from pathlib import Path
      import yaml, jsonschema
      schema = json.loads(Path("/tmp/aap/schemas/map.schema.json").read_text())
      # Adjust path to your discoverable map location
      data = yaml.safe_load(Path(".aap/map.yaml").read_text())
      jsonschema.Draft7Validator(schema).validate(data)
      print("OK consumer map validates against pinned schema")
      PY
```

Notes:

- Replace `AAP_PIN` with a **tag or SHA** your team owns; bump it in a deliberate PR.
- If you vendor the schema file instead of cloning, skip the clone step and validate against the vendored path — still record the pin next to it.
- Seed maintainers continue to run `python scripts/validate.py` on **this** repo; consumers need not import the whole seed example tree.

### Anti-patterns

- `AAP_PIN: main` or `git clone …` with default branch and no tag/SHA  
- `yaml-language-server: $schema=https://…/raw/main/map.schema.json` as the **only** CI contract  
- Validating laptop maps against pin A and CI against pin B “because both were green once”  
- Treating CI green as permission to preload SPEC / cookbook into every agent session  

## See also

- [`schema-pinning.md`](./schema-pinning.md) — pin styles, contract sidecar, Gist vs in-repo  
- [`brownfield-init.md`](./brownfield-init.md) — pin during first map copy  
- [`README.md`](../README.md) — `scripts/validate.py` one-liner for this seed  
- [`CONTRIBUTING.md`](../CONTRIBUTING.md) — Core vs profile; keep L0 small  
