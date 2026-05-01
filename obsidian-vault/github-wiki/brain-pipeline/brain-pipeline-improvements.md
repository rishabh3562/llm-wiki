---
repo: brain-pipeline
type: improvements
commit: 7448b58ed4eeb0517bcceac7bbe5e297a212a0bf
date: 2026-04-30
tags: [brain-pipeline, improvements]
related: [[brain-pipeline-index]]
---

# Improvements — brain-pipeline

## Dead Code
app/agents/ingestion.py:2: unused import 'asyncio' (90% confidence)
app/agents/ingestion.py:6: unused import 'hashlib' (90% confidence)
app/agents/ingestion.py:25: unused variable 'since' (100% confidence)
app/agents/ingestion.py:64: unused variable 'last_commit' (60% confidence)
app/api/health.py:7: unused function 'health' (60% confidence)
app/api/pipeline.py:1: unused import 'HTTPException' (90% confidence)
app/api/pipeline.py:15: unused variable 'trigger' (60% confidence)
app/api/pipeline.py:38: unused function 'trigger_ingestion' (60% confidence)
app/api/pipeline.py:45: unused function 'r
## High Complexity Areas
app/orchestrator.py
    F 65:0 run_full_pipeline - A (2)
    F 71:0 run_query_pipeline - A (2)
    F 23:0 create_full_pipeline_graph - A (1)
    F 44:0 create_query_pipeline_graph - A (1)
    C 9:0 PipelineState - A (1)
app/main.py
    F 16:0 root - A (1)
app/core/llm_client.py
    F 9:0 generate_text - A (5)
    F 51:0 generate_embedding - A (4)
    F 77:0 chat - A (1)
app/core/extended_config.py
    F 95:0 format_prompt - A (2)
    F 91:0 get_prompt_template - A (1)
    C 5:0 ModelConfig - A (1)
app/core/config.py
    C 5:0 Settings - A (1)
app/api/health.py
    F 8:0 health - A (1)
app/api/
