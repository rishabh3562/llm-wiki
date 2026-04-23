---
repo: Devr.AI
type: architecture
commit: 360c91de173dd5572afc5e56bf80605a10df08a0
date: 2026-04-23
tags: [Devr.AI, architecture]
related: [[Devr.AI-index]]
---
# Architecture — Devr.AI
## Key Files (by size)

-rw-r--r-- 1 root root 530308 Apr 23 00:32 ./poetry.lock
-rw-r--r-- 1 root root 187709 Apr 23 00:32 ./landing/package-lock.json
-rw-r--r-- 1 root root 184563 Apr 23 00:32 ./frontend/package-lock.json
-rw-r--r-- 1 root root 179170 Apr 23 00:32 ./landing/public/dashboard_preview.png
-rw-r--r-- 1 root root  81050 Apr 23 00:32 ./landing/public/aossie_logo.png
-rw-r--r-- 1 root root  46131 Apr 23 00:32 ./landing/src/components/sections/HowItWorks.tsx
-rw-r--r-- 1 root root  16556 Apr 23 00:32 ./backend/app/database/weaviate/operations.py
-rw-r--r-- 1 root root  15591 Apr 23 00:32 ./landing/src/comp
## High Churn Files
    269 
     19 backend/main.py
     17 poetry.lock
     16 pyproject.toml
     11 backend/app/agents/devrel/agent.py
      9 backend/requirements.txt
      9 backend/.env.example
      8 frontend/src/App.tsx
      8 frontend/package.json
      8 backend/app/core/orchestration/agent_coordinator.py
      8 backend/app/agents/devrel/github/github_toolkit.py
      7 landing/src/components/sections/HowItWorks.tsx
      7 landing/src/components/sections/Hero.tsx
      7 frontend/package-lock.json
      7 backend/app/scripts/weaviate/populate_db.py
      7 backend/app/db/supabase/auth.py
      7 ba
## Complexity
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
