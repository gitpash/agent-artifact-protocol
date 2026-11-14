# Cookbook: workspace tools

Small checks for a hub map, in [`scripts/aap_workspace.py`](../scripts/aap_workspace.py). They need Python, PyYAML (already needed by `validate.py`) and `git`. They read the map and `.aap/map.local.yaml` and change nothing, except `--clone`, which you must pass yourself. Nothing is copied between files: the map stays the single source.

Run from inside the hub; the map is found by searching upward, or pass `--map PATH`.

## Missing checkouts

```bash
python scripts/aap_workspace.py missing          # report + the git clone line
python scripts/aap_workspace.py missing --clone  # actually clone what is missing
```

For each node the checkout path is the overlay in `map.local.yaml` (`overlays.nodes` or `local_paths`), else the node's own `path`. If it does not exist, the script prints `git clone <locator.repo> <path>`. Nodes with no `locator.repo` are reported with "ask the owner". A node with no path anywhere is reported with a hint to add an overlay. `--strict` exits 1 if anything is missing (for scripts).

## Missing nodes

```bash
python scripts/aap_workspace.py siblings [--root ~/code]
```

Lists git repositories in the folder next to the hub (or `--root`) that are neither a node's checkout nor a node's `locator.repo`. This is a report: some repos should not be nodes, and that is your call.

## Nodes skeleton

```bash
python scripts/aap_workspace.py suggest ~/code
```

Prints a `nodes:` block (id, `locator.repo` from `origin`, `access: read-only`, a `# REVIEW` description) and the matching `overlays` block for `map.local.yaml`. Paste what you want; the script never writes or overwrites a map. Descriptions are yours to write: a node is worth having only if you can say in one line when to open it.

## State and doctor

```bash
python scripts/aap_workspace.py state    # per-node status, see node-state
python scripts/aap_workspace.py doctor   # map schema (if jsonschema is installed) + missing + state
```

`doctor` is the one command to run before a session or in CI; add `alias aap='python scripts/aap_workspace.py'` if you want it shorter. It exits 1 on any problem.

See also: [`home-repo`](./home-repo.md), [`hub-umbrella`](./hub-umbrella.md), [`local-bootstrap`](./local-bootstrap.md).
