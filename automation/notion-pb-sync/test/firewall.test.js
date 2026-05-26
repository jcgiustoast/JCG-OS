import { describe, it, expect } from 'vitest'
import { checkPhase1Firewall } from '../src/firewall.js'

describe('checkPhase1Firewall', () => {
  it('passes clean content', () => {
    const result = checkPhase1Firewall('Hello world', 'A normal post body.')
    expect(result.blocked).toBe(false)
  })

  it('blocks "Mars Men" in title', () => {
    const result = checkPhase1Firewall('How Mars Men is doing X', 'Body.')
    expect(result.blocked).toBe(true)
    expect(result.matched).toMatch(/mars/i)
  })

  it('blocks "meta ads" in body, case-insensitive', () => {
    const result = checkPhase1Firewall('Generic title', 'I run META ADS for clients.')
    expect(result.blocked).toBe(true)
    expect(result.matched).toMatch(/meta/i)
  })

  it('blocks "marsmen" (no space)', () => {
    expect(checkPhase1Firewall('marsmen rules', 'body').blocked).toBe(true)
  })

  it('blocks "asteroi founder"', () => {
    expect(checkPhase1Firewall('title', 'as ASTEROI founder I think...').blocked).toBe(true)
  })

  it('does not block standalone "asteroi"', () => {
    expect(checkPhase1Firewall('title', 'asteroi as a product').blocked).toBe(false)
  })
})
