---
repo: promptops-operator
type: architecture
commit: 8ff468dfc663fff299e9f03481001203f2f4a6d5
date: 2026-04-23
tags: [promptops-operator, architecture]
related: [[promptops-operator-index]]
---
# Architecture — promptops-operator
## Key Files (by size)

-rw-r--r-- 1 root root 4353 Apr 23 22:13 ./.gitignore
-rw-r--r-- 1 root root 3465 Apr 23 22:13 ./agents/working.py
-rw-r--r-- 1 root root 3111 Apr 23 22:13 ./skills/os_control/click_button.py
-rw-r--r-- 1 root root 3067 Apr 23 22:13 ./agents/auto_skill_updater.py
-rw-r--r-- 1 root root 2572 Apr 23 22:13 ./execution/executor.py
-rw-r--r-- 1 root root 2513 Apr 23 22:13 ./agents/skill_match_evaluator.py
-rw-r--r-- 1 root root 1620 Apr 23 22:13 ./registry/indexer.py
-rw-r--r-- 1 root root 1561 Apr 23 22:13 ./skills/generated/skill_open_discord.py
-rw-r--r-- 1 root root 1480 Apr 23 22:13 ./llm/gemi
## High Churn Files
      2 README.md
      1 web/frontend/.gitkeep
      1 web/backend/.gitkeep
      1 vision/screen_matcher.py
      1 vision/screen_capture.py
      1 vision/screen_analyzer.py
      1 vision/ocr.py
      1 vision/debug_utils.py
      1 tests/test_skills.py
      1 tests/test_registry.py
      1 tests/test_agents.py
      1 skills/web_automation/.gitkeep
      1 skills/os_control/type_text.py
      1 skills/os_control/submit.py
      1 skills/os_control/scroll_screen.py
      1 skills/os_control/scroll.py
      1 skills/os_control/press_windows_search.py
      1 skills/os_control/open_app.py
 
## Complexity
main.py
    F 6:0 main - A (1)
vision/ocr.py
    F 2:0 extract_text - A (1)
vision/screen_analyzer.py
    F 5:0 find_button_coordinates - A (3)
vision/screen_capture.py
    F 2:0 capture_screen - A (1)
llm/embedder.py
    F 9:0 get_embedding - A (1)
llm/gemini_client.py
    F 3:0 gemini_plan_tasks - A (1)
    F 9:0 gemini_generate_skill - A (1)
llm/openai_client.py
    F 2:0 openai_generate_skill - A (1)
config/clients.py
    F 20:0 get_mongo_collection - A (1)
dispatcher/trace_logger.py
    C 18:0 TraceLogger - A (2)
    F 7:0 log_event - A (1)
    M 19:4 TraceLogger.log_event - A (1)
    M 2
