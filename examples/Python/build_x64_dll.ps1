$ErrorActionPreference = "Stop"

$root = Split-Path -Parent (Split-Path -Parent $PSScriptRoot)
$sln = Join-Path $root "emoji_window.sln"
$vswhere = "${env:ProgramFiles(x86)}\Microsoft Visual Studio\Installer\vswhere.exe"

if (-not (Test-Path $vswhere)) {
    Write-Error "vswhere not found: $vswhere"
}

$msbuild = & $vswhere -latest -requires Microsoft.Component.MSBuild -find "MSBuild\**\Bin\MSBuild.exe" | Select-Object -First 1
if (-not $msbuild) {
    Write-Error "MSBuild not found"
}

& $msbuild $sln /p:Configuration=Release /p:Platform=x64 /m /v:minimal
if ($LASTEXITCODE -ne 0) {
    exit $LASTEXITCODE
}

$dll = Join-Path $root "bin\x64\Release\emoji_window.dll"
if (-not (Test-Path $dll)) {
    Write-Error "DLL not generated: $dll"
}

$pythonDemoDll = Join-Path $root "examples\Python\emoji_window.dll"
try {
    Copy-Item $dll $pythonDemoDll -Force
} catch {
    Write-Warning "examples\\Python\\emoji_window.dll is locked by a running process; skip copying."
}

Write-Host "OK: $dll"
