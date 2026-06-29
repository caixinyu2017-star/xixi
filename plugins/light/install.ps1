#!/usr/bin/env pwsh
# Light installer (Windows / PowerShell)
# Links Light's 28 skills + shared knowledge bases into Claude Code and/or Codex.
# Usage:  pwsh install.ps1            # installs into both clients found
#         pwsh install.ps1 -Client claude
#         pwsh install.ps1 -Client codex

param(
  [ValidateSet('both','claude','codex')]
  [string]$Client = 'both'
)

$ErrorActionPreference = 'Stop'
$ExpectedSkills = 28
$Repo = $PSScriptRoot

function Link-Dir($link, $target) {
  if (Test-Path -LiteralPath $link) {
    $item = Get-Item -LiteralPath $link -Force
    if (($item.Attributes -band [IO.FileAttributes]::ReparsePoint) -eq 0) {
      throw "Refusing to overwrite non-link path: $link. Remove it manually if it is an old Light install target."
    }
    & cmd.exe /c rmdir "`"$link`"" | Out-Null
    if ($LASTEXITCODE -ne 0 -or (Test-Path -LiteralPath $link)) {
      throw "Failed to remove existing link: $link"
    }
  }
  New-Item -ItemType Junction -Path $link -Target $target | Out-Null
}

function Link-File($link, $target) {
  # Shared top-level docs via hardlink (no admin needed when repo and $HOME share a volume).
  # Remove an existing link/our prior copy first (never follow through to the source); fall back to copy.
  if (Test-Path -LiteralPath $link) {
    $item = Get-Item -LiteralPath $link -Force
    if (($item.Attributes -band [IO.FileAttributes]::ReparsePoint) -ne 0) {
      & cmd.exe /c del "`"$link`"" | Out-Null
    } else {
      Remove-Item -LiteralPath $link -Force
    }
  }
  try {
    New-Item -ItemType HardLink -Path $link -Target $target -ErrorAction Stop | Out-Null
  } catch {
    Copy-Item -LiteralPath $target -Destination $link -Force
  }
}

function Install-Into($skillsDir) {
  $parent = Split-Path $skillsDir -Parent
  New-Item -ItemType Directory -Force -Path $skillsDir | Out-Null
  $skillDirs = @(Get-ChildItem -Directory "$Repo\skills" -Filter 'light-*' | Sort-Object Name)
  $n = 0
  foreach ($skill in $skillDirs) {
    Link-Dir "$skillsDir\$($skill.Name)" $skill.FullName
    if (Test-Path "$skillsDir\$($skill.Name)\SKILL.md") { $n++ }
  }
  if ($n -ne $ExpectedSkills) {
    throw "Expected $ExpectedSkills skills, linked $n"
  }
  # Shared libraries as siblings so skills' relative paths resolve.
  Link-Dir "$parent\databases"   "$Repo\databases"
  Link-Dir "$parent\code_assets" "$Repo\code_assets"
  # Shared top-level docs as siblings so skills' "see CONVENTIONS" / router references resolve after install.
  foreach ($doc in 'CONVENTIONS.md','ROUTER.md','ROUTER_EXAMPLES.md','MODE_REGISTRY.md') {
    Link-File "$parent\$doc" "$Repo\$doc"
  }
  Write-Host "  $skillsDir  ->  $n/$ExpectedSkills skills"
}

if ($Client -in 'both','claude') {
  Write-Host 'Claude Code:'
  Install-Into "$HOME\.claude\skills"
}
if ($Client -in 'both','codex') {
  Write-Host 'Codex:'
  Install-Into "$HOME\.agents\skills"
}
Write-Host 'Done. Restart your client to discover the skills.'
