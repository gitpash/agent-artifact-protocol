# What not to copy from product incubators

If you saw AAP grow inside a company monorepo first, **do not** treat that tree as the upstream product.

## Leave in the product repo

| Material | Why |
|----------|-----|
| Pilot plans and metrics | Local experiment |
| Adoption guides naming internal systems | Product-specific |
| Partner contracts / mirrors | Confidential or local |
| Runtime adapters (editor packs, desktop skills, MCP wiring) | Swappable; not Core |
| Huge architecture HTML dumps | Derived / unrelated |
| “Read SPEC every session” checklists | Violates L0 |
| Glass-box factory CLI, queue schemas, session cards | Incubator harness tooling |
| Day-manager / multi-agent orchestrator prompts and handoff paths | Runtime orchestration profile |
| Standing chat/TPM status macros | Team process, not orientation |
| Full local dispatcher product-policy dumps | Runtime file; keep thin if used at all |
| Knowledge-graph database files and rebuild scripts | Derived indexes; retrieval adapters |
| DB connection allow-lists and env enable markers | Environment adapters |
| Pilot metrics and tool-effectiveness logs | Local experiment |
| “Read SPEC + all stream packs every session” checklists | Violates progressive disclosure |
| Partner repo names and internal schema locks as if universal SoT | Consumer pin policy |

## Copy or re-implement from upstream

| Material | Why |
|----------|-----|
| Minimal map template | L0 |
| Envelope field names + core types | Interop |
| JSON Schemas (optional pin) | Validation |
| Progressive disclosure rules | Protocol law |
| Generic examples | Teaching |
| Hub-umbrella example shape | Teaching multi-node orientation |
| Stream pack **idea** + sample ids | Optional disclosure profile |
| Accept-default **idea** | Optional honesty bar |
| Thin orientation card template | Optional local card |

## Rule

> Upstream = small pinned seed.  
> Consumer = local map + local memory.  
> Incubator docs ≠ distribution unit.  
> Optional profiles stay optional — they are not a second Core.  
