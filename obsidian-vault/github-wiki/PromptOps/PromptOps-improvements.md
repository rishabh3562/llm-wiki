---
repo: PromptOps
type: improvements
commit: fe863aa3feaea4fe944787e48ad613ee0c282d7c
date: 2026-04-23
tags: [PromptOps, improvements]
related: [[PromptOps-index]]
---
# Improvements — PromptOps
## Dead Code
actions/browser.py:3: unused function 'open_url' (60% confidence)
actions/focus_window.py:3: unused function 'focus_window' (60% confidence)
actions/wait_for_ui.py:10: unused function 'wait_for_ui' (60% confidence)
agents/evaluator.py:2: unused import 'is_app_open' (90% confidence)
agents/evaluator.py:6: unused function 'extract_app_name' (60% confidence)
agents/vision.py:10: unused method 'locate' (60% confidence)
agents/vision.py:26: unused method 'analyze' (60% confidence)
interfaces/feedback.py:2: unused function 'show' (60% confidence)
utils/coords.py:3: unused function 'parse' (60% confi
## High Complexity Areas
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
