const BLOCKLIST = [
  /\bmars\s*men\b/i,
  /\bmeta\s*ads?\b/i,
  /\basteroi\s+founder\b/i
]

export function checkPhase1Firewall(title, body) {
  const haystack = `${title ?? ''}\n${body ?? ''}`
  for (const pattern of BLOCKLIST) {
    const match = haystack.match(pattern)
    if (match) {
      return { blocked: true, matched: match[0] }
    }
  }
  return { blocked: false }
}
