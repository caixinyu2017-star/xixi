#!/usr/bin/env pwsh
# Windows install guardrail for CI (and local re-run with Windows PowerShell 5.1).
# Comments are ASCII-only on purpose: Windows PowerShell 5.1 parses scripts as GBK
# on zh-CN consoles and chokes on non-ASCII bytes (see PROGRESS R1.5).
#
# Checks, all against a throwaway fake HOME whose path CONTAINS A SPACE:
#   1. install.ps1 runs twice and links exactly 28 skills both times (idempotent).
#   2. Every linked skill dir is a reparse point whose target is the source repo skill.
#   3. A safe uninstall (cmd /c rmdir, no /s) removes the links WITHOUT deleting
#      through to the source: a source sentinel file and all 28 source SKILL.md
#      files must survive. If an unsafe uninstall ever deletes through the junction,
#      this assertion exits 1 and turns the build red.
# Exit 0 = all good; non-zero = a regression CI must catch.

param([string]$Repo = $PSScriptRoot)

$ErrorActionPreference = 'Stop'
$ExpectedSkills = 28

# Resolve repo root: this script lives at <repo>/.github/scripts/, so go up two.
$RepoRoot = (Resolve-Path (Join-Path $PSScriptRoot '..\..')).Path
$Installer = Join-Path $RepoRoot 'install.ps1'
if (-not (Test-Path -LiteralPath $Installer)) { Write-Error "install.ps1 not found at $Installer"; exit 2 }

# Fake HOME with a space in the path, to catch quoting bugs.
$tmpRoot = if ($env:RUNNER_TEMP) { $env:RUNNER_TEMP } else { $env:TEMP }
$fakeHome = Join-Path $tmpRoot 'light home with space'
if (Test-Path -LiteralPath $fakeHome) { & cmd.exe /c rmdir /s /q "`"$fakeHome`"" | Out-Null }
New-Item -ItemType Directory -Force -Path $fakeHome | Out-Null

$skillsDir = Join-Path $fakeHome '.claude\skills'
$failures = 0
function Fail($msg) { Write-Host "FAIL: $msg"; $script:failures++ }
function Pass($msg) { Write-Host "PASS: $msg" }

# Save and override HOME/USERPROFILE so install.ps1 targets the fake HOME.
$savedHome = $env:HOME; $savedUserProfile = $env:USERPROFILE
$env:HOME = $fakeHome; $env:USERPROFILE = $fakeHome

try {
  $psExe = if (Get-Command pwsh -ErrorAction SilentlyContinue) { 'pwsh' } else { 'powershell' }

  # --- 1. idempotency: run twice, expect 28 each time ---
  foreach ($attempt in 1, 2) {
    & $psExe -NoProfile -ExecutionPolicy Bypass -File $Installer -Client claude | Out-Null
    if ($LASTEXITCODE -ne 0) { Fail "install.ps1 attempt $attempt exited $LASTEXITCODE" }
    $linked = @(Get-ChildItem -Directory $skillsDir -Filter 'light-*' -ErrorAction SilentlyContinue |
                Where-Object { Test-Path (Join-Path $_.FullName 'SKILL.md') })
    if ($linked.Count -eq $ExpectedSkills) { Pass "attempt $attempt linked $ExpectedSkills skills" }
    else { Fail "attempt $attempt linked $($linked.Count), expected $ExpectedSkills" }
  }

  # --- 2. junction target points back at the source repo ---
  $sample = Join-Path $skillsDir 'light-research-ethics'
  $item = Get-Item -LiteralPath $sample -Force
  $isReparse = ($item.Attributes -band [IO.FileAttributes]::ReparsePoint) -ne 0
  if ($isReparse) { Pass "linked skill is a reparse point" } else { Fail "linked skill is not a reparse point" }
  $target = ($item.Target | Select-Object -First 1)
  $expectedTarget = Join-Path $RepoRoot 'skills\light-research-ethics'
  if ($target -and ((Resolve-Path $target).Path -eq (Resolve-Path $expectedTarget).Path)) {
    Pass "junction target resolves to source repo skill"
  } else { Fail "junction target '$target' != '$expectedTarget'" }

  # --- 3. safe uninstall must not delete through to the source ---
  $sentinel = Join-Path $RepoRoot 'skills\_R12_UNINSTALL_SENTINEL.tmp'
  Set-Content -LiteralPath $sentinel -Value 'do not delete through junction'
  $srcSkillCountBefore = @(Get-ChildItem -Directory (Join-Path $RepoRoot 'skills') -Filter 'light-*' |
                           Where-Object { Test-Path (Join-Path $_.FullName 'SKILL.md') }).Count
  foreach ($d in Get-ChildItem -Directory $skillsDir -Filter 'light-*') {
    & cmd.exe /c rmdir "`"$($d.FullName)`"" | Out-Null   # safe: no /s, removes link only
  }
  $sentinelOk = Test-Path -LiteralPath $sentinel
  $srcSkillCountAfter = @(Get-ChildItem -Directory (Join-Path $RepoRoot 'skills') -Filter 'light-*' |
                          Where-Object { Test-Path (Join-Path $_.FullName 'SKILL.md') }).Count
  Remove-Item -LiteralPath $sentinel -Force -ErrorAction SilentlyContinue
  if ($sentinelOk) { Pass "source sentinel intact after uninstall" } else { Fail "source sentinel DELETED THROUGH JUNCTION" }
  if ($srcSkillCountAfter -eq $srcSkillCountBefore -and $srcSkillCountAfter -ge $ExpectedSkills) {
    Pass "all source SKILL.md intact after uninstall ($srcSkillCountAfter)"
  } else { Fail "source SKILL.md count changed: $srcSkillCountBefore -> $srcSkillCountAfter" }
}
finally {
  $env:HOME = $savedHome; $env:USERPROFILE = $savedUserProfile
  if (Test-Path -LiteralPath $fakeHome) { & cmd.exe /c rmdir /s /q "`"$fakeHome`"" | Out-Null }
}

if ($failures -gt 0) { Write-Host "install_windows_check: $failures failure(s)"; exit 1 }
Write-Host "install_windows_check: all checks passed"; exit 0
