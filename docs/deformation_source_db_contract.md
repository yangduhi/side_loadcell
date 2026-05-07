# Source DB Contract

## Input Database

Default source:

```text
D:\vscode\nhtsa_metadata\data\full_2011plus_metadata_only_refresh_2026-05-03.sqlite
```

The source database remains outside this project and is read-only from this project's point of
view.

## Tables Used

- `tests`: test-level conditions such as `test_no`, `impact_angle`, `closing_speed`,
  `offset_distance`, `test_configuration`, and `raw_row_json`.
- `vehicles`: vehicle-level dimensions and the raw vehicle metadata row.
- `test_classification`: family classification, including `test_family` and
  `classification_status`.
- `test_participants`: participant role, used to keep subject vehicles by default.
- `deformation_measurements`: canonical promoted deformation measurements. This is useful for
  coverage checks, but the first feature builder reads the richer `vehicles.raw_row_json` because
  it includes `LENCNT`, `AX/BX`, `VEHCG`, and engagement fields.

## Required Raw Vehicle Fields

Primary MDCA fields:

- `DPD1` to `DPD6`
- `LENCNT`
- `DAMDST`
- `CRHDST`

Secondary/support fields:

- `AX1` to `AX21`
- `BX1` to `BX21`
- `PDOF`
- `VDI`
- `VEHLEN`
- `VEHWID`
- `VEHTWT`
- `WHLBAS`
- `VEHCG`
- `SILENGD`
- `APLENGD`

## Current Source Observation

The checked source DB exposes promoted `deformation_measurements` for `VDI`, `PDOF`, `DPD1~DPD6`,
`DAMDST`, and `CRHDST`. Fields such as `LENCNT`, `AX/BX`, `VEHCG`, `SILENGD`, and `APLENGD` are
available through `vehicles.raw_row_json` for the deformation-bearing vehicle rows.
