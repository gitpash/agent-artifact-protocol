# AAP Motivation (outline)

**Status:** outline paired with SPEC 0.1.1-draft  

---

## 1. Thesis

Agent failure modes in real repos are often **orientation failures** and **context pollution**, not “not enough Markdown.”

Training priors invent paths (`.claude/spec`, random `docs/`, `.specify/`). Teams invent vocabulary (ADR, RFC, handoff, blast radius). Harnesses answer chaos with longer preload lists.

**AAP** proposes:

> Make repository context **addressable** without requiring repository context to be **loaded**.

- **Map** = layout-category addresses (e.g. `code` → zone → directory root)  
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
| Orientation | map, zones, layout intents, thin write fences |
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

## 7. Closing lines

> Conventions over infrastructure.  
> Discovery over preloading.  
> Progressive disclosure over context dumping.  
> Files over runtime dependencies.

Normative detail: [`SPEC.md`](./SPEC.md). This document explains motivation and positioning; it is not an evidence-backed white paper or normative specification.
