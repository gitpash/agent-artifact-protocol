# aap-map test notes

Tested 2026-10-28 on three public projects of different shape, cloned shallow into a scratch directory. In each run a fresh agent received only `SKILL.md` and followed it literally, with the validator and bundled schema. A separate reviewer then read the files looking for assumptions inherited from the private convention the skill grew out of.

| Project | Shape | Result map | Validator | REVIEW markers | Tool calls |
|---|---|---|---|---|---|
| chalk | small JS library, flat | `code: source/`, `tests: test/`, `nodes: []` | pass (after one fix) | 2 | ~12 |
| requests | Python library, `src/` layout, Sphinx docs | `code: src/requests/`, `tests: tests/`, `nodes: []` | pass (after one fix) | 0 | 5 |
| changesets | pnpm TypeScript monorepo, 21 packages | `code: packages/`, `artifacts: docs/`, extension key `site`, `nodes: []` | pass | 4 | ~7 |

No run admitted a node. Third-party libraries and README mentions were rejected, which is the intended outcome for standalone repositories.

## What broke or was ambiguous, and what changed

| Finding | Seen in | Change |
|---|---|---|
| The shape example used flow style. A description containing a comma split the value and the validator reported "additional properties", naming the stray key, not the cause. | chalk, requests | Example is now block style; descriptions must be quoted. |
| `src/` versus `src/requests/` for `code` unspecified | requests | Rule: confirm with `ls`, pick the folder that holds the code. |
| 21 packages: a list of 21 paths is absurd, globs are not supported | changesets | Use the parent folder plus a REVIEW comment; no globs. |
| Tests colocated with code, no tests folder; agent guessed a nearby folder | changesets | Omit `tests` rather than guess. |
| Published docs site versus durable notes for `artifacts` | requests, changesets | `artifacts` means working notes (ADRs, decisions, specs), not a docs website. |
| Vendored folder inside the code root; unclear how to mark read-only | chalk | Keep the root, add a REVIEW comment; splitting is the human's call. |
| Branch of the same repository mentioned in the README | changesets | Not a node. |
| File lookup was case sensitive (`readme.md`) | chalk | Case-insensitive. |
| Informational notes inflated the REVIEW count | chalk | REVIEW comments are for uncertainty only; notes go in the report. |
| Rejected candidates have no id | chalk, changesets | Report them by name as seen in the repo. |
| Validator printed line numbers not in the output contract | chalk, changesets | Contract updated. |
| Extension keys (`site`, `examples`) tempt the agent to list every folder | chalk, changesets | Optional, fewer is better. |

Reviewer findings applied: do not assume a git repo; do not guess `locator.repo` or the host; `read-only` needs written evidence, a folder name is not enough; slugify ids without reordering words; edit the map textually so comments survive; validator warns on absolute, `~`, backslash and `..` paths in `self.path`, `node.path` and `map.path` (the schema only checks layout paths); validator sort no longer crashes on mixed index and key error paths; REVIEW marker count matches only YAML comments; `python3` / `py -3` and absolute script path; honest "validation NOT RUN" fallback; do not create a second map next to an existing one.

## Known limits

- Tested with Claude subagents only. Other agents were not tried.
- The schema's `pathString` pattern rejects any path containing `..` even as part of a name (`a..b`). That is the schema's behavior and was left alone.
- `layout` paths are literal. There are no globs, so large monorepos get a coarse parent folder.
- The bundled schema keeps its original `$id`. A CI check in `scripts/validate.py` keeps it identical to `schemas/map.schema.json`.
- Not tested: Windows, a machine with no network and no Python, and a repository that already has a map.
