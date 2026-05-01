---
# RED_LINES — ABSOLUTE PROHIBITIONS

## 1. SOURCE REPO INTEGRITY
- NEVER run on source repos: git add, commit, push, checkout -b, merge, rebase, rm
- NEVER create/modify/delete any file inside /repos/<repo-name>/
- Allowed git only: clone, fetch, log, diff, rev-parse, show, status
- /repos/ is READ-ONLY. No exceptions.

## 2. SECRET PROTECTION
- NEVER read, log, print, or store: .env, *token*, *secret*, *key*, *credential*, *password* files
- If content has 20+ mixed alphanumeric chars that look like a key → replace with [REDACTED]
- Secrets must never appear in MongoDB, Obsidian, logs, or Telegram

## 3. OUTPUT ISOLATION
- All generated files → /opt/llm_wiki/output/<repo>/ ONLY
- Obsidian writes → /opt/llm_wiki/obsidian-vault/github-wiki/<repo>/ ONLY
- Zero file creation inside /repos/

## 4. NO CIRCULAR WRITES
- Analysis output never goes inside the source repo
- This prevents: analyze → write → new commit → re-analyze loop

## 5. NO DUPLICATE ANALYSIS
- Before analyzing any repo, check MongoDB repo_status collection
- If initial_analysis_done == true → SKIP. Do not re-analyze.
- MongoDB is the source of truth. Do not rely on ledger.json.

## 6. BRANCH CONVENTIONS
- Never use "master" — use "main" only
- Never create branches on source repos