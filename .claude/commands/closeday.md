---
description: Close out the day — log progress, capture new ideas, carry unfinished items forward
---

End-of-day ritual. Captures what happened and queues what matters for tomorrow. WRITES to `memory/log.md` after Juan approves the draft.

Today is {{date}}.

## Steps

1. Ask Juan: "Quick recap — what did you work on today? What came up? Anything unfinished?" Wait for his answer. If he gives a short answer, probe once for specifics.
2. Review what changed in the vault today: git status inside JCG-OS for modified/created files. Read any files he edited in `wiki/` to understand what shifted.
3. Check log entries you may have written earlier today — don't duplicate them, build on them.
4. Draft a consolidated log entry for today (one per space if activity touched both).

## Draft format

```
## [YYYY-MM-DD] session | <short title>
- Progress: <what got done, concrete>
- New ideas / threads: <anything worth revisiting>
- Unfinished — carry to tomorrow: <items>
- Pages touched: wiki/foo.md, wiki/bar.md
```

Show the draft to Juan. Ask: `Append as-is, edit, or skip?`

## On approval

1. Append the draft to `life/memory/log.md` and/or `content/memory/log.md` (whichever spaces the activity touched).
2. If there are unfinished items marked "carry to tomorrow," that's useful context for the next `/today` run — no special action needed, the log will surface them.
3. Ask if Juan wants to commit.

## Rules

- Short and honest over long and performative. If the day was quiet, one line is fine.
- Don't invent accomplishments. If nothing happened, log nothing and say so.
- Cite pages touched so future `/trace` and `/context` runs can find them.
