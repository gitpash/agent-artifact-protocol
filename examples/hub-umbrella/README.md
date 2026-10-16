# Example: hub umbrella (synthetic)

Multi-node **shell** map plus one **child** map. Synthetic names only — not a real product tree.

| File | Role |
|------|------|
| `map.yaml` | Shell with several direct hops; path ≠ repo name demo; external read-only hop |
| `child-orders-api/map.yaml` | Child with `self.parent` back to the shell |

See cookbook: [`../../cookbook/hub-umbrella.md`](../../cookbook/hub-umbrella.md).

Compared to [`../shell/`](../shell/), this shows scale (several nodes) without claiming a full dependency graph.
