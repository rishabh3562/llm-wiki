---
repo: PictoPy
type: improvements
commit: fb203872c9876b76095e4ee0753b49f477be48cb
date: 2026-04-23
tags: [PictoPy, improvements]
related: [[PictoPy-index]]
---
# Improvements — PictoPy
## Dead Code
app.py:5: unused function 'initialize_app' (60% confidence)
app.py:13: unused function 'refresh_data' (60% confidence)
backend/app/config/settings.py:21: unused variable 'TEST_INPUT_PATH' (60% confidence)
backend/app/config/settings.py:22: unused variable 'TEST_OUTPUT_PATH' (60% confidence)
backend/app/config/settings.py:25: unused variable 'IMAGES_PATH' (60% confidence)
backend/app/database/face_clusters.py:18: unused variable 'ClusterMap' (60% confidence)
backend/app/database/face_clusters.py:115: unused function 'db_get_all_clusters' (60% confidence)
backend/app/database/faces.py:15: unused
## High Complexity Areas
app.py
    F 5:0 initialize_app - A (1)
    F 13:0 refresh_data - A (1)
utils/cache.py
    F 21:0 get_cached_data - A (4)
    F 44:0 invalidate_cache - A (3)
    F 9:0 cache_data - A (1)
    F 58:0 cached - A (1)
sync-microservice/app/core/lifespan.py
    F 19:0 lifespan - A (5)
sync-microservice/app/utils/watcher_helpers.py
    F 5:0 format_debug_changes - B (8)
sync-microservice/app/utils/logger_writer.py
    C 15:0 LoggerWriter - A (4)
    M 31:4 LoggerWriter.write - A (4)
    M 55:4 LoggerWriter.flush - A (3)
    F 71:0 redirect_stdout_stderr - A (1)
    M 18:4 LoggerWriter.__init__ - A (1
