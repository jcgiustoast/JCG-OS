const PLATFORM_LIMITS = {
  Twitter: 280
}

function extractPlainText(richText) {
  if (!Array.isArray(richText)) return ''
  return richText.map(t => t.plain_text || '').join('')
}

export function blocksToCaption(blocks) {
  const lines = []
  for (const block of blocks) {
    const text = renderBlock(block)
    if (text !== null) lines.push(text)
  }
  return joinBlocks(lines)
}

function renderBlock(block) {
  switch (block.type) {
    case 'paragraph':
      return extractPlainText(block.paragraph?.rich_text)
    case 'heading_1':
    case 'heading_2':
    case 'heading_3':
      return extractPlainText(block[block.type]?.rich_text)
    case 'bulleted_list_item':
      return '- ' + extractPlainText(block.bulleted_list_item?.rich_text)
    case 'numbered_list_item':
      return '- ' + extractPlainText(block.numbered_list_item?.rich_text)
    case 'quote':
      return '> ' + extractPlainText(block.quote?.rich_text)
    default:
      return null
  }
}

function joinBlocks(lines) {
  const out = []
  for (let i = 0; i < lines.length; i++) {
    const prev = lines[i - 1]
    const curr = lines[i]
    const bothLists = prev?.startsWith('- ') && curr.startsWith('- ')
    out.push((bothLists ? '\n' : (i === 0 ? '' : '\n\n')) + curr)
  }
  return out.join('').trim()
}

export function stripSourcesHeader(text) {
  // Header pattern: starts with **Sources:** or **Wiki:**, followed by a --- separator
  const headerRe = /^(\*\*Sources:\*\*[^\n]*\n)?(\*\*Wiki:\*\*[^\n]*\n)?(\n---\n\n)/
  if (!headerRe.test(text)) return text
  return text.replace(headerRe, '').trimStart()
}

export function validateForPlatforms(caption, platforms) {
  for (const platform of platforms) {
    const limit = PLATFORM_LIMITS[platform]
    if (limit && caption.length > limit) {
      return {
        ok: false,
        reason: `${platform} caption is ${caption.length} chars, limit is ${limit}`
      }
    }
  }
  return { ok: true }
}
