# Agent 02 — Raw Time-History Ingestion

## 미션

NHTSA 원천 time-history 파일, 사진, 영상, PDF 리포트 등 분석 자산을 시험번호별로 수집·검증·색인화한다. 현재 SQLite의 `files`와 `instrumentation_channels`가 0건이므로 이 단계가 실제 신호 분석의 선행 조건이다.

## 입력

- `data/processed/side_pole_vtp_cohort.csv`
- NHTSA 시험번호별 raw time-history asset
- 사진/영상/PDF report asset

## 처리 절차

1. 시험번호별 asset URL 또는 로컬 파일 경로 inventory 작성
2. 다운로드 또는 수동 반입 파일의 checksum 기록
3. 파일 형식 분류: raw signal, report, image, video, unknown
4. test_no 단위 coverage 산출
5. channel header 파싱 가능 여부 표시
6. 누락 asset backlog 작성

## 산출물

- `data/processed/raw_asset_inventory.csv`
- `artifacts/harness/raw_asset_coverage.json`
- `artifacts/harness/raw_asset_backlog.md`

## raw_asset_inventory.csv 권장 컬럼

```text
test_no,asset_kind,file_role,source_url,local_path,file_ext,size_bytes,checksum_sha256,status,parser_hint,qa_notes
```

## 완료 조건

- 기본 코호트 554건 중 raw signal coverage가 정량화되어야 한다.
- 파일이 없어도 실패가 아니라 `missing`으로 기록한다.
- 특정 시험의 raw 파일이 없으면 해당 시험은 G3 이후 metrics 산출 대상에서 제외한다.
