# notion-backfill-sources.ps1
# One-shot backfill: for every Idea-status row in the Content DB, resolve its
# existing "Source articles" + "Source wiki" multi-select tags to Knowledge
# Mirror page IDs and:
#   1. Set the new "Source links" rich_text property with native Notion page
#      mentions.
#   2. Prepend a Sources markdown header to the page body so the source links
#      are visible inline when reading the draft.
#
# Usage:
#   .\notion-backfill-sources.ps1            # apply
#   .\notion-backfill-sources.ps1 -DryRun    # preview only

[CmdletBinding()]
param([switch]$DryRun)

$ErrorActionPreference = 'Stop'
$repoRoot   = 'C:\Users\jcgiu\Documents\JCG-OS'
$configPath = Join-Path $repoRoot 'content\.notion-config.json'
$statePath  = Join-Path $repoRoot 'content\memory\notion-sync-state.json'

$config = Get-Content $configPath -Raw -Encoding UTF8 | ConvertFrom-Json
$headers = @{
  'Authorization'  = "Bearer $($config.notionToken)"
  'Notion-Version' = $config.notionVersion
  'Content-Type'   = 'application/json; charset=utf-8'
}

function Invoke-Notion {
  param([string]$Method, [string]$Uri, [string]$JsonBody)
  if ($JsonBody) {
    $bytes = [System.Text.Encoding]::UTF8.GetBytes($JsonBody)
    return Invoke-RestMethod -Uri $Uri -Headers $headers -Method $Method -Body $bytes
  } else {
    return Invoke-RestMethod -Uri $Uri -Headers $headers -Method $Method
  }
}

# Build stem -> pageId map
$state = Get-Content $statePath -Raw -Encoding UTF8 | ConvertFrom-Json
$byStem = @{}
foreach ($p in $state.PSObject.Properties) {
  $stem = [System.IO.Path]::GetFileNameWithoutExtension($p.Name)
  $byStem[$stem] = $p.Value
}

# Query Idea rows
$payload = @{
  filter    = @{ property = 'Status'; select = @{ equals = 'Idea' } }
  page_size = 100
} | ConvertTo-Json -Depth 6 -Compress
$resp = Invoke-Notion -Method POST -Uri "https://api.notion.com/v1/data_sources/$($config.contentDataSourceId)/query" -JsonBody $payload

Write-Host "Found $($resp.results.Count) Idea rows."

$updated = 0
$skipped = 0
$errors  = New-Object System.Collections.Generic.List[string]

foreach ($row in $resp.results) {
  $title = ($row.properties.Title.title | ForEach-Object { $_.plain_text }) -join ''
  $artNames  = @($row.properties.'Source articles'.multi_select | ForEach-Object { $_.name })
  $wikiNames = @($row.properties.'Source wiki'.multi_select | ForEach-Object { $_.name })

  # Resolve
  $articles = @()
  foreach ($n in $artNames) {
    if ($byStem.ContainsKey($n)) {
      $articles += [pscustomobject]@{ stem = $n; id = $byStem[$n]; resolved = $true }
    } else {
      Write-Warning "  unresolved article: $n"
      $articles += [pscustomobject]@{ stem = $n; id = $null; resolved = $false }
    }
  }
  $wiki = @()
  foreach ($n in $wikiNames) {
    if ($byStem.ContainsKey($n)) {
      $wiki += [pscustomobject]@{ stem = $n; id = $byStem[$n]; resolved = $true }
    } else {
      Write-Warning "  unresolved wiki: $n"
      $wiki += [pscustomobject]@{ stem = $n; id = $null; resolved = $false }
    }
  }

  if (@($articles | Where-Object { $_.resolved }).Count -eq 0 -and @($wiki | Where-Object { $_.resolved }).Count -eq 0) {
    Write-Host "[SKIP] $title -- no resolved sources"
    $skipped++
    continue
  }

  # Build rich_text mention array for "Source links"
  $rt = @()
  $first = $true
  foreach ($a in $articles) {
    if (-not $a.resolved) { continue }
    if (-not $first) { $rt += @{ type = 'text'; text = @{ content = ', ' } } }
    $rt += @{ type = 'mention'; mention = @{ type = 'page'; page = @{ id = $a.id } } }
    $first = $false
  }
  if (@($wiki | Where-Object { $_.resolved }).Count -gt 0) {
    if (-not $first) { $rt += @{ type = 'text'; text = @{ content = '  |  wiki: ' } } }
    $wfirst = $true
    foreach ($w in $wiki) {
      if (-not $w.resolved) { continue }
      if (-not $wfirst) { $rt += @{ type = 'text'; text = @{ content = ', ' } } }
      $rt += @{ type = 'mention'; mention = @{ type = 'page'; page = @{ id = $w.id } } }
      $wfirst = $false
    }
  }

  # Build markdown header
  $artLinks = @()
  foreach ($a in $articles) {
    if (-not $a.resolved) { continue }
    $idNoDash = $a.id -replace '-',''
    $artLinks += "[$($a.stem)](https://www.notion.so/$idNoDash)"
  }
  $wikiLinks = @()
  foreach ($w in $wiki) {
    if (-not $w.resolved) { continue }
    $idNoDash = $w.id -replace '-',''
    $wikiLinks += "[$($w.stem)](https://www.notion.so/$idNoDash)"
  }
  $headerParts = @()
  if ($artLinks.Count -gt 0)  { $headerParts += "**Sources:** " + ($artLinks -join ', ') }
  if ($wikiLinks.Count -gt 0) { $headerParts += "**Wiki:** "    + ($wikiLinks -join ', ') }
  $header = ($headerParts -join "`n") + "`n`n---`n`n"

  # Fetch existing body via markdown endpoint
  try {
    $cur = Invoke-Notion -Method GET -Uri "https://api.notion.com/v1/pages/$($row.id)/markdown"
  } catch {
    $msg = $_.Exception.Message
    if ($_.ErrorDetails) { $msg += " | $($_.ErrorDetails.Message)" }
    Write-Warning "[ERR ] $title -- fetch body: $msg"
    $errors.Add("$title fetch: $msg")
    continue
  }
  $existingBody = ''
  if ($cur.PSObject.Properties.Match('markdown').Count -gt 0) { $existingBody = [string]$cur.markdown }
  elseif ($cur.PSObject.Properties.Match('results').Count -gt 0) { $existingBody = ($cur.results | ForEach-Object { $_.markdown }) -join "`n" }

  # Idempotence: if body already starts with "**Sources:**", do not re-prepend
  if ($existingBody -match '^\s*\*\*Sources:\*\*') {
    Write-Host "[NOOP] $title -- already has Sources header (will only refresh property)"
    $newBody = $existingBody
  } else {
    $newBody = $header + $existingBody
  }

  $mode = if ($DryRun) { 'DRY' } else { 'APPLY' }
  Write-Host "[$mode] $title"
  Write-Host "        articles: $($artLinks -join ', ')"
  Write-Host "        wiki:     $($wikiLinks -join ', ')"

  if ($DryRun) { $updated++; continue }

  # PATCH property
  $propPayload = @{ properties = @{ 'Source links' = @{ rich_text = $rt } } } | ConvertTo-Json -Depth 10 -Compress
  try {
    $null = Invoke-Notion -Method PATCH -Uri "https://api.notion.com/v1/pages/$($row.id)" -JsonBody $propPayload
  } catch {
    $msg = $_.Exception.Message
    if ($_.ErrorDetails) { $msg += " | $($_.ErrorDetails.Message)" }
    Write-Warning "[ERR ] $title -- set property: $msg"
    $errors.Add("$title property: $msg")
    continue
  }

  # Replace body only if we changed it
  if ($newBody -ne $existingBody) {
    $bodyPayload = @{
      type            = 'replace_content'
      replace_content = @{ new_str = $newBody }
    } | ConvertTo-Json -Depth 6 -Compress
    try {
      $null = Invoke-Notion -Method PATCH -Uri "https://api.notion.com/v1/pages/$($row.id)/markdown" -JsonBody $bodyPayload
    } catch {
      $msg = $_.Exception.Message
      if ($_.ErrorDetails) { $msg += " | $($_.ErrorDetails.Message)" }
      Write-Warning "[ERR ] $title -- replace body: $msg"
      $errors.Add("$title body: $msg")
      continue
    }
  }

  $updated++
  Start-Sleep -Milliseconds 350
}

Write-Host ''
Write-Host "Done. Updated: $updated   Skipped: $skipped   Errors: $($errors.Count)"
foreach ($e in $errors) { Write-Host "  - $e" }
if ($DryRun) { Write-Host '(DRY RUN -- no API writes)' }
