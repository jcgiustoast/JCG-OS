export function createPostBridgeClient({ apiKey, baseUrl = 'https://api.post-bridge.com', fetchImpl = fetch }) {
  const headers = {
    'Authorization': `Bearer ${apiKey}`,
    'Content-Type': 'application/json'
  }

  async function call(method, path, body) {
    const opts = { method, headers }
    if (body !== undefined) opts.body = JSON.stringify(body)
    const res = await fetchImpl(`${baseUrl}${path}`, opts)
    if (!res.ok) {
      const text = await res.text()
      throw new Error(`post-bridge ${method} ${path} -> ${res.status}: ${text}`)
    }
    return res.json()
  }

  async function createPost(payload) {
    return call('POST', '/v1/posts', payload)
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

  async function listRecentPosts({ status, limit = 50 } = {}) {
    const params = { limit: String(limit) }
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
