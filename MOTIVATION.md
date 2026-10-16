# AAP Motivation (outline)

**Status:** outline paired with Map v2 SPEC `0.2.1-prototype` (Core lineage `0.2.0-draft`)

---

## 1. Thesis

Agent failure modes in real repos are often **orientation failures** and **context pollution**, not “not enough Markdown.”

Training priors invent paths (`.claude/spec`, random `docs/`, `.specify/`). Teams invent vocabulary (ADR, RFC, handoff, blast radius). Harnesses answer chaos with longer preload lists.

**AAP** proposes:

> Make repository context **addressable** without requiring repository context to be **loaded**.

- **Map** = repository + direct-node + layout-category addresses (e.g. `repository` → `code` → directory root)
- **Artifacts** = optional durable depth  
- **Retrieval** = existing tools (`grep`, LSP, indexes, MCP, …)  
- **Not** a proprietary context engine  

---

## 2. Prior art

| Prior | Take | Leave |
|-------|------|-------|
| Memoryfield | Files as memory; format ≠ infrastructure | Add engineering orientation map |
| MCP | Runtime-agnostic *tool* calls | AAP is runtime-agnostic *addresses + envelopes* |
| ADR | Decision shape | Subset of `type: decision` |
| AGENTS.md / CLAUDE.md | Runtime instructions | Must not replace durable SoT or become mandatory dump |
| Heavy harness / Speckit | Structure impulse | Process engine out of Core |

---

## 3. Progressive disclosure

```text
task → L0 map → L1 zone index? → L2 one artifact? → L3 code/tools
```

Anti-feature: “before starting, read these 14 protocol files.”

---

## 4. Two layers

| Layer | Job |
|-------|-----|
| Orientation | repository map, direct nodes, layout intents, thin write fences |
| Durable artifacts | envelope, types, stability/maintain |

If artifacts swallow orientation, AAP has failed.

---

## 5. Distribution model

Upstream repo = **pinned blueprint** (spec + templates + schemas).  
Consumer = local map + optional vendored schema pin.  
No live `main` dependency during ordinary agent turns.

---

## 6. Minimal evidence experiment

```text
A) agent without map
B) agent with map only
```

Expand schemas/profiles only if B wins on time-to-locus and wrong-home rate.

---

## 6b. Experiment metrics sketch (methodology)

When a pilot runs longer than a single A/B task, prefer **cheap, honest counters** over dashboards. Sketch only — adapt labels locally; do not treat this section as a product analytics spec.

| Signal | What to count | Pass intuition |
|--------|----------------|----------------|
| **Wrong-home** | Durable writes or “fix” edits outside map write-home / wrong node checkout | B (map) lowers rate vs A |
| **Time-to-locus** | Minutes (or turns) until first correct path/node | B faster on repeat task classes |
| **Graph / index degrade honesty** | Sessions where optional retrieval was empty/stale **and** the agent said so vs silent proceed | Degrade named ≥ silent fiction |
| **Accept-bar catches** | Done-bar steps that failed before a bad “PR ready” (red checks, evidence-free blocker, skipped orient) | Catches > 0 in early weeks is success, not shame |
| **Preload pressure** | Times session opened all packs or recursive child maps | Should trend down after stream-pack profile |

**Honesty rules for the sketch:**

- Missing optional index ≠ green “nothing found” without a degrade line.  
- Wrong-home includes inventing parallel `docs/` roots the map never named.  
- Accept-bar catches are **local process metrics**; they are not Core conformance scores.  
- Do not publish internal pilot paths or vendor tool ids as if they were AAP required vocabulary.

Optional profiles that support the loop: done bar, stream packs, hub umbrella (see cookbook). Still: if plain map-only B does not win, **shrink** — do not add metrics theater.

---

## 7. Closing lines

> Conventions over infrastructure.  
> Discovery over preloading.  
> Progressive disclosure over context dumping.  
> Files over runtime dependencies.

Normative detail: [`SPEC.md`](./SPEC.md). This document explains motivation and positioning; it is not an evidence-backed white paper or normative specification.
