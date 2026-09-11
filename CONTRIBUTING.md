# Contributing to AAP

Thank you for helping keep the Core **small**.

## Version strings

| Place | Form |
|-------|------|
| Documents / CHANGELOG | `0.2.0-draft` (no `v`) |
| Git tags | `v0.2.0-draft` (with `v`) |

## What belongs in Core vs elsewhere

| In Core (expensive) | Profile / cookbook / later |
|---------------------|----------------------------|
| Map v2 discovery + layout intents | Natural-language task routing |
| `resourceRef` path/access shape | Repository-specific legacy path rules |
| Historical envelope draft | New mandatory artifact placement metadata without evidence |
| Progressive disclosure rules | Runtime adapters (Claude, CI bots) |
| `write` / `access` as **hints** | Real ACL / auth systems |
| Deployment-defined mode labels | Universal role vocabulary |
| Schema shape validation | Cross-file linters beyond seed |

## Proposing a Core change

Open an issue or PR that includes:

1. **Problem** (who hurts today)  
2. **Why not cookbook/profile only**  
3. **L0 impact** — does the mandatory first-read surface grow?  
4. **Maintenance cost**  
5. **Migration / rollback**  
6. **Schema or example diff**  
7. At least one **invalid** case if adding a restriction  

## L0 budget

If your change requires agents to read more than the local map at session start, it is probably wrong for Core.

## Validation

```bash
pip install pyyaml jsonschema
python scripts/validate.py
```

CI runs the same script on PRs.

## Write-home and security

PRs must not describe `write` or `access` as authentication or sandboxing. Host Git permissions and runtime policy enforce real boundaries. A layout string normalizes to writable; `access: read-only` removes that layout reference from write-home selection. `write` remains deployment-defined node metadata, and adapters may map local roles to it.
