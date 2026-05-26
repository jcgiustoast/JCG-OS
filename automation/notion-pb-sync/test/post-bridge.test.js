import { describe, it, expect, vi } from 'vitest'
import { createPostBridgeClient } from '../src/post-bridge.js'

function makeFetch(responses) {
  const calls = []
  const fetchMock = vi.fn(async (url, opts) => {
    calls.push({ url, opts })
    const next = responses.shift()
    if (!next) throw new Error('No mocked response left')
    return {
      ok: next.ok ?? true,
      status: next.status ?? 200,
      json: async () => next.body,
      text: async () => JSON.stringify(next.body ?? {})
    }
  })
  fetchMock.calls = calls
  return fetchMock
}

const cfg = { apiKey: 'pb_x', baseUrl: 'https://api.post-bridge.com' }

describe('post-bridge client', () => {
  it('createPost POSTs to /v1/posts', async () => {
    const fetchMock = makeFetch([{ body: { id: 'p_1', status: 'scheduled' } }])
    const client = createPostBridgeClient({ ...cfg, fetchImpl: fetchMock })
    const result = await client.createPost({
      caption: 'Hello',
      social_accounts: [25903],
      scheduled_at: '2026-06-01T12:00:00Z'
    })
    expect(result.id).toBe('p_1')
    expect(fetchMock.calls[0].url).toBe('https://api.post-bridge.com/v1/posts')
    expect(fetchMock.calls[0].opts.method).toBe('POST')
    const sent = JSON.parse(fetchMock.calls[0].opts.body)
    expect(sent.caption).toBe('Hello')
    expect(sent.social_accounts).toEqual([25903])
  })

  it('getPost GETs /v1/posts/:id', async () => {
    const fetchMock = makeFetch([{ body: { id: 'p_1', status: 'posted' } }])
    const client = createPostBridgeClient({ ...cfg, fetchImpl: fetchMock })
    const result = await client.getPost('p_1')
    expect(result.status).toBe('posted')
    expect(fetchMock.calls[0].url).toBe('https://api.post-bridge.com/v1/posts/p_1')
    expect(fetchMock.calls[0].opts.method).toBe('GET')
  })

  it('updatePost PATCHes /v1/posts/:id', async () => {
    const fetchMock = makeFetch([{ body: { id: 'p_1' } }])
    const client = createPostBridgeClient({ ...cfg, fetchImpl: fetchMock })
    await client.updatePost('p_1', { caption: 'new' })
    expect(fetchMock.calls[0].opts.method).toBe('PATCH')
  })

  it('deletePost DELETEs /v1/posts/:id', async () => {
    const fetchMock = makeFetch([{ body: {} }])
    const client = createPostBridgeClient({ ...cfg, fetchImpl: fetchMock })
    await client.deletePost('p_1')
    expect(fetchMock.calls[0].opts.method).toBe('DELETE')
  })

  it('getPostResults GETs /v1/post-results with query', async () => {
    const fetchMock = makeFetch([{ body: { data: [] } }])
    const client = createPostBridgeClient({ ...cfg, fetchImpl: fetchMock })
    await client.getPostResults('p_1')
    expect(fetchMock.calls[0].url).toContain('/v1/post-results')
    expect(fetchMock.calls[0].url).toContain('post_id=p_1')
  })

  it('listRecentPosts GETs /v1/posts with filters', async () => {
    const fetchMock = makeFetch([{ body: { data: [], count: 0 } }])
    const client = createPostBridgeClient({ ...cfg, fetchImpl: fetchMock })
    await client.listRecentPosts({ status: 'scheduled', limit: 50 })
    expect(fetchMock.calls[0].url).toContain('status=scheduled')
    expect(fetchMock.calls[0].url).toContain('limit=50')
  })

  it('createUploadUrl POSTs to /v1/media/create-upload-url', async () => {
    const fetchMock = makeFetch([{ body: { media_id: 'm_1', upload_url: 'https://...' } }])
    const client = createPostBridgeClient({ ...cfg, fetchImpl: fetchMock })
    const result = await client.createUploadUrl({ mime_type: 'image/jpeg', size_bytes: 1234, name: 'a.jpg' })
    expect(result.media_id).toBe('m_1')
    expect(fetchMock.calls[0].url).toBe('https://api.post-bridge.com/v1/media/create-upload-url')
  })

  it('throws on non-OK response', async () => {
    const fetchMock = makeFetch([{ ok: false, status: 401, body: { message: 'unauthorized' } }])
    const client = createPostBridgeClient({ ...cfg, fetchImpl: fetchMock })
    await expect(client.getPost('p_1')).rejects.toThrow(/401|unauthorized/)
  })
})
