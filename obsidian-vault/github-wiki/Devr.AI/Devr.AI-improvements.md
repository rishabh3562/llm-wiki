---
repo: Devr.AI
type: improvements
commit: 360c91de173dd5572afc5e56bf80605a10df08a0
date: 2026-04-23
tags: [Devr.AI, improvements]
related: [[Devr.AI-index]]
---
# Improvements — Devr.AI
## Dead Code
backend/app/agents/base_agent.py:56: unused method 'stream_run' (60% confidence)
backend/app/agents/devrel/agent.py:102: unused method 'get_thread_state' (60% confidence)
backend/app/agents/devrel/github/services/github_mcp_client.py:9: unused class 'GitHubMCPClient' (60% confidence)
backend/app/agents/devrel/github/services/github_mcp_client.py:23: unused variable 'exc_tb' (100% confidence)
backend/app/agents/devrel/github/services/github_mcp_client.py:23: unused variable 'exc_type' (100% confidence)
backend/app/agents/devrel/github/services/github_mcp_client.py:23: unused variable 'exc_val' 
## High Complexity Areas
tests/test_embedding_service.py
    C 9:0 TestEmbeddingService - A (2)
    M 10:4 TestEmbeddingService.asyncSetUp - A (1)
    M 13:4 TestEmbeddingService.test_get_embedding - A (1)
    M 18:4 TestEmbeddingService.test_similarity - A (1)
    M 24:4 TestEmbeddingService.test_get_model_info - A (1)
    M 40:4 TestEmbeddingService.test_clear_cache - A (1)
tests/test_weaviate.py
    ERROR: unterminated string literal (detected at line 44) (<unknown>, line 44)
tests/tests_db.py
    F 13:0 test_create_table - A (2)
    F 17:0 test_add_item - A (2)
    F 32:0 test_update_item - A (2)
    F 52:0 test_d
