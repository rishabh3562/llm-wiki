---
repo: PocketFlow-Tutorial-Codebase-Knowledge
type: quality_complexity
commit: ce0b14a8ef5b19825620efb2f61c6cb3f224ef50
date: 2026-05-01
tags: [PocketFlow-Tutorial-Codebase-Knowledge, quality_complexity]
related: [[PocketFlow-Tutorial-Codebase-Knowledge-index]]
---

# Quality — Complexity Signals

## Evidence
nodes.py
    M 118:4 IdentifyAbstractions.exec - C (17)
    M 289:4 AnalyzeRelationships.exec - C (16)
    M 454:4 OrderChapters.exec - C (11)
    M 630:4 WriteChapters.exec - B (10)
    M 754:4 CombineTutorial.prep - B (10)
    M 538:4 WriteChapters.prep - B (9)
    C 84:0 IdentifyAbstractions - B (8)
    C 240:0 AnalyzeRelationships - B (8)
    C 537:0 WriteChapters - B (8)
    C 410:0 OrderChapters - B (7)
    M 411:4 OrderChapters.prep - A (5)
    C 753:0 CombineTutorial - A (5)
    F 11:0 get_content_for_indices - A (3)
    C 22:0 FetchRepo - A (3)
    M 23:4 FetchRepo.prep - A (3)
    M 51:4 FetchRepo.exec - A (3)
    M 241:4 AnalyzeRelationships.prep - A (3)
    M 85:4 IdentifyAbstractions.prep - A (2)
    M 854:4 CombineTutorial.exec - A (2)
    M 80:4 FetchRepo.post - A (1)
    M 234:4 IdentifyAbstractions.post - A (1)
    M 404:4 AnalyzeRelationships.post - A (1)
    M 532:4 OrderChapters.post - A (1)
    M 745:4 WriteChapters.post - A (1)
    M 878:4 CombineTutorial.post - A (1)
flow.py
    F 12:0 create_tutorial_flow - A (1)
main.py
    F 39:0 main - B (8)


## Related
- [[PocketFlow-Tutorial-Codebase-Knowledge-improvements]]
- [[PocketFlow-Tutorial-Codebase-Knowledge-architecture]]
