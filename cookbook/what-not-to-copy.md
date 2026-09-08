# What not to copy from product incubators

If you saw AAP grow inside a company monorepo first, **do not** treat that tree as the upstream product.

## Leave in the product repo

| Material | Why |
|----------|-----|
| Pilot plans and metrics | Local experiment |
| Adoption guides naming internal systems | Product-specific |
| Partner contracts / mirrors | Confidential or local |
| Runtime adapters (Claude pack, DSH skills) | Swappable; not Core |
| Huge architecture HTML dumps | Derived / unrelated |
| “Read SPEC every session” checklists | Violates L0 |

## Copy or re-implement from upstream

| Material | Why |
|----------|-----|
| Minimal map template | L0 |
| Envelope field names + core types | Interop |
| JSON Schemas (optional pin) | Validation |
| Progressive disclosure rules | Protocol law |
| Generic examples | Teaching |

## Rule

> Upstream = small pinned seed.  
> Consumer = local map + local memory.  
> Incubator docs ≠ distribution unit.
