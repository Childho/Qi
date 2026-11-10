# Installs Matt Pocock's agent skills (https://github.com/mattpocock/skills)
# into the DSH user-level skill root: <DSH_HOME>/skills
#
# Usage (default = promoted set, 27 skills):
#   pwsh -File .\install-skills.ps1
#
# Optional:
#   pwsh -File .\install-skills.ps1 -IncludeMisc          # + misc/ (4 skills)
#   pwsh -File .\install-skills.ps1 -IncludeInProgress    # + in-progress/ (8 skills)
#   pwsh -File .\install-skills.ps1 -DshHome D:\somewhere # install elsewhere (dry run)

[CmdletBinding()]
param(
  [string]$DshHome = $(if ($env:DSH_HOME) { $env:DSH_HOME } else { Join-Path $env:USERPROFILE '.dsh' }),
  [string]$Repo = 'https://github.com/mattpocock/skills.git',
  [switch]$IncludeMisc,
  [switch]$IncludeInProgress
)

$ErrorActionPreference = 'Stop'
Set-StrictMode -Version Latest

$tmpRoot = [System.IO.Path]::GetTempPath()
$work = Join-Path $tmpRoot ('mp-skills-' + [guid]::NewGuid().ToString('N').Substring(0, 8))
$target = Join-Path $DshHome 'skills'

try {
  Write-Host "Cloning $Repo ..."
  & git clone --depth 1 --quiet $Repo $work
  if ($LASTEXITCODE -ne 0) { throw "git clone failed with exit code $LASTEXITCODE" }

  $commit = (& git -C $work rev-parse --short HEAD).Trim()
  Write-Host "Cloned commit $commit"

  $cats = @('engineering', 'productivity')
  if ($IncludeMisc) { $cats += 'misc' }
  if ($IncludeInProgress) { $cats += 'in-progress' }

  New-Item -ItemType Directory -Force -Path $target | Out-Null
  Write-Host "Installing into $target"

  $installed = New-Object System.Collections.Generic.List[string]
  $skipped = New-Object System.Collections.Generic.List[string]

  foreach ($cat in $cats) {
    $catDir = Join-Path (Join-Path $work 'skills') $cat
    if (-not (Test-Path $catDir)) { Write-Warning "Missing category: $cat"; continue }
    foreach ($bundle in Get-ChildItem -Path $catDir -Directory) {
      $skillFile = Join-Path $bundle.FullName 'SKILL.md'
      $dest = Join-Path $target $bundle.Name

      if (-not (Test-Path $skillFile)) {
        $skipped.Add("$cat/$($bundle.Name) (no SKILL.md)")
        continue
      }
      $head = Get-Content -Path $skillFile -TotalCount 20 -Encoding UTF8
      if (-not ($head -match '^name:')) {
        $skipped.Add("$cat/$($bundle.Name) (no frontmatter name)")
        continue
      }

      if (Test-Path $dest) { Remove-Item -Recurse -Force $dest }
      Copy-Item -Recurse -Force $bundle.FullName $dest
      $installed.Add("$cat/$($bundle.Name)")
    }
  }

  Write-Host ""
  Write-Host ("Installed {0} skill(s):" -f $installed.Count)
  foreach ($s in $installed) { Write-Host "  + $s" }
  if ($skipped.Count -gt 0) {
    Write-Host ""
    Write-Host ("Skipped {0}:" -f $skipped.Count)
    foreach ($s in $skipped) { Write-Host "  - $s" }
  }

  Write-Host ""
  Write-Host "Done. DSH watches $target, so the skills appear in the catalog without a restart."
  Write-Host "Skills with 'disable-model-invocation: true' are invocable by you only, not auto-listed for the model."
}
finally {
  if (Test-Path $work) { Remove-Item -Recurse -Force $work -ErrorAction SilentlyContinue }
}
