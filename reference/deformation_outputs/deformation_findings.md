# NHTSA Metadata-based Deformation Analysis

## 1. Executive Summary
- Source DB: `D:\vscode\nhtsa_metadata\data\full_2011plus_metadata_only_refresh_2026-05-03.sqlite`
- Target subject vehicle rows: `1944`
- A/B profile-capable rows: `1705`
- Max-only rows: `206`
- Delta-only rows: `2`
- Excluded or placeholder rows: `31`
- Quality-tier total check: `1705 + 206 + 2 + 31 = 1944`.
- Phase 2 targeted corrections prevent max-only or excluded rows from being interpreted as zero-crush profile rows.
- C_MaxOnly rows retain CRHDST-based max-only features where valid, but profile-derived mean/rms/area features are stored as NULL.
- D_DeltaOnly and X_Exclude rows are retained for auditability but are not profile-eligible.
- Negative DPD values are flagged rather than automatically discarded, because the source field format permits signed DPD values.
- Sensitivity summaries are reported for signed, clipped-to-zero, and negative-row-excluded profile calculations.

## Goal Questions Answered
- Q1. Target subject vehicle rows total `1944행`. Family counts are frontal_barrier=674, side=625, side_impactor=603, rear=42.
- Q2. A/B profile-capable rows total `1705행`. Rear family has A/B `14`행, X `28`행, and rear-damage high-confidence subset `8`행.
- Q3. DPD-based `C_mean`, `C_profile_max`, `A_crush_2d`, `asymmetry`, `centroid_norm` are profile-derived and reported only for profile-eligible rows.
- Q4. `CRHDST < DPD max - 50mm` engineering inconsistency candidates are frontal_barrier=13, side=16, side_impactor=1, rear=0. Total `30`, A/B `28`, X/audit-only `2`.
- Q5. AX/BX frontal structural delta is a moderate supplemental validation feature for DPD mean crush: Pearson r=0.436, n=669. It does not replace DPD/CRHDST.
- Q6. `VEHLEN/VEHWID` normalization and `VEHTWT * speed^2` based `KE_proxy` are severity proxies only.
- Q7. Rear family profile-capable rows are separated from the rear-damage high-confidence subset using a conservative PDOF/VDI heuristic.
- Q8. Audit-only non-target family rows total `2141` and are not interpreted with the target-family DPD profile model.

## 2. Data Scope
- Source file before: size=2649182208, mtime_ns=1777808409905223600
- Source file after: size=2649182208, mtime_ns=1777808409905223600
- Source DB was opened with SQLite `PRAGMA query_only = ON` and was not modified.
- Analysis families: `frontal_barrier`, `side`, `side_impactor`, `rear`.
- Audit-only families include rollover, sled, static airbag, ADAS, pedestrian, and other non-crush-test families.

## 3. Field Basis and Methodology
- DPD profile reconstruction uses `DPD1~DPD6`, `LENCNT`, and `DAMDST`.
- `CRHDST` is used as the maximum static crush anchor.
- `AX/BX` deltas are computed as `BXn - AXn` and interpreted by family.
- Numeric zero is preserved. NULL and blank strings are treated as missing.
- VDI blank or `0` is unusable; 7-character nonzero VDI is used for grouping and sanity checks.

## 4. Data Quality Results
| family | subject rows | A | B | C | D | X | comment |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| frontal_barrier | 674 | 635 | 35 | 0 | 2 | 2 | sufficient profile sample for family-level descriptive comparison |
| side | 625 | 332 | 145 | 148 | 0 | 0 | sufficient profile sample for family-level descriptive comparison |
| side_impactor | 603 | 544 | 0 | 58 | 0 | 1 | sufficient profile sample for family-level descriptive comparison |
| rear | 42 | 7 | 7 | 0 | 0 | 28 | limited rear family subset; split high-confidence rear damage before interpretation |

## 5. Deformation Feature Results
| family | C_mean_norm median | C_mean_norm IQR | C_max_norm median | A_crush_norm median |
| --- | ---: | ---: | ---: | ---: |
| frontal_barrier | 0.0872798 | 0.0264133 | 0.100781 | 0.0657683 |
| side | 0.0654455 | 0.0429032 | 0.187368 | 0.0254754 |
| side_impactor | 0.0674299 | 0.0263019 | 0.112505 | 0.0348025 |
| rear | 0.0401856 | 0.0573375 | 0.0533186 | 0.0188475 |

## 6. Family-specific Findings
### frontal_barrier
- Profile-capable rows: `670`; excluded rows: `2`.
- This family has enough A/B rows for descriptive family-level analysis.
- CRHDST < DPD max - 50mm cases: `13`.
### side
- Profile-capable rows: `477`; excluded rows: `0`.
- This family has enough A/B rows for descriptive family-level analysis.
- CRHDST < DPD max - 50mm cases: `16`.
### side_impactor
- Profile-capable rows: `544`; excluded rows: `1`.
- This family has enough A/B rows for descriptive family-level analysis.
- CRHDST < DPD max - 50mm cases: `1`.
### rear
- Profile-capable rows: `14`; excluded rows: `28`.
- Rear family includes A/B profile-capable rows, but the rear-damage high-confidence subset is narrower after PDOF/VDI direction screening.
- Rear family A/B rows: `14`; rear-damage high-confidence subset: `8`.
- CRHDST < DPD max - 50mm cases: `0`.

## 7. AX/BX Supplemental Analysis
AX/BX frontal structural delta is a moderate supplemental validation feature for DPD mean crush, with Pearson r=0.436 over n=669. AX/BX is not a replacement for DPD/CRHDST. Side and rear AX/BX outputs are retained as supplemental asymmetry or length-shortening signals, not direct lateral/rear crush depth.

## 8. Speed and Vehicle-size Adjusted Analysis
frontal_barrier: log(KE_proxy+1) vs C_mean_norm Pearson r=0.380, n=670; side: log(KE_proxy+1) vs C_mean_norm Pearson r=-0.029, n=477; side_impactor: log(KE_proxy+1) vs C_mean_norm Pearson r=-0.070, n=544; rear: log(KE_proxy+1) vs C_mean_norm Pearson r=-0.101, n=14. KE_proxy is used only as a test severity proxy.

## 9. Outlier and Case Review
- Outlier/audit case rows written: `2029`.
- CRHDST-DPD disagreement total rows: `30`.
- Core A/B disagreement rows: `28`.
- Audit-only/X disagreement rows: `2`.
- These rows are treated as engineering inconsistency candidates, not simple statistical outliers.
- Engineering inconsistency candidates, statistical outliers, and audit-only exclusions are written to separate Phase 2 files.
- `deformation_outlier_cases.csv` is retained for backward compatibility, but final interpretation uses anomaly summary, engineering inconsistency, and statistical outlier outputs.

## 10. Limitations
- Metadata can reconstruct a 2D crush profile proxy, not a full 3D deformation shape.
- `KE_proxy` is a severity proxy only, not absorbed energy.
- VDI is not fully decoded into SAE J224 CDC components in this phase.
- Rear rows remain sparse and require case-level review before broad modeling.
- The rear-damage high-confidence subset is based on a conservative PDOF/VDI direction heuristic until full CDC decoding is available.

## 11. Recommendations
- Promote `LENCNT`, `AX/BX`, `VEHCG`, `CRBANG`, `CARANG`, `VEHOR`, `BMPENGD`, `SILENGD`, and `APLENGD` into canonical analysis fields in the upstream catalog.
- Add CDC/SAE J224 decoding before using VDI as more than a grouping/sanity variable.
- Keep rear analysis as descriptive case review unless additional high-confidence rear-damage rows are collected.

## Figures
- `figures/fig_01_family_quality_tier_counts.png`: Quality tier counts; subject target-family rows only.
- `figures/fig_02_crhdst_distribution_by_family.png`: CRHDST; A/B/C rows when available, rear is limited.
- `figures/fig_03_c_mean_norm_distribution_by_family.png`: C_mean_norm; A/B/C rows when available, rear is limited.
- `figures/fig_04_speed_vs_c_mean_norm_by_family.png`: A/B rows only; speed uses closingSpeed then vehicleSpeed/VEHSPD fallback.
- `figures/fig_05_lencnt_norm_distribution_by_family.png`: L_norm; A/B/C rows when available, rear is limited.
- `figures/fig_06_asymmetry_distribution_by_family.png`: asymmetry; A/B/C rows when available, rear is limited.
- `figures/fig_07_dpd_profile_examples_frontal.png`: frontal_barrier A/B profile examples using normalized s.
- `figures/fig_08_dpd_profile_examples_side.png`: side A/B profile examples using normalized s.
- `figures/fig_09_rear_valid_case_profiles.png`: rear A/B profile examples using normalized s.
- `figures/fig_10_axbx_delta_vs_dpd_frontal.png`: Frontal A/B rows; AX/BX structural delta is supplemental, not DPD replacement.
