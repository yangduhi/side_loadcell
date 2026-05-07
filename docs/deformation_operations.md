# Operations

## Default Workflow

1. Confirm the source DB path in `.env.example` or local `.env`.
2. Run `source-summary` to check family and field coverage.
3. Run `build-features --limit 25` before a full build.
4. Run `build-features` without `--limit` to regenerate the derived SQLite DB.
5. Run `scripts\analyze_deformation_metadata.py --out outputs\deformation` for the full
   CSV/figure/report package.
6. Run `scripts\verify.ps1` and `.harness\run.ps1` before handoff.

## Source DB Policy

The source SQLite DB from `D:\vscode\nhtsa_metadata` is treated as read-only. This project writes
only its own generated analysis DB under `data\`, which is ignored by Git.

## Live Network Policy

This project does not need live NHTSA API calls for default development. All default commands use
the existing local SQLite catalog.
