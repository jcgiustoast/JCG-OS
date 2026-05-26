import { describe, it, expect } from 'vitest'
import { blocksToCaption, stripSourcesHeader, validateForPlatforms } from '../src/caption.js'

describe('blocksToCaption', () => {
  it('joins paragraph blocks with double newlines', () => {
    const blocks = [
      { type: 'paragraph', paragraph: { rich_text: [{ plain_text: 'First line.' }] } },
      { type: 'paragraph', paragraph: { rich_text: [{ plain_text: 'Second line.' }] } }
    ]
    expect(blocksToCaption(blocks)).toBe('First line.\n\nSecond line.')
  })

  it('handles bulleted_list_item', () => {
    const blocks = [
      { type: 'bulleted_list_item', bulleted_list_item: { rich_text: [{ plain_text: 'one' }] } },
      { type: 'bulleted_list_item', bulleted_list_item: { rich_text: [{ plain_text: 'two' }] } }
    ]
    expect(blocksToCaption(blocks)).toBe('- one\n- two')
  })

  it('handles heading_2', () => {
    const blocks = [
      { type: 'heading_2', heading_2: { rich_text: [{ plain_text: 'Headline' }] } }
    ]
    expect(blocksToCaption(blocks)).toBe('Headline')
  })

  it('returns empty string for empty input', () => {
    expect(blocksToCaption([])).toBe('')
  })

  it('skips unknown block types silently', () => {
    const blocks = [
      { type: 'paragraph', paragraph: { rich_text: [{ plain_text: 'Keep this.' }] } },
      { type: 'image', image: {} },
      { type: 'paragraph', paragraph: { rich_text: [{ plain_text: 'And this.' }] } }
    ]
    expect(blocksToCaption(blocks)).toBe('Keep this.\n\nAnd this.')
  })

  it('does not merge two lists separated by an unknown block', () => {
    const blocks = [
      { type: 'bulleted_list_item', bulleted_list_item: { rich_text: [{ plain_text: 'a' }] } },
      { type: 'image', image: {} },
      { type: 'bulleted_list_item', bulleted_list_item: { rich_text: [{ plain_text: 'b' }] } }
    ]
    expect(blocksToCaption(blocks)).toBe('- a\n\n- b')
  })
})

describe('stripSourcesHeader', () => {
  it('removes the Sources header block', () => {
    const input = '**Sources:** [a](url), [b](url)\n\n---\n\nReal content here.'
    expect(stripSourcesHeader(input)).toBe('Real content here.')
  })

  it('removes Sources + Wiki header', () => {
    const input = '**Sources:** [a](url)\n**Wiki:** [b](url)\n\n---\n\nReal content.'
    expect(stripSourcesHeader(input)).toBe('Real content.')
  })

  it('leaves input untouched when no header', () => {
    expect(stripSourcesHeader('Just content.')).toBe('Just content.')
  })

  it('does not strip a leading --- with no header', () => {
    const input = '\n---\n\nLegit content with a divider at top.'
    expect(stripSourcesHeader(input)).toBe('\n---\n\nLegit content with a divider at top.')
  })

  it('strips Wiki-only header (no Sources)', () => {
    const input = '**Wiki:** [b](url)\n\n---\n\nContent.'
    expect(stripSourcesHeader(input)).toBe('Content.')
  })
})

describe('validateForPlatforms', () => {
  it('passes a short caption for any platform', () => {
    const result = validateForPlatforms('short', ['Twitter', 'LinkedIn'])
    expect(result.ok).toBe(true)
  })

  it('fails Twitter when over 280 chars', () => {
    const longCaption = 'x'.repeat(281)
    const result = validateForPlatforms(longCaption, ['Twitter'])
    expect(result.ok).toBe(false)
    expect(result.reason).toMatch(/Twitter.*280/)
  })

  it('passes 280-char caption on Twitter', () => {
    const exactly280 = 'x'.repeat(280)
    expect(validateForPlatforms(exactly280, ['Twitter']).ok).toBe(true)
  })

  it('allows long captions when Twitter not selected', () => {
    const longCaption = 'x'.repeat(500)
    expect(validateForPlatforms(longCaption, ['LinkedIn']).ok).toBe(true)
  })
})
