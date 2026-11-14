# Cookbook: home repo

A "home repo" (the idea Matt Pocock describes in his *Home Repo* video) is one repository you always launch your agent from. It holds the routing table: which projects exist, what each is for, where to go for what. An AAP hub map is that routing table in machine-readable form: `nodes` are the rows, `layout` is the hub's own folders, `map.local.yaml` says where each row lives on this machine. The map says where things are; what the agent should *do* (the next two recipes) belongs in `AGENTS.md` or `CLAUDE.md`.

Worked example: [`examples/personal-hub/`](../examples/personal-hub/). Map shape: [`hub-umbrella`](./hub-umbrella.md). Checks: [`workspace-tools`](./workspace-tools.md). Status per node: [`node-state`](./node-state.md). Reuse: [`capability-index`](./capability-index.md).

## Auto-clone a missing node

The map names the repo (`locator.repo`) and the overlay names the path, so a missing checkout is recoverable without asking you. In the hub's `AGENTS.md`:

```markdown
If a node's checkout is missing, clone `locator.repo` to its overlay path
(`python scripts/aap_workspace.py missing` prints the command) before working.
No `locator.repo` means ask the owner.
```

Cloning is behaviour, so it is an instruction to the agent, not something the map does.

## Worktrees for parallel sessions

When two sessions might touch the same node, tell the agent to work in a `git worktree` of the target repo, not in the shared checkout. Also an `AGENTS.md` line:

```markdown
Before editing a node, create a worktree of it (`git -C <overlay path> worktree add ...`)
and work there. Never edit the shared checkout while another session may use it.
```

The map only resolves which repo; the worktree is the agent's choice for that task. `access: read-only` on a node still means "do not change it from here", worktree or not.

## 30+ repos: progressive disclosure

Do not list everything in one map. Keep the hub's `nodes` to the repos you really open, and give each group its own map reached through `map.path`:

```yaml
nodes:
  - id: platform
    kind: repository
    description: "Platform services; open its map for the individual repos."
    locator: { repo: example/platform }
    map: { path: .aap/map.yaml }
```

The agent reads the hub map (L0), hops to one child map only when the task needs it, and never preloads children recursively. Leaves stay out of the hub until you open them often.
