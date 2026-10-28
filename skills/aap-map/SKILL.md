---
name: aap-map
description: Draft, validate and review a minimal AAP (Agent Artifact Protocol) navigation map, .aap/map.yaml, for any repository. Use when the user asks to add an AAP map, create or fix .aap/map.yaml, check a map against the schema, or says "aap-map". Produces a schema-valid candidate and marks uncertain parts for human review. Not for general documentation work.
---

# aap-map

Creates a small `.aap/map.yaml` (AAP Map v2) for the repository you are in, checks it against the bundled JSON Schema, and leaves anything it could not establish from evidence marked for a human.

AAP in one line: a checked-in map that says where things live and which neighboring repositories exist, so an agent can open the right place without loading everything. It is not a dependency graph, a search index or a permission system.

Schema validity proves shape only. It does not prove that the paths are right or the nodes are useful. That is why this skill ends with a review step, not with "done".

## Files in this skill

- `schema/map.schema.json`: byte-identical copy of `schemas/map.schema.json` from the AAP repo at tag `v0.2.1-prototype`. If the two ever differ, the repo copy wins.
- `scripts/validate_map.py`: optional validator, standard-library Python 3 only, no packages to install.

Resolve these paths relative to this SKILL.md, not to the project you are mapping. Use the absolute path when you run the validator.

## Rules before you write anything

1. If `.aap/map.yaml` (or `map.yaml`, `docs/map.yaml`) already exists, do not overwrite it and do not create a second map next to it. Validate it, report, and propose a diff. Write only after the user says yes.
2. Work in the project root you were pointed at (the git top-level, if it is a git repo). If it is a subfolder of a monorepo, ask which folder is the workspace.
3. Do not edit other repositories. For a neighbor that should list this repo, give a YAML snippet and stop.
4. Do not move, rename or "tidy" any existing docs or folders to make the map look better.
5. Never put absolute or machine-specific paths into the committed map. Those belong in a gitignored `map.local.yaml`.

## Procedure

### 1. Discover (short, evidence only)

Read, in this order, and stop as soon as you can fill the map:

- README and any agent guidance file (`AGENTS.md`, `CLAUDE.md`, CONTRIBUTING), if present. Match file names case-insensitively.
- Top-level directory listing (one level, then one more level only for `src`-like roots).
- Build manifest (`package.json`, `pyproject.toml`, `go.mod`, `Cargo.toml`, `pom.xml`, `build.gradle*`, etc.) for the project name and the source layout.
- Test config or test directories.
- Where durable notes live, if anywhere: `docs/`, `doc/`, `adr/`, `docs/adr/`, `rfcs/`.
- `.gitmodules`, and workspace definitions (`pnpm-workspace.yaml`, `workspaces` in `package.json`, `[tool.uv.workspace]`, `go.work`, Cargo `[workspace]`), if present.
- Endpoints, client config or generated clients that point at other repositories, when the README mentions them.

Record what you saw as evidence for each key you add. If you cannot point at evidence, do not add the key.

### 2. Draft the map

Shape (Map v2). Use block style and quote every description (a bare comma, colon or `#` inside a flow-style value splits it and the validator then reports a confusing "additional properties" error):

```yaml
version: 2
workspace:
  id: <slug>
  description: "<one line>"
self:
  id: <slug>
  kind: repository
  path: .
layout:
  code: <path>
  tests: <path>
nodes: []
```

Rules for each part:

- **ids** (`workspace.id`, `self.id`, node ids): lowercase letters, digits and hyphens, must start with a letter. Slugify the repository name: lowercase, replace `_`, `.` and spaces with `-`, and add a short letter prefix only if it starts with a digit (`My_App` becomes `my-app`, `3d-viewer` becomes `app-3d-viewer`). Never reorder words. Mention every change in the report. `workspace.id` and `self.id` may be the same.
- **layout**: include only keys with evidence. `code` and `tests` usually, after confirming with `ls` that the folders exist; `artifacts` only for a folder of durable working notes (ADRs, decisions, specs), not for published user documentation such as a docs website, and only if it already exists or the user wants one (then list the path, say in the report that you did not create it, and expect a validator WARN); `scratch` only if the project already has one. A monorepo with a few code roots uses a list: `code: [packages/a/src/, packages/b/src/]`. With many packages (roughly more than five) use the parent folder (`packages/`) and add a REVIEW comment; do not use globs, the schema treats paths literally. If tests sit next to the code and there is no tests folder, omit `tests`; do not pick the nearest folder that merely looks like tests. If a vendored or generated subfolder sits inside a code root, keep the root and add a REVIEW comment; splitting it needs a separate `read-only` entry and is the human's call. Extension keys such as `scripts` or `infra` are optional; add one only if the folder is something an agent would plausibly be sent to, and prefer fewer keys. Omit a key rather than point it at a path that does not exist.
- **access**: default is `read-write`, so leave it out. Add `{ path, access: read-only }` only when the repo says so: a README or contributing note, CODEOWNERS, a `.gitattributes` generated/vendored entry, or a header comment in the folder. A folder name alone is not evidence. If you are guessing, do not mark it; put a REVIEW comment instead. Never invent other fields on paths.
- **description**: one line each for the workspace and for every node. Descriptions are for humans.
- **nodes**: see admission below. An empty `nodes: []` is a normal, valid answer for a standalone repository.
- Skip `relations`, `overlays`, `profiles`, `mirror`, `write` unless the user asks for them. They are optional and make the L0 file bigger.

### 3. Node admission

A node is a direct navigation hop: another repository or product someone is likely to open during a normal change here. Admit a candidate only if you can state one reason and point at local evidence:

| Reason | Evidence in this repo |
|---|---|
| calls it at runtime | client, endpoint or env/config naming the other service |
| owns a contract this repo consumes | schema, API definition, generated client, shared types sourced from it |
| current reference | design source, requirements or spec repo that the README names as the source of truth |
| intentionally shared convention | maintained import or sync workflow, not a one-time copy |

Do not admit something because it is mentioned in a README, is a transitive dependency, is a package manager dependency (third-party libraries are not nodes), was a one-time scaffold source, or is only conceptually related. Put such context in the README instead.

For a node you do admit:

- `kind`: `repository` for another repo you could check out, `external` for something you only read about. `kind` is free text; use these two unless the project has its own word.
- `locator.repo` or `locator.url` only with a value copied verbatim from `.gitmodules`, a git remote, the README or client config. If the repo does not state it, omit `locator` and add a REVIEW comment. Never guess an organization or host. A different branch or fork of this same repository is not a node. `path` only if it is checked out inside this tree (submodule, vendored folder).
- `map.path: .aap/map.yaml` only if you saw that file in that repository. Otherwise omit `map`.
- For `external` or consume-only hops add `access: read-only`.
- `description`: what is consulted there and when.

Workspace roots made of several packages in one repository: do not create one node per package by default. Use `layout.code` as a list. Add nodes for packages only if the user wants per-package maps.

### 4. Mark uncertainty

You cannot ask the schema about uncertainty, and the schema forbids unknown fields, so use YAML comments. Put `# REVIEW:` directly above or beside every line you are not sure about, with the reason:

```yaml
layout:
  code: src/
  # REVIEW: tests live in both tests/ and src/**/__tests__; only tests/ listed
  tests: tests/
nodes:
  # REVIEW: only a README mention, no client config found. Remove if not a normal-change hop.
  - id: billing-service
    kind: external
    access: read-only
```

Edit the file textually. Do not load it into a YAML library and dump it back, which deletes comments. Keep REVIEW comments for uncertainty only; put plain notes in your report. Mark for review at minimum: every node, every `read-only` you chose, any layout path you could not verify exists, any slugified id, any key where two folders competed.

### 5. Validate

Nothing here needs an install. Use the highest level that works on this machine and say which one you used.

**Level 1, always: manual checklist.** Check the file yourself against these rules (they are the whole schema):

- `version: 2`, and `workspace`, `self` and `nodes` all present. `nodes` is a list (`[]` is fine).
- `workspace` has only `id` and `description`. `self` has `id`, `kind` and optionally `path`, `description`, `parent`.
- Every id (`workspace.id`, `self.id`, node ids, `parent.id`) matches `^[a-z][a-z0-9-]*$`.
- Every layout value is a path string, or `{ path, access?, description? }`, or a non-empty list of those. `access` is `read-only` or `read-write` and nothing else.
- Paths are relative: no leading `/`, no `..`, no `~`, no backslashes, no Windows drive letters.
- A node has `id` and `kind`, and only these other fields: `description`, `path`, `locator`, `map`, `mirror`, `access`, `write`. `locator` needs `repo`, `url` or `id`. `map` needs `path` or `url`.
- No unknown fields anywhere, except extra keys under `layout`. Descriptions are quoted strings.
- Every path in the map exists on disk (check with `ls`), or is flagged with a REVIEW comment.

**Level 2, if `python3` is on the machine: bundled script.** It uses only the Python standard library.

```bash
python3 /absolute/path/to/aap-map/scripts/validate_map.py .aap/map.yaml
```

(On Windows use `py -3`.) Output contract:

```text
VALIDATION_SUCCESS
WARN ...            (zero or more; informational)
REVIEW_MARKERS N (lines ...)
# or
VALIDATION_FAILED
- path: /nodes/0/id | message: ...
```

The script reads a deliberately small YAML subset. If it answers "unsupported YAML", rewrite the map in plain block style (indented `key: value` lines, quoted strings) and run it again; that is not a schema error.

**Level 3, optional, for AAP maintainers: full JSON Schema.** The AAP repository's `scripts/validate.py` uses `jsonschema` against `schemas/map.schema.json`. Do not install anything to reach this level unless the user asks. `uv run --with pyyaml --with jsonschema python3 scripts/validate.py` runs it without touching the project's environment.

On failure at level 2, patch the file from the path and message and run again. Stop after 5 rounds and report what is still failing. Do not weaken the schema or edit the bundled copy to make a map pass.

If you could only do level 1, the map is "checked by hand, not by a machine": say that, never call it validated, and give the user the level 2 command to run later.

### 6. Hand over for review

Do not claim the map is done. End with this report, plainly:

```text
## aap-map result
- file: .aap/map.yaml (new | unchanged | proposed diff)
- validation level actually run: 1 manual checklist | 2 bundled script (PASS or FAIL) | 3 full JSON Schema (PASS or FAIL). If 2 or 3 could not run, say why. Only 2 or 3 may be called "validated".
- layout keys: <list> (each with the evidence you used)
- nodes accepted: N (id, reason) / candidates rejected: N (name as seen in the repo, why; list only candidates you actually saw)
- REVIEW markers: N (list the lines)
- ids changed by slugifying: <list or none>
- needs a human decision: <short list>
```

If the user asked for machine-local overlays, put them in a sibling `map.local.yaml` next to the map and add it to `.gitignore` (if the project uses git). Otherwise leave `.gitignore` alone.

## What the map must not become

- A list of every folder. If the tree is self-explanatory, `code` and `tests` are enough.
- A dependency graph. Libraries and transitive services stay out.
- A place for procedures, conventions or essays. Those go in `AGENTS.md`, README or docs.
- A permission system. `access` is a note between humans and agents, not enforcement.
- A speculative structure. If the project has no durable notes folder, say so and leave `artifacts` out unless the user asks to create one.

## Reading an existing map (for reference)

- Write home for a layout key is the first entry whose access is not `read-only`. If there is none, fail closed and ask.
- `overlays` and `map.local.yaml` say where a node is checked out on this machine. They never grant write rights.
- A node `write: [...]` list is a role hint, not a permission.
