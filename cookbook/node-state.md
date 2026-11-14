# Cookbook: node state (active / parked)

An optional profile for a hub: which projects are live, what the next step is, and when a parked one should wake up. It changes nothing in Core.

## Shape

The map points at a state file with a layout key, and lists the profile as a hint:

```yaml
layout:
  state: projects.yaml
profiles:
  enabled: [node-state]
```

```yaml
# projects.yaml: one row per node id
projects:
  - id: web-app
    status: active          # active | parked
    next: Ship the login rework behind a flag.
    resume_when: ""         # for parked rows: the condition that wakes it
```

Topology stays in the map, status in the state file, joined by `id`. Nothing is copied between them. A hub that already keeps a registry like this only needs the `layout.state` line.

## Why not a `status` field on nodes

Node objects in the Core schema are closed (`additionalProperties: false`), so `status` on a node would fail validation until the schema changes. The profile avoids that: no schema change, old validators keep working. The cost is a second file and a join by `id`. If the profile proves itself, adding optional `status`, `next` and `resume_when` to the node schema is a candidate for a later Map version; it is not proposed here.

## Check

```bash
python scripts/aap_workspace.py state
```

Prints one line per node and flags nodes without a row, rows without a node, and a status other than `active` or `parked`. Keep the active list short; a cap (say three) is a rule for your `AGENTS.md`, not for the map.

Example: [`examples/personal-hub/`](../examples/personal-hub/).
