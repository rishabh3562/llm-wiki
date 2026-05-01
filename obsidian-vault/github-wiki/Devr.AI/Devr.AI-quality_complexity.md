---
repo: Devr.AI
type: quality_complexity
commit: 360c91de173dd5572afc5e56bf80605a10df08a0
date: 2026-05-01
tags: [Devr.AI, quality_complexity]
related: [[Devr.AI-index]]
---

# Quality — Complexity Signals

## Evidence
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
    F 52:0 test_delete_item - A (2)
    F 56:0 test_check_connection - A (2)
    F 28:0 test_get_item - A (1)
    F 43:0 test_search - A (1)
    F 48:0 test_list_collections - A (1)
    F 60:0 run_tests - A (1)
tests/test_supabase.py
    F 8:0 insert_user_into_supabase - A (4)
    F 115:0 insert_interaction - A (4)
    F 169:0 insert_code_chunk - A (4)
    F 223:0 insert_repository - A (4)
    F 56:0 get_user_by_id - A (3)
    F 127:0 read_interaction_by_id - A (3)
    F 180:0 read_code_chunk_by_id - A (3)
    F 234:0 read_repository_by_id - A (3)
    F 64:0 update_user - A (2)
    F 70:0 delete_user - A (2)


## Related
- [[Devr.AI-improvements]]
- [[Devr.AI-architecture]]
