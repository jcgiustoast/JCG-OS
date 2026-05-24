# notion-research.ps1
# Helper for the /content-research skill: file a competitive intelligence brief
# to the Notion Research DB. Uses the Notion HTTP API (Markdown Content API).
#
# Usage:
#   .\notion-research.ps1 create-brief `
#     -Title "Twitter - LTV - 2026-05-24" `
#     -Date "2026-05-24" `
#     -Platform Twitter `
#     -Topic LTV `
#     -CreatorsScraped "Taylor Holiday,Nick Sharma" `
#     -PostsAnalyzed 50 `
#     -BodyFile C:\tmp\brief.md
#
# Output: `OK <pageId> <url>` on success; throws with Notion's error message on failure.

[CmdletBinding()]
param(
  [Parameter(Position=0, Mandatory=$true)]
  [ValidateSet('create-brief')]
  [string]$Action,

  [string]$Title,
  [string]$Date,
  [ValidateSet('Twitter','LinkedIn','Both')][string]$Platform,
  [ValidateSet('LTV','CRO','Profitability','Subscription','Metrics','Forecasting','Incrementality')][string]$Topic,
  [string]$CreatorsScraped,
  [int]$PostsAnalyzed = 0,
  [string]$BodyFile,
  [string]$Body
)

$ErrorActionPreference = 'Stop'

# --- Load config -----------------------------------------------------------
$repoRoot   = 'C:\Users\jcgiu\Documents\JCG-OS'
$configPath = Join-Path $repoRoot 'content\.notion-config.json'
if (-not (Test-Path $configPath)) {
  throw "Notion config missing at $configPath. Run Phase 1 setup first."
}
$config = Get-Content $configPath -Raw -Encoding UTF8 | ConvertFrom-Json
foreach ($k in @('notionToken','notionVersion','researchDbId','researchDataSourceId')) {
  if ([string]::IsNullOrWhiteSpace($config.$k)) {
    throw "Notion config missing required field: $k"
  }
}

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

function Get-BodyText {
  if ($BodyFile) {
    if (-not (Test-Path $BodyFile)) { throw "BodyFile not found: $BodyFile" }
    return Get-Content $BodyFile -Raw -Encoding UTF8
  } elseif ($Body) {
    return $Body
  } else {
    throw "Must supply -BodyFile or -Body"
  }
}

function To-MultiSelectArray {
  param([string]$Csv)
  if ([string]::IsNullOrWhiteSpace($Csv)) { return ,@() }
  $items = @($Csv.Split(',') | ForEach-Object { @{ name = $_.Trim() } } | Where-Object { $_.name })
  return ,$items
}

# --- Actions ---------------------------------------------------------------
switch ($Action) {

  'create-brief' {
    if (-not $Title)    { throw "create-brief requires -Title" }
    if (-not $Date)     { throw "create-brief requires -Date (YYYY-MM-DD)" }
    if (-not $Platform) { throw "create-brief requires -Platform" }
    if (-not $Topic)    { throw "create-brief requires -Topic" }
    $body = Get-BodyText

    $props = [ordered]@{
      Title    = @{ title = @(@{ type = 'text'; text = @{ content = $Title } }) }
      Date     = @{ date = @{ start = $Date } }
      Platform = @{ select = @{ name = $Platform } }
      Topic    = @{ select = @{ name = $Topic } }
    }
    if ($CreatorsScraped) {
      $props['Creators scraped'] = @{ multi_select = (To-MultiSelectArray $CreatorsScraped) }
    }
    if ($PostsAnalyzed -gt 0) {
      $props['Posts analyzed'] = @{ number = $PostsAnalyzed }
    }

    $payload = @{
      parent     = @{ type = 'data_source_id'; data_source_id = $config.researchDataSourceId }
      properties = $props
      markdown   = $body
    } | ConvertTo-Json -Depth 10 -Compress
    try {
      $r = Invoke-Notion -Method POST -Uri 'https://api.notion.com/v1/pages' -JsonBody $payload
    } catch {
      $msg = $_.Exception.Message
      if ($_.ErrorDetails) { $msg += " | $($_.ErrorDetails.Message)" }
      throw "Create brief failed: $msg"
    }
    Write-Output "OK $($r.id) $($r.url)"
    return
  }
}
