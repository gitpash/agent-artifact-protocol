# Example: tiny shell map

Minimal **one-hop** shell: this workspace map lists a direct `nodes` entry and optional `map.path` for the child. It does **not** copy the child’s layout.

| File | Role |
|------|------|
| `map.yaml` | Shell with a single `orders-api` hop |

## Scale up

For multi-node shells (path ≠ repo name, several children, external consume-only hops), use the teaching pack:

- Cookbook: [`../../cookbook/hub-umbrella.md`](../../cookbook/hub-umbrella.md)  
- Example tree: [`../hub-umbrella/`](../hub-umbrella/)

## Disclosure reminders

- Do **not** recursively preload every `map.path` at session start — see [`../invalid/anti-recursive-preload.md`](../invalid/anti-recursive-preload.md).  
- Core Orientation = this map (or your discoverable map). Stream packs remain optional profiles.
