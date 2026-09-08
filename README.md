# Agent Artifact Protocol (AAP)

**Version:** 0.1.0-draft  
**Status:** experimental specification seed  
**License:** MIT

> **AAP makes repository context addressable without requiring repository context to be loaded.**

AAP is a **runtime-agnostic filesystem convention** for:

1. **Repository orientation** — a tiny map: intent → zone → path  
2. **Optional durable memory** — typed Markdown (or profile-defined) artifacts with a small envelope  

It is **not** a context engine, RAG stack, agent harness, or mandatory preload pack.

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
2. Edit zone `path` / `layout` to match **your** tree (keep it sparse).
3. Tell the agent: *read the map first; do not preload AAP upstream docs.*
4. Compare on a real task: **no map** vs **map only**.

Optional later: copy [`schemas/`](./schemas/) into the consumer (version-pin) for editor/CI validation — never required for L0 orientation.

```bash
# conceptual pin (no runtime fetch during normal agent sessions)
# git clone --depth 1 --branch v0.1.0-draft \
#   https://github.com/gitpash/agent-artifact-protocol.git /tmp/aap
# cp /tmp/aap/templates/minimal-map.yaml .aap/map.yaml
```

Init tooling, if added later, MUST be **explicit**, **additive**, **dry-run capable**, and **human-reviewed**. It MUST NOT rewrite `CLAUDE.md` / `.specify/` / existing docs homes by default.

---

## Repository layout (this seed)

```text
README.md                 # you are here
SPEC.md                   # normative Core (on demand — not L0)
WHITE-PAPER.md            # thesis and positioning
LICENSE
CHANGELOG.md
schemas/                  # map + artifact envelope JSON Schema
templates/
  minimal-map.yaml        # L0 starter
  artifact-capability.md
  artifact-decision.md
examples/
  single-repo/map.yaml
  multi-zone/map.yaml
cookbook/
  brownfield-init.md
  what-not-to-copy.md
```

**Not in this seed (on purpose):** product adoption guides, pilot metrics, partner-repo contracts, agent runtime adapters, CLI.

---

## Core ideas (short)

| Term | Meaning |
|------|---------|
| **Map** | Sparse registry of zones + layout intents |
| **Zone** | Named **placement/coordination** scope (not automatic team ownership) |
| **Layout** | Intent → directory root(s) (`code`, `tests`, `artifacts`, `scratch`, …) |
| **Artifact** | Durable note with envelope fields (`id`, `type`, `zone`, `status`, `updated`, …) |
| **Write** | Allow-list of mutating modes: `domain`, `architect` (may be `[]`) |
| **Access** | Optional `read-only` / `read-write` |

Core artifact `type` values: `capability` | `decision` | `contract` | `gotcha` | `impact`  
Extension types use dots: `diagram.sequence`, …

External / cross-repo zones (`relation: external`) are a **provisional** schema-compatible extension — not required to claim Core orientation.

Full rules: [`SPEC.md`](./SPEC.md).

---

## Conformance (lightweight)

| Label | Means |
|-------|--------|
| **Orientation** | A discoverable sparse map exists; agents may use intent routing |
| **Artifact** | Durable notes use the envelope field set when claiming AAP addressability |
| **Topology** | Multi-root workspace map lists zones with honest paths |

Validation with JSON Schema is optional (L1+). Missing schema must not block L0.

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

`0.1.0-draft` — usable as a blueprint; expect breaking refinements until `0.1.0` or `1.0.0`.

Issues and PRs welcome. Prefer proposals that keep L0 small.
