# nhtsa_metadata_side_loadcell

Side/load-cell analysis workspace split from `D:\vscode\nhtsa_metadata_deformation`.

## Imported Databases

- `data/refactor_validation_filter_ready_2026-05-07.sqlite`
  - Source: `D:\vscode\nhtsa_metadata\data\refactor_validation_filter_ready_2026-05-07.sqlite`
  - Purpose: full 2011+ metadata DB with load-cell classification read model.
- `data/deformation_features.sqlite`
  - Source: `D:\vscode\nhtsa_metadata_deformation\data\deformation_features.sqlite`
  - Purpose: derived MDCA deformation features.
- `data/deformation_review.sqlite`
  - Source: `D:\vscode\nhtsa_metadata_deformation\outputs\deformation_review.sqlite`
  - Purpose: compact deformation review DB.
- `data/side_loadcell_seed.sqlite`
  - Purpose: small derived seed DB for side/load-cell overlap summaries and test list.
- `data/side_pole_vehicle_specs_2026-05-07.sqlite`
  - Source: `D:\vscode\nhtsa_metadata\data\refactor_validation_filter_ready_2026-05-07.sqlite`
  - Purpose: vehicle specifications for the 588 side-pole load-cell tests.
- `data/side_pole_analysis_ready_2026-05-07.sqlite`
  - Source scope: `data/side_loadcell_filtered_tests.csv`
  - Purpose: final 554-test analysis-ready DB with vehicle specs, channel inventory, QC, and download links.
- `data/side_pole_analysis_ready_2026-05-07.json`
  - Purpose: JSON export from the analysis-ready DB. Includes data package/report links only.

## Imported Reference Material

- `docs/deformation_source_db_contract.md`
- `docs/mdca_methodology.md`
- `docs/deformation_operations.md`
- `docs/NHTSA_side_impact_project_plan.docx`
- `reference/deformation_outputs/`
- `reference/deformation_review_bundle/`
- `reference/load_cell_classification/`

## Current Seed Scope

- Full metadata tests: 3,900
- Load-cell classified tests: 1,137
- Side-pole load-cell vehicle specification rows: 588
- Side-family load-cell overlap rows in seed DB: 589
- Final filtered side-pole analysis rows: 554
- Excluded filtered non-side-pole row: `15452`
- Excluded research rows: 34
- Deformation feature rows: 1,944
- Deformation profile points: 11,612

Default verification is local and read-only. No live NHTSA API call is required.

## Filtering Policy

Project-level filtering rules are in [docs/filtering_policy.md](docs/filtering_policy.md) and
are also written into `data/side_pole_analysis_ready_2026-05-07.sqlite` as
`signal_filter_policy`.

Summary:

| Physical quantity | Default filter |
|---|---|
| side pole load-cell individual force | CFC 60 |
| side pole load-cell total force | CFC 60 |
| VEHICLE CG acceleration | CFC 60 |
| velocity/displacement integration acceleration | CFC 180 |
| velocity/displacement result | CFC 180 |
| raw waveform | Preserve unfiltered |

## Build Analysis-Ready DB

```powershell
python scripts\build_side_pole_analysis_ready.py
```

Expected core counts:

- `analysis_tests`: 554
- `vehicle_specs`: 554
- `side_pole_load_cell_channels`: 4,432
- `vehicle_cg_acceleration_channels`: 1,662
- `download_links`: 52,938
- `waveform_download_links`: 2,756
- `report_download_links`: 581
- `signal_filter_policy`: 6
- `strict_full_vector_eligible`: 321
- `lateral_primary_eligible`: 348
