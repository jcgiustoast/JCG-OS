export function createPostBridgeClient({ apiKey, baseUrl = 'https://api.post-bridge.com', fetchImpl = fetch, retryDelays = [200, 1000, 5000] }) {
  const headers = {
    'Authorization': `Bearer ${apiKey}`,
    'Content-Type': 'application/json'
  }

  async function rawCall(method, path, body) {
    const opts = { method, headers }
    if (body !== undefined) opts.body = JSON.stringify(body)
    const res = await fetchImpl(`${baseUrl}${path}`, opts)
    if (!res.ok) {
      const text = await res.text()
      const err = new Error(`post-bridge ${method} ${path} -> ${res.status}: ${text}`)
      err.status = res.status
      throw err
    }
    return res.json()
  }

  async function call(method, path, body, { retry = true } = {}) {
    if (!retry) return rawCall(method, path, body)
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

  async function createPost(payload) {
    // POST /v1/posts is NOT idempotent — a 5xx after server-side commit would
    // silently double-create. Skip retry; recovery handles transient failure
    // by claiming the orphan via caption-hash lookup on the next tick.
    return call('POST', '/v1/posts', payload, { retry: false })
  }

  async function getPost(id) {
    return call('GET', `/v1/posts/${id}`)
  }

  async function updatePost(id, patch) {
    return call('PATCH', `/v1/posts/${id}`, patch)
  }

  async function deletePost(id) {
    return call('DELETE', `/v1/posts/${id}`)
  }

  async function getPostResults(postId) {
    const qs = new URLSearchParams({ post_id: postId, limit: '50' }).toString()
    return call('GET', `/v1/post-results?${qs}`)
  }

  async function listRecentPosts({ status, limit = 50, offset = 0 } = {}) {
    const params = { limit: String(limit), offset: String(offset) }
    if (status) params.status = status
    const qs = new URLSearchParams(params).toString()
    return call('GET', `/v1/posts?${qs}`)
  }

  async function createUploadUrl({ mime_type, size_bytes, name }) {
    return call('POST', '/v1/media/create-upload-url', { mime_type, size_bytes, name })
  }

  async function uploadMedia({ uploadUrl, mimeType, buffer }) {
    const res = await fetchImpl(uploadUrl, {
      method: 'PUT',
      headers: { 'Content-Type': mimeType },
      body: buffer
    })
    if (!res.ok) {
      const text = await res.text()
      throw new Error(`post-bridge upload PUT -> ${res.status}: ${text}`)
    }
  }

  return { createPost, getPost, updatePost, deletePost, getPostResults, listRecentPosts, createUploadUrl, uploadMedia }
}
