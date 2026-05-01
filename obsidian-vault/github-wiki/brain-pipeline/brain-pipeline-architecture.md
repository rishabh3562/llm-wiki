---
repo: brain-pipeline
type: architecture
commit: 7448b58ed4eeb0517bcceac7bbe5e297a212a0bf
date: 2026-04-30
tags: [brain-pipeline, architecture]
related: [[brain-pipeline-index]]
---

# Architecture — brain-pipeline

## Key Files (by size)

-rw-r--r-- 1 root root 6885 Apr 30 07:36 ./app/agents/ingestion.py
-rw-r--r-- 1 root root 4852 Apr 30 07:36 ./app/db/obsidian.py
-rw-r--r-- 1 root root 4104 Apr 30 07:36 ./app/agents/structuring.py
-rw-r--r-- 1 root root 3488 Apr 30 07:36 ./app/core/extended_config.py
-rw-r--r-- 1 root root 3271 Apr 30 07:36 ./app/core/llm_client.py
-rw-r--r-- 1 root root 3214 Apr 30 07:36 ./app/db/knowledge_graph.py
-rw-r--r-- 1 root root 3211 Apr 30 07:36 ./README.md
-rw-r--r-- 1 root root 2482 Apr 30 07:36 ./app/agents/optimization.py
-rw-r--r-- 1 root root 2280 Apr 30 07:36 ./app/orchestrator.py
-rw-r--r--
## High Churn Files
      4 
      2 .gitignore
      1 requirements.txt
      1 architecture.mmd
      1 app/orchestrator.py
      1 app/main.py
      1 app/db/vector_db.py
      1 app/db/obsidian.py
      1 app/db/mongodb.py
      1 app/db/knowledge_graph.py
      1 app/core/llm_client.py
      1 app/core/extended_config.py
      1 app/core/config.py
      1 app/api/pipeline.py
      1 app/api/health.py
      1 app/agents/structuring.py
      1 app/agents/query.py
      1 app/agents/optimization.py
      1 app/agents/ingestion.py
      1 README.md

## Complexity
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
