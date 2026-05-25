# notion-content.ps1
# Helper for the /content skill. Talks to the Notion Content DB.
#
# Schema (post-2026-05-25 simplification):
#   Title (title), Status (select), Platform (multi_select, 8 options),
#   Type (select, 9 options), Date (date), Published URL (url),
#   Source research (relation), Created (auto). Body holds the draft
#   with inline @page-mentions to the Knowledge Mirror as the only
#   source-attribution mechanism.
#
# Actions:
#   query-ideas    Return the oldest Status=Idea row as JSON
#   create-draft   Create a new row, write body, set properties
#   promote-idea   Update an existing Idea row's status + properties + body
#
# Usage examples:
#   .\notion-content.ps1 query-ideas
#   .\notion-content.ps1 create-draft -Title "X" -Platform Twitter,LinkedIn `
#       -Type Thread -SourceWiki "ltv-frameworks" `
#       -SourceArticles "asteroi-en-roas-doesnt-mean-shit" `
#       -BodyFile C:\tmp\draft.md
#   .\notion-content.ps1 promote-idea -PageId <id> -BodyFile C:\tmp\draft.md `
#       -Type Thread -SourceWiki "ltv-frameworks"

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

  [ValidateSet('Blog','LinkedIn','Twitter','Instagram','Threads','TikTok','YouTube','Spotify')]
  [string[]]$Platform,

  [ValidateSet('Thread','YouTube Video','Short','Carousel','Resource','Podcast','Authority','Infographic','Personal Post')]
  [string]$Type,

  [ValidateSet('Idea','Researching','Drafting','Ready','Scheduled','Published')]
  [string]$Status = 'Drafting',

  [string]$Date,           # YYYY-MM-DD (scheduled or published)
  [string]$PublishedUrl,

  # Source attribution: not stored as DB properties anymore. Used only to
  # build the inline mention header that gets prepended to the page body.
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

function To-MultiSelectFromArray {
  param([string[]]$Names)
  if (-not $Names -or $Names.Count -eq 0) { return ,@() }
  $items = @($Names | Where-Object { $_ } | ForEach-Object { @{ name = $_.Trim() } })
  return ,$items
}

# --- Source-mention helpers ------------------------------------------------
# Resolve filename stems (e.g. "metric-tree-subscription-ecommerce") to the
# Notion page IDs of the Knowledge Mirror via notion-sync-state.json, then
# build a markdown header prepended to the page body. Notion renders the
# markdown links as mention chips back to the mirror page.

$script:syncStateCache = $null
function Get-SyncState {
  if ($null -ne $script:syncStateCache) { return $script:syncStateCache }
  $statePath = Join-Path $repoRoot 'content\memory\notion-sync-state.json'
  if (-not (Test-Path $statePath)) {
    Write-Warning "Sync state missing at $statePath. Source mentions will be skipped."
    $script:syncStateCache = @{}
    return $script:syncStateCache
  }
  $raw = Get-Content $statePath -Raw -Encoding UTF8
  if (-not $raw.Trim()) {
    $script:syncStateCache = @{}
    return $script:syncStateCache
  }
  $parsed = $raw | ConvertFrom-Json
  $byStem = @{}
  foreach ($p in $parsed.PSObject.Properties) {
    $stem = [System.IO.Path]::GetFileNameWithoutExtension($p.Name)
    $byStem[$stem] = @{ path = $p.Name; id = $p.Value }
  }
  $script:syncStateCache = $byStem
  return $script:syncStateCache
}

function Resolve-SourceStems {
  param([string]$Csv)
  if ([string]::IsNullOrWhiteSpace($Csv)) { return @() }
  $state = Get-SyncState
  $resolved = @()
  foreach ($raw in $Csv.Split(',')) {
    $stem = $raw.Trim()
    if (-not $stem) { continue }
    if ($state.ContainsKey($stem)) {
      $resolved += [pscustomobject]@{ stem = $stem; id = $state[$stem].id; resolved = $true }
    } else {
      Write-Warning "Source not in Knowledge Mirror: $stem (skipping mention)"
      $resolved += [pscustomobject]@{ stem = $stem; id = $null; resolved = $false }
    }
  }
  return $resolved
}

function Build-SourcesMarkdownHeader {
  param($Articles, $Wiki)
  $parts = @()
  $articleLinks = @()
  foreach ($a in $Articles) {
    if (-not $a.resolved) { continue }
    $idNoDash = $a.id -replace '-',''
    $articleLinks += "[$($a.stem)](https://www.notion.so/$idNoDash)"
  }
  if ($articleLinks.Count -gt 0) {
    $parts += "**Sources:** " + ($articleLinks -join ', ')
  }
  $wikiLinks = @()
  foreach ($w in $Wiki) {
    if (-not $w.resolved) { continue }
    $idNoDash = $w.id -replace '-',''
    $wikiLinks += "[$($w.stem)](https://www.notion.so/$idNoDash)"
  }
  if ($wikiLinks.Count -gt 0) {
    $parts += "**Wiki:** " + ($wikiLinks -join ', ')
  }
  if ($parts.Count -eq 0) { return '' }
  return ($parts -join "`n") + "`n`n---`n`n"
}

# --- Actions ---------------------------------------------------------------
switch ($Action) {

  'query-ideas' {
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
    $platformNames = @()
    if ($row.properties.Platform.multi_select) {
      $platformNames = @($row.properties.Platform.multi_select | ForEach-Object { $_.name })
    }
    $typeName = $null
    if ($row.properties.Type.select) { $typeName = $row.properties.Type.select.name }
    @{
      found    = $true
      pageId   = $row.id
      title    = $titleText
      platform = ($platformNames -join ',')
      type     = $typeName
      url      = $row.url
    } | ConvertTo-Json -Compress | Write-Output
    return
  }

  'create-draft' {
    if (-not $Title)    { throw "create-draft requires -Title" }
    if (-not $Platform -or $Platform.Count -eq 0) { throw "create-draft requires -Platform (one or more values)" }
    $bodyText = Get-BodyText

    $resolvedArticles = Resolve-SourceStems $SourceArticles
    $resolvedWiki     = Resolve-SourceStems $SourceWiki
    $bodyText = (Build-SourcesMarkdownHeader -Articles $resolvedArticles -Wiki $resolvedWiki) + $bodyText

    $props = [ordered]@{
      Title    = @{ title = @(@{ type = 'text'; text = @{ content = $Title } }) }
      Status   = @{ select = @{ name = $Status } }
      Platform = @{ multi_select = (To-MultiSelectFromArray $Platform) }
    }
    if ($Type)         { $props['Type']          = @{ select = @{ name = $Type } } }
    if ($Date)         { $props['Date']          = @{ date = @{ start = $Date } } }
    if ($PublishedUrl) { $props['Published URL'] = @{ url = $PublishedUrl } }

    $payload = @{
      parent     = @{ type = 'data_source_id'; data_source_id = $config.contentDataSourceId }
      properties = $props
      markdown   = $bodyText
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
    $bodyText = Get-BodyText

    $resolvedArticles = Resolve-SourceStems $SourceArticles
    $resolvedWiki     = Resolve-SourceStems $SourceWiki
    $bodyText = (Build-SourcesMarkdownHeader -Articles $resolvedArticles -Wiki $resolvedWiki) + $bodyText

    $props = [ordered]@{
      Status = @{ select = @{ name = $Status } }
    }
    if ($Platform -and $Platform.Count -gt 0) { $props['Platform'] = @{ multi_select = (To-MultiSelectFromArray $Platform) } }
    if ($Type)         { $props['Type']          = @{ select = @{ name = $Type } } }
    if ($Date)         { $props['Date']          = @{ date = @{ start = $Date } } }
    if ($PublishedUrl) { $props['Published URL'] = @{ url = $PublishedUrl } }

    $propPayload = @{ properties = $props } | ConvertTo-Json -Depth 10 -Compress
    try {
      $r = Invoke-Notion -Method PATCH -Uri "https://api.notion.com/v1/pages/$PageId" -JsonBody $propPayload
    } catch {
      $msg = $_.Exception.Message
      if ($_.ErrorDetails) { $msg += " | $($_.ErrorDetails.Message)" }
      throw "Promote (properties) failed: $msg"
    }

    $bodyPayload = @{
      type            = 'replace_content'
      replace_content = @{ new_str = $bodyText }
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
