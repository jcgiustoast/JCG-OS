## Session Protocols

### Morning Briefing
When Juan says "morning briefing" or "what's on my plate":
1. Read both `life/wiki/index.md` and `content/wiki/index.md`
2. Read `life/wiki/professional.md` and `life/wiki/projects.md` for priorities
3. Read `life/memory/log.md` and `content/memory/log.md` for recent entries
4. Surface: today's priorities + context, what changed since last session
5. Flag stale entries, open decisions, or "to be filled" sections

### Ingest Workflow
When Juan says "ingest [filename]":
1. Read the source file in the relevant `raw/` folder
2. Discuss key takeaways with Juan
3. Create or update relevant wiki pages (a single source might touch 5-15 pages across both spaces)
4. Update the relevant `wiki/index.md`
5. Append structured entry to the relevant `memory/log.md`

### Query Workflow
When Juan asks a question:
1. Read the relevant `wiki/index.md` to find pages (check both spaces if topic spans them)
2. Read those pages
3. Synthesize answer citing wiki pages as `[[page-name]]`
4. Answers can take different forms — markdown page, comparison table, chart, structured analysis. Pick the format that fits.
5. **Good answers should be filed back into the wiki.** Offer to file them. Explorations compound just like ingested sources.

### Lint Workflow
When Juan says "lint" or "health check":
1. Scan for contradictions between pages
2. Find orphan pages (no inbound links)
3. List concepts mentioned 3+ times without their own page
4. Check for stale claims or "to be filled" placeholders
5. Suggest questions to investigate or sources to ingest next
6. Append lint results to the relevant `memory/log.md`

### Compile Workflow
When Juan says "compile":
1. Read recent `memory/log.md` entries from both spaces
2. Extract recurring patterns, themes, or insights
3. Create or update topic pages in `memory/wiki.md`
4. Cross-link with relevant wiki pages

### Update Protocol
- **After a conversation:** Claude summarizes what changed -> Juan approves -> Claude writes with today's date
- **Weekly lint:** Juan can ask Claude to review the whole system
- **Compile cycle:** Claude reads logs and compiles patterns into knowledge pages
