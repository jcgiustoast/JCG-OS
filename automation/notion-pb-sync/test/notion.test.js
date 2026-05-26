import { describe, it, expect, vi, beforeEach } from 'vitest'
import { createNotionClient } from '../src/notion.js'

const TOKEN = 'ntn_test'
const DS = 'ds_test'

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
      text: async () => JSON.stringify(next.body)
    }
  })
  fetchMock.calls = calls
  return fetchMock
}

describe('createNotionClient', () => {
  let client
  beforeEach(() => {
    client = null
  })

  it('queryByStatus posts a filtered query', async () => {
    const fetchMock = makeFetch([{ body: { results: [] } }])
    client = createNotionClient({ token: TOKEN, dataSourceId: DS, version: '2025-09-03', fetchImpl: fetchMock })
    await client.queryByStatus(['Ready'])
    expect(fetchMock.calls[0].url).toBe(`https://api.notion.com/v1/data_sources/${DS}/query`)
    expect(fetchMock.calls[0].opts.method).toBe('POST')
    const sent = JSON.parse(fetchMock.calls[0].opts.body)
    expect(sent.filter.or).toHaveLength(1)
    expect(sent.filter.or[0]).toEqual({ property: 'Status', select: { equals: 'Ready' } })
  })

  it('queryByStatus handles multiple statuses with OR', async () => {
    const fetchMock = makeFetch([{ body: { results: [] } }])
    client = createNotionClient({ token: TOKEN, dataSourceId: DS, version: '2025-09-03', fetchImpl: fetchMock })
    await client.queryByStatus(['Ready', 'Scheduling', 'Scheduled'])
    const sent = JSON.parse(fetchMock.calls[0].opts.body)
    expect(sent.filter.or).toHaveLength(3)
  })

  it('fetchPageBlocks paginates until has_more is false', async () => {
    const fetchMock = makeFetch([
      { body: { results: [{ id: 'b1' }], has_more: true, next_cursor: 'cur1' } },
      { body: { results: [{ id: 'b2' }], has_more: false } }
    ])
    client = createNotionClient({ token: TOKEN, dataSourceId: DS, version: '2025-09-03', fetchImpl: fetchMock })
    const blocks = await client.fetchPageBlocks('page_x')
    expect(blocks).toEqual([{ id: 'b1' }, { id: 'b2' }])
    expect(fetchMock.calls).toHaveLength(2)
    expect(fetchMock.calls[1].url).toContain('start_cursor=cur1')
  })

  it('updateRow sends PATCH with properties', async () => {
    const fetchMock = makeFetch([{ body: { id: 'page_x' } }])
    client = createNotionClient({ token: TOKEN, dataSourceId: DS, version: '2025-09-03', fetchImpl: fetchMock })
    await client.updateRow('page_x', {
      Status: { select: { name: 'Scheduled' } },
      'Post Bridge ID': { rich_text: [{ text: { content: 'pb_123' } }] }
    })
    expect(fetchMock.calls[0].url).toBe('https://api.notion.com/v1/pages/page_x')
    expect(fetchMock.calls[0].opts.method).toBe('PATCH')
    const sent = JSON.parse(fetchMock.calls[0].opts.body)
    expect(sent.properties.Status.select.name).toBe('Scheduled')
  })

  it('throws with message on non-OK response', async () => {
    const fetchMock = makeFetch([{ ok: false, status: 400, body: { message: 'Bad property' } }])
    client = createNotionClient({ token: TOKEN, dataSourceId: DS, version: '2025-09-03', fetchImpl: fetchMock })
    await expect(client.updateRow('page_x', {})).rejects.toThrow(/Bad property|400/)
  })
})
