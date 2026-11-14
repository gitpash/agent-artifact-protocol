# Cookbook: capability index

When a task smells like "I already built this somewhere", the map is the wrong tool: it lists repositories, not things worth borrowing. Keep a one-table index beside it and point to it from the map:

```yaml
layout:
  reuse: reuse.md
```

```markdown
| Capability | Project | Where |
|---|---|---|
| Feature-flag wrapper for gradual rollouts | web-app | src/flags/ |
```

`Project` is a node id; `Where` is a path inside it. Add a line when you notice a second use, not before. It is not a dependency graph and the agent opens it only when a task asks for reuse (L1, not L0).

Example: [`examples/personal-hub/reuse.md`](../examples/personal-hub/reuse.md).
