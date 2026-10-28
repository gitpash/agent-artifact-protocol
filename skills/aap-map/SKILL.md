---
name: aap-map
description: Add a minimal AAP (Agent Artifact Protocol) navigation map, .aap/map.yaml, to the current repository. Use when the user asks to add or fix an AAP map, or says "aap-map". Reads the repo, writes a small map, and tells the user what it guessed. Does not ask questions it can answer by looking.
---

# aap-map

Writes a small `.aap/map.yaml` for the repository you are in. AAP in one line: a checked-in map that says where things live and which neighboring repositories exist, so an agent can open the right place without loading everything.

Default behavior: look, decide, write, report. Do not interview the user. The user can say "yes" to the result, or tell you what to change.

## Ground rules

- If a map already exists (`.aap/map.yaml`, `map.yaml` or `docs/map.yaml`), do not overwrite it and do not create a second one. Show what you would change and ask once.
- Work in the project root you were pointed at. In a monorepo subfolder, use the closest sensible root and say which you chose.
- Do not touch other repositories, move folders, or rename docs. The only file you create is the map (plus its `.aap/` folder).
- No absolute or machine-specific paths in the map.
- Keep it small. A map that fits on one screen is the goal.

## Steps

1. **Look.** README and any `AGENTS.md` / `CLAUDE.md` if present (file names in any case), the top-level folders, the build manifest (`package.json`, `pyproject.toml`, `go.mod`, `Cargo.toml`, ...) for the name and source layout, test folders or config, a folder of durable notes if one exists (`docs/adr/`, `adr/`, `rfcs/`), `.gitmodules` and workspace definitions if present. Stop as soon as you can fill the map. Check that each path exists with `ls`.
2. **Write `.aap/map.yaml`** in this shape. Block style, descriptions in quotes (an unquoted comma or colon breaks flow-style YAML):

   ```yaml
   version: 2
   workspace:
     id: my-app
     description: "What this repository is, one line."
   self:
     id: my-app
     kind: repository
     path: .
   layout:
     code: src/
     tests: tests/
   nodes: []
   ```

3. **Report** in a few lines (see the end), then stop.

## Filling it in

**ids** (`workspace.id`, `self.id`, node ids): lowercase letters, digits and hyphens, starting with a letter. Slugify the repo name (`My_App` becomes `my-app`, `3d-viewer` becomes `app-3d-viewer`); never reorder words. `workspace.id` and `self.id` may be equal.

**layout** maps intent to a path in this repo. Add a key only when the folder exists:
- `code` and `tests` usually. Several code roots: a list. Many packages (more than about five): use the parent folder (`packages/`). Paths are literal, no globs.
- Tests next to the code and no tests folder: leave `tests` out.
- `artifacts` only for a folder of working notes (ADRs, decisions, specs) that already exists. A docs website is not `artifacts`. Do not create a new folder for it.
- Other keys (`docs`, `scripts`, `infra`, ...) are allowed, only if the folder really is that (a `scripts/` folder full of workspace packages is not scripts) and an agent would plausibly be sent there. Fewer is better.
- Two folders compete (old docs and a newer site, say): pick the one the repo says is current, and add a REVIEW comment.
- A vendored folder inside the code root: keep the root and mention the folder in the report.
- Paths: relative, no leading `/`, no `..`.

**access.** Paths are read-write by default; leave `access` out. Use `{ path: ..., access: read-only }` only when the repo itself says the folder is frozen, generated or vendored (README, CODEOWNERS, `.gitattributes`, a header in the folder). A folder name alone is not evidence.

**nodes** are direct hops to other repositories someone would plausibly open during a normal change here. `nodes: []` is a normal answer for a standalone repository. Admit a node only if you can name a reason and point at evidence in this repo:
- it is called at runtime (client or endpoint config),
- it owns a contract this repo consumes (schema, API definition, generated client),
- it is the named source of truth for design or requirements,
- it is an intentionally shared convention with a maintained sync.

Not nodes: third-party libraries, README mentions, transitive dependencies, a one-time scaffold source, another branch or fork of this repo, packages inside a monorepo (use `layout.code`).

For a node: `id`, `kind` (`repository`, or `external` if you only read about it), a one-line `description` of what is consulted there and when. `locator.repo` or `locator.url` only if copied from `.gitmodules`, a git remote, the README or config; never guess an organization or host. `map.path: .aap/map.yaml` only if you saw that file there. `access: read-only` for consume-only hops. Machine paths for neighbors go in a gitignored `map.local.yaml`, not here.

Leave out `relations`, `overlays`, `profiles`, `mirror`, `write` unless asked.

## Flag guesses

Anything you are not sure about gets a `# REVIEW: <reason>` comment on that line, and is listed in the report. Typical cases: a node, a `read-only`, a slugified id, two competing folders, a path you could not confirm. Edit the file as text; do not load it into a YAML library and write it back, which deletes comments.

## Checking it (optional)

You do not need to run a validator, and nothing has to be installed. Before you report, read the file once against this list:

- `version: 2`; `workspace`, `self`, `nodes` present; `nodes` is a list.
- ids match `^[a-z][a-z0-9-]*$`.
- Only known fields: `workspace` {id, description}; `self` {id, kind, path, description, parent}; nodes {id, kind, description, path, locator, map, mirror, access, write}; `access` is `read-only` or `read-write`.
- Layout paths are relative, with no `..`.

If the user wants machine checking later (for example in CI), the AAP repository has the JSON Schema (`schemas/map.schema.json`), a reference script (`scripts/validate.py`) and a guide (`cookbook/ci-validation.md`). Mention that in one line, only if they ask about validation.

## Report

Plain and short:

```text
Added .aap/map.yaml
- layout: <keys and paths>
- nodes: <none, or ids with reason>
- guessed (marked REVIEW): <list, or none>
- not checked by a tool: read against the field list by hand
Say "ok", or tell me what to change.
```

Do not claim the map is "validated". Do not offer profiles, stream packs or other extras unless asked.

## What the map must not become

A list of every folder, a dependency graph, a place for procedures or essays (those go in `AGENTS.md` or README), or a permission system (`access` is a note between humans and agents, not enforcement).
