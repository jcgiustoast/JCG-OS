const PLATFORM_LIMITS = {
  Twitter: 280
}

function extractPlainText(richText) {
  if (!Array.isArray(richText)) return ''
  return richText.map(t => t.plain_text || '').join('')
}

export function blocksToCaption(blocks) {
  const items = blocks.map(b => ({ type: b.type, text: renderBlock(b) }))
  return joinBlocks(items)
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

function joinBlocks(items) {
  const out = []
  let prevType = null
  let prevText = null
  for (const item of items) {
    if (item.text === null) {
      // Unknown block — emits no text, but breaks list adjacency
      prevType = null
      continue
    }
    const listMerge =
      prevText !== null &&
      prevType === item.type &&
      (item.type === 'bulleted_list_item' || item.type === 'numbered_list_item')
    const sep = prevText === null ? '' : (listMerge ? '\n' : '\n\n')
    out.push(sep + item.text)
    prevType = item.type
    prevText = item.text
  }
  return out.join('').trim()
}

export function stripSourcesHeader(text) {
  // Header pattern: at least one of **Sources:** or **Wiki:** lines, then \n---\n\n separator
  const headerRe = /^(?:\*\*Sources:\*\*[^\n]*\n(?:\*\*Wiki:\*\*[^\n]*\n)?|\*\*Wiki:\*\*[^\n]*\n)\n---\n\n/
  if (!headerRe.test(text)) return text
  return text.replace(headerRe, '').trimStart()
}

export function validateForPlatforms(caption, platforms) {
  for (const platform of platforms) {
    const limit = PLATFORM_LIMITS[platform]
    // post-bridge strips links from X posts; the sync moves them to the first comment,
    // so X is measured on the text that actually gets posted.
    const text = platform === 'Twitter' ? splitLinksForX(caption).text : caption
    if (limit && text.length > limit) {
      return {
        ok: false,
        reason: `${platform} caption is ${text.length} chars, limit is ${limit}`
      }
    }
  }
  return { ok: true }
}

// Same link shapes post-bridge strips from X: full URLs, www. links, bare domains.
const LINK_RE = /(?:https?:\/\/|www\.)\S+|\b[a-z0-9][a-z0-9-]*(?:\.[a-z0-9-]+)*\.(?:com|io|co|net|org|ai|dev|app|me|so|xyz|es|ar|us|shop|store)\b(?:\/\S*)?/gi
const TRAILING_PUNCT_RE = /[.,;:!?)\]]+$/

export function splitLinksForX(caption) {
  const links = []
  const stripped = caption.replace(LINK_RE, match => {
    const trail = match.match(TRAILING_PUNCT_RE)?.[0] || ''
    links.push(trail ? match.slice(0, -trail.length) : match)
    return trail
  })
  if (links.length === 0) return { text: caption, firstComment: null }
  const text = stripped
    .split('\n')
    .map(line => line.replace(/ +([.,;:!?])/g, '$1').replace(/ {2,}/g, ' ').trim())
    .join('\n')
    .replace(/\n{3,}/g, '\n\n')
    .trim()
  return { text, firstComment: links.join('\n') }
}
