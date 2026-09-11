# AAP Map v2 Specification

**Name:** Agent Artifact Protocol (AAP)
**Kind:** filesystem convention + JSON Schema
**Version:** 0.2.0-draft
**Status:** experimental

AAP makes repository context addressable without requiring it to be loaded. It is a small, runtime-agnostic navigation convention for repositories and optional durable artifacts. It is not a context engine, agent framework, retrieval protocol, dependency graph, or authorization system.

## Core model

An agent starts with one small `.aap/map.yaml`, then opens only the repository, path, or artifact relevant to the task. Linked maps are explicit hops and **MUST NOT** be recursively preloaded.

```yaml
version: 2
workspace: { id: my-repository }
self: { id: my-repository, kind: repository, path: . }
layout: { code: src/, artifacts: docs/artifacts/ }
nodes: []
```

- `workspace` identifies the opened workspace.
- `self` describes its repository. `self.parent`, when present, is one bounded navigation/container pointer; it does not imply ownership, authorization, dependency, inherited policy, or recursive traversal.
- `nodes` are direct navigational hops to related repositories or products, not a dependency graph.
- `locator` identifies a node independently of a local checkout; `map` points at its map when deeper inspection is needed.
- `layout` maps fixed vocabulary keys (`code`, `tests`, `artifacts`, `scratch`, and extensions) to directory roots in the current workspace.
- `overlays.nodes` is optional machine-local checkout GPS. An overlay resolves navigation only and never grants write authority.

The normative schema is [`schemas/map.schema.json`](./schemas/map.schema.json). Consumers pin a release tag or commit; ordinary sessions read the local map rather than fetching upstream.

## Layout resource references

Every layout value is a `resourceRef`, either a backward-compatible path string or an object:

```yaml
layout:
  artifacts:
    - path: docs/features/
      access: read-write
    - path: legacy/features/
      access: read-only
      description: Historical corpus; keep discoverable for reading.
```

- A string normalizes to `{ path: <string>, access: read-write }`.
- Object `access` defaults to `read-write` when absent.
- Paths are workspace-relative and MUST NOT be absolute or traverse through `..`.
- `access` is `read-only` or `read-write`. It is an agent coordination fence, not OS/Git/IAM authorization.
- A durable write home for a layout key is the first reference whose normalized access is not `read-only`.
- If no writable reference exists, an agent MUST fail closed for a durable write and ask; it MUST NOT invent a parallel root.

`write` on a node is an optional, deployment-defined role hint. It is separate from path access and does not grant filesystem permission. Git permissions, CODEOWNERS, protected branches, and sandboxes enforce real boundaries.

## Brownfield artifacts profile

`brownfield-artifacts` is an optional profile for repositories with a legacy documentation corpus:

1. Declare at most one writable `layout.artifacts` home.
2. Keep old roots addressable as `read-only` rather than removing history or bulk-moving it.
3. On a material update, create or update the canonical successor in the write home and retain a compatibility pointer in the legacy record.
4. Typos or urgent factual corrections may be fixed in place without making the old root a home for new durable documents.

This profile does not reserve path names or mandate a migration date.

## Artifacts

Artifacts remain optional Markdown (or profile-defined) durable units. The existing v0.1 artifact envelope is retained as a separate historical draft; map v2 does not automatically redefine artifact placement metadata. A future artifact-envelope revision may generalize its `zone` field based on usage evidence.

## Progressive disclosure

| Level | Read | When |
|---|---|---|
| L0 | map only | workspace orientation |
| L1 | targeted path/index | after choosing a layout key or node |
| L2 | one artifact | durable memory is needed |
| L3 | code and normal tools | implementation evidence |

Maps should stay sparse. Essays, whole corpora, graph indexes, embeddings, adapters, and workflow machinery do not belong in the mandatory L0 read.

## Versioning and migration

Map v2 is a breaking replacement for the historical v1 `zones` dialect. A v1 map is not auto-converted and MUST be deliberately migrated. Keep a tagged `v0.1.1-draft` checkout for historical validation. Additive v2 changes preserve existing string-layout maps; a breaking rename/removal requires a map version bump, migration note, and changelog entry.

## Validation

```bash
pip install pyyaml jsonschema
python scripts/validate.py
```

The validator checks schemas, v2 examples, resource-reference path safety, and invalid fixtures. Repository-specific policies—such as requiring external nodes to be read-only—belong in that repository's own validator or profile.
