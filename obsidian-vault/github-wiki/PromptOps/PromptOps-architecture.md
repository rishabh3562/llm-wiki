---
repo: PromptOps
type: architecture
commit: fe863aa3feaea4fe944787e48ad613ee0c282d7c
date: 2026-04-23
tags: [PromptOps, architecture]
related: [[PromptOps-index]]
---
# Architecture — PromptOps
## Key Files (by size)

-rw-r--r-- 1 root root 8028 Apr 23 08:01 ./core/controller.py
-rw-r--r-- 1 root root 4353 Apr 23 08:01 ./.gitignore
-rw-r--r-- 1 root root 4145 Apr 23 08:01 ./agents/planner.py
-rw-r--r-- 1 root root 3554 Apr 23 08:01 ./README.md
-rw-r--r-- 1 root root 2797 Apr 23 08:01 ./agents/evaluator.py
-rw-r--r-- 1 root root 2483 Apr 23 08:01 ./agents/vision.py
-rw-r--r-- 1 root root 2351 Apr 23 08:01 ./agents/fixer.py
-rw-r--r-- 1 root root 1976 Apr 23 08:01 ./models/gemini.py
-rw-r--r-- 1 root root 1687 Apr 23 08:01 ./models/gpt.py
-rw-r--r-- 1 root root 1634 Apr 23 08:01 ./main.py
-rw-r--r-- 1 root ro
## High Churn Files
     18 
     10 promptops/cli.py
      7 promptops/llm/openai_client.py
      7 promptops/dispatcher.py
      6 promptops/skills/unknown.py
      6 promptops/skills/registry.py
      6 promptops/llm/gemini_client.py
      6 promptops/core/task_planner.py
      6 promptops/actions/os/apps.py
      5 tests/test_unknown_skill.py
      5 requirements.txt
      5 promptops/config.py
      4 web/backend/routes/prompt.py
      4 web/backend/main.py
      4 skills_suggestions.jsonl
      4 promptops/skills/skill_review_agent.py
      4 promptops/skills/skill_loader.py
      4 promptops/llm/base.py
  
## Complexity
core/controller.py
    M 50:4 Controller._execute_step_with_retry - C (16)
    C 35:0 Controller - B (8)
    M 43:4 Controller.execute_plan - A (3)
    M 36:4 Controller.__init__ - A (2)
core/memory.py
    C 2:0 Memory - A (2)
    M 3:4 Memory.__init__ - A (1)
    M 6:4 Memory.record - A (1)
utils/logger.py
    F 2:0 log_action - A (1)
utils/screenshot.py
    F 4:0 capture_screenshot - A (1)
utils/coords.py
    F 3:0 parse - A (1)
utils/is_app_open.py
    F 3:0 is_app_open - A (3)
utils/timer.py
    F 3:0 wait - A (1)
models/gemini.py
    M 22:4 GeminiModel.chat - A (4)
    C 7:0 GeminiModel -
