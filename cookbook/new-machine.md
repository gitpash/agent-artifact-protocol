# Cookbook: set up a new machine

The hub is committed, the machine paths are not. On a fresh machine:

1. Clone the hub and open it.
2. Copy your overlay template to `.aap/map.local.yaml` and set the paths (see [`examples/personal-hub/map.local.yaml.example`](../examples/personal-hub/map.local.yaml.example)). Nodes that do not need to exist locally can be left out.
3. Check, then clone what is missing:

```bash
python scripts/aap_workspace.py doctor        # map schema, missing checkouts, node state
python scripts/aap_workspace.py missing --clone
```

`doctor` is read-only. Only the second command, with `--clone`, writes anything, and only clones of `locator.repo` into the overlay paths. Details: [`workspace-tools`](./workspace-tools.md).
