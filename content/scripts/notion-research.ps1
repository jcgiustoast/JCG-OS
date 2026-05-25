# notion-research.ps1
# Helper for the /content-research skill. Files one row per reference post
# to the Notion Research DB. Each row = one noteworthy competitor post.
#
# Schema (post-2026-05-25 simplification):
#   Title (title, first ~80 chars of post), Platform (select, 8 options),
#   Post URL (url), Topic (select, 7 options), Creator (select),
#   Informed pieces (relation -> Content DB), Created (auto).
#
# Usage:
#   .\notion-research.ps1 create-post `
#     -Title "Best LTV thread I've read this year" `
#     -Platform Twitter `
#     -PostUrl "https://twitter.com/.../status/..." `
#     -Topic LTV `
#     -Creator "Taylor Holiday"
#
# Optional -BodyFile or -Body to include the post text as page body.
#
# Output: `OK <pageId> <url>` on success.

[CmdletBinding()]
param(
  [Parameter(Position=0, Mandatory=$true)]
  [ValidateSet('create-post')]
  [string]$Action,

  [string]$Title,

  [ValidateSet('Blog','LinkedIn','Twitter','Instagram','Threads','TikTok','YouTube','Spotify')]
  [string]$Platform,

  [string]$PostUrl,

  [ValidateSet('LTV','CRO','Profitability','Subscription','Metrics','Forecasting','Incrementality')]
  [string]$Topic,

  [string]$Creator,

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
    return ''
  }
}

# --- Actions ---------------------------------------------------------------
switch ($Action) {

  'create-post' {
    if (-not $Title)    { throw "create-post requires -Title" }
    if (-not $Platform) { throw "create-post requires -Platform" }
    if (-not $PostUrl)  { throw "create-post requires -PostUrl" }
    if (-not $Topic)    { throw "create-post requires -Topic" }
    if (-not $Creator)  { throw "create-post requires -Creator" }
    $bodyText = Get-BodyText

    $props = [ordered]@{
      Title      = @{ title = @(@{ type = 'text'; text = @{ content = $Title } }) }
      Platform   = @{ select = @{ name = $Platform } }
      'Post URL' = @{ url = $PostUrl }
      Topic      = @{ select = @{ name = $Topic } }
      Creator    = @{ select = @{ name = $Creator } }
    }

    $payloadObj = @{
      parent     = @{ type = 'data_source_id'; data_source_id = $config.researchDataSourceId }
      properties = $props
    }
    if ($bodyText) { $payloadObj['markdown'] = $bodyText }

    $payload = $payloadObj | ConvertTo-Json -Depth 10 -Compress
    try {
      $r = Invoke-Notion -Method POST -Uri 'https://api.notion.com/v1/pages' -JsonBody $payload
    } catch {
      $msg = $_.Exception.Message
      if ($_.ErrorDetails) { $msg += " | $($_.ErrorDetails.Message)" }
      throw "Create post failed: $msg"
    }
    Write-Output "OK $($r.id) $($r.url)"
    return
  }
}
