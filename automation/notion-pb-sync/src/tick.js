import crypto from 'node:crypto'
import { STATUS } from './state.js'
import { blocksToCaption, stripSourcesHeader, validateForPlatforms } from './caption.js'
import { checkPhase1Firewall } from './firewall.js'
import { extractFiles, uploadNotionFilesToPostBridge } from './media.js'

export async function tick({ notion, pb, accountMap, fetchImpl = fetch }) {
  const activeStatuses = [STATUS.READY, STATUS.SCHEDULING, STATUS.SCHEDULED]
  const rows = await notion.queryByStatus(activeStatuses)

  for (const row of rows) {
    const status = row.properties.Status?.select?.name
    try {
      if (status === STATUS.READY) {
        await handleReady(row, { notion, pb, accountMap, fetchImpl })
      } else if (status === STATUS.SCHEDULING) {
        await handleScheduling(row, { notion, pb, accountMap, fetchImpl })
      } else if (status === STATUS.SCHEDULED) {
        await handleScheduled(row, { notion, pb })
      }
    } catch (err) {
      await markFailed(row.id, notion, err.message)
    }
  }
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

  const created = await pb.createPost(createPayload)

  // Phase 3: writeback
  await notion.updateRow(row.id, {
    Status: { select: { name: STATUS.SCHEDULED } },
    'Post Bridge ID': { rich_text: [{ text: { content: created.id } }] },
    'Last Sync At': { date: { start: new Date().toISOString() } }
  })
}

async function handleScheduling(row, { notion, pb, accountMap, fetchImpl }) {
  const blocks = await notion.fetchPageBlocks(row.id)
  const caption = stripSourcesHeader(blocksToCaption(blocks))
  const scheduledAt = row.properties.Date?.date?.start
  const targetHash = captionHash(caption)

  const recent = await pb.listRecentPosts({ status: 'scheduled', limit: 50 })
  const match = (recent.data || []).find(p => {
    return p.scheduled_at === scheduledAt && captionHash(p.caption || '') === targetHash
  })

  if (match) {
    await notion.updateRow(row.id, {
      Status: { select: { name: STATUS.SCHEDULED } },
      'Post Bridge ID': { rich_text: [{ text: { content: match.id } }] },
      'Last Sync At': { date: { start: new Date().toISOString() } }
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

  const created = await pb.createPost(payload)
  await notion.updateRow(row.id, {
    Status: { select: { name: STATUS.SCHEDULED } },
    'Post Bridge ID': { rich_text: [{ text: { content: created.id } }] },
    'Last Sync At': { date: { start: new Date().toISOString() } }
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

async function handleScheduled(row, { notion, pb }) {
  const postBridgeId = (row.properties['Post Bridge ID']?.rich_text || [])
    .map(t => t.plain_text).join('')
  if (!postBridgeId) {
    // Defensive: Scheduled state without an ID is corrupt. Surface it.
    await markFailed(row.id, notion, 'Scheduled state with no Post Bridge ID — manual review needed')
    return
  }

  const pbPost = await pb.getPost(postBridgeId)
  const status = pbPost.status

  if (status === 'posted') {
    const results = await pb.getPostResults(postBridgeId)
    const urlText = formatPublishedUrls(results.data || [])
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
  // Otherwise still pending — no-op this tick.
}

function formatPublishedUrls(results) {
  const PLATFORM_LABEL = {
    linkedin: 'LinkedIn', twitter: 'Twitter', threads: 'Threads',
    tiktok: 'TikTok', youtube: 'YouTube', instagram: 'Instagram'
  }
  const lines = results
    .filter(r => r.share_url)
    .map(r => `${PLATFORM_LABEL[r.platform] || r.platform}: ${r.share_url}`)
  return lines.join('\n')
}

async function markFailed(pageId, notion, reason) {
  await notion.updateRow(pageId, {
    Status: { select: { name: STATUS.FAILED } },
    Notes: { rich_text: [{ text: { content: reason.slice(0, 1900) } }] }
  })
}
