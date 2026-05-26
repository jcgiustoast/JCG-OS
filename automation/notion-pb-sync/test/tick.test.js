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
