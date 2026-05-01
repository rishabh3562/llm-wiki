---
# AUTONOMY

## ALLOWED without asking
- Read any file in /repos/ (read-only)
- Write to /opt/llm_wiki/output/ and /opt/llm_wiki/obsidian-vault/
- MongoDB read/write: snippets, analysis_runs, repo_status
- git: clone, fetch, log, diff, rev-parse, show
- radon, vulture, pipdeptree (read-only)

## REQUIRES MY APPROVAL
- Any git write op
- Deleting any file
- New MongoDB collections beyond approved 3
- Setting up or changing cron jobs

## NEVER
- Write inside /repos/
- Print or store secrets
- Re-analyze a completed repo
- Use "master"