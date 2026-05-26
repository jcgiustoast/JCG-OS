import { describe, it, expect, vi } from 'vitest'
import crypto from 'node:crypto'
import { tick } from '../src/tick.js'

function makeRow({ id = 'page_1', status = 'Ready', title = 'A post', platforms = ['LinkedIn'], date = '2026-06-01T12:00:00.000Z', postBridgeId = '', media = [] } = {}) {
  return {
    id,
    last_edited_time: '2026-05-26T10:00:00.000Z',
    properties: {
      Title: { title: [{ plain_text: title }] },
      Status: { select: { name: status } },
      Platform: { multi_select: platforms.map(name => ({ name })) },
      Date: { date: { start: date } },
      'Post Bridge ID': { rich_text: postBridgeId ? [{ plain_text: postBridgeId }] : [] },
      Media: { type: 'files', files: media }
    }
  }
}

function fakeNotion({ activeRows = [], blocks = [] } = {}) {
  return {
    queryByStatus: vi.fn(async () => activeRows),
    queryRowsWithPostBridgeIdInUserState: vi.fn(async () => []),
    fetchPageBlocks: vi.fn(async () => blocks),
    updateRow: vi.fn(async () => ({}))
  }
}

function fakePb({ createReturn = { id: 'pb_new' } } = {}) {
  return {
    createPost: vi.fn(async () => createReturn),
    getPost: vi.fn(),
    updatePost: vi.fn(),
    deletePost: vi.fn(),
    getPostResults: vi.fn(),
    listRecentPosts: vi.fn(async () => ({ data: [] })),
    createUploadUrl: vi.fn(),
    uploadMedia: vi.fn()
  }
}

const ACCOUNT_MAP = {
  LinkedIn: 25903, Threads: 25902, TikTok: 25901, YouTube: 25900, Twitter: 25899, Instagram: 25898
}

describe('tick — Ready → Scheduled happy path', () => {
  it('flips Ready to Scheduling, creates post-bridge post, writes back ID + Scheduled', async () => {
    const row = makeRow({ id: 'page_1', status: 'Ready', platforms: ['LinkedIn'] })
    const blocks = [{ type: 'paragraph', paragraph: { rich_text: [{ plain_text: 'Hello world' }] } }]
    const notion = fakeNotion({ activeRows: [row], blocks })
    const pb = fakePb({ createReturn: { id: 'pb_xyz', status: 'scheduled' } })

    await tick({ notion, pb, accountMap: ACCOUNT_MAP, fetchImpl: vi.fn() })

    expect(notion.updateRow).toHaveBeenNthCalledWith(1, 'page_1', expect.objectContaining({
      Status: { select: { name: 'Scheduling' } }
    }))
    expect(pb.createPost).toHaveBeenCalledWith(expect.objectContaining({
      caption: 'Hello world',
      social_accounts: [25903],
      scheduled_at: '2026-06-01T12:00:00.000Z'
    }))
    expect(notion.updateRow).toHaveBeenNthCalledWith(2, 'page_1', expect.objectContaining({
      Status: { select: { name: 'Scheduled' } },
      'Post Bridge ID': { rich_text: [{ text: { content: 'pb_xyz' } }] }
    }))
  })

  it('marks row Failed when firewall matches', async () => {
    const row = makeRow({ title: 'Mars Men is great' })
    const notion = fakeNotion({ activeRows: [row], blocks: [] })
    const pb = fakePb()
    await tick({ notion, pb, accountMap: ACCOUNT_MAP, fetchImpl: vi.fn() })
    expect(pb.createPost).not.toHaveBeenCalled()
    expect(notion.updateRow).toHaveBeenCalledWith('page_1', expect.objectContaining({
      Status: { select: { name: 'Failed' } }
    }))
  })

  it('marks row Failed when Twitter exceeds 280 chars', async () => {
    const long = 'x'.repeat(281)
    const row = makeRow({ platforms: ['Twitter'] })
    const blocks = [{ type: 'paragraph', paragraph: { rich_text: [{ plain_text: long }] } }]
    const notion = fakeNotion({ activeRows: [row], blocks })
    const pb = fakePb()
    await tick({ notion, pb, accountMap: ACCOUNT_MAP, fetchImpl: vi.fn() })
    expect(pb.createPost).not.toHaveBeenCalled()
    expect(notion.updateRow).toHaveBeenCalledWith('page_1', expect.objectContaining({
      Status: { select: { name: 'Failed' } }
    }))
  })

  it('skips Blog and Spotify platforms (no account mapping)', async () => {
    const row = makeRow({ platforms: ['Blog', 'LinkedIn', 'Spotify'] })
    const blocks = [{ type: 'paragraph', paragraph: { rich_text: [{ plain_text: 'Hi' }] } }]
    const notion = fakeNotion({ activeRows: [row], blocks })
    const pb = fakePb({ createReturn: { id: 'pb_z' } })
    await tick({ notion, pb, accountMap: ACCOUNT_MAP, fetchImpl: vi.fn() })
    expect(pb.createPost).toHaveBeenCalledWith(expect.objectContaining({
      social_accounts: [25903]
    }))
  })

  it('marks row Failed when no mappable platforms', async () => {
    const row = makeRow({ platforms: ['Blog', 'Spotify'] })
    const blocks = [{ type: 'paragraph', paragraph: { rich_text: [{ plain_text: 'Hi' }] } }]
    const notion = fakeNotion({ activeRows: [row], blocks })
    const pb = fakePb()
    await tick({ notion, pb, accountMap: ACCOUNT_MAP, fetchImpl: vi.fn() })
    expect(pb.createPost).not.toHaveBeenCalled()
    expect(notion.updateRow).toHaveBeenCalledWith('page_1', expect.objectContaining({
      Status: { select: { name: 'Failed' } }
    }))
  })
})

function captionHash(s) {
  return crypto.createHash('sha256').update(s).digest('hex').slice(0, 12)
}

describe('tick — Scheduling recovery', () => {
  it('claims an existing post-bridge post when caption hash + scheduled_at match', async () => {
    const row = makeRow({ id: 'page_2', status: 'Scheduling' })
    const blocks = [{ type: 'paragraph', paragraph: { rich_text: [{ plain_text: 'Hello world' }] } }]
    const expectedHash = captionHash('Hello world')
    const notion = fakeNotion({ activeRows: [row], blocks })
    const pb = fakePb()
    pb.listRecentPosts = vi.fn(async () => ({
      data: [
        { id: 'pb_claimed', scheduled_at: '2026-06-01T12:00:00.000Z', caption: 'Hello world' },
        { id: 'pb_other', scheduled_at: '2026-06-02T12:00:00.000Z', caption: 'Other post' }
      ]
    }))

    await tick({ notion, pb, accountMap: ACCOUNT_MAP, fetchImpl: vi.fn() })

    expect(pb.createPost).not.toHaveBeenCalled()
    expect(notion.updateRow).toHaveBeenCalledWith('page_2', expect.objectContaining({
      Status: { select: { name: 'Scheduled' } },
      'Post Bridge ID': { rich_text: [{ text: { content: 'pb_claimed' } }] }
    }))
  })

  it('retries the create when no match found', async () => {
    const row = makeRow({ id: 'page_3', status: 'Scheduling' })
    const blocks = [{ type: 'paragraph', paragraph: { rich_text: [{ plain_text: 'No match content' }] } }]
    const notion = fakeNotion({ activeRows: [row], blocks })
    const pb = fakePb({ createReturn: { id: 'pb_retry' } })
    pb.listRecentPosts = vi.fn(async () => ({ data: [] }))

    await tick({ notion, pb, accountMap: ACCOUNT_MAP, fetchImpl: vi.fn() })

    expect(pb.createPost).toHaveBeenCalled()
    expect(notion.updateRow).toHaveBeenCalledWith('page_3', expect.objectContaining({
      Status: { select: { name: 'Scheduled' } },
      'Post Bridge ID': { rich_text: [{ text: { content: 'pb_retry' } }] }
    }))
  })

  it('claims existing post when Notion Date is unset and post-bridge scheduled_at is null', async () => {
    // Ready row with no Date crashes after createPost; recovery must match the orphan post
    // (post-bridge returns scheduled_at: null, Notion returns date: null → undefined).
    const row = {
      id: 'page_null_date',
      last_edited_time: '2026-05-26T10:00:00.000Z',
      properties: {
        Title: { title: [{ plain_text: 'Undated post' }] },
        Status: { select: { name: 'Scheduling' } },
        Platform: { multi_select: [{ name: 'LinkedIn' }] },
        Date: { date: null },
        'Post Bridge ID': { rich_text: [] },
        Media: { type: 'files', files: [] }
      }
    }
    const blocks = [{ type: 'paragraph', paragraph: { rich_text: [{ plain_text: 'Hello world' }] } }]
    const notion = fakeNotion({ activeRows: [row], blocks })
    const pb = fakePb()
    pb.listRecentPosts = vi.fn(async () => ({
      data: [
        { id: 'pb_undated', scheduled_at: null, caption: 'Hello world' }
      ]
    }))

    await tick({ notion, pb, accountMap: ACCOUNT_MAP, fetchImpl: vi.fn() })

    expect(pb.createPost).not.toHaveBeenCalled()
    expect(notion.updateRow).toHaveBeenCalledWith('page_null_date', expect.objectContaining({
      Status: { select: { name: 'Scheduled' } },
      'Post Bridge ID': { rich_text: [{ text: { content: 'pb_undated' } }] }
    }))
  })
})

describe('tick — Scheduled polling', () => {
  it('writes back Published + per-platform URLs when post-bridge reports posted', async () => {
    const row = makeRow({ id: 'page_4', status: 'Scheduled', postBridgeId: 'pb_done' })
    const notion = fakeNotion({ activeRows: [row], blocks: [] })
    const pb = fakePb()
    pb.getPost = vi.fn(async () => ({ id: 'pb_done', status: 'posted' }))
    pb.getPostResults = vi.fn(async () => ({
      data: [
        { platform: 'linkedin', success: true, share_url: 'https://linkedin.com/posts/x' },
        { platform: 'twitter', success: true, share_url: 'https://x.com/y' }
      ]
    }))

    await tick({ notion, pb, accountMap: ACCOUNT_MAP, fetchImpl: vi.fn() })

    expect(notion.updateRow).toHaveBeenCalledWith('page_4', expect.objectContaining({
      Status: { select: { name: 'Published' } },
      'Published URLs': { rich_text: [{ text: { content: expect.stringContaining('LinkedIn: https://linkedin.com/posts/x') } }] }
    }))
  })

  it('marks Failed when post-bridge reports failed', async () => {
    const row = makeRow({ id: 'page_5', status: 'Scheduled', postBridgeId: 'pb_bad' })
    const notion = fakeNotion({ activeRows: [row], blocks: [] })
    const pb = fakePb()
    pb.getPost = vi.fn(async () => ({ id: 'pb_bad', status: 'failed', error: 'auth expired' }))

    await tick({ notion, pb, accountMap: ACCOUNT_MAP, fetchImpl: vi.fn() })

    expect(notion.updateRow).toHaveBeenCalledWith('page_5', expect.objectContaining({
      Status: { select: { name: 'Failed' } }
    }))
  })

  it('leaves Scheduled row alone when still scheduled', async () => {
    const row = makeRow({ id: 'page_6', status: 'Scheduled', postBridgeId: 'pb_wait' })
    const notion = fakeNotion({ activeRows: [row], blocks: [] })
    const pb = fakePb()
    pb.getPost = vi.fn(async () => ({ id: 'pb_wait', status: 'scheduled' }))

    await tick({ notion, pb, accountMap: ACCOUNT_MAP, fetchImpl: vi.fn() })

    // No Status change call
    const statusUpdates = notion.updateRow.mock.calls.filter(([, props]) => props.Status)
    expect(statusUpdates).toHaveLength(0)
  })
})

// Token shape: sha256(caption || scheduledAt || sortedAccountIds.join(','))[:16]
function computeEditToken(caption, scheduledAt, accountIds) {
  const sorted = [...accountIds].sort((a, b) => a - b).join(',')
  const input = `${caption}||${scheduledAt ?? ''}||${sorted}`
  return crypto.createHash('sha256').update(input).digest('hex').slice(0, 16)
}

describe('tick — edit propagation (Synced Edit Token)', () => {
  it('skips PATCH when stored token matches current caption + scheduled_at + accounts', async () => {
    const blocks = [{ type: 'paragraph', paragraph: { rich_text: [{ plain_text: 'Stable caption' }] } }]
    const matchingToken = computeEditToken('Stable caption', '2026-06-01T12:00:00.000Z', [25903])
    const row = makeRow({ id: 'page_clean', status: 'Scheduled', postBridgeId: 'pb_clean' })
    row.properties['Synced Edit Token'] = { rich_text: [{ plain_text: matchingToken }] }
    const notion = fakeNotion({ activeRows: [row], blocks })
    const pb = fakePb()
    pb.getPost = vi.fn(async () => ({ id: 'pb_clean', status: 'scheduled' }))

    await tick({ notion, pb, accountMap: ACCOUNT_MAP, fetchImpl: vi.fn() })

    expect(pb.updatePost).not.toHaveBeenCalled()
  })

  it('PATCHes and updates stored token when caption changed', async () => {
    const blocks = [{ type: 'paragraph', paragraph: { rich_text: [{ plain_text: 'Edited caption' }] } }]
    const staleToken = computeEditToken('Old caption', '2026-06-01T12:00:00.000Z', [25903])
    const row = makeRow({ id: 'page_edit', status: 'Scheduled', postBridgeId: 'pb_edit' })
    row.properties['Synced Edit Token'] = { rich_text: [{ plain_text: staleToken }] }
    const notion = fakeNotion({ activeRows: [row], blocks })
    const pb = fakePb()
    pb.getPost = vi.fn(async () => ({ id: 'pb_edit', status: 'scheduled' }))

    await tick({ notion, pb, accountMap: ACCOUNT_MAP, fetchImpl: vi.fn() })

    expect(pb.updatePost).toHaveBeenCalledWith('pb_edit', expect.objectContaining({
      caption: 'Edited caption'
    }))
    const newToken = computeEditToken('Edited caption', '2026-06-01T12:00:00.000Z', [25903])
    expect(notion.updateRow).toHaveBeenCalledWith('page_edit', expect.objectContaining({
      'Synced Edit Token': { rich_text: [{ text: { content: newToken } }] }
    }))
  })

  it('does NOT PATCH on every tick after initial scheduling (sync writeback would inflate last_edited_time)', async () => {
    // Initial scheduling stamped Last Sync At slightly before Notion's last_edited_time
    // (Notion stamps server-side AFTER our PATCH). Token approach must not confuse this for an edit.
    const blocks = [{ type: 'paragraph', paragraph: { rich_text: [{ plain_text: 'Just scheduled' }] } }]
    const token = computeEditToken('Just scheduled', '2026-06-01T12:00:00.000Z', [25903])
    const row = makeRow({ id: 'page_fresh', status: 'Scheduled', postBridgeId: 'pb_fresh' })
    row.last_edited_time = '2026-05-26T10:00:01.000Z'
    row.properties['Last Sync At'] = { date: { start: '2026-05-26T10:00:00.000Z' } }
    row.properties['Synced Edit Token'] = { rich_text: [{ plain_text: token }] }
    const notion = fakeNotion({ activeRows: [row], blocks })
    const pb = fakePb()
    pb.getPost = vi.fn(async () => ({ id: 'pb_fresh', status: 'scheduled' }))

    await tick({ notion, pb, accountMap: ACCOUNT_MAP, fetchImpl: vi.fn() })

    expect(pb.updatePost).not.toHaveBeenCalled()
  })
})

describe('tick — initial scheduling writes Synced Edit Token', () => {
  it('writes token on Ready → Scheduled transition', async () => {
    const row = makeRow({ id: 'page_seed', status: 'Ready', platforms: ['LinkedIn'] })
    const blocks = [{ type: 'paragraph', paragraph: { rich_text: [{ plain_text: 'Seed caption' }] } }]
    const notion = fakeNotion({ activeRows: [row], blocks })
    const pb = fakePb({ createReturn: { id: 'pb_seed' } })

    await tick({ notion, pb, accountMap: ACCOUNT_MAP, fetchImpl: vi.fn() })

    const expectedToken = computeEditToken('Seed caption', '2026-06-01T12:00:00.000Z', [25903])
    expect(notion.updateRow).toHaveBeenNthCalledWith(2, 'page_seed', expect.objectContaining({
      'Synced Edit Token': { rich_text: [{ text: { content: expectedToken } }] }
    }))
  })

  it('writes token on Scheduling recovery claim', async () => {
    const row = makeRow({ id: 'page_claim', status: 'Scheduling' })
    const blocks = [{ type: 'paragraph', paragraph: { rich_text: [{ plain_text: 'Claimed caption' }] } }]
    const notion = fakeNotion({ activeRows: [row], blocks })
    const pb = fakePb()
    pb.listRecentPosts = vi.fn(async () => ({
      data: [{ id: 'pb_existing', scheduled_at: '2026-06-01T12:00:00.000Z', caption: 'Claimed caption' }]
    }))

    await tick({ notion, pb, accountMap: ACCOUNT_MAP, fetchImpl: vi.fn() })

    const expectedToken = computeEditToken('Claimed caption', '2026-06-01T12:00:00.000Z', [25903])
    expect(notion.updateRow).toHaveBeenCalledWith('page_claim', expect.objectContaining({
      'Synced Edit Token': { rich_text: [{ text: { content: expectedToken } }] }
    }))
  })
})

describe('tick — revert / cancel', () => {
  it('deletes post-bridge post when row reverts from Scheduled to Drafting', async () => {
    const revertedRow = makeRow({ id: 'page_9', status: 'Drafting', postBridgeId: 'pb_to_kill' })
    const notion = {
      queryByStatus: vi.fn(async () => []),
      queryRowsWithPostBridgeIdInUserState: vi.fn(async () => [revertedRow]),
      fetchPageBlocks: vi.fn(async () => []),
      updateRow: vi.fn(async () => ({}))
    }
    const pb = fakePb()
    pb.deletePost = vi.fn(async () => ({}))

    await tick({ notion, pb, accountMap: ACCOUNT_MAP, fetchImpl: vi.fn() })

    expect(pb.deletePost).toHaveBeenCalledWith('pb_to_kill')
    expect(notion.updateRow).toHaveBeenCalledWith('page_9', expect.objectContaining({
      'Post Bridge ID': { rich_text: [] }
    }))
  })

  it('continues if post-bridge delete returns 404 (already gone)', async () => {
    const revertedRow = makeRow({ id: 'page_10', status: 'Idea', postBridgeId: 'pb_gone' })
    const notion = {
      queryByStatus: vi.fn(async () => []),
      queryRowsWithPostBridgeIdInUserState: vi.fn(async () => [revertedRow]),
      fetchPageBlocks: vi.fn(async () => []),
      updateRow: vi.fn(async () => ({}))
    }
    const pb = fakePb()
    const err404 = new Error('post-bridge DELETE -> 404: not found')
    err404.status = 404
    pb.deletePost = vi.fn(async () => { throw err404 })

    await tick({ notion, pb, accountMap: ACCOUNT_MAP, fetchImpl: vi.fn() })

    // Should still clear the Notion field
    expect(notion.updateRow).toHaveBeenCalledWith('page_10', expect.objectContaining({
      'Post Bridge ID': { rich_text: [] }
    }))
  })

  it('does NOT clear Post Bridge ID on 500 delete error (next tick retries)', async () => {
    const revertedRow = makeRow({ id: 'page_11', status: 'Drafting', postBridgeId: 'pb_500' })
    const notion = {
      queryByStatus: vi.fn(async () => []),
      queryRowsWithPostBridgeIdInUserState: vi.fn(async () => [revertedRow]),
      fetchPageBlocks: vi.fn(async () => []),
      updateRow: vi.fn(async () => ({}))
    }
    const pb = fakePb()
    const err500 = new Error('post-bridge DELETE -> 500: internal')
    err500.status = 500
    pb.deletePost = vi.fn(async () => { throw err500 })

    await tick({ notion, pb, accountMap: ACCOUNT_MAP, fetchImpl: vi.fn() })

    expect(pb.deletePost).toHaveBeenCalledWith('pb_500')
    // Critical: do NOT clear the ID — the row must stay linked so next tick retries
    expect(notion.updateRow).not.toHaveBeenCalled()
  })
})
