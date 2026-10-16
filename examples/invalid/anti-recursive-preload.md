# Anti-pattern: recursive preload

**Status:** teaching note — not a Map v2 fixture. Does not participate in schema validation.

## Bad

```text
Session start on a shell map:
  1. read shell .aap/map.yaml
  2. for each node.map.path → read that map
  3. for each child → read SPEC, AGENTS, skill catalogs, linked docs
  4. only then begin the task
```

Or: “Orientation = transitive closure of every `map.path` and cookbook page.”

## Why it fails AAP intent

- Core L0 is a **discoverable sparse map**, not a graph crawl.  
- Shell nodes are **navigation hops**, not a mandate to open every child.  
- Child constitutions and catalogs recreate context pollution.  
- Hub-umbrella honesty: open a hop **when the task needs it**.

## Good

```text
1. Read the opened workspace map only (L0).
2. Identify candidate node(s) from the task.
3. Hop: read that child's map when entering that checkout / locus.
4. L1–L3 as needed — never bulk-preload the fan-out.
```

Linked child maps **MUST NOT** be recursively preloaded (see hub-umbrella cookbook and SPEC progressive disclosure).

## See

- [`../../cookbook/hub-umbrella.md`](../../cookbook/hub-umbrella.md)  
- [`../hub-umbrella/`](../hub-umbrella/)  
- [`../shell/`](../shell/) — tiny one-hop shell; scale via hub-umbrella  
- [`../../SPEC.md`](../../SPEC.md) — on demand, not L0  
