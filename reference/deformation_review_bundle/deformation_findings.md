# NHTSA Metadata-based Deformation Analysis

## 1. Executive Summary
- Source DB: `D:\vscode\nhtsa_metadata\data\full_2011plus_metadata_only_refresh_2026-05-03.sqlite`
- Target subject vehicle rows: `1944`
- A/B profile-capable rows: `1705`
- Max-only rows: `206`
- Excluded or placeholder rows: `31`
- 정면 충돌은 profile 분석에 충분하다.
- 측면 및 side_impactor는 subject vehicle 분리 후 profile 분석 가능하다.
- 후방 충돌은 가능하지만 품질 필터를 통과한 제한적 subset에서만 분석한다.
- rollover/sled/static/ADAS/pedestrian은 동일 방식의 crush 분석 대상이 아니다.
- AX/BX는 정면에서 강한 보조지표이며, 측면/후방에서는 제한적 보조지표이다.

## Goal Questions Answered
- Q1. 분석 가능 데이터는 정면 `674행`, 측면 `625행`, side_impactor `603행`, 후방 `42행`의 subject feature row로 확보됐다.
- Q2. 정면/측면/side_impactor는 A/B profile row가 충분하지만, 후방은 A/B `14`행과 X `28`행으로 제한적이다.
- Q3. DPD 기반 `C_mean`, `C_profile_max`, `A_crush_2d`, `asymmetry`, `centroid_norm`을 A/B row에서 산출했다.
- Q4. `CRHDST < DPD max - 50mm` 불일치는 frontal_barrier=13, side=16, side_impactor=1, rear=0건이다.
- Q5. AX/BX는 frontal에서 DPD 평균 crush와 paired 비교가 가능하며 Pearson r=0.436, n=669; side/rear는 보조 flag와 제한적 delta로만 해석했다.
- Q6. `VEHLEN/VEHWID` 정규화와 `VEHTWT * speed^2` 기반 `KE_proxy`를 생성해 family별 normalized feature와 severity proxy correlation을 산출했다.
- Q7. 후방은 `CRHDST`, DPD, VDI, PDOF near 180, `BX1-AX1` 중 2개 이상 근거를 통과한 subset만 profile 분석 대상으로 둔다.
- Q8. rollover/sled/static/ADAS/pedestrian 등 audit-only row는 `2141`행이며, 동일한 DPD crush 축/손상면 전제가 맞지 않아 동일 방식의 crush 분석에서 제외했다.

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
| rear | 42 | 7 | 7 | 0 | 0 | 28 | limited rear subset; interpret descriptively after rear_low_confidence filter |

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
- Rear remains a limited descriptive subset; low-confidence rows are flagged.
- CRHDST < DPD max - 50mm cases: `0`.

## 7. AX/BX Supplemental Analysis
Frontal AX/BX structural delta has paired support with DPD mean crush: Pearson r=0.436 over n=669. Side and rear AX/BX outputs are retained as supplemental asymmetry or length-shortening signals, not direct lateral/rear crush depth.

## 8. Speed and Vehicle-size Adjusted Analysis
frontal_barrier: log(KE_proxy+1) vs C_mean_norm Pearson r=0.380, n=670; side: log(KE_proxy+1) vs C_mean_norm Pearson r=-0.029, n=477; side_impactor: log(KE_proxy+1) vs C_mean_norm Pearson r=-0.070, n=544; rear: log(KE_proxy+1) vs C_mean_norm Pearson r=-0.101, n=14. KE_proxy is used only as a test severity proxy.

## 9. Outlier and Case Review
- Outlier/audit case rows written: `2041`.
- Outliers include CRHDST-DPD disagreement, range flags, PDOF-family mismatch, rear low confidence, and family-level p95 normalized deformation cases.

## 10. Limitations
- Metadata can reconstruct a 2D crush profile proxy, not a full 3D deformation shape.
- `KE_proxy` is a severity proxy only, not absorbed energy.
- VDI is not fully decoded into SAE J224 CDC components in this phase.
- Rear rows remain sparse and require case-level review before broad modeling.

## 11. Recommendations
- Promote `LENCNT`, `AX/BX`, `VEHCG`, `CRBANG`, `CARANG`, `VEHOR`, `BMPENGD`, `SILENGD`, and `APLENGD` into canonical analysis fields in the upstream catalog.
- Add CDC/SAE J224 decoding before using VDI as more than a grouping/sanity variable.
- Keep rear analysis descriptive unless additional valid rear rows are collected.

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
