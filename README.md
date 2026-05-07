# nhtsa_metadata_side_loadcell

Side/load-cell analysis workspace split from `D:\vscode\nhtsa_metadata_deformation`.

## Source Inputs

- `D:\vscode\nhtsa_metadata\data\refactor_validation_filter_ready_2026-05-07.sqlite`
  - External source DB used by `scripts\build_side_pole_analysis_ready.py`.
  - Not copied into this project.
- `data/side_loadcell_filtered_tests.csv`
  - Authoritative 555-row filtered scope source.
- `data/side_pole_load_cell_channel_availability_2026-05-07.csv`
  - Side-pole availability surface used to keep 554 analysis rows and exclude `15452`.
- `data/side_pole_load_cell_and_acceleration_channel_names_2026-05-07.json`
  - Metadata-derived channel inventory source.

## Final Outputs

- `data/side_pole_analysis_ready_2026-05-07.sqlite`
  - Source scope: `data/side_loadcell_filtered_tests.csv`
  - Purpose: final 554-test analysis-ready DB with vehicle specs, channel inventory, QC, and download links.
- `data/side_pole_analysis_ready_2026-05-07.json`
  - Purpose: JSON export from the analysis-ready DB. Includes data package/report links only.

## Current Scope

- Full metadata tests: 3,900
- Load-cell classified tests: 1,137
- Final filtered side-pole analysis rows: 554
- Excluded filtered non-side-pole row: `15452`
- Excluded research rows: 34

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
