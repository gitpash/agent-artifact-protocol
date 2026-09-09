# Invalid fixtures

These files **must fail** `scripts/validate.py`. They document Core rejection cases.

| File | Why invalid |
|------|-------------|
| `internal-zone-without-path.yaml` | Internal zone missing `path` |
| `external-zone-without-remote.yaml` | `relation: external` without `remote` |
| `layout-absolute-path.yaml` | Layout path is absolute |
| `layout-dotdot.yaml` | Layout path contains `..` |
| `write-readonly.yaml` | Write mode label is empty |
| `artifact-missing-id.md` | Required envelope field `id` is missing |

These fixtures cover schema-level rejection only; cross-file rules remain outside the seed validator.

Do not copy these into real projects.
