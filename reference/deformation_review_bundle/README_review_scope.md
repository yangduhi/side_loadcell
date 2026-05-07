# MDCA Review Bundle

이 패키지는 대용량 원본 CSV 전체를 먼저 전달하지 않고도
ChatGPT가 Phase 1 결과를 검토할 수 있도록 만든 검토용 bundle입니다.

## 핵심 수치
- Target subject vehicle rows: `1944`
- A/B profile-capable rows: `1705`
- Rear rows: `42`
- Rear A/B rows: `14`
- Target-family CRHDST-DPD disagreement rows:
  `30`
- AX/BX frontal Pearson r: `0.436` over `n=669`로 보고된 Phase 1 보조지표입니다.

## 포함 파일
- `manifest.json`: 원본 산출물별 row count, column count, sha256, 생성 정보
- `schema_columns.csv`: 산출물별 컬럼 구조, inferred dtype, 결측, unique, min/max
- `deformation_family_summary.csv`: family별 요약
- `deformation_findings.md`: Phase 1 원본 findings 보고서
- `deformation_vehicle_features_review_sample.csv`: family 균형 샘플
- `deformation_quality_audit_flags_only.csv`: flag가 있는 audit row
- `deformation_outlier_cases.csv`: 원본 outlier/audit case
- `deformation_statistical_outliers.csv`: 통계적 high normalized deformation case
- `deformation_engineering_inconsistencies.csv`: engineering flag case
- `rear_all_rows.csv`: rear 42행 전체
- `crhdst_dpd_disagreement_rows.csv`: target subject family CRHDST-DPD 불일치 row
- `frontal_axbx_validation_rows.csv`: frontal AX/BX 보조지표 검토용 row
- `side_imppnt_validation_rows.csv`: side/side_impactor IMPPNT 검토용 row

## 별도 생성 파일
- `deformation_review.sqlite`: 전체 CSV를 table로 적재한 SQLite 검토 DB입니다.
  1차 zip 검토 뒤 필요할 때 추가 전달하면 됩니다.

## 검토 요청 범위
1. quality tier A/B/C/D/X 판정이 타당한지
2. rear 42행 중 usable subset 판정이 맞는지
3. CRHDST-DPD 불일치 row 처리 방식이 맞는지
4. AX/BX frontal structural delta 산식과 해석이 타당한지
5. family별 normalized deformation feature 비교가 과해석인지
