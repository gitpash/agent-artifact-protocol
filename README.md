# Agent Artifact Protocol (AAP)

A small map checked into your repository that tells coding agents where things live, so they can open the right place without loading everything first.

## Install the skill

The `aap-map` skill looks at your repository and writes the map for you. It is one text file with no dependencies.

With the [`skills`](https://skills.sh) installer, which works for Claude Code, Codex, Cursor and many other agents:

```bash
npx skills add gitpash/agent-artifact-protocol
```

In Claude Code, from the plugin marketplace:

```text
/plugin marketplace add gitpash/agent-artifact-protocol
/plugin install aap@agent-artifact-protocol
```

Then say this to your agent, inside the repository you want to map:

> Use the aap-map skill to add an AAP map to this repo.

The agent reads the repository, writes `.aap/map.yaml`, marks anything it guessed with a `# REVIEW:` comment and tells you what to check. It does not interview you and it never overwrites an existing map.

## Quick start

1. **Install the skill** with one of the commands above.
2. **Ask your agent to add the map**, as shown above, and read the `# REVIEW:` lines it left. Fix or delete them, or answer "ok".
3. **Commit `.aap/map.yaml`** and tell the agent to read the map first in future sessions. A line in `AGENTS.md` or `CLAUDE.md` is enough.

If you would rather not install anything, give your LLM this link and ask it to explain AAP or to work in a repository that has a map. The file is written for an agent to read and points to the spec only when it is needed:

```text
https://raw.githubusercontent.com/gitpash/agent-artifact-protocol/main/llms.txt
```

## What AAP is

AAP is a filesystem convention. The map is a short YAML file with the name of the workspace, the folders an agent will want (`code`, `tests`, `docs` and so on) and, for multi-repository setups, a few direct hops to neighbouring repositories. Agents read that file and nothing else at the start of a session, then open one path as the task requires.

The convention comes with a JSON Schema, so any tool can check a map, but the skill itself needs no tool to write one.

## What AAP is not

- Not a context engine or retrieval system. Your normal tools (grep, an LSP, an index, MCP) still do the searching.
- Not an agent framework or a multi-agent runtime.
- Not a security boundary. The `access` field is a note between humans and agents, and real enforcement stays with Git permissions, protected branches and sandboxes.
- Not a replacement for `AGENTS.md` or `CLAUDE.md`. Those say how to work, the map says where things are, and the two sit side by side.

## A minimal map

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
  artifacts:
    - path: docs/decisions/
      access: read-write
nodes:
  - id: orders-api
    kind: repository
    description: "Owns the orders contract this app consumes."
    path: services/orders
    access: read-only
```

- `layout` maps an intent to a path in this checkout. A plain string means read-write, and the object form adds `access: read-only` for folders that are frozen, generated or vendored. When a key lists several paths, the first one that is not read-only is where durable notes go.
- `nodes` are direct hops to other repositories you would plausibly open during a normal change here. Most standalone repositories use `nodes: []`.
- Paths are relative to the repository root, never absolute and never containing `..`.

Examples for a single repository, a hub with several repositories and path references with `access` are in [`examples/`](./examples/). The starter file is [`templates/minimal-map.yaml`](./templates/minimal-map.yaml).

## How an agent uses it

AAP asks for progressive disclosure in four levels, and only the first is required.

| Level | What the agent reads | When |
|-------|----------------------|------|
| L0 | The map only | Start of a session |
| L1 | One layout path or one node | After choosing a key or node for the task |
| L2 | One durable note | Only if the task needs durable memory |
| L3 | Code, with the usual tools | Implementation |

Linked maps are hops taken on purpose and are never preloaded recursively. Until you enable writes, an agent should prefer reading and orienting only.

## Beyond the basics

- [`SPEC.md`](./SPEC.md): the short normative specification.
- [`schemas/`](./schemas/): the JSON Schema for the map and for the optional artifact envelope.
- [`cookbook/`](./cookbook/): optional profiles such as a hub map for several repositories, schema pinning, CI validation, stream packs and a done bar. None of them is needed for the basic map.
- [`docs/motivation.md`](./docs/motivation.md) explains why the map exists, and [`docs/skill-tests.md`](./docs/skill-tests.md) describes how the skill was tested.
- [`CONTRIBUTING.md`](./CONTRIBUTING.md) and [`CHANGELOG.md`](./CHANGELOG.md).

To check maps in CI, see [`cookbook/ci-validation.md`](./cookbook/ci-validation.md). This is optional and the skill does not depend on it. This repository keeps its own map in [`.aap/map.yaml`](./.aap/map.yaml), written by the skill.

## Status

AAP is at version 0.3.0 and is experimental. The Map v2 schema has not changed since 0.2.0, but the convention has been used on a small number of repositories, mostly by its author, and it has not been measured against alternatives. Expect small changes before 1.0, and treat the tag you pin as the version you are using. The thesis, that a sparse map beats a bigger prompt, is unproven here, and [`cookbook/measuring.md`](./cookbook/measuring.md) describes how to test it on your own work. If a map does not help, shrink it before adding anything.

Feedback is welcome as issues: map size, how fine layout keys should be, and whether the skill guesses well on repositories unlike the three it was tested on.

## License

MIT. See [`LICENSE`](./LICENSE).
