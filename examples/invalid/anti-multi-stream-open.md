# Anti-pattern: multi-stream open

**Status:** teaching note — not a Map v2 fixture. Does not participate in schema validation.

## Bad

```text
Session start:
  1. read map
  2. read research.yaml
  3. read release-check.yaml
  4. read hotfix.yaml
  5. read every other pack "for context"
```

Or a dispatcher that says: *always load the full streams directory.*

## Why it fails AAP intent

- Progressive disclosure collapses into a mini-constitution dump.  
- Conflicting `process` / `forbid` rules from different task classes.  
- Token budget burned before any locus work.  
- Looks like “thoroughness”; behaves like preload.

## Good

- Choose **exactly one** stream pack for the session (human `stream: <id>` or task keywords).  
- Optionally share one accept / done bar across packs.  
- Switch pack only when the **task class** changes — start a clean procedure, do not merge packs.

## See

- [`../../cookbook/stream-packs.md`](../../cookbook/stream-packs.md)  
- [`../stream-packs/`](../stream-packs/)  
- [`../../cookbook/done-bar.md`](../../cookbook/done-bar.md)  
