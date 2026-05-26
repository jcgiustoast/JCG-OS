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
      }
      // Scheduling / Scheduled handlers added in later tasks
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

function extractTitle(row) {
  const t = row.properties.Title?.title
  return Array.isArray(t) ? t.map(x => x.plain_text).join('') : ''
}

function extractPlatforms(row) {
  const arr = row.properties.Platform?.multi_select
  return Array.isArray(arr) ? arr.map(o => o.name) : []
}

async function markFailed(pageId, notion, reason) {
  await notion.updateRow(pageId, {
    Status: { select: { name: STATUS.FAILED } },
    Notes: { rich_text: [{ text: { content: reason.slice(0, 1900) } }] }
  })
}
