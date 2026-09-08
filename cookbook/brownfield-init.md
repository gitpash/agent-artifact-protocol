# Cookbook: brownfield init

## Goal

Add AAP orientation to an existing repo **without** rewriting its docs system.

## Steps

1. **Decide compliance**
   - Orientation only (map) — start here  
   - Artifacts later (envelopes on touch)  

2. **Pin upstream (optional but recommended)**  
   Record tag/commit in a one-line note, e.g. `.aap/VERSION`:

   ```text
   v0.1.0-draft
   https://github.com/gitpash/agent-artifact-protocol
   ```

3. **Create map only (no silent overwrite)**

   ```bash
   mkdir -p .aap
   if [ -e .aap/map.yaml ]; then
     echo "Refusing to overwrite existing .aap/map.yaml — confirm per file or abort"
     exit 1
   fi
   cp templates/minimal-map.yaml .aap/map.yaml
   # edit paths
   ```

   **Rule:** if a target file already exists, init MUST **stop** or require **explicit per-file confirmation**. Never overwrite quietly (including future CLI `aap init`).

4. **Dry human review**  
   Confirm no mass moves of `docs/`, `.specify/`, `CLAUDE.md`.

5. **Map-only experiment**  
   Same task twice: without map vs with map. Measure time-to-locus and wrong-home paths.

6. **Artifacts on touch**  
   When a behavior change needs durable memory, copy an artifact template under `layout.artifacts` (same no-overwrite rule).

## Anti-patterns

- Fetching this GitHub repo on every agent session  
- Dumping `SPEC.md` into the system prompt by default  
- Renaming all existing docs on day one  
- Enabling every profile “because it exists”  
- Treating `write:` as a security sandbox  
- Silent overwrite of existing map/artifacts during bootstrap  

