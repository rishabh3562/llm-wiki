---
repo: fastapi-blocking-test
type: static_analysis
commit: 2ec211ce9898c611642047c5a14cc35a1674acaa
date: 2026-05-01
tags: [fastapi-blocking-test, static_analysis]
related: [[fastapi-blocking-test-index]]
---

{
  "largest_files": "-rw-r--r-- 1 root root 188460 May  1 07:31 ./uv.lock\n-rw-r--r-- 1 root root   4688 May  1 07:31 ./.gitignore\n-rw-r--r-- 1 root root   1833 May  1 07:31 ./main.py\n-rw-r--r-- 1 root root    241 May  1 07:31 ./pyproject.toml\n-rw-r--r-- 1 root root      5 May  1 07:31 ./.python-version\n-rw-r--r-- 1 root root      0 May  1 07:31 ./README.md\n",
  "high_churn_files": "      1 uv.lock\n      1 pyproject.toml\n      1 main.py\n      1 README.md\n      1 .python-version\n      1 .gitignore\n      1 \n",
  "complexity": "main.py\n    F 57:0 run_job - A (2)\n    F 12:0 context_agent - A (1)\n    F 20:0 question_generator - A (1)\n    F 43:0 hello - A (1)\n    F 47:0 start_job - A (1)\n    F 53:0 get_status - A (1)\n    C 6:0 JobState - A (1)\n\n7 blocks (classes, functions, methods) analyzed.\nAverage complexity: A (1.1428571428571428)\n",
  "dead_code": "main.py:42: unused function 'hello' (60% confidence)\nmain.py:46: unused function 'start_job' (60% confidence)\nmain.py:52: unused function 'get_status' (60% confidence)\n"
}