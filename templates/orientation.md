# Orientation (thin card — optional)

> Copy into a local path such as `.aap/local/orientation.md` (often gitignored).  
> **Optional profile** — not required for Orientation conformance. Keep this card short.

**Workspace:** \<one-line what this tree is\>  
**Map (L0):** `.aap/map.yaml` (or your discoverable map path)  
**GPS (optional):** `.aap/map.local.yaml` — overlays only; never write authority  
**Write home:** first non-`read-only` `layout.artifacts` (or stated intent); do not invent parallel roots  
**Indexes / retrieval:** use if present; if empty or stale → degrade and say so  

## Do

- Read the map before wide search.  
- Open **exactly one** stream pack when packs exist.  
- Cite paths, git, or command output for factual claims.  
- Run the accept / done bar before claiming ship or PR-ready.

## Don’t

- Preload SPEC, full skill catalogs, or every stream pack.  
- Recursively open every child `map.path` “just in case.”  
- Treat `write` / `access` as a security sandbox.  
- Claim PR-ready on red required checks or evidence-free blockers.

## Entry by task (edit ids to match your packs)

| Need | Stream id (example) |
|------|---------------------|
| Where is / blast radius | `research` |
| Ship / release scan | `release-check` |
| Minimal fix | `hotfix` |

## See also (upstream cookbook)

- Stream packs, local bootstrap, done bar, hub umbrella — optional profiles only.
