# Import Manifest

## Scope

This project was initialized as a side/load-cell analysis workspace split from
`D:\vscode\nhtsa_metadata_deformation`.

The imported assets preserve two surfaces:

1. Full metadata and load-cell classification evidence from `D:\vscode\nhtsa_metadata`.
2. Deformation feature and review outputs from `D:\vscode\nhtsa_metadata_deformation`.

## Imported Databases

| Local path | Source path | Bytes | Primary role |
|---|---:|---:|---|
| `data/refactor_validation_filter_ready_2026-05-07.sqlite` | `D:\vscode\nhtsa_metadata\data\refactor_validation_filter_ready_2026-05-07.sqlite` | 2,762,747,904 | Full 2011+ metadata DB with load-cell classification table |
| `data/deformation_features.sqlite` | `D:\vscode\nhtsa_metadata_deformation\data\deformation_features.sqlite` | 14,008,320 | Derived MDCA deformation feature DB |
| `data/deformation_review.sqlite` | `D:\vscode\nhtsa_metadata_deformation\outputs\deformation_review.sqlite` | 6,684,672 | Compact deformation review DB |
| `data/side_loadcell_seed.sqlite` | Generated locally from imported DBs | 1,425,408 | Focused side/loadcell and vehicle-spec seed DB |
| `data/side_pole_vehicle_specs_2026-05-07.sqlite` | `D:\vscode\nhtsa_metadata\data\refactor_validation_filter_ready_2026-05-07.sqlite` | 1,273,856 | Vehicle specifications for 588 side-pole load-cell tests |
| `data/side_pole_analysis_ready_2026-05-07.sqlite` | Generated from filtered tests, imported DBs, and metadata media links | 47,554,560 | Final 554-test analysis-ready DB |
| `data/side_pole_analysis_ready_2026-05-07.json` | Exported from `side_pole_analysis_ready_2026-05-07.sqlite` | 6,637,688 | Analysis-ready JSON export with compact download links |

## Source Selection

The deformation project contract points to
`D:\vscode\nhtsa_metadata\data\full_2011plus_metadata_only_refresh_2026-05-03.sqlite`.

For this side/load-cell workspace, the imported full metadata DB is instead the newer local
`refactor_validation_filter_ready_2026-05-07.sqlite` snapshot because it contains the
`barrier_load_cell_classification` read-model table while preserving the same core 2011+
metadata surfaces needed by the deformation workflow.

## Copied Reference Files

From `D:\vscode\nhtsa_metadata_deformation`:

- `docs/source_db_contract.md` -> `docs/deformation_source_db_contract.md`
- `docs/mdca_methodology.md`
- `docs/operations.md` -> `docs/deformation_operations.md`
- `docs/NHTSA_side_impact_project_plan.docx`
- `outputs/deformation/*` -> `reference/deformation_outputs/`
- `outputs/review_bundle/*` -> `reference/deformation_review_bundle/`

From `D:\vscode\nhtsa_metadata`:

- `docs/nhtsa_barrier_load_cell_classification_config_v2.2.3.json`
- `docs/nhtsa_barrier_load_cell_classification_final_v2.2.3_2026-05-03.md`
- `docs/phase_reports/stage_l_barrier_load_cell_db_integration_result.md`
- `src/nhtsa_metadata/services/barrier_load_cell_classifier.py`
- `tests/test_barrier_load_cell_classifier.py`

## Verification Snapshot

Copied metadata DB:

- `tests`: 3,900
- `vehicles`: 4,705
- `barriers`: 1,634
- `instrumentation_channels`: 471,566
- `deformation_measurements`: 47,050
- `barrier_load_cell_classification`: 1,137
- `barrier_load_cell_channel_map`: 0

Copied deformation feature DB:

- `deformation_features`: 1,944
- `deformation_profile_points`: 11,612
- `deformation_quality_flags`: 1,944

Copied deformation review DB:

- `deformation_vehicle_features`: 1,944
- `deformation_profile_points`: 11,612
- `deformation_quality_audit`: 4,705
- `deformation_family_summary`: 4
- `deformation_outlier_cases`: 2,041

Generated seed DB:

- `loadcell_classification_summary`: 7
- `loadcell_test_family_summary`: 3
- `side_loadcell_overlap_summary`: 3
- `side_loadcell_tests`: 589
- `side_pole_vehicle_specs`: 588
- `vehicle_spec_field_coverage`: 17

Generated vehicle specification DB:

- `vehicle_spec_import_manifest`: 7
- `side_pole_vehicle_specs`: 588
- `vehicle_spec_field_coverage`: 17

The 588 vehicle rows are one-to-one with the side-pole load-cell test list from
`data/side_pole_load_cell_channel_availability_2026-05-07.csv`. Each row preserves
`vehicles.raw_row_json` from the source DB and expands common vehicle specification fields such
as make, model, model year, body type, engine type, test weight, curb weight, length, width,
wheelbase, vehicle CG, and vehicle orientation.

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

## Seed DB Notes

`data/side_loadcell_seed.sqlite` is a convenience DB only. It does not replace the imported
source DBs.

It contains:

- `source_file_inventory`
- `loadcell_classification_summary`
- `loadcell_test_family_summary`
- `side_loadcell_overlap_summary`
- `side_loadcell_tests`
- `side_pole_vehicle_specs`
- `vehicle_spec_field_coverage`

The source DB remains the authority for raw metadata, barrier rows, and instrumentation
channels. The deformation feature DB remains the authority for derived MDCA feature rows.
