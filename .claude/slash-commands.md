## Slash Commands

Custom commands live in `.claude/commands/`. Each is a markdown prompt invoked by filename. All are READ-ONLY unless noted.

| Command | Purpose |
|---------|---------|
| `/context` | Load full state — active projects, priorities, last 7 days of logs |
| `/today` | Prioritized plan for today from recent logs + stated priorities |
| `/closeday` | End-of-day recap; writes to `memory/log.md` after approval |
| `/trace <topic>` | Timeline of how an idea evolved across the vault |
| `/connect <A> \| <B>` | Find connections between two topics via link graph |
| `/ghost <question>` | Draft a response in Juan's voice from stated beliefs |
| `/challenge <topic>` | Pressure-test positions — contradictions, weak assumptions |
| `/ideas` | Generate tools/people/topics/writing ideas grounded in the vault |
| `/graduate` | Promote log asides to standalone pages; writes after approval |
| `/drift` | Surface recurring patterns Juan hasn't labeled yet |
| `/emerge` | Clusters ready to become a project, essay, or product |
| `/schedule` | Map stated priorities to a suggested weekly shape |
| `/process-inbox` | Triage captures in `life/raw/inbox/` and file them into the wiki |
| `/content` | Create LinkedIn/X/blog posts — builds personal brand, inbound for ASTEROI |
| `/content-research` | Scrape reference creators to find what's performing; feeds `/content` |
| `/engage` | Daily Twitter engagement briefing — pulls 24h tweets from curated DTC targets, scores reply opportunities. LinkedIn is manual (not automated) — see engagement-targets.md |

Only `/closeday`, `/graduate`, and `/process-inbox` write files, and all require explicit approval before doing so.
