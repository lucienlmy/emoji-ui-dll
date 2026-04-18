$ErrorActionPreference = "Stop"
Set-StrictMode -Version Latest

$root = Split-Path -Parent $MyInvocation.MyCommand.Path
$sln = Join-Path $root "emoji_window.sln"
$outputDir = Join-Path $root "DLL"
$vswhere = Join-Path ${env:ProgramFiles(x86)} "Microsoft Visual Studio\Installer\vswhere.exe"

if (-not (Test-Path -LiteralPath $sln)) {
    throw "Solution not found: $sln"
}

if (-not (Test-Path -LiteralPath $vswhere)) {
    throw "vswhere not found: $vswhere"
}

$msbuild = & $vswhere -latest -requires Microsoft.Component.MSBuild -find "MSBuild\**\Bin\MSBuild.exe" | Select-Object -First 1
if (-not $msbuild) {
    throw "MSBuild not found"
}

New-Item -ItemType Directory -Path $outputDir -Force | Out-Null

$builds = @(
    @{
        Platform = "Win32"
        Source = Join-Path $root "bin\Win32\Release\emoji_window.dll"
        Target = Join-Path $outputDir "emoji_window_x86.dll"
    },
    @{
        Platform = "x64"
        Source = Join-Path $root "bin\x64\Release\emoji_window.dll"
        Target = Join-Path $outputDir "emoji_window_x64.dll"
    }
)

foreach ($build in $builds) {
    Write-Host "Building Release|$($build.Platform) ..."
    & $msbuild $sln /p:Configuration=Release /p:Platform=$($build.Platform) /m /v:minimal
    if ($LASTEXITCODE -ne 0) {
        exit $LASTEXITCODE
    }

    if (-not (Test-Path -LiteralPath $build.Source)) {
        throw "DLL not generated: $($build.Source)"
    }

    Copy-Item -LiteralPath $build.Source -Destination $build.Target -Force
}

$rootDll = Join-Path $root "emoji_window.dll"
Copy-Item -LiteralPath (Join-Path $outputDir "emoji_window_x64.dll") -Destination $rootDll -Force

Write-Host "OK:"
Write-Host "  $rootDll"
Write-Host "  $(Join-Path $outputDir 'emoji_window_x86.dll')"
Write-Host "  $(Join-Path $outputDir 'emoji_window_x64.dll')"
