# Close Session

Cleanly close the current work session. Ensures local, remote, GitHub, and
the project's deploy target (if any) are in sync and nothing is lost.

## Scope

`/close` operates on the **current chat's work**: the current branch in the
current worktree, plus any worktrees this chat itself created. Other branches,
unrelated worktrees, and parallel-chat work are **never touched**.

If cwd is not inside a git repo, abort with:
`Not in a git repo — cd into the project first.`

## Instructions

Execute these steps in order. Print a one-line status (`OK` / `SKIPPED` /
`PENDING <reason>`) at the end of each step so the summary can be assembled.

### 1. Check for uncommitted work

Run `git status` in the current working directory. If there are staged or unstaged changes:
- Show the user what's pending
- Ask if they want to commit before closing
- If yes, create a conventional commit with a clear message

If there are untracked files, mention them but don't auto-add.

`--no-commit` arg: skip this step.

### 2. Push committed work to remote

Check the branch's position relative to its upstream:

```
git fetch origin <branch> --quiet
git rev-list --left-right --count origin/<branch>...<branch>
```

- Ahead > 0 and behind = 0 → run `git push` and print its output. No prompt.
- No upstream → run `git push -u origin <branch>` and print its output. No prompt.
- Behind > 0 → do NOT push (would need rebase/force). Surface the count, leave for the user to reconcile.
- Ahead = 0 and behind = 0 → nothing to push, continue.

This auto-pushes any branch including `main`. The user opted in. Pass
`--no-push` to skip, or use a PR flow before `/close` for gated repos.

### 3. Open PRs from this branch

```
gh pr list --head <branch> --state open --json number,title,url,isDraft,mergeable
```

For each open PR: show number / title / URL / draft / mergeable, then prompt
merge / close / leave-open. Do not auto-merge or auto-close. If `gh` fails with
"Repository not found", it's the two-account trap — try
`gh auth switch --user jcgiustoast` and retry; otherwise surface the raw error
and continue with `PENDING gh auth`.

### 4. Deploy sync (auto-detect host)

Skip entirely if `--no-deploy`.

**Do not assume Railway.** Detect which host the project actually deploys to,
then run the host-specific sync. If detection is ambiguous (multiple signals)
ask the user which target to sync. If no host is detected, print
`SKIPPED (no deploy target detected)` and continue.

#### 4a. Detect the host

Check these signals in order. Stop at the first match unless multiple are
present (then ask):

| Host | Detection signals |
|---|---|
| **Railway** | `railway.json` / `railway.toml` at repo root; `.railway/` dir; `railway status` returns a linked project (not an error) |
| **AWS (ECS/Fargate)** | `task-definition.json`, `ecs-*.yml`, `appspec.yml`, `Dockerrun.aws.json`; `aws ecs` references in `Makefile` / `package.json` scripts / `.github/workflows/*.yml` |
| **AWS (Lambda / API Gateway / SAM / CDK)** | `template.yaml` (SAM), `samconfig.toml`, `serverless.yml` (Serverless framework), `cdk.json`, `sst.config.*`, `.aws-sam/` dir, `aws lambda` in workflows |
| **AWS (S3 + CloudFront CDN)** | `aws s3 sync` / `cloudfront create-invalidation` in scripts or workflows |
| **Vercel** | `vercel.json`, `.vercel/` dir |
| **Netlify** | `netlify.toml`, `.netlify/` dir |
| **Fly.io** | `fly.toml` |
| **Render** | `render.yaml` |
| **Cloudflare (Pages/Workers)** | `wrangler.toml`, `wrangler.jsonc` |
| **Heroku** | `Procfile` + `app.json` (or a `heroku` git remote) |
| **GitHub Pages** | workflow that runs `actions/deploy-pages` |
| **CI-driven (host unclear)** | `.github/workflows/deploy*.yml` or similar but no other signal — treat as "push-and-watch" |

Cross-check user memory for the current project if available
(e.g. Mars Men LP Generator = AWS ECS/Fargate, Mars Men Quiz = AWS Lambda +
API Gateway + S3/CloudFront, Solari = Railway). Memory hints when it disagrees
with repo signals; repo signals win, but flag the mismatch.

#### 4b. Sync the detected host

For each detected target, compare what's deployed vs. `git rev-parse HEAD` and
take the host-appropriate action. Never run host CLI commands you haven't
confirmed exist locally.

**Railway** — for each service in `railway status` for this project+environment,
compare the latest **successful** deployment's commit SHA against `HEAD`.

| Latest deploy SHA | In-flight deploy? | Verdict | Action |
|---|---|---|---|
| == HEAD | — | Up-to-date | `OK` |
| != HEAD | yes, in progress | Auto-deploy running | Poll ≤3 min → `OK` / `PENDING build` |
| != HEAD | no, > 5 min old | Manual-mode | Prompt `railway up --service <name> --ci` from project root |

Railway quirks: re-link from inside the project root before `railway up`
(a parent-dir link OOMs the indexer); verify the target service name in
`railway status` before shipping (e.g. Solari `mmm-r` slot can receive the
wrong image). `railway up` may exit 1 client-side while the upload landed —
verify via the deployment list, not the exit code.

**AWS (CI-driven, the common case here)** — most Mars Men AWS repos deploy
automatically on push to `main` via GitHub Actions. After step 2's push:

1. List recent runs of the deploy workflow:
   `gh run list --workflow=<deploy-workflow> --branch <branch> --limit 3`.
2. If a run for the just-pushed SHA is `in_progress` or `queued`, poll up to
   ~3 min → `OK` (success) / `PENDING build` (still running) / surface failure.
3. If no workflow exists, ask whether to invoke the project's documented
   deploy command (e.g. `make deploy`, `sam deploy`, `cdk deploy`,
   `aws s3 sync && aws cloudfront create-invalidation`). Do not guess —
   prompt with the candidate command read from `Makefile` / `package.json` /
   project CLAUDE.md.

**Vercel / Netlify / Cloudflare Pages** — usually git-push triggered. After
step 2's push, list the latest deployment via the host's CLI if available
(`vercel ls`, `netlify status`, `wrangler deployments list`) and confirm the
HEAD SHA shipped. If CLI is missing, print `PENDING (verify in <host> dashboard)`.

**Fly.io / Render / Heroku / others** — same pattern: if the project's
documented deploy command lives in CLAUDE.md or `package.json` scripts, prompt
to run it; otherwise surface `PENDING (manual deploy)`.

**Never** invoke a host CLI for a host you didn't detect, and never force a
Railway link / `railway up` on a repo that doesn't use Railway.

### 5. Clean up THIS chat's worktrees

Automatically remove worktrees and their branches that **this chat created or
worked on**. Never touch worktrees or branches unrelated to this chat — a
parallel session may be using them. `--keep-worktrees` arg: skip this step.

1. **Identify chat-owned worktrees.** From this conversation's context, list the
   worktree paths + branches this chat created (e.g. `git worktree add` or a
   superpowers worktree). Cross-check against `git worktree list --porcelain`.
   If none, print `OK (none)` and skip. Only act on that list — never glob
   `.worktrees/` and delete blindly, never act on the main/trunk worktree.

2. **Operate from the main checkout root**, never from inside a worktree being removed:
   ```
   MAIN_ROOT=$(git -C "$(git rev-parse --git-common-dir)/.." rev-parse --show-toplevel)
   cd "$MAIN_ROOT"
   ```

3. **Remove only when safe** — for each chat-owned worktree, ALL must hold:
   - working tree clean — `git -C <wt> status --porcelain` empty;
   - no open PRs from the branch — `gh pr list --head <branch> --state open` empty;
   - branch merged (squash-aware) — a PR for it is `MERGED`
     (`gh pr list --head <branch> --state merged`), or `git diff <trunk>..<branch>` is empty.

   Then:
   ```
   git worktree remove <path>
   git branch -D <branch>             # force: squash-merged branches aren't trunk ancestors
   git push origin --delete <branch>  # only if the remote branch exists and its PR is merged
   ```

4. **Never remove** a chat-owned worktree that is dirty, unmerged, or has an
   open PR — list it under Next steps instead.

5. After removals, run `git worktree prune`.

### 6. Update project CLAUDE.md if needed

Read the project's CLAUDE.md. Update only sections that became stale this session:
- New features or patterns added
- Known issues resolved
- Architecture / deployment-state changes
- Open questions answered or new ones discovered

Only update stale sections. Do NOT rewrite accurate ones, and do not append
"we did X today" narrative (that's for commits/memory). Avoid the
"always update CLAUDE.md" framing trap (memory: `claudemd-no-always-update-rule`).

`quick` arg: skip this step.

### 7. Save meaningful session learnings to memory

Persist to `C:\Users\jcgiu\.claude-personal\projects\c--Users-jcgiu\memory\`:
- Resolved questions (move Open → Resolved)
- New project context (decisions, blockers, deadlines)
- User feedback or corrections
- External references discovered

Do NOT save: things already in CLAUDE.md or code; ephemeral debugging steps;
anything derivable from git log; duplicates (update in place instead).

`quick` arg: skip this step.

### 8. Summary

Print a concise closing summary:

```
SESSION CLOSED
==============
Project:   <name>
Branch:    <branch> (<ahead/behind>)
Changes:   <committed/uncommitted/none>
Pushed:    <yes <sha> | nothing to push | PENDING (behind upstream)>
PRs:       <none open | merged #N | leave-open #N>
Deploy:    <host>: <up-to-date | deployed | PENDING build | skipped (no target)>
Worktrees: <removed N (branches) | none owned | kept N | skipped>
Memory:    <updated/no changes>
Docs:      <updated/no changes>

Next steps:
- <1-3 actionable items, incl. any PENDING items or kept worktrees>
```

If any step is `PENDING` or a chat-owned worktree was kept, do not declare the
session fully closed — list what the user still has to do.

## Arguments

$ARGUMENTS can be:
- (empty) - Full close, all 8 steps
- `quick` - Skip steps 6 + 7 (docs/memory); still run git + PR + Railway + worktree cleanup
- `--no-commit` - Skip step 1's commit prompt
- `--no-push` - Skip step 2's auto-push (commit only, don't ship)
- `--no-deploy` - Skip step 4 (host deploy sync), when work isn't ready to ship
- `--keep-worktrees` - Skip step 5 (leave this chat's worktrees in place)
