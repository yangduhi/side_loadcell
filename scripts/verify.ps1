param(
    [switch]$RebuildAnalysisReady
)

$ErrorActionPreference = "Stop"

$Root = Resolve-Path (Join-Path $PSScriptRoot "..")
Set-Location $Root

$Python = Join-Path $Root ".venv\Scripts\python.exe"
if (-not (Test-Path $Python)) {
    $Python = "python"
}

New-Item -ItemType Directory -Force -Path "artifacts\harness", "data\processed", "reports" | Out-Null

$SourceDb = $env:NHTSA_SIDE_LOADCELL_METADATA_DB_PATH
if (-not $SourceDb) {
    $SourceDb = "D:\vscode\nhtsa_metadata\data\refactor_validation_filter_ready_2026-05-07.sqlite"
}

function Invoke-PythonStep {
    param(
        [string]$Name,
        [string[]]$Arguments
    )
    Write-Host "== $Name"
    & $Python @Arguments
    if ($LASTEXITCODE -ne 0) {
        exit $LASTEXITCODE
    }
}

if ($RebuildAnalysisReady) {
    Invoke-PythonStep "rebuild analysis-ready DB" @(
        "scripts\build_side_pole_analysis_ready.py"
    )
}

Invoke-PythonStep "validate baseline" @(
    ".harness\scripts\validate_baseline.py",
    "--csv", "data\side_loadcell_filtered_tests.csv",
    "--sqlite", $SourceDb,
    "--analysis-ready", "data\side_pole_analysis_ready_2026-05-07.sqlite",
    "--out", "artifacts\harness\baseline_validation.json"
)

Invoke-PythonStep "build cohort" @(
    ".harness\scripts\build_cohort.py",
    "--csv", "data\side_loadcell_filtered_tests.csv",
    "--out", "data\processed\side_pole_vtp_cohort.csv",
    "--exclusions", "data\processed\excluded_tests.csv",
    "--summary", "artifacts\harness\cohort_summary.json"
)

Invoke-PythonStep "profile metadata" @(
    ".harness\scripts\profile_metadata.py",
    "--cohort", "data\processed\side_pole_vtp_cohort.csv",
    "--out", "artifacts\harness\metadata_profile.json"
)

Invoke-PythonStep "write readiness report" @(
    ".harness\scripts\make_readiness_report.py",
    "--baseline", "artifacts\harness\baseline_validation.json",
    "--cohort", "artifacts\harness\cohort_summary.json",
    "--profile", "artifacts\harness\metadata_profile.json",
    "--out", "reports\project_readiness_report.md"
)

Invoke-PythonStep "pytest harness" @(
    "-m", "pytest", ".harness\tests"
)
