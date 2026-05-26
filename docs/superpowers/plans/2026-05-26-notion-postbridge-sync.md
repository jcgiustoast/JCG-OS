# Notion → post-bridge Publish Sync Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a stateless Node.js cron service on Railway that reconciles Notion Content DB rows with post-bridge: when a row flips to `Ready`, the sync schedules the post; status + URLs writeback automatically.

**Architecture:** One `tick()` function called every 5 min via Railway cron. Reads Notion → reconciles each row's `Status` with post-bridge → writes back. No DB, no queue, no webhooks. Crash safety via a `Scheduling` intermediate status + caption-hash recovery lookup.

**Tech Stack:** Node.js 20 (ESM), native `fetch`, vitest for tests, Railway for runtime + cron. No HTTP framework — the service is invoked by cron, not by inbound HTTP.

**Spec reference:** `docs/superpowers/specs/2026-05-26-notion-postbridge-sync-design.md`

---

## Prerequisites (do these before starting Task 1)

1. **Create a worktree** for this work using the `superpowers:using-git-worktrees` skill. Branch name suggestion: `feat/notion-pb-sync`.
2. **Confirm env vars available** in the dev shell:
   - `POST_BRIDGE_API_KEY` (already set in Windows user scope per handoff)
   - Notion credentials live in `content/.notion-config.json` (gitignored) — values can be exported locally during testing.
3. **Do NOT push to `master`.** All work lands on the feature branch → PR.

## File structure

```
automation/notion-pb-sync/
├── package.json              # Node project + deps + scripts
├── README.md                 # How to run locally, env vars, deploy
├── railway.toml              # Railway cron schedule config
├── .env.example              # All env vars documented (no secrets)
├── .gitignore                # node_modules, .env, etc.
├── vitest.config.js          # Test runner config
├── src/
│   ├── index.js              # Bootstrap: load config, call tick(), exit
│   ├── config.js             # Env var loading + validation
│   ├── tick.js               # Main reconciliation loop
│   ├── notion.js             # Notion API client (query, update, fetch body)
│   ├── post-bridge.js        # post-bridge API client
│   ├── media.js              # Notion file → post-bridge media_id
│   ├── caption.js            # Notion blocks → caption text, validate limits
│   ├── firewall.js           # Phase 1 keyword blocklist
│   └── state.js              # Status enum + transition validation
├── scripts/
│   └── apply-schema.js       # Idempotent Notion schema setup (one-off)
└── test/
    ├── caption.test.js
    ├── firewall.test.js
    ├── state.test.js
    ├── notion.test.js
    ├── post-bridge.test.js
    ├── media.test.js
    └── tick.test.js
```

**Why this shape:** pure-logic files (`caption`, `firewall`, `state`) are testable without mocks. API clients (`notion`, `post-bridge`, `media`) wrap `fetch` and are tested with mocked responses. `tick.js` orchestrates and is tested with mocked clients. `index.js` is a thin shell — no logic.

**Build order:** pure logic first (TDD-friendly, no mocking) → API clients → tick orchestration → entry point + Railway config → schema script → manual e2e.

---

### Task 1: Scaffold the Node project

**Files:**
- Create: `automation/notion-pb-sync/package.json`
- Create: `automation/notion-pb-sync/.gitignore`
- Create: `automation/notion-pb-sync/.env.example`
- Create: `automation/notion-pb-sync/vitest.config.js`
- Create: `automation/notion-pb-sync/README.md`

- [ ] **Step 1: Create the directory and `package.json`**

```bash
mkdir -p automation/notion-pb-sync/src automation/notion-pb-sync/test automation/notion-pb-sync/scripts
```

Write `automation/notion-pb-sync/package.json`:

```json
{
  "name": "notion-pb-sync",
  "version": "0.1.0",
  "private": true,
  "type": "module",
  "engines": {
    "node": ">=20"
  },
  "scripts": {
    "start": "node src/index.js",
    "test": "vitest run",
    "test:watch": "vitest",
    "schema:apply": "node scripts/apply-schema.js"
  },
  "devDependencies": {
    "vitest": "^2.0.0"
  }
}
```

- [ ] **Step 2: Create `.gitignore`**

Write `automation/notion-pb-sync/.gitignore`:

```
node_modules/
.env
.env.local
*.log
coverage/
```

- [ ] **Step 3: Create `.env.example`**

Write `automation/notion-pb-sync/.env.example`:

```
# Notion
NOTION_TOKEN=
NOTION_CONTENT_DATA_SOURCE_ID=
NOTION_VERSION=2025-09-03

# post-bridge
POST_BRIDGE_API_KEY=

# Social account ID mapping (verified 2026-05-26)
PB_ACCOUNT_LINKEDIN=25903
PB_ACCOUNT_THREADS=25902
PB_ACCOUNT_TIKTOK=25901
PB_ACCOUNT_YOUTUBE=25900
PB_ACCOUNT_TWITTER=25899
PB_ACCOUNT_INSTAGRAM=25898
```

- [ ] **Step 4: Create `vitest.config.js`**

Write `automation/notion-pb-sync/vitest.config.js`:

```js
import { defineConfig } from 'vitest/config'

export default defineConfig({
  test: {
    environment: 'node',
    coverage: {
      provider: 'v8',
      reporter: ['text', 'html'],
      include: ['src/**/*.js']
    }
  }
})
```

- [ ] **Step 5: Create `README.md`**

Write `automation/notion-pb-sync/README.md`:

```markdown
# notion-pb-sync

One-way sync from the Notion Content DB to post-bridge. Notion is the source of truth for the content calendar; post-bridge is the executor.

See spec at `docs/superpowers/specs/2026-05-26-notion-postbridge-sync-design.md`.

## Local run

1. Copy `.env.example` to `.env` and fill in values.
2. `npm install`
3. `npm test` — run unit tests
4. `npm run schema:apply` — one-off, applies Notion schema changes
5. `npm start` — runs one tick and exits

## Deploy

Push to Railway with `railway.toml` cron config. See spec deployment section.
```

- [ ] **Step 6: Install deps + verify**

```bash
cd automation/notion-pb-sync
npm install
```

Expected: `node_modules/` created with vitest installed. No errors.

- [ ] **Step 7: Commit**

```bash
git add automation/notion-pb-sync
git commit -m "feat(sync): scaffold notion-pb-sync project"
```

---

### Task 2: `state.js` — Status enum + transitions

**Files:**
- Create: `automation/notion-pb-sync/src/state.js`
- Create: `automation/notion-pb-sync/test/state.test.js`

- [ ] **Step 1: Write the failing tests**

Write `automation/notion-pb-sync/test/state.test.js`:

```js
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
```

- [ ] **Step 2: Run tests, verify they fail**

```bash
cd automation/notion-pb-sync && npm test
```

Expected: FAIL — `Failed to load url ../src/state.js`.

- [ ] **Step 3: Implement `state.js`**

Write `automation/notion-pb-sync/src/state.js`:

```js
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
```

- [ ] **Step 4: Run tests, verify they pass**

```bash
npm test
```

Expected: PASS — all `state` tests green.

- [ ] **Step 5: Commit**

```bash
git add src/state.js test/state.test.js
git commit -m "feat(sync): add Status enum + transition validation"
```

---

### Task 3: `caption.js` — Notion blocks → caption text

**Files:**
- Create: `automation/notion-pb-sync/src/caption.js`
- Create: `automation/notion-pb-sync/test/caption.test.js`

- [ ] **Step 1: Write failing tests**

Write `automation/notion-pb-sync/test/caption.test.js`:

```js
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
```

- [ ] **Step 2: Run tests, verify they fail**

```bash
npm test
```

Expected: FAIL — `Failed to load url ../src/caption.js`.

- [ ] **Step 3: Implement `caption.js`**

Write `automation/notion-pb-sync/src/caption.js`:

```js
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
```

- [ ] **Step 4: Run tests, verify they pass**

```bash
npm test
```

Expected: PASS — all `caption` tests green.

- [ ] **Step 5: Commit**

```bash
git add src/caption.js test/caption.test.js
git commit -m "feat(sync): caption extraction + platform limit validation"
```

---

### Task 4: `firewall.js` — Phase 1 keyword blocklist

**Files:**
- Create: `automation/notion-pb-sync/src/firewall.js`
- Create: `automation/notion-pb-sync/test/firewall.test.js`

- [ ] **Step 1: Write failing tests**

Write `automation/notion-pb-sync/test/firewall.test.js`:

```js
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
```

- [ ] **Step 2: Run tests, verify they fail**

Expected: FAIL — `Failed to load url ../src/firewall.js`.

- [ ] **Step 3: Implement `firewall.js`**

Write `automation/notion-pb-sync/src/firewall.js`:

```js
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
```

- [ ] **Step 4: Run tests, verify they pass**

Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add src/firewall.js test/firewall.test.js
git commit -m "feat(sync): Phase 1 firewall keyword blocklist"
```

---

### Task 5: `config.js` — env var loading + validation

**Files:**
- Create: `automation/notion-pb-sync/src/config.js`
- Create: `automation/notion-pb-sync/test/config.test.js`

- [ ] **Step 1: Write failing tests**

Write `automation/notion-pb-sync/test/config.test.js`:

```js
import { describe, it, expect } from 'vitest'
import { loadConfig } from '../src/config.js'

describe('loadConfig', () => {
  it('returns a config object when all vars present', () => {
    const env = {
      NOTION_TOKEN: 'ntn_x',
      NOTION_CONTENT_DATA_SOURCE_ID: 'ds_x',
      NOTION_VERSION: '2025-09-03',
      POST_BRIDGE_API_KEY: 'pb_x',
      PB_ACCOUNT_LINKEDIN: '25903',
      PB_ACCOUNT_THREADS: '25902',
      PB_ACCOUNT_TIKTOK: '25901',
      PB_ACCOUNT_YOUTUBE: '25900',
      PB_ACCOUNT_TWITTER: '25899',
      PB_ACCOUNT_INSTAGRAM: '25898'
    }
    const cfg = loadConfig(env)
    expect(cfg.notion.token).toBe('ntn_x')
    expect(cfg.notion.dataSourceId).toBe('ds_x')
    expect(cfg.postBridge.apiKey).toBe('pb_x')
    expect(cfg.accountMap.LinkedIn).toBe(25903)
    expect(cfg.accountMap.Threads).toBe(25902)
  })

  it('throws on missing required var', () => {
    const env = { POST_BRIDGE_API_KEY: 'pb_x' }
    expect(() => loadConfig(env)).toThrow(/NOTION_TOKEN/)
  })

  it('uses default Notion version when not set', () => {
    const env = {
      NOTION_TOKEN: 'x', NOTION_CONTENT_DATA_SOURCE_ID: 'x', POST_BRIDGE_API_KEY: 'x',
      PB_ACCOUNT_LINKEDIN: '1', PB_ACCOUNT_THREADS: '1', PB_ACCOUNT_TIKTOK: '1',
      PB_ACCOUNT_YOUTUBE: '1', PB_ACCOUNT_TWITTER: '1', PB_ACCOUNT_INSTAGRAM: '1'
    }
    expect(loadConfig(env).notion.version).toBe('2025-09-03')
  })
})
```

- [ ] **Step 2: Run tests, verify they fail**

- [ ] **Step 3: Implement `config.js`**

Write `automation/notion-pb-sync/src/config.js`:

```js
const REQUIRED = [
  'NOTION_TOKEN',
  'NOTION_CONTENT_DATA_SOURCE_ID',
  'POST_BRIDGE_API_KEY',
  'PB_ACCOUNT_LINKEDIN',
  'PB_ACCOUNT_THREADS',
  'PB_ACCOUNT_TIKTOK',
  'PB_ACCOUNT_YOUTUBE',
  'PB_ACCOUNT_TWITTER',
  'PB_ACCOUNT_INSTAGRAM'
]

export function loadConfig(env = process.env) {
  for (const key of REQUIRED) {
    if (!env[key]) throw new Error(`Missing required env var: ${key}`)
  }
  return {
    notion: {
      token: env.NOTION_TOKEN,
      dataSourceId: env.NOTION_CONTENT_DATA_SOURCE_ID,
      version: env.NOTION_VERSION || '2025-09-03'
    },
    postBridge: {
      apiKey: env.POST_BRIDGE_API_KEY,
      baseUrl: env.POST_BRIDGE_BASE_URL || 'https://api.post-bridge.com'
    },
    accountMap: {
      LinkedIn: Number(env.PB_ACCOUNT_LINKEDIN),
      Threads: Number(env.PB_ACCOUNT_THREADS),
      TikTok: Number(env.PB_ACCOUNT_TIKTOK),
      YouTube: Number(env.PB_ACCOUNT_YOUTUBE),
      Twitter: Number(env.PB_ACCOUNT_TWITTER),
      Instagram: Number(env.PB_ACCOUNT_INSTAGRAM)
    }
  }
}
```

- [ ] **Step 4: Run tests, verify they pass**

- [ ] **Step 5: Commit**

```bash
git add src/config.js test/config.test.js
git commit -m "feat(sync): config loader with env var validation"
```

---

### Task 6: `notion.js` — Notion API client

**Files:**
- Create: `automation/notion-pb-sync/src/notion.js`
- Create: `automation/notion-pb-sync/test/notion.test.js`

This client wraps Notion's REST API. Methods needed: `queryByStatus`, `queryActiveRows`, `fetchPageBlocks`, `updateRow`. We test against mocked `fetch`.

- [ ] **Step 1: Write failing tests**

Write `automation/notion-pb-sync/test/notion.test.js`:

```js
import { describe, it, expect, vi, beforeEach } from 'vitest'
import { createNotionClient } from '../src/notion.js'

const TOKEN = 'ntn_test'
const DS = 'ds_test'

function makeFetch(responses) {
  const calls = []
  const fetchMock = vi.fn(async (url, opts) => {
    calls.push({ url, opts })
    const next = responses.shift()
    if (!next) throw new Error('No mocked response left')
    return {
      ok: next.ok ?? true,
      status: next.status ?? 200,
      json: async () => next.body,
      text: async () => JSON.stringify(next.body)
    }
  })
  fetchMock.calls = calls
  return fetchMock
}

describe('createNotionClient', () => {
  let client
  beforeEach(() => {
    client = null
  })

  it('queryByStatus posts a filtered query', async () => {
    const fetchMock = makeFetch([{ body: { results: [] } }])
    client = createNotionClient({ token: TOKEN, dataSourceId: DS, version: '2025-09-03', fetchImpl: fetchMock })
    await client.queryByStatus(['Ready'])
    expect(fetchMock.calls[0].url).toBe(`https://api.notion.com/v1/data_sources/${DS}/query`)
    expect(fetchMock.calls[0].opts.method).toBe('POST')
    const sent = JSON.parse(fetchMock.calls[0].opts.body)
    expect(sent.filter.or).toHaveLength(1)
    expect(sent.filter.or[0]).toEqual({ property: 'Status', select: { equals: 'Ready' } })
  })

  it('queryByStatus handles multiple statuses with OR', async () => {
    const fetchMock = makeFetch([{ body: { results: [] } }])
    client = createNotionClient({ token: TOKEN, dataSourceId: DS, version: '2025-09-03', fetchImpl: fetchMock })
    await client.queryByStatus(['Ready', 'Scheduling', 'Scheduled'])
    const sent = JSON.parse(fetchMock.calls[0].opts.body)
    expect(sent.filter.or).toHaveLength(3)
  })

  it('fetchPageBlocks paginates until has_more is false', async () => {
    const fetchMock = makeFetch([
      { body: { results: [{ id: 'b1' }], has_more: true, next_cursor: 'cur1' } },
      { body: { results: [{ id: 'b2' }], has_more: false } }
    ])
    client = createNotionClient({ token: TOKEN, dataSourceId: DS, version: '2025-09-03', fetchImpl: fetchMock })
    const blocks = await client.fetchPageBlocks('page_x')
    expect(blocks).toEqual([{ id: 'b1' }, { id: 'b2' }])
    expect(fetchMock.calls).toHaveLength(2)
    expect(fetchMock.calls[1].url).toContain('start_cursor=cur1')
  })

  it('updateRow sends PATCH with properties', async () => {
    const fetchMock = makeFetch([{ body: { id: 'page_x' } }])
    client = createNotionClient({ token: TOKEN, dataSourceId: DS, version: '2025-09-03', fetchImpl: fetchMock })
    await client.updateRow('page_x', {
      Status: { select: { name: 'Scheduled' } },
      'Post Bridge ID': { rich_text: [{ text: { content: 'pb_123' } }] }
    })
    expect(fetchMock.calls[0].url).toBe('https://api.notion.com/v1/pages/page_x')
    expect(fetchMock.calls[0].opts.method).toBe('PATCH')
    const sent = JSON.parse(fetchMock.calls[0].opts.body)
    expect(sent.properties.Status.select.name).toBe('Scheduled')
  })

  it('throws with message on non-OK response', async () => {
    const fetchMock = makeFetch([{ ok: false, status: 400, body: { message: 'Bad property' } }])
    client = createNotionClient({ token: TOKEN, dataSourceId: DS, version: '2025-09-03', fetchImpl: fetchMock })
    await expect(client.updateRow('page_x', {})).rejects.toThrow(/Bad property|400/)
  })
})
```

- [ ] **Step 2: Run tests, verify they fail**

- [ ] **Step 3: Implement `notion.js`**

Write `automation/notion-pb-sync/src/notion.js`:

```js
export function createNotionClient({ token, dataSourceId, version, fetchImpl = fetch }) {
  const base = 'https://api.notion.com/v1'
  const headers = {
    'Authorization': `Bearer ${token}`,
    'Notion-Version': version,
    'Content-Type': 'application/json'
  }

  async function call(method, path, body) {
    const opts = { method, headers }
    if (body !== undefined) opts.body = JSON.stringify(body)
    const res = await fetchImpl(`${base}${path}`, opts)
    if (!res.ok) {
      const text = await res.text()
      throw new Error(`Notion ${method} ${path} -> ${res.status}: ${text}`)
    }
    return res.json()
  }

  async function queryByStatus(statuses) {
    const filter = {
      or: statuses.map(name => ({ property: 'Status', select: { equals: name } }))
    }
    const result = await call('POST', `/data_sources/${dataSourceId}/query`, { filter, page_size: 100 })
    return result.results
  }

  async function queryRowsWithPostBridgeIdInUserState() {
    // Rows where Post Bridge ID is set but Status is user-owned (revert/cancel)
    const filter = {
      and: [
        { property: 'Post Bridge ID', rich_text: { is_not_empty: true } },
        {
          or: [
            { property: 'Status', select: { equals: 'Idea' } },
            { property: 'Status', select: { equals: 'Drafting' } },
            { property: 'Status', select: { equals: 'Ready' } }
          ]
        }
      ]
    }
    const result = await call('POST', `/data_sources/${dataSourceId}/query`, { filter, page_size: 100 })
    return result.results
  }

  async function fetchPageBlocks(pageId) {
    const out = []
    let cursor = null
    while (true) {
      const qs = cursor ? `?start_cursor=${encodeURIComponent(cursor)}&page_size=100` : '?page_size=100'
      const result = await call('GET', `/blocks/${pageId}/children${qs}`)
      out.push(...result.results)
      if (!result.has_more) break
      cursor = result.next_cursor
    }
    return out
  }

  async function updateRow(pageId, properties) {
    return call('PATCH', `/pages/${pageId}`, { properties })
  }

  return { queryByStatus, queryRowsWithPostBridgeIdInUserState, fetchPageBlocks, updateRow }
}
```

- [ ] **Step 4: Run tests, verify they pass**

- [ ] **Step 5: Commit**

```bash
git add src/notion.js test/notion.test.js
git commit -m "feat(sync): Notion API client with query/update/blocks fetch"
```

---

### Task 7: `post-bridge.js` — post-bridge API client

**Files:**
- Create: `automation/notion-pb-sync/src/post-bridge.js`
- Create: `automation/notion-pb-sync/test/post-bridge.test.js`

Methods needed: `createPost`, `getPost`, `updatePost`, `deletePost`, `getPostResults`, `listRecentPosts`, `createUploadUrl`, `uploadMedia`.

- [ ] **Step 1: Write failing tests**

Write `automation/notion-pb-sync/test/post-bridge.test.js`:

```js
import { describe, it, expect, vi } from 'vitest'
import { createPostBridgeClient } from '../src/post-bridge.js'

function makeFetch(responses) {
  const calls = []
  const fetchMock = vi.fn(async (url, opts) => {
    calls.push({ url, opts })
    const next = responses.shift()
    if (!next) throw new Error('No mocked response left')
    return {
      ok: next.ok ?? true,
      status: next.status ?? 200,
      json: async () => next.body,
      text: async () => JSON.stringify(next.body ?? {})
    }
  })
  fetchMock.calls = calls
  return fetchMock
}

const cfg = { apiKey: 'pb_x', baseUrl: 'https://api.post-bridge.com' }

describe('post-bridge client', () => {
  it('createPost POSTs to /v1/posts', async () => {
    const fetchMock = makeFetch([{ body: { id: 'p_1', status: 'scheduled' } }])
    const client = createPostBridgeClient({ ...cfg, fetchImpl: fetchMock })
    const result = await client.createPost({
      caption: 'Hello',
      social_accounts: [25903],
      scheduled_at: '2026-06-01T12:00:00Z'
    })
    expect(result.id).toBe('p_1')
    expect(fetchMock.calls[0].url).toBe('https://api.post-bridge.com/v1/posts')
    expect(fetchMock.calls[0].opts.method).toBe('POST')
    const sent = JSON.parse(fetchMock.calls[0].opts.body)
    expect(sent.caption).toBe('Hello')
    expect(sent.social_accounts).toEqual([25903])
  })

  it('getPost GETs /v1/posts/:id', async () => {
    const fetchMock = makeFetch([{ body: { id: 'p_1', status: 'posted' } }])
    const client = createPostBridgeClient({ ...cfg, fetchImpl: fetchMock })
    const result = await client.getPost('p_1')
    expect(result.status).toBe('posted')
    expect(fetchMock.calls[0].url).toBe('https://api.post-bridge.com/v1/posts/p_1')
    expect(fetchMock.calls[0].opts.method).toBe('GET')
  })

  it('updatePost PATCHes /v1/posts/:id', async () => {
    const fetchMock = makeFetch([{ body: { id: 'p_1' } }])
    const client = createPostBridgeClient({ ...cfg, fetchImpl: fetchMock })
    await client.updatePost('p_1', { caption: 'new' })
    expect(fetchMock.calls[0].opts.method).toBe('PATCH')
  })

  it('deletePost DELETEs /v1/posts/:id', async () => {
    const fetchMock = makeFetch([{ body: {} }])
    const client = createPostBridgeClient({ ...cfg, fetchImpl: fetchMock })
    await client.deletePost('p_1')
    expect(fetchMock.calls[0].opts.method).toBe('DELETE')
  })

  it('getPostResults GETs /v1/post-results with query', async () => {
    const fetchMock = makeFetch([{ body: { data: [] } }])
    const client = createPostBridgeClient({ ...cfg, fetchImpl: fetchMock })
    await client.getPostResults('p_1')
    expect(fetchMock.calls[0].url).toContain('/v1/post-results')
    expect(fetchMock.calls[0].url).toContain('post_id=p_1')
  })

  it('listRecentPosts GETs /v1/posts with filters', async () => {
    const fetchMock = makeFetch([{ body: { data: [], count: 0 } }])
    const client = createPostBridgeClient({ ...cfg, fetchImpl: fetchMock })
    await client.listRecentPosts({ status: 'scheduled', limit: 50 })
    expect(fetchMock.calls[0].url).toContain('status=scheduled')
    expect(fetchMock.calls[0].url).toContain('limit=50')
  })

  it('createUploadUrl POSTs to /v1/media/create-upload-url', async () => {
    const fetchMock = makeFetch([{ body: { media_id: 'm_1', upload_url: 'https://...' } }])
    const client = createPostBridgeClient({ ...cfg, fetchImpl: fetchMock })
    const result = await client.createUploadUrl({ mime_type: 'image/jpeg', size_bytes: 1234, name: 'a.jpg' })
    expect(result.media_id).toBe('m_1')
    expect(fetchMock.calls[0].url).toBe('https://api.post-bridge.com/v1/media/create-upload-url')
  })

  it('throws on non-OK response', async () => {
    const fetchMock = makeFetch([{ ok: false, status: 401, body: { message: 'unauthorized' } }])
    const client = createPostBridgeClient({ ...cfg, fetchImpl: fetchMock })
    await expect(client.getPost('p_1')).rejects.toThrow(/401|unauthorized/)
  })
})
```

- [ ] **Step 2: Run tests, verify they fail**

- [ ] **Step 3: Implement `post-bridge.js`**

Write `automation/notion-pb-sync/src/post-bridge.js`:

```js
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
```

- [ ] **Step 4: Run tests, verify they pass**

- [ ] **Step 5: Commit**

```bash
git add src/post-bridge.js test/post-bridge.test.js
git commit -m "feat(sync): post-bridge API client"
```

---

### Task 8: `media.js` — Notion file → post-bridge media_id

**Files:**
- Create: `automation/notion-pb-sync/src/media.js`
- Create: `automation/notion-pb-sync/test/media.test.js`

- [ ] **Step 1: Write failing tests**

Write `automation/notion-pb-sync/test/media.test.js`:

```js
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
```

- [ ] **Step 2: Run tests, verify they fail**

- [ ] **Step 3: Implement `media.js`**

Write `automation/notion-pb-sync/src/media.js`:

```js
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
```

- [ ] **Step 4: Run tests, verify they pass**

- [ ] **Step 5: Commit**

```bash
git add src/media.js test/media.test.js
git commit -m "feat(sync): media upload pipeline (Notion -> post-bridge)"
```

---

### Task 9: `tick.js` — Ready → Scheduled (happy path)

**Files:**
- Create: `automation/notion-pb-sync/src/tick.js`
- Create: `automation/notion-pb-sync/test/tick.test.js`

This task implements only the `Ready → Scheduling → Scheduled` path. Recovery, polling, edits, and cancels come in later tasks.

- [ ] **Step 1: Write the failing test for happy path**

Write `automation/notion-pb-sync/test/tick.test.js`:

```js
import { describe, it, expect, vi } from 'vitest'
import { tick } from '../src/tick.js'

function makeRow({ id = 'page_1', status = 'Ready', title = 'A post', platforms = ['LinkedIn'], date = '2026-06-01T12:00:00.000Z', postBridgeId = '', media = [] } = {}) {
  return {
    id,
    last_edited_time: '2026-05-26T10:00:00.000Z',
    properties: {
      Title: { title: [{ plain_text: title }] },
      Status: { select: { name: status } },
      Platform: { multi_select: platforms.map(name => ({ name })) },
      Date: { date: { start: date } },
      'Post Bridge ID': { rich_text: postBridgeId ? [{ plain_text: postBridgeId }] : [] },
      Media: { type: 'files', files: media }
    }
  }
}

function fakeNotion({ activeRows = [], blocks = [] } = {}) {
  return {
    queryByStatus: vi.fn(async () => activeRows),
    queryRowsWithPostBridgeIdInUserState: vi.fn(async () => []),
    fetchPageBlocks: vi.fn(async () => blocks),
    updateRow: vi.fn(async () => ({}))
  }
}

function fakePb({ createReturn = { id: 'pb_new' } } = {}) {
  return {
    createPost: vi.fn(async () => createReturn),
    getPost: vi.fn(),
    updatePost: vi.fn(),
    deletePost: vi.fn(),
    getPostResults: vi.fn(),
    listRecentPosts: vi.fn(async () => ({ data: [] })),
    createUploadUrl: vi.fn(),
    uploadMedia: vi.fn()
  }
}

const ACCOUNT_MAP = {
  LinkedIn: 25903, Threads: 25902, TikTok: 25901, YouTube: 25900, Twitter: 25899, Instagram: 25898
}

describe('tick — Ready → Scheduled happy path', () => {
  it('flips Ready to Scheduling, creates post-bridge post, writes back ID + Scheduled', async () => {
    const row = makeRow({ id: 'page_1', status: 'Ready', platforms: ['LinkedIn'] })
    const blocks = [{ type: 'paragraph', paragraph: { rich_text: [{ plain_text: 'Hello world' }] } }]
    const notion = fakeNotion({ activeRows: [row], blocks })
    const pb = fakePb({ createReturn: { id: 'pb_xyz', status: 'scheduled' } })

    await tick({ notion, pb, accountMap: ACCOUNT_MAP, fetchImpl: vi.fn() })

    expect(notion.updateRow).toHaveBeenNthCalledWith(1, 'page_1', expect.objectContaining({
      Status: { select: { name: 'Scheduling' } }
    }))
    expect(pb.createPost).toHaveBeenCalledWith(expect.objectContaining({
      caption: 'Hello world',
      social_accounts: [25903],
      scheduled_at: '2026-06-01T12:00:00.000Z'
    }))
    expect(notion.updateRow).toHaveBeenNthCalledWith(2, 'page_1', expect.objectContaining({
      Status: { select: { name: 'Scheduled' } },
      'Post Bridge ID': { rich_text: [{ text: { content: 'pb_xyz' } }] }
    }))
  })

  it('marks row Failed when firewall matches', async () => {
    const row = makeRow({ title: 'Mars Men is great' })
    const notion = fakeNotion({ activeRows: [row], blocks: [] })
    const pb = fakePb()
    await tick({ notion, pb, accountMap: ACCOUNT_MAP, fetchImpl: vi.fn() })
    expect(pb.createPost).not.toHaveBeenCalled()
    expect(notion.updateRow).toHaveBeenCalledWith('page_1', expect.objectContaining({
      Status: { select: { name: 'Failed' } }
    }))
  })

  it('marks row Failed when Twitter exceeds 280 chars', async () => {
    const long = 'x'.repeat(281)
    const row = makeRow({ platforms: ['Twitter'] })
    const blocks = [{ type: 'paragraph', paragraph: { rich_text: [{ plain_text: long }] } }]
    const notion = fakeNotion({ activeRows: [row], blocks })
    const pb = fakePb()
    await tick({ notion, pb, accountMap: ACCOUNT_MAP, fetchImpl: vi.fn() })
    expect(pb.createPost).not.toHaveBeenCalled()
    expect(notion.updateRow).toHaveBeenCalledWith('page_1', expect.objectContaining({
      Status: { select: { name: 'Failed' } }
    }))
  })

  it('skips Blog and Spotify platforms (no account mapping)', async () => {
    const row = makeRow({ platforms: ['Blog', 'LinkedIn', 'Spotify'] })
    const blocks = [{ type: 'paragraph', paragraph: { rich_text: [{ plain_text: 'Hi' }] } }]
    const notion = fakeNotion({ activeRows: [row], blocks })
    const pb = fakePb({ createReturn: { id: 'pb_z' } })
    await tick({ notion, pb, accountMap: ACCOUNT_MAP, fetchImpl: vi.fn() })
    expect(pb.createPost).toHaveBeenCalledWith(expect.objectContaining({
      social_accounts: [25903]
    }))
  })

  it('marks row Failed when no mappable platforms', async () => {
    const row = makeRow({ platforms: ['Blog', 'Spotify'] })
    const blocks = [{ type: 'paragraph', paragraph: { rich_text: [{ plain_text: 'Hi' }] } }]
    const notion = fakeNotion({ activeRows: [row], blocks })
    const pb = fakePb()
    await tick({ notion, pb, accountMap: ACCOUNT_MAP, fetchImpl: vi.fn() })
    expect(pb.createPost).not.toHaveBeenCalled()
    expect(notion.updateRow).toHaveBeenCalledWith('page_1', expect.objectContaining({
      Status: { select: { name: 'Failed' } }
    }))
  })
})
```

- [ ] **Step 2: Run tests, verify they fail**

- [ ] **Step 3: Implement `tick.js` (Ready path only — recovery + polling stubs added in later tasks)**

Write `automation/notion-pb-sync/src/tick.js`:

```js
import { STATUS } from './state.js'
import { blocksToCaption, stripSourcesHeader, validateForPlatforms } from './caption.js'
import { checkPhase1Firewall } from './firewall.js'
import { extractFiles, uploadNotionFilesToPostBridge } from './media.js'

export async function tick({ notion, pb, accountMap, fetchImpl = fetch }) {
  const activeStatuses = [STATUS.READY, STATUS.SCHEDULING, STATUS.SCHEDULED]
  const rows = await notion.queryByStatus(activeStatuses)

  for (const row of rows) {
    const status = row.properties.Status?.select?.name
    try {
      if (status === STATUS.READY) {
        await handleReady(row, { notion, pb, accountMap, fetchImpl })
      }
      // Scheduling / Scheduled handlers added in later tasks
    } catch (err) {
      await markFailed(row.id, notion, err.message)
    }
  }
}

async function handleReady(row, { notion, pb, accountMap, fetchImpl }) {
  const title = extractTitle(row)
  const platforms = extractPlatforms(row)
  const scheduledAt = row.properties.Date?.date?.start

  const blocks = await notion.fetchPageBlocks(row.id)
  const rawCaption = blocksToCaption(blocks)
  const caption = stripSourcesHeader(rawCaption)

  const firewall = checkPhase1Firewall(title, caption)
  if (firewall.blocked) {
    await markFailed(row.id, notion, `Phase 1 firewall: matched "${firewall.matched}"`)
    return
  }

  const mappedAccounts = platforms
    .map(p => accountMap[p])
    .filter(Boolean)

  if (mappedAccounts.length === 0) {
    await markFailed(row.id, notion, 'No mappable platforms selected (Blog/Spotify are skipped)')
    return
  }

  const validation = validateForPlatforms(caption, platforms)
  if (!validation.ok) {
    await markFailed(row.id, notion, validation.reason)
    return
  }

  // Phase 1 of two-phase commit: flip to Scheduling
  await notion.updateRow(row.id, {
    Status: { select: { name: STATUS.SCHEDULING } }
  })

  // Upload media if any
  const files = extractFiles(row.properties.Media)
  const mediaIds = files.length
    ? await uploadNotionFilesToPostBridge(files, { pb, fetchImpl })
    : []

  // Phase 2: create the post-bridge post
  const createPayload = {
    caption,
    social_accounts: mappedAccounts
  }
  if (scheduledAt) createPayload.scheduled_at = scheduledAt
  if (mediaIds.length) createPayload.media = mediaIds

  const created = await pb.createPost(createPayload)

  // Phase 3: writeback
  await notion.updateRow(row.id, {
    Status: { select: { name: STATUS.SCHEDULED } },
    'Post Bridge ID': { rich_text: [{ text: { content: created.id } }] },
    'Last Sync At': { date: { start: new Date().toISOString() } }
  })
}

function extractTitle(row) {
  const t = row.properties.Title?.title
  return Array.isArray(t) ? t.map(x => x.plain_text).join('') : ''
}

function extractPlatforms(row) {
  const arr = row.properties.Platform?.multi_select
  return Array.isArray(arr) ? arr.map(o => o.name) : []
}

async function markFailed(pageId, notion, reason) {
  await notion.updateRow(pageId, {
    Status: { select: { name: STATUS.FAILED } },
    Notes: { rich_text: [{ text: { content: reason.slice(0, 1900) } }] }
  })
}
```

- [ ] **Step 4: Run tests, verify they pass**

- [ ] **Step 5: Commit**

```bash
git add src/tick.js test/tick.test.js
git commit -m "feat(sync): tick happy path (Ready -> Scheduled)"
```

---

### Task 10: `tick.js` — Scheduling recovery

Resume from `Scheduling` state by matching post-bridge posts on caption hash + scheduled_at.

**Files:**
- Modify: `automation/notion-pb-sync/src/tick.js`
- Modify: `automation/notion-pb-sync/test/tick.test.js`

- [ ] **Step 1: Add a failing recovery test**

Append to `automation/notion-pb-sync/test/tick.test.js`:

```js
import crypto from 'node:crypto'

function captionHash(s) {
  return crypto.createHash('sha256').update(s).digest('hex').slice(0, 12)
}

describe('tick — Scheduling recovery', () => {
  it('claims an existing post-bridge post when caption hash + scheduled_at match', async () => {
    const row = makeRow({ id: 'page_2', status: 'Scheduling' })
    const blocks = [{ type: 'paragraph', paragraph: { rich_text: [{ plain_text: 'Hello world' }] } }]
    const expectedHash = captionHash('Hello world')
    const notion = fakeNotion({ activeRows: [row], blocks })
    const pb = fakePb()
    pb.listRecentPosts = vi.fn(async () => ({
      data: [
        { id: 'pb_claimed', scheduled_at: '2026-06-01T12:00:00.000Z', caption: 'Hello world' },
        { id: 'pb_other', scheduled_at: '2026-06-02T12:00:00.000Z', caption: 'Other post' }
      ]
    }))

    await tick({ notion, pb, accountMap: ACCOUNT_MAP, fetchImpl: vi.fn() })

    expect(pb.createPost).not.toHaveBeenCalled()
    expect(notion.updateRow).toHaveBeenCalledWith('page_2', expect.objectContaining({
      Status: { select: { name: 'Scheduled' } },
      'Post Bridge ID': { rich_text: [{ text: { content: 'pb_claimed' } }] }
    }))
  })

  it('retries the create when no match found', async () => {
    const row = makeRow({ id: 'page_3', status: 'Scheduling' })
    const blocks = [{ type: 'paragraph', paragraph: { rich_text: [{ plain_text: 'No match content' }] } }]
    const notion = fakeNotion({ activeRows: [row], blocks })
    const pb = fakePb({ createReturn: { id: 'pb_retry' } })
    pb.listRecentPosts = vi.fn(async () => ({ data: [] }))

    await tick({ notion, pb, accountMap: ACCOUNT_MAP, fetchImpl: vi.fn() })

    expect(pb.createPost).toHaveBeenCalled()
    expect(notion.updateRow).toHaveBeenCalledWith('page_3', expect.objectContaining({
      Status: { select: { name: 'Scheduled' } },
      'Post Bridge ID': { rich_text: [{ text: { content: 'pb_retry' } }] }
    }))
  })
})
```

- [ ] **Step 2: Run tests, verify recovery tests fail**

- [ ] **Step 3: Implement recovery in `tick.js`**

In `automation/notion-pb-sync/src/tick.js`, add the `Scheduling` case and the recovery helpers:

```js
// Add to top of file
import crypto from 'node:crypto'

// In the for-loop in tick(), add:
//   if (status === STATUS.SCHEDULING) {
//     await handleScheduling(row, { notion, pb, accountMap, fetchImpl })
//   }

async function handleScheduling(row, { notion, pb, accountMap, fetchImpl }) {
  const blocks = await notion.fetchPageBlocks(row.id)
  const caption = stripSourcesHeader(blocksToCaption(blocks))
  const scheduledAt = row.properties.Date?.date?.start
  const targetHash = captionHash(caption)

  const recent = await pb.listRecentPosts({ status: 'scheduled', limit: 50 })
  const match = (recent.data || []).find(p => {
    return p.scheduled_at === scheduledAt && captionHash(p.caption || '') === targetHash
  })

  if (match) {
    await notion.updateRow(row.id, {
      Status: { select: { name: STATUS.SCHEDULED } },
      'Post Bridge ID': { rich_text: [{ text: { content: match.id } }] },
      'Last Sync At': { date: { start: new Date().toISOString() } }
    })
    return
  }

  // No match — retry as if Ready (re-creates the post). Re-uses handleReady's logic
  // by directly invoking, but skip the "flip to Scheduling" step since we're already there.
  await retryCreate(row, caption, { notion, pb, accountMap, fetchImpl })
}

function captionHash(s) {
  return crypto.createHash('sha256').update(s).digest('hex').slice(0, 12)
}

async function retryCreate(row, caption, { notion, pb, accountMap, fetchImpl }) {
  const platforms = extractPlatforms(row)
  const scheduledAt = row.properties.Date?.date?.start
  const mappedAccounts = platforms.map(p => accountMap[p]).filter(Boolean)

  if (mappedAccounts.length === 0) {
    await markFailed(row.id, notion, 'Recovery: no mappable platforms')
    return
  }

  const files = extractFiles(row.properties.Media)
  const mediaIds = files.length
    ? await uploadNotionFilesToPostBridge(files, { pb, fetchImpl })
    : []

  const payload = { caption, social_accounts: mappedAccounts }
  if (scheduledAt) payload.scheduled_at = scheduledAt
  if (mediaIds.length) payload.media = mediaIds

  const created = await pb.createPost(payload)
  await notion.updateRow(row.id, {
    Status: { select: { name: STATUS.SCHEDULED } },
    'Post Bridge ID': { rich_text: [{ text: { content: created.id } }] },
    'Last Sync At': { date: { start: new Date().toISOString() } }
  })
}
```

Then update the `for` loop in `tick()`:

```js
for (const row of rows) {
  const status = row.properties.Status?.select?.name
  try {
    if (status === STATUS.READY) {
      await handleReady(row, { notion, pb, accountMap, fetchImpl })
    } else if (status === STATUS.SCHEDULING) {
      await handleScheduling(row, { notion, pb, accountMap, fetchImpl })
    }
  } catch (err) {
    await markFailed(row.id, notion, err.message)
  }
}
```

- [ ] **Step 4: Run tests, verify they pass**

- [ ] **Step 5: Commit**

```bash
git add src/tick.js test/tick.test.js
git commit -m "feat(sync): Scheduling recovery via caption-hash lookup"
```

---

### Task 11: `tick.js` — Scheduled polling (post-bridge → Notion writeback)

Detect post-bridge state changes (`posted`, `failed`) and writeback to Notion.

**Files:**
- Modify: `automation/notion-pb-sync/src/tick.js`
- Modify: `automation/notion-pb-sync/test/tick.test.js`

- [ ] **Step 1: Add failing tests for Scheduled polling**

Append to `test/tick.test.js`:

```js
describe('tick — Scheduled polling', () => {
  it('writes back Published + per-platform URLs when post-bridge reports posted', async () => {
    const row = makeRow({ id: 'page_4', status: 'Scheduled', postBridgeId: 'pb_done' })
    const notion = fakeNotion({ activeRows: [row], blocks: [] })
    const pb = fakePb()
    pb.getPost = vi.fn(async () => ({ id: 'pb_done', status: 'posted' }))
    pb.getPostResults = vi.fn(async () => ({
      data: [
        { platform: 'linkedin', success: true, share_url: 'https://linkedin.com/posts/x' },
        { platform: 'twitter', success: true, share_url: 'https://x.com/y' }
      ]
    }))

    await tick({ notion, pb, accountMap: ACCOUNT_MAP, fetchImpl: vi.fn() })

    expect(notion.updateRow).toHaveBeenCalledWith('page_4', expect.objectContaining({
      Status: { select: { name: 'Published' } },
      'Published URLs': { rich_text: [{ text: { content: expect.stringContaining('LinkedIn: https://linkedin.com/posts/x') } }] }
    }))
  })

  it('marks Failed when post-bridge reports failed', async () => {
    const row = makeRow({ id: 'page_5', status: 'Scheduled', postBridgeId: 'pb_bad' })
    const notion = fakeNotion({ activeRows: [row], blocks: [] })
    const pb = fakePb()
    pb.getPost = vi.fn(async () => ({ id: 'pb_bad', status: 'failed', error: 'auth expired' }))

    await tick({ notion, pb, accountMap: ACCOUNT_MAP, fetchImpl: vi.fn() })

    expect(notion.updateRow).toHaveBeenCalledWith('page_5', expect.objectContaining({
      Status: { select: { name: 'Failed' } }
    }))
  })

  it('leaves Scheduled row alone when still scheduled', async () => {
    const row = makeRow({ id: 'page_6', status: 'Scheduled', postBridgeId: 'pb_wait' })
    const notion = fakeNotion({ activeRows: [row], blocks: [] })
    const pb = fakePb()
    pb.getPost = vi.fn(async () => ({ id: 'pb_wait', status: 'scheduled' }))

    await tick({ notion, pb, accountMap: ACCOUNT_MAP, fetchImpl: vi.fn() })

    // No Status change call
    const statusUpdates = notion.updateRow.mock.calls.filter(([, props]) => props.Status)
    expect(statusUpdates).toHaveLength(0)
  })
})
```

- [ ] **Step 2: Run tests, verify they fail**

- [ ] **Step 3: Implement Scheduled handler in `tick.js`**

Add `handleScheduled` to `src/tick.js`:

```js
async function handleScheduled(row, { notion, pb }) {
  const postBridgeId = (row.properties['Post Bridge ID']?.rich_text || [])
    .map(t => t.plain_text).join('')
  if (!postBridgeId) {
    // Defensive: Scheduled state without an ID is corrupt. Surface it.
    await markFailed(row.id, notion, 'Scheduled state with no Post Bridge ID — manual review needed')
    return
  }

  const pbPost = await pb.getPost(postBridgeId)
  const status = pbPost.status

  if (status === 'posted') {
    const results = await pb.getPostResults(postBridgeId)
    const urlText = formatPublishedUrls(results.data || [])
    await notion.updateRow(row.id, {
      Status: { select: { name: STATUS.PUBLISHED } },
      'Published URLs': { rich_text: [{ text: { content: urlText } }] },
      'Last Sync At': { date: { start: new Date().toISOString() } }
    })
    return
  }

  if (status === 'failed') {
    await markFailed(row.id, notion, `post-bridge failed: ${pbPost.error || 'unknown reason'}`)
    return
  }
  // Otherwise still pending — no-op this tick.
}

function formatPublishedUrls(results) {
  const PLATFORM_LABEL = {
    linkedin: 'LinkedIn', twitter: 'Twitter', threads: 'Threads',
    tiktok: 'TikTok', youtube: 'YouTube', instagram: 'Instagram'
  }
  const lines = results
    .filter(r => r.share_url)
    .map(r => `${PLATFORM_LABEL[r.platform] || r.platform}: ${r.share_url}`)
  return lines.join('\n')
}
```

Update the `for` loop in `tick()`:

```js
for (const row of rows) {
  const status = row.properties.Status?.select?.name
  try {
    if (status === STATUS.READY) {
      await handleReady(row, { notion, pb, accountMap, fetchImpl })
    } else if (status === STATUS.SCHEDULING) {
      await handleScheduling(row, { notion, pb, accountMap, fetchImpl })
    } else if (status === STATUS.SCHEDULED) {
      await handleScheduled(row, { notion, pb })
    }
  } catch (err) {
    await markFailed(row.id, notion, err.message)
  }
}
```

- [ ] **Step 4: Run tests, verify they pass**

- [ ] **Step 5: Commit**

```bash
git add src/tick.js test/tick.test.js
git commit -m "feat(sync): poll Scheduled rows, write Published or Failed"
```

---

### Task 12: `tick.js` — Edit propagation via PATCH

If Notion `last_edited_time` > `Last Sync At`, push updated caption/date/accounts to post-bridge.

**Files:**
- Modify: `automation/notion-pb-sync/src/tick.js`
- Modify: `automation/notion-pb-sync/test/tick.test.js`

- [ ] **Step 1: Add failing edit-propagation test**

Append to `test/tick.test.js`:

```js
describe('tick — edit propagation', () => {
  it('PATCHes post-bridge when Notion was edited after last sync', async () => {
    const row = makeRow({ id: 'page_7', status: 'Scheduled', postBridgeId: 'pb_edit' })
    row.last_edited_time = '2026-05-26T11:00:00.000Z'
    row.properties['Last Sync At'] = { date: { start: '2026-05-26T10:00:00.000Z' } }
    const blocks = [{ type: 'paragraph', paragraph: { rich_text: [{ plain_text: 'Updated caption' }] } }]
    const notion = fakeNotion({ activeRows: [row], blocks })
    const pb = fakePb()
    pb.getPost = vi.fn(async () => ({ id: 'pb_edit', status: 'scheduled' }))

    await tick({ notion, pb, accountMap: ACCOUNT_MAP, fetchImpl: vi.fn() })

    expect(pb.updatePost).toHaveBeenCalledWith('pb_edit', expect.objectContaining({
      caption: 'Updated caption'
    }))
    // Last Sync At gets updated
    expect(notion.updateRow).toHaveBeenCalledWith('page_7', expect.objectContaining({
      'Last Sync At': { date: { start: expect.any(String) } }
    }))
  })

  it('does NOT PATCH when no edit since last sync', async () => {
    const row = makeRow({ id: 'page_8', status: 'Scheduled', postBridgeId: 'pb_clean' })
    row.last_edited_time = '2026-05-26T09:00:00.000Z'
    row.properties['Last Sync At'] = { date: { start: '2026-05-26T10:00:00.000Z' } }
    const notion = fakeNotion({ activeRows: [row], blocks: [] })
    const pb = fakePb()
    pb.getPost = vi.fn(async () => ({ id: 'pb_clean', status: 'scheduled' }))

    await tick({ notion, pb, accountMap: ACCOUNT_MAP, fetchImpl: vi.fn() })

    expect(pb.updatePost).not.toHaveBeenCalled()
  })
})
```

- [ ] **Step 2: Run tests, verify they fail**

- [ ] **Step 3: Extend `handleScheduled` in `tick.js` to handle edits**

Update `handleScheduled` in `src/tick.js`:

```js
async function handleScheduled(row, { notion, pb, accountMap }) {
  const postBridgeId = (row.properties['Post Bridge ID']?.rich_text || [])
    .map(t => t.plain_text).join('')
  if (!postBridgeId) {
    await markFailed(row.id, notion, 'Scheduled state with no Post Bridge ID — manual review needed')
    return
  }

  const pbPost = await pb.getPost(postBridgeId)
  const status = pbPost.status

  if (status === 'posted') {
    const results = await pb.getPostResults(postBridgeId)
    const urlText = formatPublishedUrls(results.data || [])
    await notion.updateRow(row.id, {
      Status: { select: { name: STATUS.PUBLISHED } },
      'Published URLs': { rich_text: [{ text: { content: urlText } }] },
      'Last Sync At': { date: { start: new Date().toISOString() } }
    })
    return
  }

  if (status === 'failed') {
    await markFailed(row.id, notion, `post-bridge failed: ${pbPost.error || 'unknown reason'}`)
    return
  }

  // Status is 'scheduled' — check for edits
  await maybePropagateEdit(row, postBridgeId, { notion, pb, accountMap })
}

async function maybePropagateEdit(row, postBridgeId, { notion, pb, accountMap }) {
  const lastEdited = row.last_edited_time
  const lastSyncAt = row.properties['Last Sync At']?.date?.start
  if (!lastEdited || (lastSyncAt && new Date(lastEdited) <= new Date(lastSyncAt))) return

  const blocks = await notion.fetchPageBlocks(row.id)
  const caption = stripSourcesHeader(blocksToCaption(blocks))
  const platforms = extractPlatforms(row)
  const scheduledAt = row.properties.Date?.date?.start
  const mappedAccounts = platforms.map(p => accountMap[p]).filter(Boolean)

  const patch = { caption, social_accounts: mappedAccounts }
  if (scheduledAt) patch.scheduled_at = scheduledAt

  await pb.updatePost(postBridgeId, patch)
  await notion.updateRow(row.id, {
    'Last Sync At': { date: { start: new Date().toISOString() } }
  })
}
```

Update the `for` loop accordingly (pass `accountMap` into `handleScheduled`):

```js
} else if (status === STATUS.SCHEDULED) {
  await handleScheduled(row, { notion, pb, accountMap })
}
```

- [ ] **Step 4: Run tests, verify they pass**

- [ ] **Step 5: Commit**

```bash
git add src/tick.js test/tick.test.js
git commit -m "feat(sync): propagate Notion edits to post-bridge via PATCH"
```

---

### Task 13: `tick.js` — Revert / cancel handling

When a row that has `Post Bridge ID` set is moved back to `Idea`/`Drafting`/`Ready`, DELETE the post-bridge post and clear the ID.

**Files:**
- Modify: `automation/notion-pb-sync/src/tick.js`
- Modify: `automation/notion-pb-sync/test/tick.test.js`

- [ ] **Step 1: Add failing revert/cancel tests**

Append to `test/tick.test.js`:

```js
describe('tick — revert / cancel', () => {
  it('deletes post-bridge post when row reverts from Scheduled to Drafting', async () => {
    const revertedRow = makeRow({ id: 'page_9', status: 'Drafting', postBridgeId: 'pb_to_kill' })
    const notion = {
      queryByStatus: vi.fn(async () => []),
      queryRowsWithPostBridgeIdInUserState: vi.fn(async () => [revertedRow]),
      fetchPageBlocks: vi.fn(async () => []),
      updateRow: vi.fn(async () => ({}))
    }
    const pb = fakePb()
    pb.deletePost = vi.fn(async () => ({}))

    await tick({ notion, pb, accountMap: ACCOUNT_MAP, fetchImpl: vi.fn() })

    expect(pb.deletePost).toHaveBeenCalledWith('pb_to_kill')
    expect(notion.updateRow).toHaveBeenCalledWith('page_9', expect.objectContaining({
      'Post Bridge ID': { rich_text: [] }
    }))
  })

  it('continues if post-bridge delete returns 404 (already gone)', async () => {
    const revertedRow = makeRow({ id: 'page_10', status: 'Idea', postBridgeId: 'pb_gone' })
    const notion = {
      queryByStatus: vi.fn(async () => []),
      queryRowsWithPostBridgeIdInUserState: vi.fn(async () => [revertedRow]),
      fetchPageBlocks: vi.fn(async () => []),
      updateRow: vi.fn(async () => ({}))
    }
    const pb = fakePb()
    pb.deletePost = vi.fn(async () => { throw new Error('post-bridge DELETE -> 404: not found') })

    await tick({ notion, pb, accountMap: ACCOUNT_MAP, fetchImpl: vi.fn() })

    // Should still clear the Notion field
    expect(notion.updateRow).toHaveBeenCalledWith('page_10', expect.objectContaining({
      'Post Bridge ID': { rich_text: [] }
    }))
  })
})
```

- [ ] **Step 2: Run tests, verify they fail**

- [ ] **Step 3: Add revert handling to `tick()`**

Update `tick()` in `src/tick.js` to also query reverted rows:

```js
export async function tick({ notion, pb, accountMap, fetchImpl = fetch }) {
  const activeStatuses = [STATUS.READY, STATUS.SCHEDULING, STATUS.SCHEDULED]
  const rows = await notion.queryByStatus(activeStatuses)

  for (const row of rows) {
    const status = row.properties.Status?.select?.name
    try {
      if (status === STATUS.READY) {
        await handleReady(row, { notion, pb, accountMap, fetchImpl })
      } else if (status === STATUS.SCHEDULING) {
        await handleScheduling(row, { notion, pb, accountMap, fetchImpl })
      } else if (status === STATUS.SCHEDULED) {
        await handleScheduled(row, { notion, pb, accountMap })
      }
    } catch (err) {
      await markFailed(row.id, notion, err.message)
    }
  }

  const reverted = await notion.queryRowsWithPostBridgeIdInUserState()
  for (const row of reverted) {
    const postBridgeId = (row.properties['Post Bridge ID']?.rich_text || [])
      .map(t => t.plain_text).join('')
    if (!postBridgeId) continue
    try {
      await pb.deletePost(postBridgeId)
    } catch (err) {
      // 404 is fine — already gone. Log and continue.
      if (!String(err.message).match(/404/)) {
        console.error(`Revert delete failed for ${row.id}: ${err.message}`)
      }
    }
    await notion.updateRow(row.id, {
      'Post Bridge ID': { rich_text: [] }
    })
  }
}
```

- [ ] **Step 4: Run tests, verify they pass**

- [ ] **Step 5: Commit**

```bash
git add src/tick.js test/tick.test.js
git commit -m "feat(sync): handle revert/cancel by deleting post-bridge post"
```

---

### Task 14: `index.js` — entry point

Thin bootstrap that loads config, builds clients, calls `tick()`, exits.

**Files:**
- Create: `automation/notion-pb-sync/src/index.js`

- [ ] **Step 1: Write `index.js`**

Write `automation/notion-pb-sync/src/index.js`:

```js
import { loadConfig } from './config.js'
import { createNotionClient } from './notion.js'
import { createPostBridgeClient } from './post-bridge.js'
import { tick } from './tick.js'

async function main() {
  const cfg = loadConfig()
  const notion = createNotionClient(cfg.notion)
  const pb = createPostBridgeClient(cfg.postBridge)
  const startedAt = Date.now()
  console.log(`[${new Date().toISOString()}] tick start`)
  await tick({ notion, pb, accountMap: cfg.accountMap })
  console.log(`[${new Date().toISOString()}] tick done in ${Date.now() - startedAt}ms`)
}

main().catch(err => {
  console.error('tick crashed:', err)
  process.exit(1)
})
```

- [ ] **Step 2: Smoke test (dry — no real API call needed yet)**

```bash
node src/index.js
```

Expected: throws on missing env vars. That's correct — confirms config loader runs.

- [ ] **Step 3: Commit**

```bash
git add src/index.js
git commit -m "feat(sync): index.js entry point"
```

---

### Task 15: `scripts/apply-schema.js` — Notion schema setup script

Idempotent script that applies the six schema changes via Notion API. Run once before first deploy.

**Files:**
- Create: `automation/notion-pb-sync/scripts/apply-schema.js`

- [ ] **Step 1: Implement `apply-schema.js`**

Write `automation/notion-pb-sync/scripts/apply-schema.js`:

```js
#!/usr/bin/env node
// Idempotent Notion schema setup for the Content DB.
// Run: node scripts/apply-schema.js
//
// Adds:
//   - Status options: Scheduling, Failed (preserves existing options)
//   - Post Bridge ID (rich_text)
//   - Media (files)
//   - Published URLs (rich_text) — replaces existing 'Published URL' (url)
//   - Notes (rich_text)
//   - Last Sync At (date)

import { loadConfig } from '../src/config.js'

const cfg = loadConfig()
const headers = {
  'Authorization': `Bearer ${cfg.notion.token}`,
  'Notion-Version': cfg.notion.version,
  'Content-Type': 'application/json'
}

async function getDataSource() {
  const res = await fetch(`https://api.notion.com/v1/data_sources/${cfg.notion.dataSourceId}`, { headers })
  if (!res.ok) throw new Error(`GET data source failed: ${res.status} ${await res.text()}`)
  return res.json()
}

async function patchDataSource(properties) {
  const res = await fetch(`https://api.notion.com/v1/data_sources/${cfg.notion.dataSourceId}`, {
    method: 'PATCH',
    headers,
    body: JSON.stringify({ properties })
  })
  if (!res.ok) throw new Error(`PATCH data source failed: ${res.status} ${await res.text()}`)
  return res.json()
}

function mergeStatusOptions(existing, additions) {
  const names = new Set(existing.map(o => o.name))
  const added = additions.filter(a => !names.has(a.name))
  return [...existing, ...added]
}

async function main() {
  const ds = await getDataSource()
  const props = ds.properties

  const patch = {}

  // 1. Status: add Scheduling + Failed
  const currentStatusOpts = props.Status?.select?.options || []
  const mergedOpts = mergeStatusOptions(currentStatusOpts, [
    { name: 'Scheduling', color: 'gray' },
    { name: 'Failed', color: 'red' }
  ])
  if (mergedOpts.length !== currentStatusOpts.length) {
    patch.Status = { select: { options: mergedOpts } }
  }

  // 2. Post Bridge ID
  if (!props['Post Bridge ID']) {
    patch['Post Bridge ID'] = { rich_text: {} }
  }

  // 3. Media
  if (!props.Media) {
    patch.Media = { files: {} }
  }

  // 4. Published URLs (rich_text) — also remove old 'Published URL' (url) if present
  if (!props['Published URLs']) {
    patch['Published URLs'] = { rich_text: {} }
  }
  if (props['Published URL']) {
    // Setting a property to null removes it
    patch['Published URL'] = null
  }

  // 5. Notes
  if (!props.Notes) {
    patch.Notes = { rich_text: {} }
  }

  // 6. Last Sync At
  if (!props['Last Sync At']) {
    patch['Last Sync At'] = { date: {} }
  }

  if (Object.keys(patch).length === 0) {
    console.log('Schema already up to date — nothing to do.')
    return
  }

  console.log('Applying changes:', Object.keys(patch).join(', '))
  await patchDataSource(patch)
  console.log('Done.')
}

main().catch(err => {
  console.error('apply-schema failed:', err)
  process.exit(1)
})
```

- [ ] **Step 2: Commit (don't run yet — needs Juan's review against the live DB)**

```bash
git add scripts/apply-schema.js
git commit -m "feat(sync): idempotent Notion schema setup script"
```

- [ ] **Step 3: Manual review checkpoint**

Before running `npm run schema:apply` against the live DB, Juan reviews the script. If approved:

```bash
# Export Notion env vars or copy from content/.notion-config.json
export NOTION_TOKEN=<from content/.notion-config.json>
export NOTION_CONTENT_DATA_SOURCE_ID=<from content/.notion-config.json>
export POST_BRIDGE_API_KEY=<from windows env>
export PB_ACCOUNT_LINKEDIN=25903
export PB_ACCOUNT_THREADS=25902
export PB_ACCOUNT_TIKTOK=25901
export PB_ACCOUNT_YOUTUBE=25900
export PB_ACCOUNT_TWITTER=25899
export PB_ACCOUNT_INSTAGRAM=25898

npm run schema:apply
```

Expected: `Applying changes: Status, Post Bridge ID, Media, Published URLs, Published URL, Notes, Last Sync At` → `Done.` Second run: `Schema already up to date — nothing to do.`

---

### Task 16: Railway deploy + cron config

**Files:**
- Create: `automation/notion-pb-sync/railway.toml`

- [ ] **Step 1: Write `railway.toml`**

Write `automation/notion-pb-sync/railway.toml`:

```toml
[build]
builder = "NIXPACKS"

[deploy]
startCommand = "npm start"
cronSchedule = "*/5 * * * *"
restartPolicyType = "NEVER"
```

- [ ] **Step 2: Commit**

```bash
git add railway.toml
git commit -m "chore(sync): Railway cron config (every 5 min)"
```

- [ ] **Step 3: Manual deploy (Juan)**

```bash
# In automation/notion-pb-sync/
railway init           # create new project
railway link           # link to project
railway up             # deploy
```

Then in Railway dashboard:
- Set all env vars from `.env.example` (real values)
- Verify cron schedule shows in the Service settings.

Expected: first scheduled tick fires within 5 minutes; Railway logs show `tick start` / `tick done`.

---

### Task 17: End-to-end manual test

**Files:** none (this is a verification step)

- [ ] **Step 1: Create a test row in Notion Content DB**

In Notion:
- Title: `Test row — delete me after verifying`
- Status: `Drafting`
- Platform: `LinkedIn` only
- Date: 30 minutes from now
- Body: A short caption like "Test post — please ignore" (no firewall-matching words)

- [ ] **Step 2: Flip Status to `Ready`**

In Notion: change Status from `Drafting` to `Ready`.

- [ ] **Step 3: Wait up to 5 min, observe Railway logs**

Expected: Railway log shows `tick start` → calls → `tick done`. Within seconds, Notion row should reflect:
- Status: `Scheduled`
- Post Bridge ID: populated
- Last Sync At: now

- [ ] **Step 4: Verify post-bridge has the post**

Open the post-bridge dashboard → scheduled posts → confirm the test post is there with correct caption + scheduled time + LinkedIn account.

- [ ] **Step 5: Wait for scheduled time, then verify Published**

After the post actually publishes (at the scheduled Date), wait one more tick (≤5min). The row should flip to `Published` with `Published URLs` filled in.

- [ ] **Step 6: Clean up**

Delete the test row in Notion. (No need to delete the published LinkedIn post unless you want to.)

- [ ] **Step 7: Open PR**

```bash
git push -u origin feat/notion-pb-sync
gh pr create --title "feat(sync): Notion -> post-bridge publish automation" --body "$(cat <<'EOF'
## Summary
- New Node.js service at `automation/notion-pb-sync/` syncing Notion Content DB → post-bridge
- Stateless cron-driven reconciliation, every 5 min on Railway
- 1:1 mapping (one Notion row → one post-bridge post with multiple social_accounts)
- Crash-safe via Scheduling intermediate status + caption-hash recovery
- See spec: `docs/superpowers/specs/2026-05-26-notion-postbridge-sync-design.md`

## Test plan
- [x] Unit tests passing (`npm test`)
- [x] Schema applied to live Notion DB via `npm run schema:apply`
- [x] End-to-end manual test: created Ready row → verified Scheduled in <5min → verified Published after publish
- [ ] Railway logs reviewed for first week of operation

🤖 Generated with [Claude Code](https://claude.com/claude-code)
EOF
)"
```

---

## Self-review

Spec coverage check:
- Schema additions (Failed, Scheduling, Post Bridge ID, Media, Published URLs, Notes, Last Sync At) → covered in Task 15.
- State machine transitions → Task 2 (validation logic), Tasks 9-13 (transitions in tick).
- 1:1 multi-platform model → Task 9 (mapping in `handleReady`).
- Caption extraction + sources header strip + char-limit validation → Task 3.
- Phase 1 firewall → Task 4.
- Media flow (Notion file → upload → media_id) → Task 8.
- Cron cadence 5 min → Task 16 (`*/5 * * * *`).
- Crash safety via Scheduling + caption-hash recovery → Task 10.
- Revert/cancel detection → Task 13.
- Edit propagation → Task 12.
- Railway deployment → Task 16.
- E2E verification → Task 17.

Placeholder check: no `TBD` / `TODO` / "implement later" remain in the plan.

Type consistency check: function and method names match across tasks. `createNotionClient`, `createPostBridgeClient`, `tick`, `handleReady`, `handleScheduling`, `handleScheduled` are stable across their definitions. `STATUS` enum constants used consistently.

---

## Execution Handoff

Plan complete and saved to `docs/superpowers/plans/2026-05-26-notion-postbridge-sync.md`. Two execution options:

**1. Subagent-Driven (recommended)** — I dispatch a fresh subagent per task, review between tasks, fast iteration. Best for a 17-task plan like this where momentum matters.

**2. Inline Execution** — Execute tasks in this session using executing-plans. Better when you want to watch each step closely; slower.

**Which approach?**
