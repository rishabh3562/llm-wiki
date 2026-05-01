---
repo: fastapi-blocking-test
type: architecture
commit: 2ec211ce9898c611642047c5a14cc35a1674acaa
date: 2026-05-01
tags: [fastapi-blocking-test, architecture]
related: [[fastapi-blocking-test-index]]
---

# Architecture — fastapi-blocking-test

## Key Files (by size)

-rw-r--r-- 1 root root 188460 May  1 07:31 ./uv.lock
-rw-r--r-- 1 root root   4688 May  1 07:31 ./.gitignore
-rw-r--r-- 1 root root   1833 May  1 07:31 ./main.py
-rw-r--r-- 1 root root    241 May  1 07:31 ./pyproject.toml
-rw-r--r-- 1 root root      5 May  1 07:31 ./.python-version
-rw-r--r-- 1 root root      0 May  1 07:31 ./README.md

## High Churn Files
      1 uv.lock
      1 pyproject.toml
      1 main.py
      1 README.md
      1 .python-version
      1 .gitignore
      1 

## Complexity
main.py
    F 57:0 run_job - A (2)
    F 12:0 context_agent - A (1)
    F 20:0 question_generator - A (1)
    F 43:0 hello - A (1)
    F 47:0 start_job - A (1)
    F 53:0 get_status - A (1)
    C 6:0 JobState - A (1)

7 blocks (classes, functions, methods) analyzed.
Average complexity: A (1.1428571428571428)

