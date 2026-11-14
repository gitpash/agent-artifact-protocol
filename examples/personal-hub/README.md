# Example: personal hub (synthetic)

The "home repo" shape: one repository you always start the agent in. Generic names only.

| File | Role |
|------|------|
| `map.yaml` | Topology: the nodes, plus pointers to the state file and reuse index |
| `map.local.yaml.example` | Template for the gitignored `.aap/map.local.yaml` (machine paths) |
| `projects.yaml` | Status per node: active or parked, next step, resume condition |
| `reuse.md` | Capability index: what to borrow, from which project |

Recipes: [`home-repo`](../../cookbook/home-repo.md), [`node-state`](../../cookbook/node-state.md), [`capability-index`](../../cookbook/capability-index.md), [`workspace-tools`](../../cookbook/workspace-tools.md).
