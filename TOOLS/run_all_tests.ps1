<#
.SYNOPSIS
  Lance tous les tests de l'académie (wrapper de TOOLS/run_all_tests.py) puis vérifie le manifeste.
.EXAMPLE
  .\TOOLS\run_all_tests.ps1
  .\TOOLS\run_all_tests.ps1 CH01_03
  .\TOOLS\run_all_tests.ps1 -Blender "G:\Apps\Blender\blender-5.4.0-windows-x64\blender.exe"
#>
param(
  [string]$Blender = "C:\Program Files\Blender Foundation\Blender 5.3\blender.exe",
  [Parameter(ValueFromRemainingArguments=$true)][string[]]$Filters
)
& python (Join-Path $PSScriptRoot "run_all_tests.py") --blender $Blender @Filters
$code = $LASTEXITCODE
& python (Join-Path $PSScriptRoot "check_manifest.py") --update-hashes
if ($LASTEXITCODE -ne 0) { $code = 1 }
if ($code -eq 0) { Write-Host "TOUS LES TESTS PASSENT" -ForegroundColor Green } else { Write-Host "ECHECS : voir ci-dessus" -ForegroundColor Red }
exit $code
