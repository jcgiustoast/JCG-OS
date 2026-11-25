import crypto from 'node:crypto'
import { STATUS } from './state.js'
import { blocksToCaption, stripSourcesHeader, validateForPlatforms, splitLinksForX } from './caption.js'
import { checkPhase1Firewall } from './firewall.js'
import { extractFiles, uploadNotionFilesToPostBridge } from './media.js'

const YOUTUBE_TITLE_LIMIT = 100
const LATE_WINDOW_MS = 2 * 60 * 60 * 1000
const LATE_MARKER = 'NOT SCHEDULED'

export async function tick({ notion, pb, accountMap, fetchImpl = fetch, now = new Date() }) {
  const activeStatuses = [STATUS.READY, STATUS.SCHEDULING, STATUS.SCHEDULED]
  const rows = await notion.queryByStatus(activeStatuses)
  const handledIds = new Set(rows.map(r => r.id))

  for (const row of rows) {
    const status = row.properties.Status?.select?.name
    try {
      if (status === STATUS.READY) {
        await handleReady(row, { notion, pb, accountMap, fetchImpl })
      } else if (status === STATUS.SCHEDULING) {
        await handleScheduling(row, { notion, pb, accountMap, fetchImpl })
      } else if (status === STATUS.SCHEDULED) {
        await handleScheduled(row, { notion, pb, accountMap })
      }
    } catch (err) {
      await markFailed(row.id, notion, err.message)
    }
  }

  const reverted = await notion.queryRowsWithPostBridgeIdInUserState()
  for (const row of reverted) {
    const postBridgeId = (row.properties['Post Bridge ID']?.rich_text || [])
      .map(t => t.plain_text).join('')
    if (!postBridgeId) continue
    let confirmedGone = false
    try {
      await pb.deletePost(postBridgeId)
      confirmedGone = true
    } catch (err) {
      // 404 = already deleted — also confirmed gone.
      if (err.status === 404 || String(err.message).match(/404/)) {
        confirmedGone = true
      } else {
        // Any other error: do NOT clear the link. Next tick will retry.
        console.error(`Revert delete failed for ${row.id}: ${err.message}`)
      }
    }
    if (confirmedGone) {
      await notion.updateRow(row.id, {
        'Post Bridge ID': { rich_text: [] }
      })
    }
  }

  try {
    await flagUnscheduledSoon({ notion, now, handledIds })
  } catch (err) {
    console.error(`Late-row check failed: ${err.message}`)
  }
}

// A row whose posting time is under 2 hours away and still isn't scheduled gets one
// warning line added under its Notes. Existing notes are kept; the line is added once.
async function flagUnscheduledSoon({ notion, now, handledIds }) {
  const from = now.toISOString()
  const to = new Date(now.getTime() + LATE_WINDOW_MS).toISOString()
  const rows = await notion.queryUnscheduledSoon({ from, to })
  for (const row of rows) {
    if (handledIds.has(row.id)) continue
    const slot = row.properties.Date?.date?.start
    if (!slot || !slot.includes('T')) continue
    const existing = (row.properties.Notes?.rich_text || []).map(t => t.plain_text).join('')
    if (existing.includes(LATE_MARKER)) continue
    const warning = `⚠ ${LATE_MARKER} — slot ${slot}`
    const room = 1900 - warning.length - 1
    const kept = existing.length > room ? existing.slice(0, room) : existing
    const content = kept ? `${kept}\n${warning}` : warning
    await notion.updateRow(row.id, {
      Notes: { rich_text: [{ text: { content } }] }
    })
  }
}

// Per-platform settings post-bridge needs beyond the shared caption.
function buildPlatformConfigurations({ caption, platforms, title }) {
  const configs = {}
  if (platforms.includes('Twitter')) {
    const x = splitLinksForX(caption)
    if (x.firstComment) configs.twitter = { caption: x.text, first_comment: x.firstComment }
  }
  if (platforms.includes('YouTube')) {
    configs.youtube = { title }
  }
  return Object.keys(configs).length ? configs : undefined
}

function validateYouTubeTitle(title, platforms) {
  if (!platforms.includes('YouTube')) return { ok: true }
  if (!title) return { ok: false, reason: 'YouTube title is empty — fill in the row Title' }
  if (title.length > YOUTUBE_TITLE_LIMIT) {
    return { ok: false, reason: `YouTube title is ${title.length} chars, limit is ${YOUTUBE_TITLE_LIMIT}` }
  }
  return { ok: true }
}

async function handleReady(row, { notion, pb, accountMap, fetchImpl }) {
  const title = extractTitle(row)
  const platforms = extractPlatforms(row)
  const scheduledAt = row.properties.Date?.date?.start

  const blocks = await notion.fetchPageBlocks(row.id)
  const rawCaption = blocksToCaption(blocks)
  const caption = stripSourcesHeader(rawCaption)

  const firewall = checkPhase1Firewall(title, caption)
  if (firewall.blocked) {
    await markFailed(row.id, notion, `Phase 1 firewall: matched "${firewall.matched}"`)
    return
  }

  const mappedAccounts = platforms
    .map(p => accountMap[p])
    .filter(Boolean)

  if (mappedAccounts.length === 0) {
    await markFailed(row.id, notion, 'No mappable platforms selected (Blog/Spotify are skipped)')
    return
  }

  const validation = validateForPlatforms(caption, platforms)
  if (!validation.ok) {
    await markFailed(row.id, notion, validation.reason)
    return
  }

  const titleCheck = validateYouTubeTitle(title, platforms)
  if (!titleCheck.ok) {
    await markFailed(row.id, notion, titleCheck.reason)
    return
  }

  // Phase 1 of two-phase commit: flip to Scheduling
  await notion.updateRow(row.id, {
    Status: { select: { name: STATUS.SCHEDULING } }
  })

  // Upload media if any
  const files = extractFiles(row.properties.Media)
  const mediaIds = files.length
    ? await uploadNotionFilesToPostBridge(files, { pb, fetchImpl })
    : []

  // Phase 2: create the post-bridge post
  const createPayload = {
    caption,
    social_accounts: mappedAccounts
  }
  if (scheduledAt) createPayload.scheduled_at = scheduledAt
  if (mediaIds.length) createPayload.media = mediaIds
  const createConfigs = buildPlatformConfigurations({ caption, platforms, title })
  if (createConfigs) createPayload.platform_configurations = createConfigs

  const created = await pb.createPost(createPayload)

  // Phase 3: writeback (with sync token so the next tick doesn't re-PATCH)
  const token = computeEditToken(caption, scheduledAt, mappedAccounts, files.map(f => f.name))
  await notion.updateRow(row.id, {
    Status: { select: { name: STATUS.SCHEDULED } },
    'Post Bridge ID': { rich_text: [{ text: { content: created.id } }] },
    'Last Sync At': { date: { start: new Date().toISOString() } },
    'Synced Edit Token': { rich_text: [{ text: { content: token } }] }
  })
}

async function handleScheduling(row, { notion, pb, accountMap, fetchImpl }) {
  const blocks = await notion.fetchPageBlocks(row.id)
  const caption = stripSourcesHeader(blocksToCaption(blocks))
  const scheduledAt = row.properties.Date?.date?.start
  const platforms = extractPlatforms(row)
  const mappedAccounts = platforms.map(p => accountMap[p]).filter(Boolean)
  const targetHash = captionHash(caption)

  const predicate = (p) =>
    (p.scheduled_at ?? null) === (scheduledAt ?? null) && captionHash(p.caption || '') === targetHash
  const match = await findScheduledMatch(pb, predicate)

  if (match) {
    const token = computeEditToken(caption, scheduledAt, mappedAccounts, mediaNamesFromRow(row))
    await notion.updateRow(row.id, {
      Status: { select: { name: STATUS.SCHEDULED } },
      'Post Bridge ID': { rich_text: [{ text: { content: match.id } }] },
      'Last Sync At': { date: { start: new Date().toISOString() } },
      'Synced Edit Token': { rich_text: [{ text: { content: token } }] }
    })
    return
  }

  // No match — retry as if Ready (re-creates the post). Re-uses handleReady's logic
  // by directly invoking, but skip the "flip to Scheduling" step since we're already there.
  await retryCreate(row, caption, { notion, pb, accountMap, fetchImpl })
}

function captionHash(s) {
  return crypto.createHash('sha256').update(s).digest('hex').slice(0, 12)
}

// Page through scheduled posts. Bounded by maxPages so a corrupted/empty match condition
// can't loop indefinitely; post-bridge offers no created_at or since-time filter.
async function findScheduledMatch(pb, predicate, { pageSize = 50, maxPages = 10 } = {}) {
  for (let page = 0; page < maxPages; page++) {
    const result = await pb.listRecentPosts({ status: 'scheduled', limit: pageSize, offset: page * pageSize })
    const items = result.data || []
    const match = items.find(predicate)
    if (match) return match
    if (items.length < pageSize) return null
  }
  console.warn(`findScheduledMatch hit maxPages=${maxPages} (${maxPages * pageSize} posts) without match — may duplicate on retry. Raise maxPages if scheduled backlog has grown.`)
  return null
}

function computeEditToken(caption, scheduledAt, accountIds, mediaNames = []) {
  const sortedAccounts = [...accountIds].sort((a, b) => a - b).join(',')
  const sortedMedia = [...mediaNames].sort().join(',')
  const input = `${caption}||${scheduledAt ?? ''}||${sortedAccounts}||${sortedMedia}`
  return crypto.createHash('sha256').update(input).digest('hex').slice(0, 16)
}

function mediaNamesFromRow(row) {
  return extractFiles(row.properties.Media).map(f => f.name)
}

function extractEditToken(row) {
  const arr = row.properties['Synced Edit Token']?.rich_text || []
  return arr.map(t => t.plain_text).join('') || null
}

async function retryCreate(row, caption, { notion, pb, accountMap, fetchImpl }) {
  const platforms = extractPlatforms(row)
  const scheduledAt = row.properties.Date?.date?.start
  const mappedAccounts = platforms.map(p => accountMap[p]).filter(Boolean)

  if (mappedAccounts.length === 0) {
    await markFailed(row.id, notion, 'Recovery: no mappable platforms')
    return
  }

  const files = extractFiles(row.properties.Media)
  const mediaIds = files.length
    ? await uploadNotionFilesToPostBridge(files, { pb, fetchImpl })
    : []

  const payload = { caption, social_accounts: mappedAccounts }
  if (scheduledAt) payload.scheduled_at = scheduledAt
  if (mediaIds.length) payload.media = mediaIds
  const retryConfigs = buildPlatformConfigurations({ caption, platforms, title: extractTitle(row) })
  if (retryConfigs) payload.platform_configurations = retryConfigs

  const created = await pb.createPost(payload)
  const token = computeEditToken(caption, scheduledAt, mappedAccounts, files.map(f => f.name))
  await notion.updateRow(row.id, {
    Status: { select: { name: STATUS.SCHEDULED } },
    'Post Bridge ID': { rich_text: [{ text: { content: created.id } }] },
    'Last Sync At': { date: { start: new Date().toISOString() } },
    'Synced Edit Token': { rich_text: [{ text: { content: token } }] }
  })
}

function extractTitle(row) {
  const t = row.properties.Title?.title
  return Array.isArray(t) ? t.map(x => x.plain_text).join('') : ''
}

function extractPlatforms(row) {
  const arr = row.properties.Platform?.multi_select
  return Array.isArray(arr) ? arr.map(o => o.name) : []
}

async function handleScheduled(row, { notion, pb, accountMap }) {
  const postBridgeId = (row.properties['Post Bridge ID']?.rich_text || [])
    .map(t => t.plain_text).join('')
  if (!postBridgeId) {
    await markFailed(row.id, notion, 'Scheduled state with no Post Bridge ID — manual review needed')
    return
  }

  const pbPost = await pb.getPost(postBridgeId)
  const status = pbPost.status

  if (status === 'posted') {
    const results = await pb.getPostResults(postBridgeId)
    const urlText = formatPublishedUrls(results.data || [], accountMap)
    await notion.updateRow(row.id, {
      Status: { select: { name: STATUS.PUBLISHED } },
      'Published URLs': { rich_text: [{ text: { content: urlText } }] },
      'Last Sync At': { date: { start: new Date().toISOString() } }
    })
    return
  }

  if (status === 'failed') {
    await markFailed(row.id, notion, `post-bridge failed: ${pbPost.error || 'unknown reason'}`)
    return
  }

  // Status is 'scheduled' — check for edits
  await maybePropagateEdit(row, postBridgeId, { notion, pb, accountMap })
}

async function maybePropagateEdit(row, postBridgeId, { notion, pb, accountMap }) {
  const blocks = await notion.fetchPageBlocks(row.id)
  const caption = stripSourcesHeader(blocksToCaption(blocks))
  const platforms = extractPlatforms(row)
  const scheduledAt = row.properties.Date?.date?.start
  const mappedAccounts = platforms.map(p => accountMap[p]).filter(Boolean)

  const currentToken = computeEditToken(caption, scheduledAt, mappedAccounts, mediaNamesFromRow(row))
  const storedToken = extractEditToken(row)
  if (currentToken === storedToken) return

  // Backfill case: row was scheduled before this property existed. Trust current state
  // and write the token without PATCHing — the post-bridge post is presumed correct.
  if (storedToken === null) {
    await notion.updateRow(row.id, {
      'Synced Edit Token': { rich_text: [{ text: { content: currentToken } }] }
    })
    return
  }

  const patch = { caption, social_accounts: mappedAccounts }
  if (scheduledAt) patch.scheduled_at = scheduledAt
  const patchConfigs = buildPlatformConfigurations({ caption, platforms, title: extractTitle(row) })
  if (patchConfigs) patch.platform_configurations = patchConfigs

  await pb.updatePost(postBridgeId, patch)
  await notion.updateRow(row.id, {
    'Last Sync At': { date: { start: new Date().toISOString() } },
    'Synced Edit Token': { rich_text: [{ text: { content: currentToken } }] }
  })
}

function formatPublishedUrls(results, accountMap = {}) {
  const idToPlatform = Object.fromEntries(
    Object.entries(accountMap).map(([name, id]) => [id, name])
  )
  const lines = results
    .filter(r => r.platform_data?.url)
    .map(r => `${idToPlatform[r.social_account_id] || r.social_account_id}: ${r.platform_data.url}`)
  return lines.join('\n')
}

async function markFailed(pageId, notion, reason) {
  await notion.updateRow(pageId, {
    Status: { select: { name: STATUS.FAILED } },
    Notes: { rich_text: [{ text: { content: reason.slice(0, 1900) } }] }
  })
}
