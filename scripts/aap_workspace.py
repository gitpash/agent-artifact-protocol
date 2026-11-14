#!/usr/bin/env python3
"""Workspace helpers for an AAP hub map. Read-only unless --clone is given.

  missing   nodes whose checkout is absent, with the `git clone` for locator.repo
  siblings  git repos next to the map's repo that are not in the map's nodes
  suggest   print a nodes skeleton for the git repos in a folder (never writes)

Needs only PyYAML (the same dependency as validate.py) and git.
"""
from __future__ import annotations
import argparse
import subprocess
import sys
from pathlib import Path

try:
    import yaml  # type: ignore
except ImportError:
    sys.exit("ERROR: PyYAML required: pip install pyyaml")


def load_yaml(path: Path) -> dict:
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    return data if isinstance(data, dict) else {}


def find_map(start: Path) -> Path:
    for base in [start, *start.parents]:
        candidate = base / ".aap" / "map.yaml"
        if candidate.is_file():
            return candidate
    sys.exit("ERROR: no .aap/map.yaml found; pass --map")


def overlay_paths(map_path: Path) -> dict[str, str]:
    """Machine-local checkout paths from the gitignored map.local.yaml (or overlays in the map)."""
    found: dict[str, str] = {}
    sources = [load_yaml(map_path), *(load_yaml(p) for p in (map_path.with_name("map.local.yaml"),) if p.is_file())]
    for data in sources:  # the local file comes last and wins
        overlays = data.get("overlays") or {}
        for node_id, entry in (overlays.get("nodes") or {}).items():
            if isinstance(entry, dict) and entry.get("path"):
                found[node_id] = entry["path"]
        for node_id, path in (overlays.get("local_paths") or {}).items():
            if isinstance(path, str):
                found[node_id] = path
    return found


def resolve(node: dict, overlays: dict[str, str], repo_root: Path) -> Path | None:
    raw = overlays.get(node["id"]) or node.get("path")
    if not raw:
        return None
    path = Path(raw).expanduser()
    return (path if path.is_absolute() else repo_root / path).resolve()


def clone_url(repo: str) -> str:
    return repo if ("://" in repo or "@" in repo) else f"https://github.com/{repo}.git"


def git_remote(path: Path) -> str | None:
    result = subprocess.run(["git", "-C", str(path), "remote", "get-url", "origin"],
                            capture_output=True, text=True)
    return result.stdout.strip() if result.returncode == 0 and result.stdout.strip() else None


def repo_slug(remote: str | None) -> str | None:
    """owner/name from a GitHub-style remote URL, else None."""
    if not remote:
        return None
    tail = remote.removesuffix(".git").replace(":", "/").split("/")
    return "/".join(tail[-2:]) if len(tail) >= 2 else None


def git_repos(root: Path) -> list[Path]:
    return sorted(p for p in root.iterdir() if p.is_dir() and (p / ".git").exists())


def cmd_missing(args: argparse.Namespace) -> int:
    map_path = Path(args.map).resolve() if args.map else find_map(Path.cwd())
    repo_root = map_path.parent.parent
    overlays = overlay_paths(map_path)
    missing = 0
    for node in load_yaml(map_path).get("nodes") or []:
        path = resolve(node, overlays, repo_root)
        repo = (node.get("locator") or {}).get("repo")
        if path and path.exists():
            print(f"ok       {node['id']}: {path}")
            continue
        missing += 1
        if not path:
            print(f"MISSING  {node['id']}: no checkout path (add it to map.local.yaml under overlays.nodes)")
            if repo:
                print(f"         git clone {clone_url(repo)} <where-you-keep-it>")
            continue
        print(f"MISSING  {node['id']}: {path}")
        if not repo:
            print("         no locator.repo, so nothing to clone; ask the owner")
            continue
        print(f"         git clone {clone_url(repo)} {path}")
        if args.clone:
            path.parent.mkdir(parents=True, exist_ok=True)
            subprocess.run(["git", "clone", clone_url(repo), str(path)], check=False)
    print(f"{missing} missing")
    return 1 if (missing and args.strict) else 0


def cmd_siblings(args: argparse.Namespace) -> int:
    map_path = Path(args.map).resolve() if args.map else find_map(Path.cwd())
    repo_root = map_path.parent.parent
    root = Path(args.root).expanduser().resolve() if args.root else repo_root.parent
    data = load_yaml(map_path)
    overlays = overlay_paths(map_path)
    known_paths = {repo_root}
    known_repos: set[str] = set()
    for node in data.get("nodes") or []:
        path = resolve(node, overlays, repo_root)
        if path:
            known_paths.add(path)
        repo = (node.get("locator") or {}).get("repo")
        if repo:
            known_repos.add(repo_slug(repo) or repo)
    extra = 0
    for repo in git_repos(root):
        slug = repo_slug(git_remote(repo))
        if repo.resolve() in known_paths or (slug and slug in known_repos):
            continue
        extra += 1
        print(f"not in map: {repo.name}" + (f"  ({slug})" if slug else "  (no remote)"))
    print(f"{extra} repo(s) in {root} are not nodes of {map_path}")
    return 1 if (extra and args.strict) else 0


def cmd_suggest(args: argparse.Namespace) -> int:
    root = Path(args.root).expanduser().resolve()
    print(f"# Suggested nodes for the git repos in {root}. Review, trim, then paste into .aap/map.yaml.")
    print("# Machine paths go in the gitignored .aap/map.local.yaml, not here.")
    print("nodes:")
    for repo in git_repos(root):
        slug = repo_slug(git_remote(repo))
        node_id = "".join(c if c.isalnum() else "-" for c in repo.name.lower()).strip("-")
        if not node_id or not node_id[0].isalpha():
            node_id = f"repo-{node_id}"
        print(f"  - id: {node_id}")
        print("    kind: repository")
        print('    description: "REVIEW: one line on when to open this repository."')
        if slug:
            print(f"    locator:\n      repo: {slug}")
        print("    access: read-only")
    print("\n# overlays for .aap/map.local.yaml (gitignored):")
    print("overlays:\n  nodes:")
    for repo in git_repos(root):
        node_id = "".join(c if c.isalnum() else "-" for c in repo.name.lower()).strip("-")
        print(f"    {node_id}: {{ path: {repo} }}")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = parser.add_subparsers(dest="cmd", required=True)
    for name, func in (("missing", cmd_missing), ("siblings", cmd_siblings)):
        p = sub.add_parser(name)
        p.add_argument("--map", help="path to .aap/map.yaml (default: search upward from cwd)")
        p.add_argument("--strict", action="store_true", help="exit 1 when something is reported")
        if name == "missing":
            p.add_argument("--clone", action="store_true", help="actually run git clone for missing nodes")
        else:
            p.add_argument("--root", help="folder to scan (default: parent of the map's repository)")
        p.set_defaults(func=func)
    p = sub.add_parser("suggest")
    p.add_argument("root", help="folder that holds the repositories")
    p.set_defaults(func=cmd_suggest)
    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
