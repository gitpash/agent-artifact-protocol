# Contributing to AAP

Thank you for helping keep the Core **small**.

## Version strings

| Place | Form |
|-------|------|
| Documents / CHANGELOG | `0.2.1-prototype` (no `v`) |
| Git tags | `v0.2.1-prototype` (with `v`) |
| Prior Core intro label | `0.2.0-draft` / historical commits — Map v2 rules unchanged in `0.2.1-prototype` |

## What belongs in Core vs elsewhere

| In Core (expensive) | Profile / cookbook / later |
|---------------------|----------------------------|
| Map v2 discovery + layout intents | Natural-language task routing |
| `resourceRef` path/access shape | Repository-specific legacy path rules |
| Historical envelope draft | New mandatory artifact placement metadata without evidence |
| Progressive disclosure rules | Runtime adapters (editor packs, CI bots, desktop harnesses) |
| `write` / `access` as **hints** | Real ACL / auth systems |
| Deployment-defined mode labels | Universal role vocabulary |
| Schema shape validation | Cross-file linters beyond seed |
| | **Stream packs**, **accept / done bars**, **orientation cards**, **local dispatcher** templates |
| | Hub-umbrella teaching |
| | Schema-pinning ops notes, brownfield init prose |

### Profile PRs are not Core MUST

Pull requests that add or edit:

- stream pack samples / templates  
- accept-default / done-bar checklists  
- thin orientation cards  

…are **profile / cookbook** changes. Reviewers **MUST NOT** treat them as new Orientation requirements or as justification to grow mandatory L0. Optional profiles stay optional even when examples look polished.

Prefer: cookbook page starts with *“Optional profile — not required for Orientation conformance.”*

## Proposing a Core change

Open an issue or PR that includes:

1. **Problem** (who hurts today)  
2. **Why not cookbook/profile only**  
3. **L0 impact** — does the mandatory first-read surface grow?  
4. **Maintenance cost**  
5. **Migration / rollback**  
6. **Schema or example diff**  
7. At least one **invalid** case if adding a restriction  

If the answer to (2) is “cookbook is enough,” ship a profile PR instead.

## L0 budget

If your change requires agents to read more than the local map at session start, it is probably wrong for Core.

**Reminder:** profile bootstrap (orientation card + one stream pack + done bar) is **consumer/runtime policy**. Document it in the cookbook; do **not** redefine Core L0 as “map + packs” in SPEC MUST language without an explicit, evidence-gated Core revision.

## Validation

```bash
pip install pyyaml jsonschema
python scripts/validate.py
```

CI runs the same script on PRs.

## Write-home and security

PRs must not describe `write` or `access` as authentication or sandboxing. Host Git permissions and runtime policy enforce real boundaries. A layout string normalizes to writable; `access: read-only` removes that layout reference from write-home selection. `write` remains deployment-defined node metadata, and adapters may map local roles to it.
