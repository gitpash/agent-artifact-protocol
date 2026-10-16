# Cookbook: glass-box factory (optional pattern)

> **Optional pattern — not required for Orientation conformance.**  
> Documents a *shape* for visible multi-session work. **No CLI or harness ships in this Core repo.**

## Problem

Incubators often grow a “factory”: queues, conductor scripts, session cards, prompt packs. Useful locally — toxic when mistaken for AAP Core or copied as mandatory infrastructure.

## Pattern (ideas only)

Keep the factory **glass-box** and **file-first**:

| Idea | Meaning |
|------|---------|
| **Dumb file conductor** | Orchestration reads/writes ordinary files (queues, status, prompts). Logic stays boring and inspectable. |
| **Visible sessions** | Each worker/session has an on-disk card humans can open without a special UI. |
| **Prompts on disk** | Prompt text lives in the repo or scratch as files — not only inside a proprietary runtime blob. |
| **No hidden brain** | The conductor does not silently own product judgment; agents and humans do. |

AAP’s job stops at **addresses and disclosure**. A factory is an **incubator/runtime** choice that may *use* maps and packs — it is not a Map v2 feature.

## What this repo deliberately omits

- Conductor CLIs / `*.mjs` runners  
- Queue schemas and lease protocols  
- Session card formats as Core types  
- Mandatory multi-agent boards  

See [`what-not-to-copy.md`](./what-not-to-copy.md).

## How it relates to AAP

```text
map (L0) → optional stream pack → optional done bar
                ↑
     factory may schedule sessions that follow the above
     factory is not itself an AAP level
```

If you adopt a factory:

1. Keep Core maps sparse.  
2. Put factory state under layout `scratch` / local paths — not new mandatory L0 files.  
3. Prefer copying **templates** into the consumer over live-fetching incubator `main`.  
4. Document the factory as **runtime**, never as Orientation law.

## Anti-patterns

- Shipping a conductor binary “because AAP needs it”  
- Preloading every session card and prompt pack at L0  
- Treating queue depth as a protocol conformance metric  
- Renaming product factory docs as `SPEC.md`  

## See also

- [`orchestrator-session.md`](./orchestrator-session.md) — manager/worker shape without harness lock-in  
- [`stream-packs.md`](./stream-packs.md)  
- [`done-bar.md`](./done-bar.md)  
- [`what-not-to-copy.md`](./what-not-to-copy.md)  
