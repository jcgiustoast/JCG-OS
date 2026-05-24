# notion-content.ps1
# Helper for the /content skill: query the Ideas backlog, create new drafts in
# the Notion Content DB, or promote an existing Idea row to Drafting with a
# body. Uses the Notion HTTP API (Markdown Content API).
#
# Usage examples:
#   .\notion-content.ps1 query-ideas
#   .\notion-content.ps1 create-draft -Title "X" -Platform Twitter -Topic LTV `
#       -HookType "Economics Reveal" -SourceWiki "ltv-frameworks" `
#       -SourceArticles "asteroi-en-roas-doesnt-mean-shit" `
#       -BodyFile C:\tmp\draft.md
#   .\notion-content.ps1 promote-idea -PageId <id> -BodyFile C:\tmp\draft.md
#
# Output (create-draft, promote-idea): one line per stdout `OK <pageId> <url>`
# Output (query-ideas): JSON to stdout
#   { "pageId": "...", "title": "...", "platform": "...", "topic": "...", "found": true }

[CmdletBinding()]
param(
  [Parameter(Position=0, Mandatory=$true)]
  [ValidateSet('query-ideas','create-draft','promote-idea')]
  [string]$Action,

  # Common
  [string]$PageId,
  [string]$BodyFile,
  [string]$Body,

  # Properties
  [string]$Title,
  [ValidateSet('Twitter','LinkedIn','Blog')][string]$Platform,
  [ValidateSet('LTV','CRO','Profitability','Subscription','Metrics','Forecasting','Incrementality')][string]$Topic,
  [ValidateSet('Economics Reveal','Contrarian Premise','Framework-First','Specificity','Credential Anchor')][string]$HookType,
  [ValidateSet('Idea','Researching','Drafting','Ready','Scheduled','Published')][string]$Status = 'Drafting',
  [string]$SourceWiki,
  [string]$SourceArticles
)

$ErrorActionPreference = 'Stop'

# --- Load config -----------------------------------------------------------
$repoRoot   = 'C:\Users\jcgiu\Documents\JCG-OS'
$configPath = Join-Path $repoRoot 'content\.notion-config.json'
if (-not (Test-Path $configPath)) {
  throw "Notion config missing at $configPath. Run Phase 1 setup first."
}
$config = Get-Content $configPath -Raw -Encoding UTF8 | ConvertFrom-Json
foreach ($k in @('notionToken','notionVersion','contentDbId','contentDataSourceId')) {
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
  # Leading comma forces caller to receive an array even when there's a single
  # element; PowerShell otherwise unwraps single-element arrays.
  return ,$items
}

# --- Actions ---------------------------------------------------------------
switch ($Action) {

  'query-ideas' {
    # Notion data-source query no longer honors the {timestamp: created_time}
    # sort syntax. Sort client-side on the row's built-in created_time field.
    $payload = @{
      filter    = @{ property = 'Status'; select = @{ equals = 'Idea' } }
      page_size = 100
    } | ConvertTo-Json -Depth 6 -Compress
    try {
      $r = Invoke-Notion -Method POST -Uri "https://api.notion.com/v1/data_sources/$($config.contentDataSourceId)/query" -JsonBody $payload
    } catch {
      $msg = $_.Exception.Message
      if ($_.ErrorDetails) { $msg += " | $($_.ErrorDetails.Message)" }
      throw "Query failed: $msg"
    }
    if ($r.results.Count -eq 0) {
      @{ found = $false } | ConvertTo-Json -Compress | Write-Output
      return
    }
    $row = $r.results | Sort-Object created_time | Select-Object -First 1
    $titleText = ($row.properties.Title.title | ForEach-Object { $_.plain_text }) -join ''
    $platformName = $null; if ($row.properties.Platform.select) { $platformName = $row.properties.Platform.select.name }
    $topicName    = $null; if ($row.properties.Topic.select)    { $topicName    = $row.properties.Topic.select.name }
    @{
      found    = $true
      pageId   = $row.id
      title    = $titleText
      platform = $platformName
      topic    = $topicName
      url      = $row.url
    } | ConvertTo-Json -Compress | Write-Output
    return
  }

  'create-draft' {
    if (-not $Title)    { throw "create-draft requires -Title" }
    if (-not $Platform) { throw "create-draft requires -Platform" }
    if (-not $Topic)    { throw "create-draft requires -Topic" }
    $body = Get-BodyText

    $props = [ordered]@{
      Title    = @{ title = @(@{ type = 'text'; text = @{ content = $Title } }) }
      Status   = @{ select = @{ name = $Status } }
      Platform = @{ select = @{ name = $Platform } }
      Topic    = @{ select = @{ name = $Topic } }
    }
    if ($HookType)        { $props['Hook type']        = @{ select = @{ name = $HookType } } }
    if ($SourceWiki)      { $props['Source wiki']      = @{ multi_select = (To-MultiSelectArray $SourceWiki) } }
    if ($SourceArticles)  { $props['Source articles']  = @{ multi_select = (To-MultiSelectArray $SourceArticles) } }

    $payload = @{
      parent     = @{ type = 'data_source_id'; data_source_id = $config.contentDataSourceId }
      properties = $props
      markdown   = $body
    } | ConvertTo-Json -Depth 10 -Compress
    try {
      $r = Invoke-Notion -Method POST -Uri 'https://api.notion.com/v1/pages' -JsonBody $payload
    } catch {
      $msg = $_.Exception.Message
      if ($_.ErrorDetails) { $msg += " | $($_.ErrorDetails.Message)" }
      throw "Create failed: $msg"
    }
    Write-Output "OK $($r.id) $($r.url)"
    return
  }

  'promote-idea' {
    if (-not $PageId) { throw "promote-idea requires -PageId" }
    $body = Get-BodyText

    # Step A: update status (+optional properties) on the existing row
    $props = [ordered]@{
      Status = @{ select = @{ name = $Status } }
    }
    if ($Platform)        { $props['Platform']         = @{ select = @{ name = $Platform } } }
    if ($Topic)           { $props['Topic']            = @{ select = @{ name = $Topic } } }
    if ($HookType)        { $props['Hook type']        = @{ select = @{ name = $HookType } } }
    if ($SourceWiki)      { $props['Source wiki']      = @{ multi_select = (To-MultiSelectArray $SourceWiki) } }
    if ($SourceArticles)  { $props['Source articles']  = @{ multi_select = (To-MultiSelectArray $SourceArticles) } }

    $propPayload = @{ properties = $props } | ConvertTo-Json -Depth 10 -Compress
    try {
      $r = Invoke-Notion -Method PATCH -Uri "https://api.notion.com/v1/pages/$PageId" -JsonBody $propPayload
    } catch {
      $msg = $_.Exception.Message
      if ($_.ErrorDetails) { $msg += " | $($_.ErrorDetails.Message)" }
      throw "Promote (properties) failed: $msg"
    }

    # Step B: replace page body content
    $bodyPayload = @{
      type            = 'replace_content'
      replace_content = @{ new_str = $body }
    } | ConvertTo-Json -Depth 6 -Compress
    try {
      $null = Invoke-Notion -Method PATCH -Uri "https://api.notion.com/v1/pages/$PageId/markdown" -JsonBody $bodyPayload
    } catch {
      $msg = $_.Exception.Message
      if ($_.ErrorDetails) { $msg += " | $($_.ErrorDetails.Message)" }
      throw "Promote (body) failed: $msg"
    }
    Write-Output "OK $($r.id) $($r.url)"
    return
  }
}
