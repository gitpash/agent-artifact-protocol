# Invalid map fixtures

These files **must fail** `scripts/validate.py`. They document Core rejection cases.

| File | Why invalid |
|------|-------------|
| `internal-zone-without-path.yaml` | Internal zone missing `path` |
| `external-zone-without-remote.yaml` | `relation: external` without `remote` |
| `layout-absolute-path.yaml` | Layout path is absolute |
| `layout-dotdot.yaml` | Layout path contains `..` |
| `write-readonly.yaml` | `readonly` is not a write grant |

Do not copy these into real projects.
