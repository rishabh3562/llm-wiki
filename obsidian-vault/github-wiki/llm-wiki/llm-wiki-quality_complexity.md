---
repo: llm-wiki
type: quality_complexity
commit: 4405647d940b50e9991d7b7af9f1bbf907cba6d1
date: 2026-05-01
tags: [llm-wiki, quality_complexity]
related: [[llm-wiki-index]]
---

# Quality — Complexity Signals

## Evidence
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


## Related
- [[llm-wiki-improvements]]
- [[llm-wiki-architecture]]
