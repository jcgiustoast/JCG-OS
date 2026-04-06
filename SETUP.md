# JC OS — Setup Instructions

## Step 1: Create the GitHub repo

```bash
gh repo create JCG-OS --public --clone
cd JCG-OS
```

## Step 2: Copy the JC OS files into the repo

Copy the entire contents (CLAUDE.md, wiki/, memory/, raw/, .gitignore) into your `JCG-OS` directory.

## Step 3: Initial commit

```bash
git add -A
git commit -m "Initial JC OS setup — personal operating system"
git push -u origin main
```

## Step 4: Point Obsidian at this folder

1. Open Obsidian
2. "Open folder as vault" -> select your `JCG-OS` folder
3. Enable "Graph view" to see how files link to each other
4. Optional: install the "Dataview" community plugin for queries across frontmatter fields

## Step 5: Use Claude Code

```bash
cd ~/path-to/JCG-OS
claude
```

Claude Code automatically reads CLAUDE.md at session start. No setup needed.

## Two Spaces

JC OS has two spaces in one vault:

- **life/** — Professional & personal: career, role, learning, projects, goals
- **content/** — Content creation & exploration: ideas, topics, research, drafts

Both are visible in Obsidian's graph view. Cross-references between spaces work naturally.

## Daily Workflow

1. Open terminal, `cd JCG-OS`, run `claude`
2. Say "morning briefing" -> Claude reads both spaces and surfaces priorities
3. Have your conversation
4. At the end, Claude proposes file updates -> you approve
5. Claude commits the changes (or you do it manually)
6. Obsidian reflects the changes instantly (same files)

## Key Commands

| Say this | Claude does this |
|----------|-----------------|
| "morning briefing" | Reads priorities from both spaces, recent logs, surfaces context |
| "ingest [filename]" | Processes raw/ source into wiki pages (routes to correct space) |
| "lint" or "health check" | Scans for contradictions, stale entries, gaps |
| "compile" | Extracts patterns from logs into knowledge topics |

## Reference Links

### Karpathy's LLM Wiki
- [Gist (LLM Wiki schema)](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f)
- [Tweet thread](https://x.com/karpathy/status/2039805659525644595)
- [Antigravity deep dive](https://antigravity.codes/blog/karpathy-llm-wiki-idea-file)
- [DAIR.AI walkthrough](https://academy.dair.ai/blog/llm-knowledge-bases-karpathy)

### Tools
- [Obsidian](https://obsidian.md) — Markdown IDE / vault viewer
- [Obsidian Web Clipper](https://obsidian.md/clipper) — Clip articles to markdown
- [Dataview plugin](https://blacksmithgu.github.io/obsidian-dataview/) — Query frontmatter fields

### Claude Code
- [How CLAUDE.md works](https://code.claude.com/docs/en/memory)
- [Writing a good CLAUDE.md](https://www.builder.io/blog/claude-md-guide)
