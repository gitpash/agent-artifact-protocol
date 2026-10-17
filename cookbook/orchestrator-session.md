# Cookbook: orchestrator session (optional profile)

> **Profile status:** tried once

> **Optional profile — not required for Orientation conformance.**  
> Harness-agnostic **shape** for manager / worker / handoff. Multi-agent “teams” features are **one** possible implementation — not required by AAP.

## Problem

Long-running or multi-role work needs:

- a plan someone can re-open tomorrow  
- bounded worker tasks  
- an end-of-day or end-of-stream **handoff**  

Teams then either paste huge chat logs into the next session or bind the protocol to one vendor’s teammate API.

## Shape (runtime-agnostic)

| Role | Responsibility |
|------|----------------|
| **Manager (orchestrator)** | Owns the plan, spawns or sequences work, integrates results, writes handoff |
| **Worker** | Executes a bounded slice with map + **one** stream pack; returns evidence |
| **Handoff** | Durable note: done / in flight / blockers / next map locus — under layout write-home or scratch |

```text
plan → assign bounded work → workers orient (map) → optional pack → evidence →
  manager integrates → accept bar → handoff file
```

Nothing here requires a particular desktop app, teammate RPC, or shared task-board product.

## Implementation menu (examples, not mandates)

| Approach | Notes |
|----------|--------|
| Single human + one agent session | Manager is the human; handoff is a Markdown file |
| Sequential agent sessions | Same shape; new session reads handoff first |
| Multi-agent / “agent teams” runtime | **One** way to spawn workers; still optional |
| External ticket system | Tickets carry handoff; map still orients code |

**AAP does not require multi-agent runtimes.** If your harness has teams/teammates, use them as an adapter — do not encode spawn APIs into Core maps.

## Handoff sketch (informative)

```markdown
# Handoff — YYYY-MM-DD

## Done
- …

## In flight
- … (owner, path locus)

## Blockers
- … (evidence links)

## Next
- Open map → node X → layout Y
- Suggested stream: research | release-check | …
```

Prefer layout `artifacts` or `scratch` paths from the map. Do not invent a parallel durable root.

## Session bootstrap (when using this profile)

1. Read local map (L0).  
2. Read handoff if continuing prior work.  
3. Open **exactly one** stream pack for this session’s class of work.  
4. Before “done,” walk the [done bar](./done-bar.md).  

Profile bootstrap is **consumer policy** — it does not redefine Core L0.

## Anti-patterns

- “AAP compliance = must use agent teams”  
- Manager preloads every worker prompt and child map  
- Handoff that is only chat memory with no file  
- Encoding vendor spawn tool names into shared cookbook examples as required vocabulary  
- Growing Map v2 schema with orchestrator fields without multi-consumer evidence  

## See also

- [`glass-box-factory.md`](./glass-box-factory.md) — visible sessions; no Core CLI  
- [`stream-packs.md`](./stream-packs.md)  
- [`done-bar.md`](./done-bar.md)  
- [`local-bootstrap.md`](./local-bootstrap.md)  
- [`what-not-to-copy.md`](./what-not-to-copy.md)  
