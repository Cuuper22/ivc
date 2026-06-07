param(
  [string]$Root = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
)

$ErrorActionPreference = 'Stop'

$manifestPath = Join-Path $Root 'evidence/tmp/002390x_3335_yajnadevam_repo_trace_20260531/repo/_git_history/objects/pack/pack-f09fc4a9f75467afad858ed3a2ffed85bce03448.pack.split/manifest.json'
$manifest = Get-Content -LiteralPath $manifestPath -Raw | ConvertFrom-Json
$outputPath = Join-Path $Root ($manifest.original_path -replace '/', [IO.Path]::DirectorySeparatorChar)
$splitDir = Join-Path $Root ($manifest.split_dir -replace '/', [IO.Path]::DirectorySeparatorChar)

if (Test-Path -LiteralPath $outputPath) {
  $existingHash = (Get-FileHash -LiteralPath $outputPath -Algorithm SHA256).Hash.ToLowerInvariant()
  if ($existingHash -eq $manifest.original_sha256) {
    Write-Output "Already reconstructed: $($manifest.original_path)"
    exit 0
  }
  throw "Output exists but hash does not match: $outputPath"
}

$out = [System.IO.File]::Create($outputPath)
try {
  foreach ($part in $manifest.parts) {
    $partPath = Join-Path $splitDir $part.name
    $partHash = (Get-FileHash -LiteralPath $partPath -Algorithm SHA256).Hash.ToLowerInvariant()
    if ($partHash -ne $part.sha256) {
      throw "Part hash mismatch: $partPath"
    }
    $bytes = [System.IO.File]::ReadAllBytes($partPath)
    $out.Write($bytes, 0, $bytes.Length)
  }
} finally {
  $out.Dispose()
}

$hash = (Get-FileHash -LiteralPath $outputPath -Algorithm SHA256).Hash.ToLowerInvariant()
if ($hash -ne $manifest.original_sha256) {
  throw "Reconstructed file hash mismatch: $outputPath"
}

Write-Output "Reconstructed $($manifest.original_path)"
