export function extractFiles(prop) {
  if (!prop || prop.type !== 'files' || !Array.isArray(prop.files)) return []
  return prop.files
    .map(f => {
      if (f.type === 'file') return { name: f.name, url: f.file?.url }
      if (f.type === 'external') return { name: f.name, url: f.external?.url }
      return null
    })
    .filter(f => f && f.url)
}

export async function uploadNotionFilesToPostBridge(files, { pb, fetchImpl = fetch }) {
  const mediaIds = []
  for (const file of files) {
    const downloadRes = await fetchImpl(file.url)
    if (!downloadRes.ok) {
      throw new Error(`Failed to download Notion file ${file.name}: ${downloadRes.status}`)
    }
    const mimeType = downloadRes.headers.get('content-type') || 'application/octet-stream'
    const buffer = await downloadRes.arrayBuffer()
    const { media_id, upload_url } = await pb.createUploadUrl({
      mime_type: mimeType,
      size_bytes: buffer.byteLength,
      name: file.name
    })
    await pb.uploadMedia({ uploadUrl: upload_url, mimeType, buffer })
    mediaIds.push(media_id)
  }
  return mediaIds
}
