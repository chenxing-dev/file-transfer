<#
Root-level quick start for Windows PowerShell
Usage:
  powershell -ExecutionPolicy Bypass -File .\start.ps1
Or double-click start.bat which will run this script.
#>

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

$Root = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $Root
Write-Host "[start] Project root: $Root"

function Get-Python {
  try { & py -V *>$null; if ($LASTEXITCODE -eq 0) { return 'py' } } catch {}
  try { & python -V *>$null; if ($LASTEXITCODE -eq 0) { return 'python' } } catch {}
  throw 'Python is not installed or not on PATH. Please install Python 3.'
}

$python = Get-Python
Write-Host "[start] Using Python: $python"

if (-not (Test-Path "$Root/venv")) {
  Write-Host "[start] Creating virtual environment..."
  & $python -m venv venv
  $venvCreated = $true
} else {
  $venvCreated = $false
}

Write-Host "[start] Activating virtual environment..."
. "$Root/venv/Scripts/Activate.ps1"

if ($venvCreated) {
  Write-Host "[start] Upgrading pip (first run)..."
  python -m pip install --upgrade --disable-pip-version-check pip wheel *> $null
}

# Install deps only when requirements changed
$ReqFile = Join-Path $Root 'requirements.txt'
$HashFile = Join-Path $Root 'venv/.requirements.sha256'
$ForceInstall = ($args -contains '--force-install')

if (Test-Path $ReqFile) {
  $currHash = (Get-FileHash -Algorithm SHA256 $ReqFile).Hash.ToLower()
  $oldHash = ''
  if (Test-Path $HashFile) {
    $oldHash = (Get-Content $HashFile -ErrorAction SilentlyContinue).Trim().ToLower()
  }

  if ($ForceInstall -or $venvCreated -or ($currHash -ne $oldHash)) {
    Write-Host "[start] Installing/updating Python dependencies..."
    # Quiet install, but still show errors if any
    pip install -r $ReqFile --disable-pip-version-check -q *> $null
    if ($LASTEXITCODE -ne 0) {
      pip install -r $ReqFile --disable-pip-version-check
    }
    Set-Content -NoNewline -Path $HashFile -Value $currHash
  } else {
    Write-Host "[start] Dependencies up to date; skipping install."
  }
}

Write-Host "[start] Running app..."
python app.py
