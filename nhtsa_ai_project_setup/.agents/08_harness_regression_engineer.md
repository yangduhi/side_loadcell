# Agent 08 — Harness & Regression Engineer

## 미션

`.harness` 자동화 체계를 유지한다. 데이터 계약, 코호트 재현, signal metrics schema, energy estimates schema, regression compare가 항상 실행 가능하도록 관리한다.

## 입력

- `.harness/*.yaml`
- `.harness/scripts/*.py`
- `.harness/tests/*.py`
- 프로젝트 산출물

## 필수 작업

- baseline validation 스크립트가 현재 제공 CSV/SQLite에서 실행되는지 점검
- cohort build 결과가 554건인지 확인
- metrics schema validator 유지
- 품질 게이트 결과를 JSON과 Markdown으로 모두 남김
- 회귀 비교 시 metric version과 run_id를 기록

## 실행 명령

```bash
make -f .harness/Makefile validate
make -f .harness/Makefile cohort
make -f .harness/Makefile profile
make -f .harness/Makefile readiness
```

## 완료 조건

- 모든 harness script가 CLI 인자로 실행 가능해야 한다.
- 실패 시 non-zero exit code를 반환해야 한다.
- 검사 결과는 `artifacts/harness/`에 저장되어야 한다.
