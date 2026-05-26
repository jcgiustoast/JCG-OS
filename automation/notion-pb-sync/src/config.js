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
