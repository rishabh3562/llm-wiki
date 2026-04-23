---
repo: PictoPy
type: architecture
commit: fb203872c9876b76095e4ee0753b49f477be48cb
date: 2026-04-23
tags: [PictoPy, architecture]
related: [[PictoPy-index]]
---
# Architecture — PictoPy
## Key Files (by size)

-rw-r--r-- 1 root root 91199342 Apr 23 06:12 ./backend/app/models/ONNX_Exports/FaceNet_128D.onnx
-rw-r--r-- 1 root root 80604626 Apr 23 06:12 ./backend/app/models/ONNX_Exports/YOLOv11_Medium.onnx
-rw-r--r-- 1 root root 80359785 Apr 23 06:12 ./backend/app/models/ONNX_Exports/YOLOv11_Medium_Face.onnx
-rw-r--r-- 1 root root 37988605 Apr 23 06:12 ./backend/app/models/ONNX_Exports/YOLOv11_Small.onnx
-rw-r--r-- 1 root root 37865100 Apr 23 06:12 ./backend/app/models/ONNX_Exports/YOLOv11_Small_Face.onnx
-rw-r--r-- 1 root root 10678327 Apr 23 06:12 ./backend/app/models/ONNX_Exports/YOLOv11_Nano.onnx
-r
## High Churn Files
    964 
     77 backend/app/routes/images.py
     53 backend/main.py
     50 frontend/src/components/Navigation/Navbar/Navbar.tsx
     48 frontend/src-tauri/tauri.conf.json
     42 frontend/src/components/Media/MediaView.tsx
     39 frontend/src/components/Navigation/Sidebar/Sidebar.tsx
     39 frontend/package-lock.json
     38 frontend/package.json
     36 backend/app/database/images.py
     35 frontend/src/pages/SettingsPage/Settings.tsx
     35 README.md
     34 frontend/src/components/AITagging/AIgallery.tsx
     34 backend/app/routes/albums.py
     28 frontend/src/components/Album/Album
## Complexity
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
