# NHTSA 측면 충돌 분석 프로젝트 Readiness Report

- 생성 시각(UTC): 2026-05-07T04:01:38.604751+00:00
- Baseline status: `pass_with_known_blockers`
- Cohort status: `pass`
- 다음 게이트: `G1_raw_asset_inventory`

## 1. 코호트 요약

| 항목 | 값 |
|---|---:|
| CSV 원천 건수 | 555 |
| 권장 분석 코호트 | 554 |
| 제외 건수 | 1 |
| 기대 코호트 건수 | 554 |

기본 코호트 필터:

```text
{'crash_type_rule': 'side', 'test_config_code': 'VTP', 'test_config_label': 'VEHICLE INTO POLE', 'load_cell_barrier_family': 'side_pole_load_cell_barrier', 'load_cell_barrier_classification_id': 'side_pole_load_cell_8'}
```

하드 제외 시험번호: `['15452']`

## 2. Baseline 검증 결과

| Check | Status | Expected | Observed |
|---|---:|---:|---:|
| csv_required_columns | pass |  |  |
| csv_source_row_count | pass | 555 | 555 |
| csv_unique_test_no | pass | 555 | 555 |
| excluded_test_no_present | pass | ['15452'] | ['15452'] |
| recommended_cohort_count | pass | 554 | 554 |
| sqlite_required_tables | pass |  |  |
| sqlite_broader_side_pole_inventory | warn |  | 580 |

## 3. Known Blockers

- SQLite files table has 0 rows; raw asset inventory is not loaded.
- SQLite instrumentation_channels table has 0 rows; channel-level time-history metadata is not loaded.

## 4. Warnings

- SQLite injury_metrics table has 0 rows; occupant injury metrics are outside current baseline.
- SQLite intrusions table has 0 rows; intrusion validation is outside current baseline.
- SQLite VTP side_pole_load_cell_8 inventory count is 580, while filtered CSV recommended cohort is 554. Reconcile only if project scope changes.

## 5. 메타데이터 분포 요약

- 상위 제조사: FORD(62), TOYOTA(62), CHEVROLET(49), NISSAN(43), KIA(35), HYUNDAI(35), HONDA(29), MAZDA(18), JEEP(17), LEXUS(17), ACURA(16), VOLKSWAGEN(16)
- 상위 body style: UTILITY VEHICLE(243), FOUR DOOR SEDAN(154), 4 DOOR PICKUP(44), FIVE DOOR HATCHBACK(40), EXTENDED CAB PICKUP(22), TWO DOOR COUPE(17), MINIVAN(15), THREE DOOR HATCHBACK(5), TRUCK(3), STATION WAGON(3), VAN(2), PICKUP TRUCK(2)
- impact speed 요약: `{'count': 554, 'min': 30.76, 'p25': 32.08, 'median': 32.2, 'p75': 32.3175, 'max': 32.95, 'mean': 32.20530685920578}`
- test weight 요약: `{'count': 554, 'min': 993.0, 'p25': 1580.25, 'median': 1795.5, 'p75': 2111.0, 'max': 3311.0, 'mean': 1880.3393501805053}`
- width 요약: `{'count': 554, 'min': 1456.0, 'p25': 1785.0, 'median': 1836.0, 'p75': 1920.0, 'max': 2087.0, 'mean': 1853.1949458483755}`
- crush 요약: `{'count': 554, 'min': 149.0, 'p25': 313.0, 'median': 348.0, 'p75': 395.0, 'max': 699.0, 'mean': 354.87003610108303}`

## 6. 다음 작업

1. `data/processed/raw_asset_inventory.csv` 생성
2. 시험번호별 raw time-history 파일 확보
3. 로드셀 force channel과 차체 acceleration channel dictionary 작성
4. 단위·축·샘플링·time-zero 검증 후 signal metrics 산출
5. cell/zone/member mapping table 작성 및 engineering estimate confidence 부여

## 7. 보고서 반영 시 주의 문구

현재 SQLite에는 시계열 및 파일 관련 테이블이 비어 있으므로 실제 force-time, acceleration-time, impulse, ΔV, 부재별 energy는 raw time-history 확보 전까지 산출 완료로 표현하면 안 됩니다. 부재별 에너지 흡수량은 직접 계측값이 아니라 engineering estimate입니다.
