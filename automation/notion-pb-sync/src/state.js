export const STATUS = Object.freeze({
  IDEA: 'Idea',
  RESEARCHING: 'Researching',
  DRAFTING: 'Drafting',
  READY: 'Ready',
  SCHEDULING: 'Scheduling',
  SCHEDULED: 'Scheduled',
  PUBLISHED: 'Published',
  FAILED: 'Failed'
})

const ALL_STATES = new Set(Object.values(STATUS))

const ALLOWED = {
  Idea: ['Researching', 'Drafting', 'Ready'],
  Researching: ['Drafting', 'Ready', 'Idea'],
  Drafting: ['Ready', 'Idea'],
  Ready: ['Scheduling', 'Drafting'],
  Scheduling: ['Scheduled', 'Failed', 'Ready'],
  Scheduled: ['Published', 'Failed', 'Drafting', 'Idea', 'Ready'],
  Published: [],
  Failed: ['Drafting', 'Ready']
}

export function isValidTransition(from, to) {
  if (!ALL_STATES.has(from) || !ALL_STATES.has(to)) return false
  if (to === STATUS.FAILED) return true
  return ALLOWED[from].includes(to)
}

const SYNC_OWNED = new Set([STATUS.SCHEDULING, STATUS.SCHEDULED, STATUS.PUBLISHED, STATUS.FAILED])

export function isSyncOwnedTransition(state) {
  return SYNC_OWNED.has(state)
}
