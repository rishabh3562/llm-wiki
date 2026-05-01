---
repo: PictoPy
type: quality_complexity
commit: fb203872c9876b76095e4ee0753b49f477be48cb
date: 2026-05-01
tags: [PictoPy, quality_complexity]
related: [[PictoPy-index]]
---

# Quality — Complexity Signals

## Evidence
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
    M 18:4 LoggerWriter.__init__ - A (1)
sync-microservice/app/utils/watcher.py
    F 241:0 watcher_util_start_folder_watcher - B (8)
    F 52:0 watcher_util_handle_file_changes - B (7)
    F 91:0 watcher_util_find_closest_parent_folder - B (6)
    F 183:0 watcher_util_watcher_worker - A (5)
    F 126:0 watcher_util_call_sync_folder_api - A (4)
    F 156:0 watcher_util_call_delete_folders_api - A (4)
    F 215:0 watcher_util_get_existing_folders - A (4)
    F 300:0 watcher_util_stop_folder_watcher - A (4)
    F 343:0 watcher_util_get_watcher_info - A (4)
    F 357:0 watcher_util_wait_for_watcher - A (4)
    F 31:0 watcher_util_get_

## Related
- [[PictoPy-improvements]]
- [[PictoPy-architecture]]
