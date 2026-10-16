# Cookbook: done bar (optional profile)

> **Optional profile — not required for Orientation conformance.**  
> Core L0 remains: discoverable map only.

## Problem

Agents and humans claim “done,” “ship,” or “PR ready” when:

- orientation never happened  
- claims have no path / git / CI evidence  
- optional indexes failed silently  
- required checks are red  

A map does not encode session honesty. Without a shared bar, each turn invents its own exit criteria.

## Pattern: accept pack before done

A **done bar** (accept pack) is a small checklist file, often shared across stream packs, run **before** claiming completion.

Typical steps:

| Step | Intent |
|------|--------|
| **orient** | Map was read; active node / layout home stated when relevant |
| **evidence** | Factual claims cite paths, git, CI, or command output |
| **degrade** | Missing optional tools or indexes were named and degraded — not faked |
| **write-home** | Durable writes used layout write-home; no invented parallel roots |
| **checks** | When a PR or ship claim exists: pass / fail / skip(reason) for required checks |

**Rule:** do **not** claim PR-ready or ship-ready on red required checks. Evidence-free BLOCKER is not a substitute for investigation.

## Suggested shape (informative)

```yaml
id: accept-default
summary: Honesty bar shared across stream packs
steps:
  - id: orient
    check: Map was read this session; active node or layout home is stated when relevant
  - id: evidence
    check: Factual claims cite paths, git, or command output — not vibes
  - id: degrade
    check: Missing optional indexes or tools were degraded explicitly
  - id: write-home
    check: Durable writes used layout write-home rules
  - id: checks
    check: PR/ship claims report CI status pass/fail/skip(reason)
forbid:
  - Claiming PR-ready or ship-ready on red required checks
  - Evidence-free BLOCKER as a substitute for investigation
  - Treating this bar as Core L0 mandatory for map-only repos
```

## Where it lives

Often next to stream packs (local / frequently gitignored):

```text
.aap/local/streams/_accept-default.yaml
```

Index it from a local profile file if useful (see [`local-bootstrap.md`](./local-bootstrap.md)). Keep it **out** of committed Core `map.yaml` required fields.

## Samples and links

- Sample accept file: [`examples/stream-packs/streams/_accept-default.yaml`](../examples/stream-packs/streams/_accept-default.yaml)  
- Stream pack profile: [`stream-packs.md`](./stream-packs.md)  
- Profile samples hub: [`examples/stream-packs/`](../examples/stream-packs/)

## Evidence (lightweight)

Teams MAY record a short accept run (pass/fail/skip) under scratch for dogfood. That log is **local experiment material**, not Core. Do not invent a mandatory accept-artifact type.

## Runtime note

Harnesses MAY require walking the bar before “done.” That is **consumer/runtime policy**. Org CI gates remain org policy — teach them here as a profile, not as Map v2 law.

## Anti-patterns

- Shipping on red checks because “the diff looks fine”  
- Treating graph/index silence as proof nothing exists  
- Growing the L0 map with full QA playbooks  
- Requiring every Orientation-only repo to adopt an accept pack  
- Vendor-specific check tool names as if universal Core  

## See also

- [`stream-packs.md`](./stream-packs.md)  
- [`local-bootstrap.md`](./local-bootstrap.md)  
- [`what-not-to-copy.md`](./what-not-to-copy.md)  
