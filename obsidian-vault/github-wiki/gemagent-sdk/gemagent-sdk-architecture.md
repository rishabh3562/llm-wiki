---
repo: gemagent-sdk
type: architecture
commit: 48b9cf8ec2d6bc0aada67fb8a0b77abb2c0e47cb
date: 2026-04-23
tags: [gemagent-sdk, architecture]
related: [[gemagent-sdk-index]]
---
# Architecture — gemagent-sdk
## Key Files (by size)

-rw-r--r-- 1 root root 10898 Apr 23 20:00 ./examples/test-0.1.1.ipynb
-rw-r--r-- 1 root root  4319 Apr 23 20:00 ./.gitignore
-rw-r--r-- 1 root root  3474 Apr 23 20:00 ./requirement.txt
-rw-r--r-- 1 root root  3465 Apr 23 20:00 ./gemagent/agent.py
-rw-r--r-- 1 root root  2509 Apr 23 20:00 ./examples/hello_tool_example.ipynb
-rw-r--r-- 1 root root  2069 Apr 23 20:00 ./gemagent/runner.py
-rw-r--r-- 1 root root  1451 Apr 23 20:00 ./tests/test_agent.py
-rw-r--r-- 1 root root  1196 Apr 23 20:00 ./README.md
-rw-r--r-- 1 root root   656 Apr 23 20:00 ./pyproject.toml
-rw-r--r-- 1 root root   553 Apr 23
## High Churn Files
      7 
      3 pyproject.toml
      3 gemagent/agent.py
      3 gemagent/__init__.py
      3 README.md
      2 tests/test_agent.py
      2 setup.py
      2 gemagent/utils.py
      2 gemagent/tools.py
      2 gemagent/stream.py
      2 gemagent/parser.py
      2 gemagent/config.py
      2 examples/hello_tool_example.ipynb
      1 requirement.txt
      1 gemagent/runner.py
      1 examples/test-0.1.1.ipynb
      1 examples/.env.example
      1 .gitignore

## Complexity
tests/test_agent.py
    F 7:0 test_say_hello_tool - A (2)
    F 11:0 test_agent_without_tool - A (2)
    F 29:0 test_agent_with_tool - A (2)
gemagent/parser.py
    F 1:0 parse_args - A (3)
gemagent/utils.py
    F 4:0 trace - A (1)
gemagent/stream.py
    C 5:0 STREAM_SIM - A (3)
    M 13:4 STREAM_SIM.stream_events - A (2)
    M 10:4 STREAM_SIM.__init__ - A (1)
gemagent/tools.py
    F 3:0 tool_custom - A (2)
    F 16:0 say_hello - A (1)
    F 21:0 word_count - A (1)
gemagent/runner.py
    M 10:4 Runner.run - B (7)
    C 8:0 Runner - B (6)
    C 49:0 STREAM_SIM - A (3)
    M 39:4 Runner.run_strea
