# notion-sync.ps1
# Push local markdown (content/wiki/ + content/raw/articles/) to the Notion
# Knowledge Mirror. Idempotent — re-runs update existing pages instead of
# creating duplicates. One-way only (local -> Notion).
#
# Usage:
#   .\notion-sync.ps1                    # Full sync (wiki + articles)
#   .\notion-sync.ps1 wiki               # Only content/wiki/
#   .\notion-sync.ps1 articles           # Only content/raw/articles/
#   .\notion-sync.ps1 -DryRun            # Print plan, no API calls, no state write
#   .\notion-sync.ps1 wiki -DryRun       # Combined
#
# Config: content/.notion-config.json (gitignored)
# State:  content/memory/notion-sync-state.json (gitignored)

param(
  [Parameter(Position=0)]
  [ValidateSet('all','wiki','articles')]
  [string]$Scope = 'all',
  [switch]$DryRun
)

$ErrorActionPreference = 'Stop'

$repoRoot   = 'C:\Users\jcgiu\Documents\JCG-OS'
$configPath = Join-Path $repoRoot 'content\.notion-config.json'
$statePath  = Join-Path $repoRoot 'content\memory\notion-sync-state.json'

# --- Load config -----------------------------------------------------------
if (-not (Test-Path $configPath)) {
  throw "Notion config missing at $configPath. Run Phase 1 setup first."
}
$config = Get-Content $configPath -Raw -Encoding UTF8 | ConvertFrom-Json
foreach ($k in @('notionToken','notionVersion','knowledgeMirrorParentId')) {
  if ([string]::IsNullOrWhiteSpace($config.$k)) {
    throw "Notion config missing required field: $k"
  }
}

# --- Load state ------------------------------------------------------------
$state = @{}
if (Test-Path $statePath) {
  $raw = Get-Content $statePath -Raw -Encoding UTF8
  if ($raw.Trim()) {
    $parsed = $raw | ConvertFrom-Json
    foreach ($p in $parsed.PSObject.Properties) {
      $state[$p.Name] = $p.Value
    }
  }
}

# --- Enumerate files -------------------------------------------------------
$roots = @()
switch ($Scope) {
  'all'      { $roots = @('content\wiki','content\raw\articles') }
  'wiki'     { $roots = @('content\wiki') }
  'articles' { $roots = @('content\raw\articles') }
}

$excludeFilenames = @('content-index.md','pipeline.md')

$files = @()
foreach ($r in $roots) {
  $absRoot = Join-Path $repoRoot $r
  if (Test-Path $absRoot) {
    $files += Get-ChildItem -Path $absRoot -Recurse -File -Filter '*.md' |
      Where-Object { $excludeFilenames -notcontains $_.Name }
  }
}

if ($files.Count -eq 0) {
  Write-Host "No files found for scope '$Scope'. Nothing to do."
  exit 0
}

# --- API setup -------------------------------------------------------------
$headers = @{
  'Authorization'  = "Bearer $($config.notionToken)"
  'Notion-Version' = $config.notionVersion
  'Content-Type'   = 'application/json; charset=utf-8'
}

# --- Helpers ---------------------------------------------------------------
function Get-FrontmatterAndBody {
  param([string]$Content)
  if ($Content -match '^---\s*\r?\n([\s\S]*?)\r?\n---\s*\r?\n?([\s\S]*)$') {
    $fmText = $matches[1]
    $body   = $matches[2]
    $fm = @{}
    foreach ($line in $fmText -split "`r?`n") {
      if ($line -match '^([A-Za-z_][A-Za-z0-9_-]*):\s*(.*)$') {
        $key = $matches[1].Trim()
        $val = $matches[2].Trim()
        if ($val.StartsWith('"') -and $val.EndsWith('"')) { $val = $val.Trim('"') }
        elseif ($val.StartsWith("'") -and $val.EndsWith("'")) { $val = $val.Trim("'") }
        $fm[$key] = $val
      }
    }
    return @{ Frontmatter = $fm; Body = $body }
  }
  return @{ Frontmatter = @{}; Body = $Content }
}

function Get-Title {
  param($Parsed, [string]$RelativePath)
  if ($Parsed.Frontmatter.ContainsKey('title') -and $Parsed.Frontmatter['title']) {
    return [string]$Parsed.Frontmatter['title']
  }
  $h1 = [regex]::Match($Parsed.Body, '(?m)^#\s+(.+)$')
  if ($h1.Success) { return $h1.Groups[1].Value.Trim() }
  return [System.IO.Path]::GetFileNameWithoutExtension($RelativePath)
}

function Get-RelativePath {
  param([string]$AbsPath)
  $rel = $AbsPath.Substring($repoRoot.Length).TrimStart('\','/')
  return $rel.Replace('\','/')
}

function Invoke-Notion {
  param(
    [string]$Method,
    [string]$Uri,
    [string]$JsonBody
  )
  if ($JsonBody) {
    $bytes = [System.Text.Encoding]::UTF8.GetBytes($JsonBody)
    return Invoke-RestMethod -Uri $Uri -Headers $headers -Method $Method -Body $bytes
  } else {
    return Invoke-RestMethod -Uri $Uri -Headers $headers -Method $Method
  }
}

# --- Counters --------------------------------------------------------------
$created  = 0
$updated  = 0
$archived = 0
$skipped  = 0
$errors   = New-Object System.Collections.Generic.List[string]

# --- Sync loop -------------------------------------------------------------
$total = $files.Count
$idx = 0
foreach ($file in $files) {
  $idx++
  $rel = Get-RelativePath $file.FullName

  if ($file.Length -gt 1MB) {
    Write-Host "[$idx/$total] SKIP (>1MB): $rel"
    $skipped++
    continue
  }

  $rawContent = Get-Content $file.FullName -Raw -Encoding UTF8
  $parsed = Get-FrontmatterAndBody -Content $rawContent
  $title  = Get-Title -Parsed $parsed -RelativePath $rel
  $bodyMd = $parsed.Body

  if ($state.ContainsKey($rel)) {
    # ----- UPDATE branch -----
    $pageId = $state[$rel]
    if ($DryRun) {
      Write-Host "[$idx/$total] WOULD UPDATE: $pageId <- $rel"
      continue
    }
    $payload = @{
      type            = 'replace_content'
      replace_content = @{ new_str = $bodyMd }
    } | ConvertTo-Json -Depth 8 -Compress
    try {
      $null = Invoke-Notion -Method 'PATCH' -Uri "https://api.notion.com/v1/pages/$pageId/markdown" -JsonBody $payload
      Write-Host "[$idx/$total] UPDATED: $rel"
      $updated++
    } catch {
      $msg = $_.Exception.Message
      if ($_.ErrorDetails) { $msg += " | $($_.ErrorDetails.Message)" }
      Write-Warning "[$idx/$total] ERROR updating ${rel}: $msg"
      $errors.Add("${rel}: $msg")
    }
  } else {
    # ----- CREATE branch -----
    if ($DryRun) {
      Write-Host "[$idx/$total] WOULD CREATE: $rel (title: $title)"
      continue
    }
    $payload = @{
      parent     = @{ page_id = $config.knowledgeMirrorParentId }
      properties = @{
        title = @{
          title = @(@{ type = 'text'; text = @{ content = $title } })
        }
      }
      markdown   = $bodyMd
    } | ConvertTo-Json -Depth 8 -Compress
    try {
      $r = Invoke-Notion -Method 'POST' -Uri 'https://api.notion.com/v1/pages' -JsonBody $payload
      Write-Host "[$idx/$total] CREATED: $rel -> $($r.id)"
      $state[$rel] = $r.id
      $created++
    } catch {
      $msg = $_.Exception.Message
      if ($_.ErrorDetails) { $msg += " | $($_.ErrorDetails.Message)" }
      Write-Warning "[$idx/$total] ERROR creating ${rel}: $msg"
      $errors.Add("${rel}: $msg")
    }
  }

  # Rate limit: keep below Notion's ~3 req/sec
  Start-Sleep -Milliseconds 350
}

# --- Deletions -------------------------------------------------------------
# Only consider deletions when scope covers them; partial scopes should not
# archive pages that belong to a different scope.
$currentRels = @{}
foreach ($f in $files) { $currentRels[(Get-RelativePath $f.FullName)] = $true }

$stateKeys = @($state.Keys)
foreach ($key in $stateKeys) {
  $isInScope = switch ($Scope) {
    'all'      { $true }
    'wiki'     { $key -like 'content/wiki/*' }
    'articles' { $key -like 'content/raw/articles/*' }
  }
  if (-not $isInScope) { continue }
  if ($currentRels.ContainsKey($key)) { continue }

  $pageId = $state[$key]
  if ($DryRun) {
    Write-Host "WOULD ARCHIVE: $pageId <- $key"
    continue
  }
  # Notion API >= 2025-09-03 uses `in_trash` (the old `archived` field is rejected).
  $payload = '{"in_trash":true}'
  try {
    $null = Invoke-Notion -Method 'PATCH' -Uri "https://api.notion.com/v1/pages/$pageId" -JsonBody $payload
    Write-Host "ARCHIVED: $key"
    $state.Remove($key)
    $archived++
  } catch {
    $msg = $_.Exception.Message
    if ($_.ErrorDetails) { $msg += " | $($_.ErrorDetails.Message)" }
    Write-Warning "ERROR archiving ${key}: $msg"
    $errors.Add("${key}: $msg")
  }
  Start-Sleep -Milliseconds 350
}

# --- Write state -----------------------------------------------------------
if (-not $DryRun) {
  $stateObj = [PSCustomObject]@{}
  foreach ($k in ($state.Keys | Sort-Object)) {
    Add-Member -InputObject $stateObj -MemberType NoteProperty -Name $k -Value $state[$k]
  }
  $json = $stateObj | ConvertTo-Json -Depth 3
  # Set-Content with -Encoding UTF8 on PS 5.1 writes a BOM; use System.IO to avoid that
  [System.IO.File]::WriteAllText($statePath, $json, [System.Text.UTF8Encoding]::new($false))
}

# --- Report ----------------------------------------------------------------
Write-Host ''
Write-Host 'Sync complete.'
Write-Host "  Created:  $created pages"
Write-Host "  Updated:  $updated pages"
Write-Host "  Archived: $archived pages"
Write-Host "  Skipped:  $skipped pages (>1MB)"
Write-Host "  Errors:   $($errors.Count)"
foreach ($e in $errors) { Write-Host "    - $e" }
if ($DryRun) {
  Write-Host '  (DRY RUN - no API calls made, no state written)'
} else {
  Write-Host "  State:    $statePath"
}
