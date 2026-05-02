---
repo: promptops-operator
type: quality_complexity
commit: 8ff468dfc663fff299e9f03481001203f2f4a6d5
date: 2026-05-02
tags: [promptops-operator, quality_complexity]
related: [[promptops-operator-index]]
---

# Quality — Complexity Signals

## Evidence
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
    M 22:4 TraceLogger.__call__ - A (1)
execution/executor.py
    F 7:0 execute_skills - A (5)
agents/working.py
    F 9:0 handle_user_prompt - A (5)
agents/skill_match_evaluator.py
    F 45:0 call_llm - A (2)
    F 19:0 _call_gemini - A (1)
    F 30:0 _call_openai - A (1)


## Related
- [[promptops-operator-improvements]]
- [[promptops-operator-architecture]]
