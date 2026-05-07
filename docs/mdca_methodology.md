# MDCA Methodology

MDCA means Metadata-based Deformation & Crush Analysis.

## Measurement Layers

1. Crush profile: `DPD1~DPD6`, `LENCNT`, `DAMDST`
2. Maximum penetration: `CRHDST`
3. Pre/post dimension delta: `AX1~AX21`, `BX1~BX21`

`AX/BX` values are not treated as universal crush depth. They are family-specific support
features.

## Target Families

| family | profile axis | normal axis | default interpretation |
| --- | --- | --- | --- |
| `frontal_barrier` | `Y` | `X` | left-to-right frontal profile |
| `side` | `X` | `Y` | rear-to-front side profile |
| `side_impactor` | `X` | `Y` | subject vehicle rear-to-front side profile |
| `rear` | `Y` | `X` | left-to-right rear profile |

## DPD Point Handling

- `0` is retained as a valid boundary value.
- All-zero deformation bundles are treated as placeholders when `CRHDST`, `VDI`, and `AX/BX`
  deltas are also non-informative.
- If `LENCNT > 400`, six DPD points are expected.
- If `0 < LENCNT <= 400` and `DPD5 == 0` and `DPD6 == 0`, four points are used.
- If `LENCNT` is missing or zero, the profile is computed on normalized local coordinates.

## Feature Outputs

The builder writes three generated tables:

- `deformation_profile_points`
- `deformation_features`
- `deformation_quality_flags`

These tables are generated analysis artifacts. They can be deleted and rebuilt from the source DB.

