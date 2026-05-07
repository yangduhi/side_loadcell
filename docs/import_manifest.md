# Import Manifest

## Scope

This project was initialized as a side/load-cell analysis workspace split from
`D:\vscode\nhtsa_metadata_deformation`.

The retained assets preserve two surfaces:

1. The 554-test side/load-cell analysis scope from `data/side_loadcell_filtered_tests.csv`.
2. Metadata-derived side-pole load-cell and VEHICLE CG channel inventory needed before waveform analysis.

## Current Data Files

| Local path | Source path | Bytes | Primary role |
|---|---:|---:|---|
| `data/side_loadcell_filtered_tests.csv` | Existing filtered test scope | 142,178 | Authoritative filtered scope source |
| `data/side_pole_load_cell_channel_availability_2026-05-07.csv` | Existing side-pole availability export | 577,393 | Side-pole channel availability source |
| `data/side_pole_load_cell_and_acceleration_channel_names_2026-05-07.json` | Existing metadata-derived channel inventory | 30,162,047 | Channel inventory source |
| `data/side_pole_analysis_ready_2026-05-07.sqlite` | Generated from filtered tests, channel inventory, and external metadata DB media links | 47,554,560 | Final 554-test analysis-ready DB |
| `data/side_pole_analysis_ready_2026-05-07.json` | Exported from `side_pole_analysis_ready_2026-05-07.sqlite` | 6,637,674 | Analysis-ready JSON export with compact download links |

## Source Selection

The deformation project contract points to
`D:\vscode\nhtsa_metadata\data\full_2011plus_metadata_only_refresh_2026-05-03.sqlite`.

For this side/load-cell workspace, the full metadata DB is read from
`D:\vscode\nhtsa_metadata\data\refactor_validation_filter_ready_2026-05-07.sqlite`. The DB is not
copied into this project after cleanup.

## Removed Intermediate Material

The cleanup removed redundant local copies and old handoff/reference material:

- Local copied metadata DB: `data/refactor_validation_filter_ready_2026-05-07.sqlite`
- Deformation intermediate DBs: `data/deformation_features.sqlite`, `data/deformation_review.sqlite`
- Superseded seed DB: `data/side_loadcell_seed.sqlite`
- Superseded vehicle-spec export: `data/side_pole_vehicle_specs_2026-05-07.*`
- Empty raw/processed/derived folders
- `reference/` copied review/reference bundle

## Verification Snapshot

Generated analysis-ready DB:

- `analysis_tests`: 554
- `vehicle_specs`: 554
- `test_qc_summary`: 554
- `side_pole_load_cell_channels`: 4,432
- `vehicle_cg_acceleration_channels`: 1,662
- `download_links`: 52,938
- `download_link_summary`: 2,202
- `signal_filter_policy`: 6
- `excluded_tests`: 35

Views:

- `waveform_download_links`: 2,756 data-package URLs
- `report_download_links`: 581 report URLs
- `analysis_ready_view`: compact test/vehicle/QC join surface

The 554-row analysis scope is the intersection of `data/side_loadcell_filtered_tests.csv` and
the side-pole `side_pole_load_cell_8` availability surface. `15452` is retained only in
`excluded_tests` because it is an `advanced_11x16_176_full` wall load-cell row, not a side-pole
load-cell row. The 34 `research_other` availability rows are also retained only in
`excluded_tests`.

Generated analysis-ready JSON:

- Includes `analysis_tests`, `vehicle_specs`, QC summary, 4,432 side-pole load-cell channels,
  and 1,662 vehicle CG acceleration channels.
- Includes `signal_filter_policy` so downstream waveform processing can read the same filter
  policy as the SQLite DB.
- Includes only `data_package` and `report` download links.
- Full photo/video/other media links remain in the SQLite `download_links` table.

## Authority Notes

The external metadata DB remains the authority for raw metadata, barrier rows,
instrumentation channels, vehicle specs, and media/download links. This project keeps only the
filtered scope files and the generated analysis-ready SQLite/JSON outputs required for
side-pole load-cell analysis preparation.
