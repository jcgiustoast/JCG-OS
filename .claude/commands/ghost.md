---
description: Draft a response in Juan's voice, grounded in his stated beliefs and writing
argument-hint: <question>
---

Answer a question the way Juan would, based on what's already in JCG-OS. READ-ONLY.

Question: **$ARGUMENTS**

If no question was provided, ask Juan what to answer and stop.

## Steps

1. Identify the domain of the question (professional? content? learning? personal?). Route to the relevant space.
2. Read the relevant `wiki/index.md` descriptions to find pages touching the question.
3. Read the 3-5 pages most relevant to the question in full.
4. Scan recent log entries (last 30 days) in the matching space for Juan's phrasing, tone, and recent stances on the topic.
5. Draft the response.

## Output

- **Draft response** — written as Juan would write it. First person. Direct. No throat-clearing. Whatever length the question deserves.
- **Sources** — bullet list of the pages and log entries you pulled from. Use `[[page]]` and `log [YYYY-MM-DD]`.
- **Where I'm guessing** — any place the draft extends beyond what's in the vault. Mark clearly so Juan can correct.

## Rules

- Voice rules from `CLAUDE.md`: push back, reason from first principles, say when unsure. That applies here too — if Juan's recorded views are thin, say so rather than inventing a stance.
- No emojis.
- If the vault contradicts itself on this topic, flag the contradiction in the draft, don't paper over it.