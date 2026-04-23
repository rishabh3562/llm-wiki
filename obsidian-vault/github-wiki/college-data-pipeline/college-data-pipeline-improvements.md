---
repo: college-data-pipeline
type: improvements
commit: 7a8c489b961cb3a5447034c3046b6e8e0c64cc7f
date: 2026-04-23
tags: [college-data-pipeline, improvements]
related: [[college-data-pipeline-index]]
---
# Improvements — college-data-pipeline
## Dead Code
config/settings.py:5: unused variable 'MONGO_URI' (60% confidence)
config/settings.py:6: unused variable 'REDIS_URL' (60% confidence)
config/settings.py:7: unused variable 'BATCH_SIZE' (60% confidence)

## High Complexity Areas
worker.py
    ERROR: invalid non-printable character U+FEFF (<unknown>, line 1)
run_pipeline.py
    ERROR: invalid non-printable character U+FEFF (<unknown>, line 1)
enqueue_batches.py
    ERROR: invalid non-printable character U+FEFF (<unknown>, line 1)
main.py
    F 1:0 main - A (1)
queue/job_queue.py
    ERROR: invalid non-printable character U+FEFF (<unknown>, line 1)
queue/worker_pool.py
    ERROR: invalid non-printable character U+FEFF (<unknown>, line 1)
queue/retry.py
    ERROR: invalid non-printable character U+FEFF (<unknown>, line 1)
tests/test_enricher.py
    ERROR: invalid non-pri
