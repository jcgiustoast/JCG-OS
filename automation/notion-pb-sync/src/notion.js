export function createNotionClient({ token, dataSourceId, version, fetchImpl = fetch, retryDelays = [200, 1000, 5000] }) {
  const base = 'https://api.notion.com/v1'
  const headers = {
    'Authorization': `Bearer ${token}`,
    'Notion-Version': version,
    'Content-Type': 'application/json'
  }

  async function rawCall(method, path, body) {
    const opts = { method, headers }
    if (body !== undefined) opts.body = JSON.stringify(body)
    const res = await fetchImpl(`${base}${path}`, opts)
    if (!res.ok) {
      const text = await res.text()
      const err = new Error(`Notion ${method} ${path} -> ${res.status}: ${text}`)
      err.status = res.status
      throw err
    }
    return res.json()
  }

  async function call(method, path, body) {
    for (let i = 0; i <= retryDelays.length; i++) {
      try {
        return await rawCall(method, path, body)
      } catch (err) {
        const retryable = err.status === 429 || (err.status >= 500 && err.status < 600)
        if (!retryable || i === retryDelays.length) throw err
        await new Promise(r => setTimeout(r, retryDelays[i]))
      }
    }
  }

  async function queryByStatus(statuses) {
    const filter = {
      or: statuses.map(name => ({ property: 'Status', select: { equals: name } }))
    }
    const result = await call('POST', `/data_sources/${dataSourceId}/query`, { filter, page_size: 100 })
    return result.results
  }

  async function queryRowsWithPostBridgeIdInUserState() {
    // Rows where Post Bridge ID is set but Status is user-owned (revert/cancel)
    const filter = {
      and: [
        { property: 'Post Bridge ID', rich_text: { is_not_empty: true } },
        {
          or: [
            { property: 'Status', select: { equals: 'Idea' } },
            { property: 'Status', select: { equals: 'Drafting' } },
            { property: 'Status', select: { equals: 'Ready' } }
          ]
        }
      ]
    }
    const result = await call('POST', `/data_sources/${dataSourceId}/query`, { filter, page_size: 100 })
    return result.results
  }

  async function fetchPageBlocks(pageId) {
    const out = []
    let cursor = null
    while (true) {
      const qs = cursor ? `?start_cursor=${encodeURIComponent(cursor)}&page_size=100` : '?page_size=100'
      const result = await call('GET', `/blocks/${pageId}/children${qs}`)
      out.push(...result.results)
      if (!result.has_more) break
      cursor = result.next_cursor
    }
    return out
  }

  async function updateRow(pageId, properties) {
    return call('PATCH', `/pages/${pageId}`, { properties })
  }

  return { queryByStatus, queryRowsWithPostBridgeIdInUserState, fetchPageBlocks, updateRow }
}
