# AAP Core Specification

**Name:** Agent Artifact Protocol (AAP)  
**Kind:** Filesystem **convention** + JSON Schemas (draft; not a complete interop test suite)  
**Version:** 0.1.1-draft  
**Git tag:** `v0.1.1-draft`  
**Status:** Draft  
**Keywords:** MUST / MUST NOT / SHOULD / MAY as in [RFC 2119](https://www.rfc-editor.org/rfc/rfc2119)

---

## 0. Abstract

AAP is a **runtime-agnostic filesystem convention** for repository orientation and optional durable agent/human memory.

**One-liner:** *AAP makes repository context addressable without requiring repository context to be loaded.*

It standardizes:

1. **Thin topology (map)** — zones + **layout-category** → directory root addresses  
2. **Artifacts** — typed envelope-addressable units when memory must persist  
3. **Duty classes** — scratch vs durable maintain expectations  
4. **Light conformance** — orientation / artifact / topology labels  

It does **not** standardize retrieval engines, agent orchestration, embeddings, IDE hooks, task trackers, or OS/Git access control.

In v0.1, layout “intents” are **fixed vocabulary keys** (`code`, `tests`, `artifacts`, `scratch`, …), not natural-language task routing.

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
- Not a security boundary: `write` / `access` do **not** authenticate or sandbox agents  
- Not a natural-language intent classifier

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
| **Layout** | Layout-category key → directory root(s) relative to resolved zone root |
| **Layout key (v0.1 “intent”)** | Vocabulary token: `code`, `tests`, `artifacts`, `scratch`, … — not free-text tasks |
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
- **write:** Mutating allow-list (`domain` \| `architect`). Empty = no declared write grant. **Not authentication.**  
- **access:** Optional. Prefer `access: read-only` with `write: []` for consume-only zones.  

#### Active mutating mode (runtime input)

- The **active mode** is supplied by the human or host adapter (e.g. user said “implement in this service” → `domain`).  
- It is **not** an authenticated identity and MUST NOT be inferred solely from file presence.  
- **If no active mutating mode is explicitly provided, the default is no write grant** (orientation/read only).  
- Adapters MAY map UI roles to `domain` / `architect`; Core does not define SSO or permissions.  
- AAP **cannot** stop writes outside layout roots; Git permissions, CODEOWNERS, and sandboxes do.

Machine-local overlays SHOULD use `map.local.yaml` / `docs/map.local.yaml` / `.aap/map.local.yaml` (gitignored). Absolute paths MUST NOT be required for CI.

JSON Schema: [`schemas/map.schema.json`](./schemas/map.schema.json).

### 3.3 Layout keys (directory categories)

Layout MUST NOT inventory individual source files.  
This is **layout-based discovery**, not natural-language intent routing.

**Core keys:** `code`, `tests`, `artifacts`, `scratch`  
**Standard optional:** `scripts`, `infra`, `proposals`, `architecture`  
**Extension:** any other key → path or path list  

Paths: relative to resolved zone root; `/` separators; MUST NOT contain `..`; SHOULD NOT be absolute.

**Merge:** zone `layout` overrides `defaults.layout` key-wise (replace).  
**Write target:** first listed root for a key unless specified.  
**Missing key:** MUST NOT invent a parallel conventional root for a key that already exists; ask or fail closed for that write.

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

**`updated` semantics:** date when artifact **content or envelope was last materially changed**. It is **not** a verification timestamp (a future `last_verified` MAY be added; not required in 0.1). Typo-only fixes MAY leave `updated` unchanged; meaning changes SHOULD bump it. Timezone: calendar date as agreed by the team (UTC date RECOMMENDED for distributed teams).

Recommended: `title`, `summary`, `stability`, `maintain`, `owner`, `refs`, `supersedes` / `superseded_by`.

JSON Schema: [`schemas/artifact-envelope.schema.json`](./schemas/artifact-envelope.schema.json).

**Schema posture (permissive Core):** the Core envelope schema validates **shape** of common fields. It does **not** require `type` to be only the five Core values (extensions allowed). It does **not** fully enforce dotted extension syntax. Profiles or repo linters MAY tighten `type` patterns. Cross-file rules (zone exists, unique ids, path under zone root) are **out of Core schema scope** in 0.1.

### 4.2 Core types

| type | Role |
|------|------|
| `capability` | What a zone exposes |
| `decision` | Why this way |
| `contract` | Cross-zone guarantee (prefer global/shell zone when multi-zone) |
| `gotcha` | Costly rediscovery hazard |
| `impact` | Change blast sketch (often short-lived) |

Extension types SHOULD use a dot (`diagram.sequence`, …). Readers MUST parse Core fields even if `type` is unknown.

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
3. Choose zone + layout key from task (human/agent judgment — not NL classifier in Core)
4. Targeted retrieve under layout roots (grep/LSP/index/…)
5. Open specific artifacts only if needed
6. Open SPEC only when editing/validating convention structure
```

### 5.2 Write

```text
1. Orient via map
2. Determine active mutating mode from explicit user/runtime input (default: none)
3. If mode absent or not in zone.write → do not claim write grant; ask or stay read-only
4. Resolve layout key path
5. Do not invent parallel roots
6. Write envelope + body
7. Cross-zone conflict → BLOCKED with reason (not silent foreign edits)
```

Remember: even a declared grant is a **hint**; hosts enforce real filesystem policy.

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
