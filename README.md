# Agent Artifact Protocol (AAP)

**Version:** 0.2.0-draft
**Status:** experimental Map v2 proposal
**License:** MIT
**Git tag form:** `v0.2.0-draft` (documents omit the `v` prefix)

> **AAP makes repository context addressable without requiring repository context to be loaded.**

> **Breaking draft revision.** `0.2.0-draft` replaces the historical v1 `zones` map with a repository-oriented v2 `workspace` / `self` / `nodes` map. The v1 material is retained under `legacy/v1/` for historical reference and is not compatible with v2.

AAP is a **runtime-agnostic filesystem convention** for:

1. **Repository orientation** — a tiny map using **layout categories** → zone → directory root  
2. **Optional durable memory** — typed Markdown (or profile-defined) artifacts with a small envelope  

It is **not** a context engine, RAG stack, agent harness, security sandbox, or mandatory preload pack.

In v0.1, an “intent” is a **small vocabulary key** such as `code`, `tests`, `artifacts`, or `scratch` — **not** a natural-language task classifier. AAP does not understand phrases like “modernize the API” by itself; the agent (or human) picks a layout key and looks under that root.

Philosophy (aligned with formats like [Memoryfield](https://github.com/calpaterson/memoryfield-spec)):

- conventions over infrastructure  
- discovery over preloading  
- progressive disclosure over context dumping  
- files over runtime dependencies  

---

## Progressive disclosure

| Level | What | When |
|-------|------|------|
| **L0** | Map only | Session / workspace start |
| **L1** | Optional zone index | After choosing a zone |
| **L2** | One artifact | When durable memory is needed |
| **L3** | Code + `grep` / LSP / indexes | Implementation — outside AAP |

**MUST NOT:** force agents to load this whole repository, the full SPEC, or an artifact corpus into the model context to begin work.

---

## 60-second start (brownfield)

1. Copy [`templates/minimal-map.yaml`](./templates/minimal-map.yaml) to **one** of:
   - `.aap/map.yaml` (preferred)
   - `map.yaml`
   - `docs/map.yaml`
2. Edit `self`, direct `nodes`, and `layout` paths to match **your** repository (keep it sparse).
3. Tell the agent: *read the map first; do not preload AAP upstream docs.*
4. Compare on a real task: **no map** vs **map only**.

For editor/CI validation, pin this repository by immutable tag or commit. `schemas/map.schema.json` is the current v2 contract; do not validate against a floating branch tip. Validation is never required for L0 orientation.

```bash
# conceptual pin (no runtime fetch during normal agent sessions)
# git clone --depth 1 --branch v0.2.0-draft \
#   https://github.com/gitpash/agent-artifact-protocol.git /tmp/aap
# mkdir -p .aap && cp /tmp/aap/templates/minimal-map.yaml .aap/map.yaml
```

Init tooling, if added later, MUST be **explicit**, **additive**, **dry-run capable**, and **human-reviewed**. It MUST NOT rewrite `CLAUDE.md` / `.specify/` / existing docs homes by default. **If a target file already exists, init MUST stop or require explicit per-file confirmation** — never silent overwrite.

---

## Repository layout (this seed)

```text
README.md
SPEC.md                   # Map v2 Core (on demand — not L0)
MOTIVATION.md
CONTRIBUTING.md
LICENSE
CHANGELOG.md
schemas/                  # current Map v2 schema
legacy/v1/                # historical v1 zones schema and examples
templates/
examples/
  single-repo/ shell/ resource-ref/ invalid/
cookbook/
scripts/validate.py
.github/workflows/validate.yml
```

**Not in this seed (on purpose):** product adoption guides, pilot metrics, partner-repo contracts, agent runtime adapters, CLI.

---

## Core ideas (short)

| Term | Meaning |
|------|---------|
| **Map** | Sparse description of the opened workspace, its layout, and direct navigation nodes |
| **Node** | Direct navigational hop to a related repository/product; not a dependency declaration |
| **Layout key** | `code`, `tests`, `artifacts`, `scratch`, … → resource reference(s) |
| **resourceRef** | A relative path string or `{ path, access?, description? }`; default access is `read-write` |
| **Artifact** | Optional durable note; the historical v1 envelope remains separately versioned |
| **Write / access** | Advisory coordination metadata, never access control |

### `write` is not security

```yaml
# Coordination hint only — NOT access control / sandboxing.
write: [maintainer]
```

AAP **cannot** prevent a human or agent from writing outside these paths. Real enforcement requires Git permissions, CODEOWNERS, host policy, or a runtime sandbox.

If no active mutating mode is **explicitly** provided by the user/runtime, the default is **no write grant** (read/orient only).

Core artifact `type` values: `capability` | `decision` | `contract` | `gotcha` | `impact`  
Recommended stable ids use a namespace-like form such as `<zone>/<type>/<slug>`. Id uniqueness across a corpus is a tooling concern, not distributed allocation provided by Core.
Extension types SHOULD use dots (`diagram.sequence`). The Core JSON Schema validates **envelope shape**; it does not fully police extension namespaces (repository validators MAY).

External / cross-repo nodes are schema-compatible direct navigation hops; their write policy is deployment-specific.

Full rules: [`SPEC.md`](./SPEC.md).

---

## Conformance (lightweight)

| Label | Means |
|-------|--------|
| **Orientation** | A discoverable sparse map exists; agents may use layout-based discovery |
| **Artifact** | Durable notes use the envelope field set when claiming AAP addressability |
| **Topology** | A workspace map lists honest direct navigation nodes and paths |

This draft is a **convention + schemas**, not a complete cross-file protocol suite. Schema does not yet prove zone membership of every path, unique ids across a corpus, etc.

```bash
pip install pyyaml jsonschema
python scripts/validate.py
```

---

## Relationship to consumer repos

| This repo (upstream) | Your product repo |
|----------------------|-------------------|
| Spec + templates + examples | **Pinned** copy or reference by tag |
| Evolves via semver / tags | Local `map.yaml` + local artifacts |
| Not fetched on every agent turn | L0 = local map only |

Pin by **tag or commit**. Do not treat `main` as a live runtime dependency.

---

## Experiment before you expand

```text
A) agent without map
B) agent with map only   (no SPEC dump)
```

If B does not improve time-to-locus / wrong-home rate, **shrink** the map — do not add schemas and profiles first.

---

## Status

`0.2.0-draft` — experimental Map v2 blueprint. **Not** production infrastructure or a finished interoperability standard.

Feedback is especially welcome on:

- map size and usefulness in brownfield repos  
- whether layout keys are the right granularity  
- interoperability across agent runtimes without preload  
- whether Core is still too large  

See [`CONTRIBUTING.md`](./CONTRIBUTING.md). Issues and PRs welcome; prefer proposals that keep L0 small.
