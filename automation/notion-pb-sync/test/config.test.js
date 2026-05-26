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
