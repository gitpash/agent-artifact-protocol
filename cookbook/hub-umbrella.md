# Cookbook: hub umbrella (multi-repo shell)

> **Teaching pattern on Core maps.** Core already allows shell maps (`nodes` + child `map.path`). This page scales the idea. Not a new Core requirement.

## Problem

Meta-repos and monorepo shells fail orientation when:

- directory name ≠ remote repository name  
- agents invent transitive dependency graphs from the shell map  
- every child constitution or linked map is preloaded  

## Pattern

1. **Shell map** lists **direct** hops only (`nodes`), not each child’s dependencies.  
2. Each node has `path` (workspace-relative), optional `locator.repo`, optional `map.path` for the child’s own map.  
3. Child maps MAY set `self.parent` as a **bounded navigation pointer** (not ownership/ACL).  
4. Machine checkouts outside the shell use gitignored `overlays.nodes` / `map.local.yaml` GPS — overlays never grant write authority.  
5. `map.path` MAY be aspirational (“adopt on touch”) — do not imply the child map already exists on the default branch unless true.

## Minimal shell sketch

```yaml
version: 2
workspace: { id: product-shell }
self: { id: product-shell, kind: repository, path: . }
layout:
  artifacts: docs/artifacts/
  scratch: docs/scratch/
nodes:
  - id: orders-api
    kind: repository
    path: services/orders-api   # may differ from repo name
    locator: { repo: example/orders-api }
    map: { path: .aap/map.yaml }
  - id: scorecard
    kind: repository
    path: vendor-scorecard      # path ≠ repo id
    locator: { repo: example/pepsi-scorecard }
    map: { path: .aap/map.yaml }
  - id: edge-gateway
    kind: repository
    path: apps/edge-gateway
    locator: { repo: example/edge-gateway }
    map: { path: .aap/map.yaml }
  - id: partner-billing
    kind: external
    description: Consume-only billing docs hop.
    locator: { repo: example/partner-billing }
    access: read-only
```

## Child sketch

```yaml
version: 2
workspace: { id: orders-api }
self:
  id: orders-api
  kind: repository
  path: .
  parent:
    id: product-shell
    locator: { repo: example/product-shell }
    map: { path: .aap/map.yaml }
layout:
  code: src/
  artifacts: docs/artifacts/
nodes: []   # or peers only — not the whole company
```

## Honesty rules

- Nodes are **navigation**, not a complete service mesh.  
- Frontend maps list gateway + backends the UI actually calls — not backend-to-backend chains (those live on backend maps).  
- External consume-only hops: `kind: external` (or equivalent) + `access: read-only`.  
- Prefer generating shell nodes from an inventory source (e.g. `.gitmodules`) in the **consumer** so map and inventory cannot drift — that generator is local tooling, not Core.  
- Linked child maps **MUST NOT** be recursively preloaded; open a hop only when the task needs it.

## See also

- [`examples/shell/`](../examples/shell/) — tiny one-hop shell (README points here for scale-up)  
- [`examples/hub-umbrella/`](../examples/hub-umbrella/) — synthetic multi-node shell + child  
- [`examples/invalid/anti-recursive-preload.md`](../examples/invalid/anti-recursive-preload.md) — negative teaching  
- [`stream-packs.md`](./stream-packs.md) — optional session procedure after orientation  
- [`local-bootstrap.md`](./local-bootstrap.md) — GPS and thin local files  
 
