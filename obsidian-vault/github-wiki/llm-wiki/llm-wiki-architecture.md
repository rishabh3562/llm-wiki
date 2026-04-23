---
repo: llm-wiki
type: architecture
commit: 135162b583a65494404b2cd8625b29154789a513
date: 2026-04-23
tags: [llm-wiki, architecture]
related: [[llm-wiki-index]]
---
# Architecture — llm-wiki
## Key Files (by size)

-rw-r--r-- 1 root root 18236 Apr 23 22:01 ./run_llm_wiki.py
-rw-r--r-- 1 root root 14210 Apr 23 22:01 ./ledger.json
-rw-r--r-- 1 root root 12960 Apr 23 22:01 ./obsidian-vault/github-wiki/agents-ed/intent_recovery.md
-rw-r--r-- 1 root root 12414 Apr 23 22:01 ./repos.json
-rw-r--r-- 1 root root  5947 Apr 23 22:01 ./obsidian-vault/github-wiki/Devr.AI/Devr.AI-static_analysis.md
-rw-r--r-- 1 root root  5901 Apr 23 22:01 ./obsidian-vault/github-wiki/PictoPy/PictoPy-static_analysis.md
-rw-r--r-- 1 root root  5828 Apr 23 22:01 ./obsidian-vault/github-wiki/agents-ed/agents-ed-static_analysis.md
-rw-r--
## High Churn Files
     66 
      3 .gitignore
      2 run_llm_wiki.py
      2 repos.json
      2 ledger.json
      1 obsidian-vault/github-wiki/volt-bnb/self_portrait.md
      1 obsidian-vault/github-wiki/volt-bnb/progression.md
      1 obsidian-vault/github-wiki/volt-bnb/patterns.md
      1 obsidian-vault/github-wiki/volt-bnb/intent_recovery.md
      1 obsidian-vault/github-wiki/volt-bnb/improvements.md
      1 obsidian-vault/github-wiki/volt-bnb/architecture.md
      1 obsidian-vault/github-wiki/vector-shift-yc-assignment/self_portrait.md
      1 obsidian-vault/github-wiki/vector-shift-yc-assignment/progressi
## Complexity
run_llm_wiki.py
    F 95:0 process_repo - D (26)
    F 371:0 main - C (11)
    F 47:0 discover_github_repos - B (9)
    F 24:0 load_json - A (2)
    F 34:0 run_cmd - A (2)
    F 41:0 get_github_token - A (2)
    F 30:0 save_json - A (1)

7 blocks (classes, functions, methods) analyzed.
Average complexity: B (7.571428571428571)

