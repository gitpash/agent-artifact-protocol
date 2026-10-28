#!/usr/bin/env python3
"""Validate an AAP Map v2 file against the bundled JSON Schema.

Usage: python validate_map.py [MAP] [--root DIR] [--schema FILE]

MAP defaults to .aap/map.yaml. Exit codes: 0 valid, 1 invalid, 2 setup problem.
Needs PyYAML and jsonschema (pip install pyyaml jsonschema, or
uv run --with pyyaml --with jsonschema python validate_map.py ...).
Warnings never change the exit code; they point at things a human should check.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent


def setup_error(message: str) -> None:
    print(f"SETUP_ERROR: {message}", file=sys.stderr)
    raise SystemExit(2)


def refs(value: object) -> list[tuple[str, bool]]:
    """Return (path, writable) for a layout value."""
    items = value if isinstance(value, list) else [value]
    out = []
    for item in items:
        if isinstance(item, str):
            out.append((item, True))
        elif isinstance(item, dict) and isinstance(item.get("path"), str):
            out.append((item["path"], item.get("access", "read-write") != "read-only"))
    return out


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("map", nargs="?", default=".aap/map.yaml")
    parser.add_argument("--root", help="workspace root for path checks (default: parent of .aap/, else map dir)")
    parser.add_argument("--schema", default=str(HERE.parent / "schema" / "map.schema.json"))
    args = parser.parse_args()

    try:
        import yaml
        import jsonschema
    except ImportError:
        setup_error("PyYAML and jsonschema are required: pip install pyyaml jsonschema")

    map_path = Path(args.map)
    if not map_path.is_file():
        setup_error(f"map not found: {map_path}")
    schema_path = Path(args.schema)
    if not schema_path.is_file():
        setup_error(f"schema not found: {schema_path}")

    text = map_path.read_text(encoding="utf-8")
    try:
        data = yaml.safe_load(text)
    except yaml.YAMLError as error:
        print("VALIDATION_FAILED")
        print(f"- path: / | message: YAML does not parse: {error}")
        raise SystemExit(1)
    schema = json.loads(schema_path.read_text(encoding="utf-8"))
    validator = jsonschema.Draft7Validator(schema)
    errors = sorted(validator.iter_errors(data), key=lambda e: [str(p) for p in e.absolute_path])
    if errors:
        print("VALIDATION_FAILED")
        for error in errors:
            pointer = "/" + "/".join(str(p) for p in error.absolute_path)
            print(f"- path: {pointer} | message: {error.message[:200]}")
        raise SystemExit(1)

    root = Path(args.root) if args.root else (
        map_path.resolve().parent.parent if map_path.resolve().parent.name == ".aap" else map_path.resolve().parent
    )
    warnings: list[str] = []
    for key, value in (data.get("layout") or {}).items():
        entries = refs(value)
        for path, _ in entries:
            if not (root / path).exists():
                warnings.append(f"layout.{key}: '{path}' does not exist on disk (fine if intended, otherwise fix or drop)")
        if entries and not any(writable for _, writable in entries):
            warnings.append(f"layout.{key}: no writable entry, agents will fail closed on durable writes")
    seen: set[str] = set()
    for index, node in enumerate(data.get("nodes") or []):
        if node["id"] in seen:
            warnings.append(f"nodes[{index}]: duplicate id '{node['id']}'")
        seen.add(node["id"])
        if "path" in node and not (root / node["path"]).exists():
            warnings.append(f"nodes[{index}] ({node['id']}): path '{node['path']}' does not exist on disk")
        if "description" not in node:
            warnings.append(f"nodes[{index}] ({node['id']}): no description; say what is consulted there and when")
    def bad_path(value: object) -> bool:
        return isinstance(value, str) and (
            value.startswith(("/", "~", "\\")) or re.match(r"^[A-Za-z]:", value) is not None
            or "\\" in value or ".." in value.split("/")
        )

    candidates = [("self.path", (data.get("self") or {}).get("path"))]
    for index, node in enumerate(data.get("nodes") or []):
        candidates.append((f"nodes[{index}].path", node.get("path")))
        candidates.append((f"nodes[{index}].map.path", (node.get("map") or {}).get("path")))
    for name, value in candidates:
        if bad_path(value):
            warnings.append(f"{name}: '{value}' must be workspace-relative (no absolute, '~', backslash or '..'); machine paths belong in map.local.yaml")
    review = [n + 1 for n, line in enumerate(text.splitlines()) if re.search(r"#\s*REVIEW:", line)]
    print("VALIDATION_SUCCESS")
    for warning in warnings:
        print(f"WARN {warning}")
    print(f"REVIEW_MARKERS {len(review)}" + (f" (lines {', '.join(map(str, review))})" if review else ""))


if __name__ == "__main__":
    main()
