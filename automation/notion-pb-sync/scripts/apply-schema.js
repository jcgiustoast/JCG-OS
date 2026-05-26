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
//   - Synced Edit Token (rich_text)

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

  // 7. Synced Edit Token
  if (!props['Synced Edit Token']) {
    patch['Synced Edit Token'] = { rich_text: {} }
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
