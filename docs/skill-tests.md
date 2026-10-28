# aap-map skill: test notes

Tested 2026-10-28 on three public projects of different shape, cloned shallow into a scratch directory: chalk (small JS library), requests (Python library, `src/` layout, Sphinx docs) and changesets (pnpm TypeScript monorepo, 21 packages). In each run a fresh agent received only `SKILL.md` and followed it literally. A separate reviewer read the skill looking for assumptions inherited from a private team-side original.

The skill was first written with a bundled schema and validator, then simplified to a single text file (the validator added install friction and little value at install time). Results below are from both versions.

## Results

| Project | Map produced | Notes |
|---|---|---|
| chalk | `code: source/`, `tests: test/`, `nodes: []` | No `read-only` guessed for the vendored folder inside the code root. Passes the JSON Schema. |
| requests | `code: src/requests/`, `tests: tests/`, `nodes: []` | Libraries (urllib3, certifi, ...) correctly not nodes. Passes (first version). |
| changesets | `code: packages/`, `docs` or `site` key, `nodes: []` | Parent folder used instead of 21 paths; tests next to code left out; one REVIEW on competing docs folders. Passes the JSON Schema. |

No run admitted a node. Third-party libraries, README mentions and a branch of the same repo were all rejected, which is the intended result for standalone repositories. Final maps were checked against `schemas/map.schema.json` by the tester after the fact; the skill itself runs no tool.

## What broke or was ambiguous, and what changed

| Finding | Change |
|---|---|
| Flow-style example with a comma in a description split the value and the validator gave a confusing error | Example is block style; descriptions are quoted |
| `src/` versus `src/requests/` for `code` | Pick the folder that holds the code; check with `ls` |
| 21 packages, globs not supported | Use the parent folder |
| Tests next to code, no tests folder | Leave `tests` out |
| Docs website versus durable notes for `artifacts` | `artifacts` is working notes only |
| Vendored folder inside the code root | Keep the root, mention it in the report |
| Two competing docs folders; `scripts/` full of packages | Pick the current one with a REVIEW; key must really be what it says |
| A branch of the same repo in the README | Not a node |
| Case-sensitive file lookup | Case-insensitive |
| Rejected candidates have no id | Not needed in the shorter report |

Reviewer findings applied: do not assume git; do not guess `locator.repo` or the host; `read-only` needs written evidence; slugify ids without reordering; edit the map as text so comments survive; never overwrite or create a second map.

## Known limits

- Tested with Claude subagents on macOS only. Other agents, Windows, and a repo that already has a map were not tried.
- Schema quirk: `pathString` rejects any path containing `..`, even inside a name (`a..b`). Left alone.
- Layout paths are literal, so large monorepos get a coarse parent folder.
