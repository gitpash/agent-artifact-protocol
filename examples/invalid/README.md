# Invalid fixtures and anti-pattern teaching

## Schema / validator fixtures

These files **must fail** `scripts/validate.py`. They document Core rejection cases.

| File | Why invalid |
|------|-------------|
| `absolute-resource-path.yaml` | Layout path is absolute |
| `malformed-resource-ref.yaml` | `resourceRef` shape rejected by schema / path rules |
| `artifact-missing-id.md` | Required envelope field `id` is missing |

These fixtures cover seed-validator rejection only; cross-file rules remain outside the seed validator.

Do not copy these into real projects.

## Profile / disclosure anti-patterns (not schema fixtures)

The following notes teach **behavioral** anti-patterns. They are **not** Map v2 documents and are **not** expected to fail JSON Schema as maps — many are procedure mistakes, not invalid YAML maps.

| Doc | Anti-pattern |
|-----|----------------|
| [`anti-multi-stream-open.md`](./anti-multi-stream-open.md) | Opening every stream pack in one session |
| [`anti-recursive-preload.md`](./anti-recursive-preload.md) | Recursively preloading child maps / SPEC / catalogs at session start |

Correct profile shape: [`../stream-packs/`](../stream-packs/), cookbook [`../../cookbook/stream-packs.md`](../../cookbook/stream-packs.md), hub hops [`../../cookbook/hub-umbrella.md`](../../cookbook/hub-umbrella.md).
