---
repo: College-data-transformation
type: architecture
commit: 505a7d4af04f0f1948de755fbbfaa7fa117da1ac
date: 2026-04-30
tags: [College-data-transformation, architecture]
related: [[College-data-transformation-index]]
---

# Architecture — College-data-transformation

## Key Files (by size)

-rw-r--r-- 1 root root 209569 Apr 30 20:00 ./uv.lock
-rw-r--r-- 1 root root  25714 Apr 30 20:00 ./docs/TRANSFORMATION_REPORT.md
-rw-r--r-- 1 root root  17946 Apr 30 20:00 ./scripts/07_normalize_addresses_structured.py
-rw-r--r-- 1 root root  14994 Apr 30 20:00 ./scripts/06_enhance_addresses_ai.py
-rw-r--r-- 1 root root  13895 Apr 30 20:00 ./docs/MONGODB_TRANSFORMATION.md
-rw-r--r-- 1 root root  12803 Apr 30 20:00 ./scripts/05_transform_to_mongodb.py
-rw-r--r-- 1 root root   9806 Apr 30 20:00 ./scripts/analyze_address_data.py
-rw-r--r-- 1 root root   7624 Apr 30 20:00 ./scripts/03_clean_pipelin
## High Churn Files
      8 
      4 scripts/07_normalize_addresses_structured.py
      3 uv.lock
      3 scripts/06_enhance_addresses_ai.py
      3 pyproject.toml
      3 .gitignore
      2 .env.example
      1 scripts/test_toon_comparison.py
      1 scripts/main.py
      1 scripts/example_usage.py
      1 scripts/analyze_address_data.py
      1 scripts/05_transform_to_mongodb.py
      1 scripts/04_create_master_dataset.py
      1 scripts/03_clean_pipeline.py
      1 scripts/02_profile_data.py
      1 scripts/01_inspect_files.py
      1 run_pipeline.py
      1 docs/TRANSFORMATION_REPORT.md
      1 docs/SCHEMA_DE
## Complexity
run_pipeline.py
    F 31:0 main - A (4)
    F 17:0 run_script - A (1)
scripts/05_transform_to_mongodb.py
    F 179:0 transform_to_mongodb - B (6)
    F 52:0 safe_get - A (3)
    F 59:0 safe_int - A (3)
    F 79:0 extract_pin_code - A (3)
    F 236:0 generate_summary - A (3)
    F 312:0 print_statistics - A (3)
    F 88:0 clean_state_name - A (2)
    F 159:0 validate_document - A (2)
    F 212:0 save_output - A (2)
    F 344:0 main - A (2)
    F 69:0 map_institution_type - A (1)
    F 74:0 map_level_to_degree - A (1)
    F 95:0 generate_mongodb_id - A (1)
    F 100:0 get_timestamp - A (1)
    F
