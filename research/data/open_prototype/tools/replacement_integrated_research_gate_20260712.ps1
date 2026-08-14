# Runs the three 2026-07-12 replacement-branch operations end to end and refuses to
# report success unless each one landed exactly as expected. It calls the Vector-4
# 158-806 / Phyt source-family gate (node), the P050 / local-220 strict source gate
# (python), and one local from-scratch micro language model through
# "ivcslm run-matrix" against slm\configs\ivc_local_integrated.json, writing model
# runs to $ModelOutputDir (E:\ivc_slm_runs when the E: drive exists, otherwise a
# folder under LOCALAPPDATA). It then reads the two gate summary JSONs and the model
# run's completion.json and summary.json and throws if the Vector-4 decision is not
# the closed/not-claim-eligible one, if the P050 outcome is not PARK, if the matrix
# ran anything other than the one planned run, if it hit the runtime guard, if the
# held-out evaluation produced no masked positions or no hypothesis-family holdout
# records, or if the model did not start from random_initialization. Those checks
# exist because a gate that silently changes its verdict, or a model that leaks its
# answer through pretrained weights or an unheld family, would look like a clean run
# while proving nothing. On success it writes
# reports\replacement_integrated_research_gate_20260712_summary.json holding the two
# decisions, the model metrics, the current git commit and branch, and SHA-256
# hashes of the three input summaries. Passing means the instrument executed and two
# annotations are closed; it promotes no model metric, crosswalk, sign meaning, or
# reading, and every claim ledger increment stays 0.

param(
    [string]$PythonExe = 'C:\Users\Acer\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe',
    [string]$ModelOutputDir = ''
)

$ErrorActionPreference = 'Stop'
$repoRoot = (Resolve-Path (Join-Path $PSScriptRoot '..\..\..\..')).Path
$reports = Join-Path $repoRoot 'research\data\open_prototype\reports'
$v4Runner = Join-Path $PSScriptRoot 'vector4_158806_source_family_gate_20260712.mjs'
$p050Runner = Join-Path $PSScriptRoot 'replacement_p050_local220_strict_fish_family_source_gate_20260712.py'
$localConfig = Join-Path $repoRoot 'slm\configs\ivc_local_integrated.json'

if (-not (Test-Path -LiteralPath $PythonExe -PathType Leaf)) {
    throw "Python runtime does not exist: $PythonExe"
}
if (-not $ModelOutputDir) {
    $ModelOutputDir = if (Test-Path -LiteralPath 'E:\') {
        'E:\ivc_slm_runs'
    } else {
        Join-Path $env:LOCALAPPDATA 'ivc_slm_runs'
    }
}
New-Item -ItemType Directory -Force -Path $ModelOutputDir | Out-Null

Push-Location $repoRoot
try {
    & node $v4Runner
    if ($LASTEXITCODE -ne 0) { throw "Vector-4 source-family gate exited $LASTEXITCODE" }

    & $PythonExe $p050Runner
    if ($LASTEXITCODE -ne 0) { throw "P050/local-220 gate exited $LASTEXITCODE" }

    $env:IVCSLM_OUTPUT_DIR = $ModelOutputDir
    $modelLog = @(& $PythonExe -m ivcslm run-matrix --config $localConfig 2>&1)
    if ($LASTEXITCODE -ne 0) {
        $modelLog | ForEach-Object { Write-Host $_ }
        throw "Local substantive SLM experiment exited $LASTEXITCODE"
    }
    $modelLog | ForEach-Object { Write-Host $_ }
    $runRootText = [string]$modelLog[-1]
    $runRoot = [System.IO.Path]::GetFullPath($runRootText.Trim())
    if (-not (Test-Path -LiteralPath $runRoot -PathType Container)) {
        throw "SLM runner did not return a run directory: $runRootText"
    }

    $v4SummaryPath = Join-Path $reports 'vector4_158806_source_family_gate_20260712_summary.json'
    $p050SummaryPath = Join-Path $reports 'replacement_p050_local220_strict_fish_family_source_gate_20260712_summary.json'
    $completionPath = Join-Path $runRoot 'completion.json'
    foreach ($required in @($v4SummaryPath, $p050SummaryPath, $completionPath)) {
        if (-not (Test-Path -LiteralPath $required -PathType Leaf)) { throw "Integrated output missing: $required" }
    }
    $v4 = Get-Content -Raw -LiteralPath $v4SummaryPath | ConvertFrom-Json
    $p050 = Get-Content -Raw -LiteralPath $p050SummaryPath | ConvertFrom-Json
    $completion = Get-Content -Raw -LiteralPath $completionPath | ConvertFrom-Json

    if ($v4.decision -ne 'closed_not_claim_eligible_support_below_floor_source_independence_unresolved') {
        throw "Unexpected Vector-4 decision: $($v4.decision)"
    }
    if ($p050.outcome -ne 'PARK') { throw "Unexpected P050 outcome: $($p050.outcome)" }
    if ([int]$completion.completed_runs -ne 1 -or [int]$completion.planned_runs -ne 1) {
        throw "Local model matrix was not the one planned substantive run."
    }
    if ([bool]$completion.stopped_for_runtime_guard) { throw "Local model run hit the runtime guard." }
    $modelSummaryPath = Join-Path $runRoot ($completion.run_ids[0] + '\summary.json')
    $model = Get-Content -Raw -LiteralPath $modelSummaryPath | ConvertFrom-Json
    if ([int]$model.masked_token.positions -le 0) { throw "Model held-out evaluation produced no positions." }
    if ([int]$model.forced_hypothesis_holdout_records -le 0) {
        throw "The hypothesis-family holdout did not place any records in test."
    }
    if ($model.initialization.policy -ne 'random_initialization') {
        throw "The local from-scratch run did not start from random initialization."
    }

    $integratedSummaryPath = Join-Path $reports 'replacement_integrated_research_gate_20260712_summary.json'
    $integrated = [ordered]@{
        date = '2026-07-12'
        status = 'pass_integrated_execution_and_evidence_boundaries'
        substantive_operations = @(
            'closed the 158-806 / Phyt queue item by support/source/form-motif adjudication',
            'parked the strict local-220 / Mayig-P050 bridge on unresolved source detail',
            'trained and exhaustively evaluated one leakage-blocked random-init micro SLM'
        )
        vector4 = [ordered]@{
            decision = $v4.decision
            exact_text_families = $v4.exact_text_families
            conservative_form_motif_sensitivity_strata = $v4.conservative_form_motif_sensitivity_strata
            summary = 'research/data/open_prototype/reports/vector4_158806_source_family_gate_20260712_summary.json'
        }
        p050_local220 = [ordered]@{
            outcome = $p050.outcome
            same_position_source_bound = $p050.counts.same_position_source_bound
            strict_identity_usable = $p050.counts.strict_identity_usable
            summary = 'research/data/open_prototype/reports/replacement_p050_local220_strict_fish_family_source_gate_20260712_summary.json'
        }
        local_slm = [ordered]@{
            run_root = $runRoot
            run_id = $model.run_id
            parameter_count = $model.parameter_count
            forced_hypothesis_holdout_records = $model.forced_hypothesis_holdout_records
            test_records = $model.records.test
            test_positions = $model.masked_token.positions
            masked_nll = $model.masked_token.mean_negative_log_likelihood
            masked_top1 = $model.masked_token.top1
            masked_top5 = $model.masked_token.top5
            multiclass_brier = $model.masked_token.multiclass_brier
            stored_order_win_share = $model.directionality.stored_win_share
            authentic_over_reversed_share = $model.corruption_ranking.authentic_over_reversed_share
            elapsed_seconds = $model.elapsed_seconds
            estimated_compute_cost_usd = $completion.estimated_compute_cost_usd
        }
        claim_ledger_increment = [ordered]@{
            translations = 0
            phonetic_values = 0
            sign_meanings = 0
            language_identification = 0
            structural_findings = 0
            external_anchors = 0
        }
        evidence_boundary = 'Execution success validates the instrument and closes two annotations; it does not promote a model metric, crosswalk, sign meaning, or reading.'
        git = [ordered]@{
            commit = (git rev-parse HEAD).Trim()
            branch = (git branch --show-current).Trim()
        }
        output_hashes = [ordered]@{
            vector4_summary = (Get-FileHash -Algorithm SHA256 -LiteralPath $v4SummaryPath).Hash.ToLowerInvariant()
            p050_summary = (Get-FileHash -Algorithm SHA256 -LiteralPath $p050SummaryPath).Hash.ToLowerInvariant()
            model_summary = (Get-FileHash -Algorithm SHA256 -LiteralPath $modelSummaryPath).Hash.ToLowerInvariant()
        }
    }
    $integrated | ConvertTo-Json -Depth 12 | Set-Content -LiteralPath $integratedSummaryPath -Encoding utf8
    Write-Host "Integrated research gate complete: $integratedSummaryPath"
} finally {
    Pop-Location
}
