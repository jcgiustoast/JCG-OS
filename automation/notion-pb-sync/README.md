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
