# Example: meta-repo shell (fictional)

Synthetic multi-repo **shell** for hub orientation. All names
(`acme-platform`, `orders-api`, `admin-web`, `billing-worker`,
`external-gateway`) are **fictional** — not a real product.

| Path | Role |
|------|------|
| `map.yaml` | Hub: hops, `business`/`reports` layout, read-only external |
| `orders-api/map.yaml` | Child with `self.parent` → hub |
| `admin-web/map.yaml` | Child with `self.parent` → hub |
| `billing-worker/map.yaml` | Child with `self.parent` → hub |

Parent hops + consume-only external. See [`../hub-umbrella/`](../hub-umbrella/)
and [`../../cookbook/hub-umbrella.md`](../../cookbook/hub-umbrella.md).
