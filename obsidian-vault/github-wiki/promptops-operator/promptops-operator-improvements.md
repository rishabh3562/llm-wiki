---
repo: promptops-operator
type: improvements
commit: 8ff468dfc663fff299e9f03481001203f2f4a6d5
date: 2026-04-23
tags: [promptops-operator, improvements]
related: [[promptops-operator-index]]
---
# Improvements — promptops-operator
## Dead Code
config/clients.py:20: unused function 'get_mongo_collection' (60% confidence)
registry/query.py:18: unused function 'query_mongo' (60% confidence)
skills/base.py:7: unused variable 'description' (60% confidence)
skills/base.py:8: unused variable 'parameters' (60% confidence)
skills/base.py:9: unused variable 'params_model' (60% confidence)
skills/base.py:12: unused variable 'kwargs' (100% confidence)
skills/generated/skill_close_brave_window.py:5: unused class 'Skill_close_brave_window' (60% confidence)
skills/generated/skill_close_brave_window.py:6: unused variable 'kwargs' (100% confidence)

## High Complexity Areas
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
