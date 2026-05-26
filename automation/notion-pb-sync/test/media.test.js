import { describe, it, expect, vi } from 'vitest'
import { uploadNotionFilesToPostBridge, extractFiles } from '../src/media.js'

describe('extractFiles', () => {
  it('reads files from a Notion Files property', () => {
    const prop = {
      type: 'files',
      files: [
        { name: 'a.jpg', type: 'file', file: { url: 'https://notion-s3/a.jpg' } },
        { name: 'b.mp4', type: 'external', external: { url: 'https://cdn/b.mp4' } }
      ]
    }
    const out = extractFiles(prop)
    expect(out).toEqual([
      { name: 'a.jpg', url: 'https://notion-s3/a.jpg' },
      { name: 'b.mp4', url: 'https://cdn/b.mp4' }
    ])
  })

  it('returns empty array for missing property', () => {
    expect(extractFiles(undefined)).toEqual([])
    expect(extractFiles({ type: 'files', files: [] })).toEqual([])
  })
})

describe('uploadNotionFilesToPostBridge', () => {
  it('downloads each file, requests upload URL, PUTs binary, returns media_ids', async () => {
    const downloads = [
      { ok: true, headers: { get: (h) => h === 'content-type' ? 'image/jpeg' : null }, arrayBuffer: async () => new Uint8Array([1,2,3]).buffer }
    ]
    const fetchImpl = vi.fn(async (url) => {
      const next = downloads.shift()
      if (next) return next
      throw new Error('No mocked download left')
    })
    const pb = {
      createUploadUrl: vi.fn(async ({ name }) => ({ media_id: `m_${name}`, upload_url: `https://upload/${name}` })),
      uploadMedia: vi.fn(async () => {})
    }
    const result = await uploadNotionFilesToPostBridge(
      [{ name: 'a.jpg', url: 'https://notion-s3/a.jpg' }],
      { pb, fetchImpl }
    )
    expect(result).toEqual(['m_a.jpg'])
    expect(pb.createUploadUrl).toHaveBeenCalledWith({ mime_type: 'image/jpeg', size_bytes: 3, name: 'a.jpg' })
    expect(pb.uploadMedia).toHaveBeenCalledWith({ uploadUrl: 'https://upload/a.jpg', mimeType: 'image/jpeg', buffer: expect.any(ArrayBuffer) })
  })

  it('returns empty array for empty input', async () => {
    const result = await uploadNotionFilesToPostBridge([], { pb: {}, fetchImpl: vi.fn() })
    expect(result).toEqual([])
  })
})
