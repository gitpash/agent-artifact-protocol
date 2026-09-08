# AAP Core Specification

**Protocol:** Agent Artifact Protocol (AAP)  
**Version:** 0.1.0-draft  
**Status:** Draft  
**Keywords:** MUST / MUST NOT / SHOULD / MAY as in [RFC 2119](https://www.rfc-editor.org/rfc/rfc2119)

---

## 0. Abstract

AAP is a **runtime-agnostic filesystem convention** for repository orientation and optional durable agent/human memory.

**One-liner:** *AAP makes repository context addressable without requiring repository context to be loaded.*

It standardizes:

1. **Thin topology (map)** — zones + intent→path addresses  
2. **Artifacts** — typed envelope-addressable units when memory must persist  
3. **Duty classes** — scratch vs durable maintain expectations  
4. **Light conformance** — orientation / artifact / topology labels  

It does **not** standardize retrieval engines, agent orchestration, embeddings, IDE hooks, or task trackers.

**Philosophy:** conventions over infrastructure; discovery over preloading; progressive disclosure over context dumping; files over runtime dependencies.

---

## 1. Goals and non-goals

### 1.1 Goals

- Improve agent navigation **without** becoming another context dependency  
- Stop path hallucination via explicit layout intents when a map is present  
- Keep Source of Truth in git-diffable files  
- Brownfield adoption (`migrate-on-touch`) without mass rewrite  
- Keep the **L0 orientation surface tiny**  

### 1.2 Non-goals

- Not a context engine, RAG stack, or dynamic context loader  
- Not an agent framework or step engine  
- Not a replacement for LSP, tests, or `grep`/search  
- Not mandatory embeddings or knowledge graphs  
- Not GitHub-only process binding  
- Not a mandate to preload SPEC, schemas, or artifact corpora at session start  

### 1.3 Progressive disclosure (normative)

| Level | What | When |
|-------|------|------|
| **L0** | Map only | New session / workspace |
| **L1** | Optional zone index | After intent→zone |
| **L2** | One artifact | Durable memory needed |
| **L3** | Code + tools | Implementation evidence |

**MUST NOT:**

1. Require loading the entire artifact library, this upstream repository, or full SPEC into model context to begin work.  
2. Define a proprietary retrieval protocol; tools resolve addresses.  
3. Implement adapters as “always attach full AAP docs to the system prompt.”  

Producers SHOULD keep maps sparse. Essays belong in L1/L2, not the map.

**Orientation leads; artifacts follow.** Artifact features MUST NOT force L0 bloat.

---

## 2. Concepts

| Term | Meaning |
|------|---------|
| **Workspace** | Tree where the agent operates |
| **Map** | Registry of zones (+ optional defaults, overlays, profiles list) |
| **Zone** | Named **placement and coordination** scope; ownership is optional and not implied |
| **Layout** | Intent → directory root(s) relative to resolved zone root |
| **Intent** | Why read/write: `code`, `tests`, `artifacts`, `scratch`, … |
| **Artifact** | Durable unit with Core envelope + body |
| **Envelope** | Portable metadata (YAML frontmatter or sidecar) |
| **Derived** | Regenerable views (HTML, vectors, graphs) — not canonical SoT |

---

## 3. Map

### 3.1 Discovery (first hit wins)

1. `./.aap/map.yaml`  
2. `./map.yaml`  
3. `./docs/map.yaml`  

L0 agents SHOULD read **only** this file at orientation unless the task already names paths.

### 3.2 Shape

```yaml
version: 1
defaults:
  layout: { ... }
zones:
  <zone-id>:
    path: <rel path from workspace root>   # required for internal zones
    kind: <string>                         # soft hint
    write: [domain | architect]            # may be []
    access: read-only | read-write         # optional
    layout: { ... }
overlays:                                  # prefer gitignored map.local.yaml
  local_paths:
    <zone-id>: <absolute or other checkout path>
profiles:
  enabled: [<id>, ...]                     # optional; unknown ids ignored
```

- **version:** MUST be `1` for this draft.  
- **Zone ids:** SHOULD match `^[a-z][a-z0-9-]*$`.  
- **path:** Relative to workspace root; `.` for repo root.  
- **write:** Mutating allow-list. Empty = no declared write grant.  
- **access:** Optional. Prefer `access: read-only` with `write: []` for consume-only zones.  

Machine-local overlays SHOULD use `map.local.yaml` / `docs/map.local.yaml` / `.aap/map.local.yaml` (gitignored). Absolute paths MUST NOT be required for CI.

JSON Schema: [`schemas/map.schema.json`](./schemas/map.schema.json).

### 3.3 Layout intents

Layout MUST NOT inventory individual source files.

**Core intents:** `code`, `tests`, `artifacts`, `scratch`  
**Standard optional:** `scripts`, `infra`, `proposals`, `architecture`  
**Extension:** any other key → path or path list  

Paths: relative to resolved zone root; `/` separators; MUST NOT contain `..`; SHOULD NOT be absolute.

**Merge:** zone `layout` overrides `defaults.layout` key-wise (replace).  
**Write target:** first listed root for an intent unless specified.  
**Missing intent:** MUST NOT invent a parallel conventional root for an intent that already exists; ask or fail closed for that write.

### 3.4 Resolved root

```text
if overlays.local_paths[zone] exists → use it
else join(workspace, zone.path) if present
else UNRESOLVED for tree IO (zone metadata may still be useful)
```

Longest-prefix match of resolved roots selects the zone for a filesystem path.

### 3.5 External zones (provisional)

`relation: external` + `remote` is schema-compatible and **not required** for Core orientation conformance.  
Use for partner checkouts without git submodules. Details may graduate via a future profile; consumers MAY ignore unknown external-only fields.

### 3.6 When a map is required

| Workspace | Map |
|-----------|-----|
| Claiming **topology** multi-root orientation | SHOULD provide a map |
| Single repo orientation | MAY use one-zone map or omit (artifact-only still possible) |

---

## 4. Artifacts

### 4.1 Envelope (required when claiming AAP addressability)

| Field | Rule |
|-------|------|
| `id` | Stable; MUST NOT reuse for a new meaning |
| `type` | Core enum or dotted extension |
| `zone` | Map zone id, or default single-zone id |
| `status` | `draft` \| `active` \| `deprecated` |
| `updated` | `YYYY-MM-DD` |

Recommended: `title`, `summary`, `stability`, `maintain`, `owner`, `refs`, `supersedes` / `superseded_by`.

JSON Schema: [`schemas/artifact-envelope.schema.json`](./schemas/artifact-envelope.schema.json).

### 4.2 Core types

| type | Role |
|------|------|
| `capability` | What a zone exposes |
| `decision` | Why this way |
| `contract` | Cross-zone guarantee (prefer global/shell zone when multi-zone) |
| `gotcha` | Costly rediscovery hazard |
| `impact` | Change blast sketch (often short-lived) |

Extension types MUST use a dot (`diagram.sequence`, …). Readers MUST parse Core fields even if `type` is unknown.

### 4.3 Body

- Default body: UTF-8 Markdown with YAML frontmatter.  
- Non-Markdown canonical files: envelope via sidecar `*.aap.md` or `*.aap.yaml` + `canonical_path` / `body_format`.  
- Bodies SHOULD stay small (Memoryfield-inspired ~8KiB guidance); split rather than grow endless pages.  

### 4.4 stability / maintain

| stability | Meaning |
|-----------|---------|
| `scratch` | Disposable; MUST NOT gate merge on freshness |
| `experimental` | Trying a convention |
| `durable` | Intentional memory |

| maintain | Who pays |
|----------|----------|
| `nobody` | No duty |
| `owner` | Named owner |
| `zone` | Zone writers |
| `core` | Rare; workspace-wide expectation |

Committed ≠ must maintain. Scratch is first-class.

### 4.5 refs

Opaque strings. URI-like forms RECOMMENDED (`gh:owner/repo#1`, `id:other`, `path:…`). Core MUST NOT require a single tracker.

---

## 5. Agent algorithms

### 5.1 Orientation (default)

```text
1. Discover map only
2. Merge local overlays if present
3. Choose zone + intent from task
4. Targeted retrieve under layout roots (grep/LSP/index/…)
5. Open specific artifacts only if needed
6. Open SPEC only when editing/validating protocol structure
```

### 5.2 Write

```text
1. Orient via map
2. Check write allow-list for active mutating mode
3. Resolve layout intent path
4. Do not invent parallel roots
5. Write envelope + body
6. Cross-zone conflict → BLOCKED with reason (not silent foreign edits)
```

---

## 6. Conformance labels

| Label | Meaning |
|-------|---------|
| **Orientation** | Discoverable sparse map; intent routing possible |
| **Artifact** | Claimed AAP notes carry required envelope fields |
| **Topology** | Multi-root zones with honest paths / resolution rules |

Optional schema validation is L1+. L0 MUST work without a linter.

---

## 7. Distribution and pinning

- This repository is a **blueprint**, not a live session dependency.  
- Consumers SHOULD pin a **tag or commit** if they vendor schemas/templates.  
- Ordinary agent turns MUST use the **local** map, not fetch upstream.  
- Bootstrap tools (if any) MUST be explicit, additive, dry-run capable, human-reviewed.  

---

## 8. Security

- Artifacts MUST NOT store secrets or raw PII.  
- Write/access fields are coordination fences, not authentication.  
- Map edits that expand write authority are sensitive in review.  

---

## 9. Versioning

Breaking Core changes require a version bump and changelog entry.  
`0.1.0-draft` may still change before `0.1.0`.
