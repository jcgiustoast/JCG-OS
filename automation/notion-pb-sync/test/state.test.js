import { describe, it, expect } from 'vitest'
import { STATUS, isValidTransition, isSyncOwnedTransition } from '../src/state.js'

describe('STATUS enum', () => {
  it('contains all expected values', () => {
    expect(STATUS).toEqual({
      IDEA: 'Idea',
      RESEARCHING: 'Researching',
      DRAFTING: 'Drafting',
      READY: 'Ready',
      SCHEDULING: 'Scheduling',
      SCHEDULED: 'Scheduled',
      PUBLISHED: 'Published',
      FAILED: 'Failed'
    })
  })
})

describe('isValidTransition', () => {
  it('allows Ready -> Scheduling', () => {
    expect(isValidTransition('Ready', 'Scheduling')).toBe(true)
  })

  it('allows Scheduling -> Scheduled', () => {
    expect(isValidTransition('Scheduling', 'Scheduled')).toBe(true)
  })

  it('allows Scheduled -> Published', () => {
    expect(isValidTransition('Scheduled', 'Published')).toBe(true)
  })

  it('allows any state -> Failed', () => {
    expect(isValidTransition('Ready', 'Failed')).toBe(true)
    expect(isValidTransition('Scheduled', 'Failed')).toBe(true)
  })

  it('rejects unknown source state', () => {
    expect(isValidTransition('Bogus', 'Scheduled')).toBe(false)
  })

  it('rejects illegal Published -> Ready', () => {
    expect(isValidTransition('Published', 'Ready')).toBe(false)
  })
})

describe('isSyncOwnedTransition', () => {
  it('Scheduling, Scheduled, Published, Failed are sync-owned', () => {
    expect(isSyncOwnedTransition('Scheduling')).toBe(true)
    expect(isSyncOwnedTransition('Scheduled')).toBe(true)
    expect(isSyncOwnedTransition('Published')).toBe(true)
    expect(isSyncOwnedTransition('Failed')).toBe(true)
  })

  it('user-owned states return false', () => {
    expect(isSyncOwnedTransition('Idea')).toBe(false)
    expect(isSyncOwnedTransition('Researching')).toBe(false)
    expect(isSyncOwnedTransition('Drafting')).toBe(false)
    expect(isSyncOwnedTransition('Ready')).toBe(false)
  })
})
