# Cookbook: brownfield init

## Goal

Add AAP orientation to an existing repo **without** rewriting its docs system.

## Steps

1. **Decide compliance**
   - Orientation only (map) — start here  
   - Artifacts later (envelopes on touch)  

2. **Pin upstream (optional but recommended)**  
   Record the immutable v2 tag or commit in a one-line note, e.g. `.aap/VERSION`. Do not validate against a floating branch tip. Details: [`schema-pinning.md`](./schema-pinning.md).

   ```text
   v0.2.1-prototype
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
   When a behavior change needs durable memory, use the first writable `layout.artifacts` resource reference (same no-overwrite rule). In a brownfield corpus, keep legacy roots `read-only`; a material update creates or updates a canonical successor and leaves a compatibility pointer. Do not bulk-migrate.

7. **Optional profiles (only after map-only helps)**  
   Multi-repo shell: [`hub-umbrella.md`](./hub-umbrella.md). Session procedure: [`stream-packs.md`](./stream-packs.md) + [`local-bootstrap.md`](./local-bootstrap.md). Honesty exit: [`done-bar.md`](./done-bar.md). Stubs: [`templates/orientation.md`](../templates/orientation.md), [`templates/stream-pack.yaml`](../templates/stream-pack.yaml). Do not enable every profile because it exists.

## Anti-patterns

- Fetching this GitHub repo on every agent session  
- Dumping `SPEC.md` into the system prompt by default  
- Renaming all existing docs on day one  
- Enabling every profile “because it exists”  
- Treating `write:` as a security sandbox  
- Silent overwrite of existing map/artifacts during bootstrap  

