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
