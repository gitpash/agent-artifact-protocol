#!/usr/bin/env python3
"""Validate AAP seed: JSON schemas, example/template maps, layout path rules, invalid fixtures."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def die(msg: str) -> None:
    print(f"ERROR: {msg}", file=sys.stderr)
    raise SystemExit(1)


def load_json(path: Path) -> object:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        die(f"invalid JSON {path}: {e}")


def layout_path_errors(data: dict) -> list[str]:
    errs: list[str] = []

    def check_path_val(p: str, loc: str) -> None:
        if p.startswith("/") or ".." in p.split("/"):
            errs.append(f"forbidden layout path at {loc}: {p!r}")

    def walk_layout(layout: dict, loc: str) -> None:
        for key, val in layout.items():
            if isinstance(val, str):
                check_path_val(val, f"{loc}.{key}")
            elif isinstance(val, list):
                for i, item in enumerate(val):
                    if not isinstance(item, str):
                        errs.append(f"{loc}.{key}[{i}] must be string")
                    else:
                        check_path_val(item, f"{loc}.{key}[{i}]")
            else:
                errs.append(f"{loc}.{key} must be string or list of strings")

    defaults = data.get("defaults") or {}
    if isinstance(defaults, dict) and isinstance(defaults.get("layout"), dict):
        walk_layout(defaults["layout"], "defaults.layout")

    zones = data.get("zones")
    if not isinstance(zones, dict) or len(zones) < 1:
        errs.append("zones must be non-empty object")
        return errs

    for zid, zone in zones.items():
        if not isinstance(zone, dict):
            errs.append(f"zone {zid} must be object")
            continue
        layout = zone.get("layout")
        if isinstance(layout, dict):
            walk_layout(layout, f"zones.{zid}.layout")
        write = zone.get("write")
        if write is not None:
            if not isinstance(write, list):
                errs.append(f"zones.{zid}.write must be list")
            else:
                for mode in write:
                    if mode not in ("domain", "architect"):
                        errs.append(
                            f"zones.{zid}.write invalid mode {mode!r} "
                            "(readonly is not a write grant; use access: read-only and write: [])"
                        )
    return errs


def main() -> None:
    try:
        import yaml  # type: ignore
    except ImportError:
        die("PyYAML required: pip install pyyaml")

    try:
        import jsonschema  # type: ignore
    except ImportError:
        die("jsonschema required: pip install jsonschema")

    map_schema = load_json(ROOT / "schemas" / "map.schema.json")
    env_schema = load_json(ROOT / "schemas" / "artifact-envelope.schema.json")
    jsonschema.Draft7Validator.check_schema(map_schema)
    jsonschema.Draft7Validator.check_schema(env_schema)
    print("OK schemas self-validate")

    map_validator = jsonschema.Draft7Validator(map_schema)
    env_validator = jsonschema.Draft7Validator(env_schema)

    positive_maps = [
        p
        for p in list((ROOT / "examples").rglob("map.yaml"))
        + [ROOT / "templates" / "minimal-map.yaml"]
        if "invalid" not in p.parts
    ]

    for path in sorted(positive_maps):
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
        if not isinstance(data, dict):
            die(f"{path}: root must be mapping")
        schema_errs = sorted(map_validator.iter_errors(data), key=lambda e: list(e.path))
        if schema_errs:
            for e in schema_errs:
                print(f"  schema {path}: {list(e.path)}: {e.message}", file=sys.stderr)
            die(f"schema validation failed for {path}")
        path_errs = layout_path_errors(data)
        if path_errs:
            for e in path_errs:
                print(f"  layout {path}: {e}", file=sys.stderr)
            die(f"layout validation failed for {path}")
        print(f"OK map {path.relative_to(ROOT)}")

    invalid_dir = ROOT / "examples" / "invalid"
    if invalid_dir.is_dir():
        for path in sorted(invalid_dir.glob("*.yaml")):
            data = yaml.safe_load(path.read_text(encoding="utf-8"))
            failed = False
            if not isinstance(data, dict):
                failed = True
            else:
                if list(map_validator.iter_errors(data)):
                    failed = True
                if layout_path_errors(data):
                    failed = True
            if not failed:
                die(f"expected invalid fixture to fail but passed: {path}")
            print(f"OK invalid fixture rejected {path.relative_to(ROOT)}")

    for path in sorted((ROOT / "templates").glob("artifact-*.md")):
        text = path.read_text(encoding="utf-8")
        if not text.startswith("---"):
            die(f"{path}: missing frontmatter")
        parts = text.split("---", 2)
        if len(parts) < 3:
            die(f"{path}: malformed frontmatter")
        meta = yaml.safe_load(parts[1])
        # YAML 1.1 may load bare dates as datetime.date — normalize for schema.
        if isinstance(meta, dict) and hasattr(meta.get("updated"), "isoformat"):
            meta["updated"] = meta["updated"].isoformat()
        env_errs = list(env_validator.iter_errors(meta))
        if env_errs:
            for e in env_errs:
                print(f"  {path}: {e.message}", file=sys.stderr)
            die(f"envelope invalid {path}")
        print(f"OK envelope {path.relative_to(ROOT)}")

    for path in (ROOT / "examples").rglob("*.yaml"):
        if "invalid" in path.parts:
            continue
        for line in path.read_text(encoding="utf-8").splitlines()[:8]:
            if "$schema=" in line and "../../schemas/" in line:
                rel = line.split("$schema=", 1)[1].strip()
                target = (path.parent / rel).resolve()
                if not target.is_file():
                    die(f"{path}: schema path missing {rel} -> {target}")

    print("All checks passed.")


if __name__ == "__main__":
    main()
