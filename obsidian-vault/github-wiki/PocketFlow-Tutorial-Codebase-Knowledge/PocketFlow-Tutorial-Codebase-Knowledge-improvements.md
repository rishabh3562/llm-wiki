---
repo: PocketFlow-Tutorial-Codebase-Knowledge
type: improvements
commit: ce0b14a8ef5b19825620efb2f61c6cb3f224ef50
date: 2026-04-23
tags: [PocketFlow-Tutorial-Codebase-Knowledge, improvements]
related: [[PocketFlow-Tutorial-Codebase-Knowledge-index]]
---
# Improvements — PocketFlow-Tutorial-Codebase-Knowledge
## Dead Code
nodes.py:2: unused import 're' (90% confidence)
nodes.py:23: unused method 'prep' (60% confidence)
nodes.py:51: unused method 'exec' (60% confidence)
nodes.py:80: unused method 'post' (60% confidence)
nodes.py:85: unused method 'prep' (60% confidence)
nodes.py:118: unused method 'exec' (60% confidence)
nodes.py:234: unused method 'post' (60% confidence)
nodes.py:241: unused method 'prep' (60% confidence)
nodes.py:289: unused method 'exec' (60% confidence)
nodes.py:404: unused method 'post' (60% confidence)
nodes.py:411: unused method 'prep' (60% confidence)
nodes.py:454: unused method 'exec' (
## High Complexity Areas
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
    M 
