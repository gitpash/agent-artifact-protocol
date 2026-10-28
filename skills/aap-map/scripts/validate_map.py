#!/usr/bin/env python3
"""Validate an AAP Map v2 file with nothing but the Python 3 standard library.

Usage: python3 validate_map.py [MAP] [--root DIR]

MAP defaults to .aap/map.yaml. Exit codes: 0 valid, 1 invalid, 2 setup problem.

This is a hand-written check of the Map v2 schema plus a small YAML reader for
the subset a map needs: block mappings and sequences, flow {} and [] values,
quoted and plain scalars, comments, and | or > block scalars. Anything else
(anchors, tags, multi-line plain scalars, tabs) is rejected on purpose with
"unsupported YAML"; rewrite the map in block style. The full JSON Schema check
(scripts/validate.py in the AAP repo) is the reference; CI runs both on the
same fixtures so they cannot drift apart.
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

ID = re.compile(r"^[a-z][a-z0-9-]*$")
KEY_RE = (
    r'^("(?:[^"\\]|\\.)*"'          # double-quoted key
    r"|'[^']*'"                          # single-quoted key
    r"|[^\s:#\"'\[{][^:#]*?)"           # plain key
    r"\s*:(?:\s+(.*)|$)"
)


class YamlError(Exception):
    pass


# ---------------------------------------------------------------- YAML subset

def strip_comment(line: str) -> str:
    quote = ""
    for i, ch in enumerate(line):
        if quote:
            if ch == quote:
                quote = ""
        elif ch in "\"'" and (i == 0 or line[i - 1] in " \t:[{,-"):
            quote = ch
        elif ch == "#" and (i == 0 or line[i - 1] in " \t"):
            return line[:i]
    return line.rstrip()


def scalar(text: str):
    t = text.strip()
    if t == "":
        return None
    if t[0] == '"':
        if len(t) < 2 or t[-1] != '"':
            raise YamlError(f"unterminated double quote: {t[:40]}")
        return re.sub(r'\\(["\\/])', r"\1", t[1:-1]).replace("\\n", "\n").replace("\\t", "\t")
    if t[0] == "'":
        if len(t) < 2 or t[-1] != "'":
            raise YamlError(f"unterminated single quote: {t[:40]}")
        return t[1:-1].replace("''", "'")
    if t[0] in "&*!@`%":
        raise YamlError(f"unsupported YAML (anchors, tags, aliases): {t[:40]}")
    if t in ("null", "~", "Null", "NULL"):
        return None
    if t in ("true", "True", "TRUE"):
        return True
    if t in ("false", "False", "FALSE"):
        return False
    if re.fullmatch(r"-?\d+", t):
        return int(t)
    if t[0] in "{[":
        return flow(t)
    return t


def flow(text: str):
    pos = 0

    def skip() -> None:
        nonlocal pos
        while pos < len(text) and text[pos] in " \t":
            pos += 1

    def value(stop: str):
        nonlocal pos
        skip()
        if pos >= len(text):
            raise YamlError("unterminated flow collection")
        ch = text[pos]
        if ch == "{":
            pos += 1
            out: dict = {}
            skip()
            if text[pos:pos + 1] == "}":
                pos += 1
                return out
            while True:
                key = value(":")
                skip()
                if text[pos:pos + 1] != ":":
                    raise YamlError("flow mapping key without ':' (quote values that contain commas, colons or #, or use block style)")
                pos += 1
                out[key] = value(",}")
                skip()
                if text[pos:pos + 1] == ",":
                    pos += 1
                    continue
                if text[pos:pos + 1] == "}":
                    pos += 1
                    return out
                raise YamlError("bad flow mapping")
        if ch == "[":
            pos += 1
            items: list = []
            skip()
            if text[pos:pos + 1] == "]":
                pos += 1
                return items
            while True:
                items.append(value(",]"))
                skip()
                if text[pos:pos + 1] == ",":
                    pos += 1
                    continue
                if text[pos:pos + 1] == "]":
                    pos += 1
                    return items
                raise YamlError("bad flow sequence")
        if ch in "\"'":
            end = pos + 1
            while end < len(text) and text[end] != ch:
                end += 1
            if end >= len(text):
                raise YamlError("unterminated quote in flow collection")
            raw = text[pos:end + 1]
            pos = end + 1
            return scalar(raw)
        start = pos
        while pos < len(text) and text[pos] not in stop:
            pos += 1
        return scalar(text[start:pos])

    result = value("")
    skip()
    if pos != len(text):
        raise YamlError(f"unexpected text after flow value: {text[pos:pos + 30]}")
    return result


def parse_yaml(source: str):
    if "\t" in source:
        raise YamlError("unsupported YAML: tab characters (use spaces)")
    raw = source.splitlines()
    lines: list[tuple[int, str, int]] = []  # (indent, text, original index)
    for n, line in enumerate(raw):
        stripped = strip_comment(line)
        if stripped.strip() == "" or stripped.strip() in ("---", "..."):
            continue
        lines.append((len(stripped) - len(stripped.lstrip(" ")), stripped.strip(), n))
    if not lines:
        raise YamlError("empty document")
    pos = 0

    def block_scalar(indent: int, style: str, header_line: int) -> str:
        nonlocal pos
        body = []
        n = header_line + 1
        while n < len(raw) and (raw[n].strip() == "" or len(raw[n]) - len(raw[n].lstrip(" ")) > indent):
            body.append(raw[n].strip())
            n += 1
        while pos < len(lines) and lines[pos][2] < n:
            pos += 1
        joined = ("\n" if style.startswith("|") else " ").join(body).strip()
        return joined

    def split_key(text: str):
        m = re.match(KEY_RE, text)
        if not m:
            return None
        key = scalar(m.group(1))
        return key, (m.group(2) or "")

    def value_of(rest: str, indent: int, line_no: int):
        nonlocal pos
        if rest in ("|", ">", "|-", ">-", "|+", ">+"):
            return block_scalar(indent, rest, line_no)
        if rest == "":
            if pos < len(lines) and (lines[pos][0] > indent or (lines[pos][0] == indent and lines[pos][1].startswith("- "))):
                return parse_block(lines[pos][0])
            return None
        if rest[0] in "{[" and not (rest.endswith("}") or rest.endswith("]")):
            raise YamlError(f"unsupported YAML: multi-line flow collection at line {line_no + 1}")
        val = scalar(rest)
        if pos < len(lines) and lines[pos][0] > indent and not isinstance(val, (dict, list)):
            raise YamlError(f"unsupported YAML: multi-line plain scalar near line {lines[pos][2] + 1}; quote it on one line")
        return val

    def parse_block(indent: int):
        nonlocal pos
        indent_now, text, _ = lines[pos]
        if text.startswith("- ") or text == "-":
            seq: list = []
            while pos < len(lines) and lines[pos][0] == indent and (lines[pos][1].startswith("- ") or lines[pos][1] == "-"):
                _, t, ln = lines[pos]
                rest = t[1:].strip()
                pos += 1
                kv = split_key(rest) if rest and rest[0] not in "{[" else None
                if kv is not None:
                    # "- key: value": re-inject as a mapping indented past the dash
                    offset = len(t) - len(rest)
                    lines.insert(pos, (indent + offset, rest, ln))
                    seq.append(parse_block(indent + offset))
                elif rest == "":
                    seq.append(parse_block(lines[pos][0]) if pos < len(lines) and lines[pos][0] > indent else None)
                else:
                    seq.append(value_of(rest, indent, ln))
            return seq
        out: dict = {}
        while pos < len(lines) and lines[pos][0] == indent:
            _, t, ln = lines[pos]
            if t.startswith("- "):
                break
            kv = split_key(t)
            if kv is None:
                raise YamlError(f"unsupported YAML or not a mapping at line {ln + 1}: {t[:50]}")
            key, rest = kv
            pos += 1
            if key in out:
                raise YamlError(f"duplicate key '{key}' at line {ln + 1}")
            out[key] = value_of(rest, indent, ln)
        if pos < len(lines) and lines[pos][0] > indent:
            raise YamlError(f"unexpected indentation at line {lines[pos][2] + 1}")
        return out

    doc = parse_block(lines[0][0])
    if pos < len(lines):
        raise YamlError(f"unexpected content at line {lines[pos][2] + 1}: {lines[pos][1][:50]}")
    return doc


# --------------------------------------------------------------- schema rules

def is_str(v) -> bool:
    return isinstance(v, str) and v != ""


def check_path(v, where, errs, allow_empty=False):
    if not isinstance(v, str) or (v == "" and not allow_empty):
        errs.append((where, "must be a non-empty string"))
    elif v.startswith("/") or ".." in v:
        errs.append((where, f"must be workspace-relative with no '..' (got {v!r})"))


def check_id(v, where, errs):
    if not (isinstance(v, str) and ID.match(v)):
        errs.append((where, f"id must match ^[a-z][a-z0-9-]*$ (got {v!r})"))


def check_keys(obj, where, allowed, required, errs):
    if not isinstance(obj, dict):
        errs.append((where, "must be a mapping"))
        return False
    for k in obj:
        if k not in allowed:
            errs.append((f"{where}/{k}", "additional property not allowed"))
    for k in required:
        if k not in obj:
            errs.append((where, f"missing required property '{k}'"))
    return True


def check_access(v, where, errs):
    if v not in ("read-only", "read-write"):
        errs.append((where, "access must be 'read-only' or 'read-write'"))


def check_resource(v, where, errs):
    if isinstance(v, str):
        check_path(v, where, errs)
    elif isinstance(v, dict):
        if check_keys(v, where, {"path", "access", "description"}, ["path"], errs):
            if "path" in v:
                check_path(v["path"], f"{where}/path", errs)
            if "access" in v:
                check_access(v["access"], f"{where}/access", errs)
            if "description" in v and not isinstance(v["description"], str):
                errs.append((f"{where}/description", "must be a string"))
    else:
        errs.append((where, "must be a path string or {path, access?, description?}"))


def check_locator(v, where, errs):
    if check_keys(v, where, {"repo", "url", "id", "default_branch"}, [], errs):
        for k in ("repo", "url", "id"):
            if k in v and not is_str(v[k]):
                errs.append((f"{where}/{k}", "must be a non-empty string"))
        if not any(k in v for k in ("repo", "url", "id")):
            errs.append((where, "needs at least one of repo, url, id"))


def check_mappointer(v, where, errs):
    if check_keys(v, where, {"path", "url", "ref"}, [], errs):
        for k in ("path", "url", "ref"):
            if k in v and not is_str(v[k]):
                errs.append((f"{where}/{k}", "must be a non-empty string"))
        if not ("path" in v or "url" in v):
            errs.append((where, "needs path or url"))


def schema_errors(d) -> list[tuple[str, str]]:
    errs: list[tuple[str, str]] = []
    top = {"version", "workspace", "self", "layout", "nodes", "relations", "overlays", "profiles"}
    if not check_keys(d, "", top, ["version", "workspace", "self", "nodes"], errs):
        return errs
    if d.get("version") != 2 or isinstance(d.get("version"), bool):
        errs.append(("/version", "must be the integer 2"))
    ws = d.get("workspace")
    if check_keys(ws, "/workspace", {"id", "description"}, ["id"], errs):
        if "id" in ws:
            check_id(ws["id"], "/workspace/id", errs)
        if "description" in ws and not isinstance(ws["description"], str):
            errs.append(("/workspace/description", "must be a string"))
    me = d.get("self")
    if check_keys(me, "/self", {"id", "kind", "path", "description", "parent"}, ["id", "kind"], errs):
        if "id" in me:
            check_id(me["id"], "/self/id", errs)
        for k in ("kind", "path"):
            if k in me and not is_str(me[k]):
                errs.append((f"/self/{k}", "must be a non-empty string"))
        if "description" in me and not isinstance(me["description"], str):
            errs.append(("/self/description", "must be a string"))
        if "parent" in me:
            p = me["parent"]
            if check_keys(p, "/self/parent", {"id", "locator", "map"}, ["id"], errs):
                if "id" in p:
                    check_id(p["id"], "/self/parent/id", errs)
                if "locator" in p:
                    check_locator(p["locator"], "/self/parent/locator", errs)
                if "map" in p:
                    check_mappointer(p["map"], "/self/parent/map", errs)
    layout = d.get("layout")
    if "layout" in d:
        if not isinstance(layout, dict):
            errs.append(("/layout", "must be a mapping"))
        else:
            for k, v in layout.items():
                if isinstance(v, list):
                    if not v:
                        errs.append((f"/layout/{k}", "list must not be empty"))
                    for i, item in enumerate(v):
                        check_resource(item, f"/layout/{k}/{i}", errs)
                else:
                    check_resource(v, f"/layout/{k}", errs)
    nodes = d.get("nodes")
    if not isinstance(nodes, list):
        errs.append(("/nodes", "must be a list (use 'nodes: []' for none)"))
    else:
        allowed = {"id", "kind", "description", "path", "locator", "map", "mirror", "access", "write"}
        for i, n in enumerate(nodes):
            w = f"/nodes/{i}"
            if not check_keys(n, w, allowed, ["id", "kind"], errs):
                continue
            if "id" in n:
                check_id(n["id"], f"{w}/id", errs)
            for k in ("kind", "path"):
                if k in n and not is_str(n[k]):
                    errs.append((f"{w}/{k}", "must be a non-empty string"))
            if "description" in n and not isinstance(n["description"], str):
                errs.append((f"{w}/description", "must be a string"))
            if "locator" in n:
                check_locator(n["locator"], f"{w}/locator", errs)
            if "map" in n:
                check_mappointer(n["map"], f"{w}/map", errs)
            if "mirror" in n:
                m = n["mirror"]
                if check_keys(m, f"{w}/mirror", {"path"}, ["path"], errs) and "path" in m and not is_str(m["path"]):
                    errs.append((f"{w}/mirror/path", "must be a non-empty string"))
            if "access" in n:
                check_access(n["access"], f"{w}/access", errs)
            if "write" in n:
                wr = n["write"]
                if not isinstance(wr, list) or not all(is_str(x) for x in wr):
                    errs.append((f"{w}/write", "must be a list of non-empty strings"))
    if "relations" in d:
        rel = d["relations"]
        if not isinstance(rel, list):
            errs.append(("/relations", "must be a list"))
        else:
            for i, r in enumerate(rel):
                w = f"/relations/{i}"
                if check_keys(r, w, {"from", "to", "type", "description"}, ["from", "to", "type"], errs):
                    for k in ("from", "to"):
                        if k in r:
                            check_id(r[k], f"{w}/{k}", errs)
                    if "type" in r and not is_str(r["type"]):
                        errs.append((f"{w}/type", "must be a non-empty string"))
                    if "description" in r and not isinstance(r["description"], str):
                        errs.append((f"{w}/description", "must be a string"))
    if "overlays" in d:
        o = d["overlays"]
        if check_keys(o, "/overlays", {"nodes", "local_paths"}, [], errs):
            if "nodes" in o:
                on = o["nodes"]
                if not isinstance(on, dict):
                    errs.append(("/overlays/nodes", "must be a mapping"))
                else:
                    for k, v in on.items():
                        check_id(k, f"/overlays/nodes/{k}", errs)
                        if check_keys(v, f"/overlays/nodes/{k}", {"path"}, [], errs) and "path" in v and not is_str(v["path"]):
                            errs.append((f"/overlays/nodes/{k}/path", "must be a non-empty string"))
            if "local_paths" in o:
                lp = o["local_paths"]
                if not isinstance(lp, dict):
                    errs.append(("/overlays/local_paths", "must be a mapping"))
                else:
                    for k, v in lp.items():
                        check_id(k, f"/overlays/local_paths/{k}", errs)
                        if not is_str(v):
                            errs.append((f"/overlays/local_paths/{k}", "must be a non-empty string"))
    if "profiles" in d:
        p = d["profiles"]
        if check_keys(p, "/profiles", {"enabled"}, [], errs) and "enabled" in p:
            if not isinstance(p["enabled"], list) or not all(is_str(x) for x in p["enabled"]):
                errs.append(("/profiles/enabled", "must be a list of non-empty strings"))
    return errs


# ----------------------------------------------------------------------- main

def layout_refs(value):
    for item in value if isinstance(value, list) else [value]:
        if isinstance(item, str):
            yield item, True
        elif isinstance(item, dict) and isinstance(item.get("path"), str):
            yield item["path"], item.get("access", "read-write") != "read-only"


def validate_text(text: str) -> tuple[list[tuple[str, str]], object]:
    """Return (errors, parsed document). Used by the AAP repo's CI as well."""
    try:
        data = parse_yaml(text)
    except YamlError as error:
        return [("/", f"{error}")], None
    return schema_errors(data), data


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("map", nargs="?", default=".aap/map.yaml")
    ap.add_argument("--root", help="workspace root for path checks (default: parent of .aap/, else map dir)")
    args = ap.parse_args()
    map_path = Path(args.map)
    if not map_path.is_file():
        print(f"SETUP_ERROR: map not found: {map_path}", file=sys.stderr)
        raise SystemExit(2)
    text = map_path.read_text(encoding="utf-8")
    errors, data = validate_text(text)
    if errors:
        print("VALIDATION_FAILED")
        for pointer, message in errors:
            print(f"- path: {pointer or '/'} | message: {message[:200]}")
        raise SystemExit(1)

    here = map_path.resolve().parent
    root = Path(args.root) if args.root else (here.parent if here.name == ".aap" else here)
    warnings: list[str] = []
    for key, value in (data.get("layout") or {}).items():
        entries = list(layout_refs(value))
        for path, _ in entries:
            if not (root / path).exists():
                warnings.append(f"layout.{key}: '{path}' does not exist on disk (fine if intended, otherwise fix or drop)")
        if entries and not any(w for _, w in entries):
            warnings.append(f"layout.{key}: no writable entry, agents will fail closed on durable writes")
    seen: set[str] = set()
    for i, node in enumerate(data.get("nodes") or []):
        if node["id"] in seen:
            warnings.append(f"nodes[{i}]: duplicate id '{node['id']}'")
        seen.add(node["id"])
        if "path" in node and not (root / node["path"]).exists():
            warnings.append(f"nodes[{i}] ({node['id']}): path '{node['path']}' does not exist on disk")
        if "description" not in node:
            warnings.append(f"nodes[{i}] ({node['id']}): no description; say what is consulted there and when")

    def bad(v) -> bool:
        return isinstance(v, str) and (v.startswith(("/", "~", "\\")) or re.match(r"^[A-Za-z]:", v) is not None
                                      or "\\" in v or ".." in v.split("/"))

    cands = [("self.path", (data.get("self") or {}).get("path"))]
    for i, node in enumerate(data.get("nodes") or []):
        cands += [(f"nodes[{i}].path", node.get("path")), (f"nodes[{i}].map.path", (node.get("map") or {}).get("path"))]
    for name, v in cands:
        if bad(v):
            warnings.append(f"{name}: '{v}' must be workspace-relative (no absolute, '~', backslash or '..'); machine paths belong in map.local.yaml")
    review = [n + 1 for n, line in enumerate(text.splitlines()) if re.search(r"#\s*REVIEW:", line)]
    print("VALIDATION_SUCCESS")
    for w in warnings:
        print(f"WARN {w}")
    print(f"REVIEW_MARKERS {len(review)}" + (f" (lines {', '.join(map(str, review))})" if review else ""))


if __name__ == "__main__":
    main()
