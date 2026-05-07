CSV ?= data/source/side_loadcell_filtered_tests.csv
SQLITE ?= data/source/nhtsa_gui.sqlite
COHORT ?= data/processed/side_pole_vtp_cohort.csv
EXCLUSIONS ?= data/processed/excluded_tests.csv
ARTIFACT_DIR ?= artifacts/harness
REPORT_DIR ?= reports

validate:
	mkdir -p $(ARTIFACT_DIR)
	python .harness/scripts/validate_baseline.py --csv $(CSV) --sqlite $(SQLITE) --out $(ARTIFACT_DIR)/baseline_validation.json

cohort:
	mkdir -p data/processed $(ARTIFACT_DIR)
	python .harness/scripts/build_cohort.py --csv $(CSV) --out $(COHORT) --exclusions $(EXCLUSIONS) --summary $(ARTIFACT_DIR)/cohort_summary.json

profile:
	mkdir -p $(ARTIFACT_DIR)
	python .harness/scripts/profile_metadata.py --cohort $(COHORT) --out $(ARTIFACT_DIR)/metadata_profile.json

readiness:
	mkdir -p $(REPORT_DIR)
	python .harness/scripts/make_readiness_report.py --baseline $(ARTIFACT_DIR)/baseline_validation.json --cohort $(ARTIFACT_DIR)/cohort_summary.json --profile $(ARTIFACT_DIR)/metadata_profile.json --out $(REPORT_DIR)/project_readiness_report.md

all: validate cohort profile readiness
