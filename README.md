# Agent Artifact Protocol (AAP)

**Version:** 0.2.1-prototype  
**Status:** experimental Map v2 Core + dogfood-informed **optional** profiles (working-prototype **docs**)  
**License:** MIT  
**Git tag form:** `v0.2.1-prototype` (documents omit the `v` prefix)

> **AAP makes repository context addressable without requiring repository context to be loaded.**

> **Map v2** (`0.2.0-draft` lineage) replaced the historical v1 `zones` map with a repository-oriented `workspace` / `self` / `nodes` map. **`0.2.1-prototype`** is a **docs/cookbook** label on that same Core — optional profiles and examples, **not** a claim that Core is a finished interop standard. v1 material remains under `legacy/v1/`.

AAP is a **runtime-agnostic filesystem convention** for:

1. **Repository orientation** — a tiny map using **layout categories** → directory root  
2. **Optional durable memory** — typed Markdown (or profile-defined) artifacts with a small envelope  

It is **not** a context engine, RAG stack, agent harness, security sandbox, or mandatory preload pack.

In v0.2, a layout key is a **small vocabulary key** such as `code`, `tests`, `artifacts`, or `scratch` — **not** a natural-language task classifier. AAP does not understand phrases like “modernize the API” by itself; the agent (or human) picks a layout key and looks under that root.

Philosophy (aligned with formats like [Memoryfield](https://github.com/calpaterson/memoryfield-spec)):

- conventions over infrastructure  
- discovery over preloading  
- progressive disclosure over context dumping  
- files over runtime dependencies  

---

## Progressive disclosure

| Level | What | When |
|-------|------|------|
| **L0** | Map only | Session / workspace start (**Orientation conformance**) |
| **L1** | Targeted path or layout index | After choosing a layout key or node |
| **L2** | One artifact | When durable memory is needed |
| **L3** | Code + normal tools (`grep` / LSP / indexes) | Implementation — outside AAP |

**Optional profile bootstrap (not Core L0):** some deployments also open a thin orientation card and **exactly one** task-class stream pack after the map. That is **consumer/runtime policy**. It does **not** redefine L0 and **MUST NOT** become “read the whole cookbook every session.”

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
5. **Optional profiles** (after the map-only experiment helps): multi-repo shell → [`cookbook/hub-umbrella.md`](./cookbook/hub-umbrella.md); session procedure → [`cookbook/stream-packs.md`](./cookbook/stream-packs.md) + [`cookbook/local-bootstrap.md`](./cookbook/local-bootstrap.md); honesty exit → [`cookbook/done-bar.md`](./cookbook/done-bar.md). Stubs: [`templates/orientation.md`](./templates/orientation.md), [`templates/stream-pack.yaml`](./templates/stream-pack.yaml).

For editor/CI validation, pin this repository by immutable tag or commit (see [`cookbook/schema-pinning.md`](./cookbook/schema-pinning.md)). `schemas/map.schema.json` is the current v2 contract; do not validate against a floating branch tip. Validation is never required for L0 orientation.

```bash
# conceptual pin (no runtime fetch during normal agent sessions)
# git clone --depth 1 --branch v0.2.1-prototype \
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
  minimal-map.yaml
  orientation.md          # optional thin card stub
  stream-pack.yaml        # optional pack stub
  artifact-*.md
examples/
  single-repo/ shell/ hub-umbrella/ resource-ref/
  stream-packs/           # optional profile samples (not Core maps)
  invalid/                # schema fixtures + disclosure anti-pattern notes
cookbook/
  brownfield-init.md
  hub-umbrella.md
  stream-packs.md
  local-bootstrap.md
  done-bar.md
  schema-pinning.md
  glass-box-factory.md    # pattern only — no CLI in this repo
  orchestrator-session.md # harness-agnostic manager/worker shape
  what-not-to-copy.md
scripts/validate.py
.github/workflows/validate.yml
```

**Not in this seed (on purpose):** product adoption guides, pilot metrics dashboards, partner-repo contracts, agent runtime adapters, factory/conductor CLI, mandatory multi-agent harnesses.

---

## Core vs profile

| Layer | In tree | Required for Orientation? |
|-------|---------|---------------------------|
| Map v2 (`workspace` / `self` / `nodes` / `layout`) | Yes | **Yes** |
| Progressive disclosure law (L0 map → … → L3 tools) | Yes | **Yes** (behavior) |
| Artifact envelope (historical draft) | Yes | Only if claiming Artifact addressability |
| `brownfield-artifacts` profile | SPEC prose | **No** |
| Stream packs / accept bars / orientation cards | Cookbook + examples + templates | **No** (Profile) |
| Thin runtime dispatcher (`AGENTS.md` / local bootstrap) | Cookbook only | **No** (Profile) |
| Multi-repo hub-umbrella teaching pattern | Cookbook + examples | **No** (pattern on Core maps) |
| Done bar / schema-pinning ops notes | Cookbook | **No** (Profile / ops) |
| Orchestrator session / glass-box factory **patterns** | Cookbook only (no CLI shipped) | **No** |
| Multi-agent “teams” runtimes | Out of tree | **No** (one possible impl of orchestrator shape) |

**Core** stays small: sparse maps + disclosure law + optional artifact envelope.  
**Profiles** are optional elaborations documented in the cookbook. They **MUST NOT** be treated as a mandatory first-read corpus.

---

## Core ideas (short)

| Term | Meaning |
|------|---------|
| **Map** | Sparse description of the opened workspace, its layout, and direct navigation nodes |
| **Node** | Direct navigational hop to a related repository/product; not a dependency declaration |
| **Layout key** | `code`, `tests`, `artifacts`, `scratch`, … → resource reference(s); extensions allowed |
| **resourceRef** | A relative path string or `{ path, access?, description? }`; default access is `read-write` |
| **Artifact** | Optional durable note; the historical v1 envelope remains separately versioned |
| **Write / access** | Advisory coordination metadata, never access control |
| **Profile** | Optional named elaboration (streams, accept bar, brownfield-artifacts, …) — not Core L0 |

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
| **Disclosure profile** *(optional)* | Consumer adds stream packs / accept bars / thin orientation — **not** required for Orientation |

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
| Cookbook profiles | Opt-in local files (often gitignored) |

Pin by **tag or commit**. Do not treat `main` as a live runtime dependency.

---

## Experiment before you expand

```text
A) agent without map
B) agent with map only   (no SPEC dump)
```

If B does not improve time-to-locus / wrong-home rate, **shrink** the map — do not add schemas and profiles first.

Only after B helps, try optional profiles (one stream pack, hub umbrella, accept bar).

---

## Status

`0.2.1-prototype` — experimental Map v2 Core **plus** a dogfood-informed **cookbook prototype** (hub umbrella, stream packs, local bootstrap, done-bar, schema pinning, session patterns). Useful in multi-repo pilots. **Not** production infrastructure or a finished interoperability standard. Optional profiles do **not** promote Core to stable; pin with git tag `v0.2.1-prototype` (or commit SHA).

Feedback is especially welcome on:

- map size and usefulness in brownfield repos  
- whether layout keys are the right granularity  
- interoperability across agent runtimes without preload  
- whether Core is still too large  
- whether optional profiles stay clearly optional in practice  

See [`CONTRIBUTING.md`](./CONTRIBUTING.md). Issues and PRs welcome; prefer proposals that keep L0 small.
