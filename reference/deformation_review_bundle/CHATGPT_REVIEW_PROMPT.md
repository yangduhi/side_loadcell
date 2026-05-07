# ChatGPT 검토 요청

첨부한 `mdca_review_bundle.zip`은 NHTSA metadata 기반 MDCA Phase 1
deformation/crush 분석 결과의 검토용 패키지입니다.

## 검토 목표
다음 판단이 데이터와 방법론 관점에서 타당한지 검토해주세요.

1. Phase 1 핵심 결과 요약의 타당성
   - target subject vehicle rows `1944`
   - A/B profile-capable rows `1705`
   - rear rows `42`
   - rear A/B rows `14`
   - AX/BX frontal structural delta와 DPD mean crush의 Pearson r=`0.436`
   - AX/BX 상관 분석 n=`669`
2. quality tier A/B/C/D/X 판정 기준과 flag 처리의 타당성
3. rear row를 제한적 descriptive subset으로만 해석하는 것이 적절한지
4. target subject family의 CRHDST-DPD disagreement row 처리 방식
5. normalized feature 기반 family 비교가 과해석인지 여부

## 먼저 볼 파일
1. `README_review_scope.md`
2. `manifest.json`
3. `schema_columns.csv`
4. `deformation_family_summary.csv`
5. `deformation_quality_audit_flags_only.csv`
6. `rear_all_rows.csv`
7. `crhdst_dpd_disagreement_rows.csv`
8. `frontal_axbx_validation_rows.csv`
9. `side_imppnt_validation_rows.csv`

## 검토 방식 요청
- 전체 CSV 재분석보다 manifest/schema/summary/flag/subset을 먼저 봐주세요.
- 불확실한 경우 필요한 추가 row subset 또는 SQLite query를 요청해주세요.
- 결론은 `타당`, `조건부 타당`, `수정 필요`, `판단 보류`로 구분해주세요.
- 방법론상 과해석 가능성과 추가 검증 지점을 분리해서 적어주세요.

## 참고
- 원본 산출물 위치: `D:\vscode\nhtsa_metadata_deformation\outputs\deformation`
- source DB: `D:\vscode\nhtsa_metadata\data\full_2011plus_metadata_only_refresh_2026-05-03.sqlite`
- 검토용 SQLite가 필요하면 `deformation_review.sqlite` 파일을 추가로 전달할 수 있습니다.
