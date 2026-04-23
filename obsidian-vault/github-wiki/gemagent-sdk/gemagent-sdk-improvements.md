---
repo: gemagent-sdk
type: improvements
commit: 48b9cf8ec2d6bc0aada67fb8a0b77abb2c0e47cb
date: 2026-04-23
tags: [gemagent-sdk, improvements]
related: [[gemagent-sdk-index]]
---
# Improvements — gemagent-sdk
## Dead Code
gemagent/agent.py:84: unused method 'run_streamed' (60% confidence)
gemagent/runner.py:38: unused method 'run_streamed' (60% confidence)
gemagent/tools.py:20: unused function 'word_count' (60% confidence)
gemagent/utils.py:3: unused function 'trace' (60% confidence)
tests/test_agent.py:17: unused variable 'model_name' (100% confidence)
tests/test_agent.py:19: unused variable 'prompts' (100% confidence)
tests/test_agent.py:35: unused variable 'model_name' (100% confidence)
tests/test_agent.py:37: unused variable 'prompts' (100% confidence)

## High Complexity Areas
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
