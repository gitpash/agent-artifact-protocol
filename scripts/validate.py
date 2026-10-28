#!/usr/bin/env python3
"""Validate AAP Map v2 schemas, examples, resource references, and artifacts."""
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
    except json.JSONDecodeError as error:
        die(f"invalid JSON {path}: {error}")

def layout_path_errors(data: dict) -> list[str]:
    errors: list[str] = []
    def check(value: object, location: str) -> None:
        if isinstance(value, str):
            path = value
        elif isinstance(value, dict) and isinstance(value.get("path"), str):
            path = value["path"]
        else:
            errors.append(f"{location} must be a path string or resourceRef object")
            return
        if path.startswith("/") or ".." in path.split("/"):
            errors.append(f"forbidden layout path at {location}: {path!r}")
    layout = data.get("layout")
    if not isinstance(layout, dict):
        return errors
    for key, value in layout.items():
        for index, ref in enumerate(value if isinstance(value, list) else [value]):
            check(ref, f"layout.{key}[{index}]")
    return errors

def parse_envelope(path: Path, yaml: object) -> dict:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---"):
        die(f"{path}: missing frontmatter")
    parts = text.split("---", 2)
    if len(parts) < 3:
        die(f"{path}: malformed frontmatter")
    meta = yaml.safe_load(parts[1])
    if not isinstance(meta, dict):
        die(f"{path}: frontmatter must be a mapping")
    if hasattr(meta.get("updated"), "isoformat"):
        meta["updated"] = meta["updated"].isoformat()
    return meta

def main() -> None:
    try:
        import yaml  # type: ignore
        import jsonschema  # type: ignore
    except ImportError:
        die("PyYAML and jsonschema required: pip install pyyaml jsonschema")
    map_schema = load_json(ROOT / "schemas" / "map.schema.json")
    envelope_schema = load_json(ROOT / "schemas" / "artifact-envelope.schema.json")
    bundled = ROOT / "skills" / "aap-map" / "schema" / "map.schema.json"
    if bundled.exists() and load_json(bundled) != map_schema:
        die("skills/aap-map/schema/map.schema.json differs from schemas/map.schema.json (re-copy it)")
    for manifest in sorted((ROOT / ".claude-plugin").glob("*.json")):
        load_json(manifest)
        print(f"OK json {manifest.relative_to(ROOT)}")
    jsonschema.Draft7Validator.check_schema(map_schema)
    jsonschema.Draft7Validator.check_schema(envelope_schema)
    print("OK schemas self-validate")
    map_validator = jsonschema.Draft7Validator(map_schema)
    envelope_validator = jsonschema.Draft7Validator(envelope_schema)
    # templates + every examples/**/map.yaml except under examples/invalid/
    example_maps = sorted(
        path
        for path in (ROOT / "examples").rglob("map.yaml")
        if "invalid" not in path.relative_to(ROOT / "examples").parts
    )
    positives = [ROOT / "templates" / "minimal-map.yaml"] + example_maps
    for path in positives:
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
        errors = list(map_validator.iter_errors(data)) + [Exception(error) for error in layout_path_errors(data)]
        if errors:
            for error in errors: print(f"  {path}: {error}", file=sys.stderr)
            die(f"validation failed for {path}")
        print(f"OK map {path.relative_to(ROOT)}")
    for path in sorted((ROOT / "examples" / "invalid").glob("*.yaml")):
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
        if not list(map_validator.iter_errors(data)) and not layout_path_errors(data):
            die(f"expected invalid fixture to fail but passed: {path}")
        print(f"OK invalid fixture rejected {path.relative_to(ROOT)}")
    for path in sorted((ROOT / "templates").glob("artifact-*.md")):
        if list(envelope_validator.iter_errors(parse_envelope(path, yaml))): die(f"envelope invalid {path}")
        print(f"OK envelope {path.relative_to(ROOT)}")
    print("All checks passed.")
if __name__ == "__main__": main()
