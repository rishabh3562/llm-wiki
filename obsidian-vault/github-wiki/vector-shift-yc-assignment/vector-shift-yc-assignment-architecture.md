---
repo: vector-shift-yc-assignment
type: architecture
commit: 128d912292816b2ed393ba3ec6df01d95489acf3
date: 2026-05-02
tags: [vector-shift-yc-assignment, architecture]
related: [[vector-shift-yc-assignment-index]]
---

# Architecture — vector-shift-yc-assignment

## Key Files (by size)

-rw-r--r-- 1 root root 699509 May  2 11:00 ./frontend/package-lock.json
-rw-r--r-- 1 root root  19898 May  2 11:00 ./frontend/src/styles/global.css
-rw-r--r-- 1 root root  14004 May  2 11:00 ./frontend/src/styles/nodes.css
-rw-r--r-- 1 root root   9664 May  2 11:00 ./frontend/public/logo512.png
-rw-r--r-- 1 root root   9057 May  2 11:00 ./README.md
-rw-r--r-- 1 root root   5699 May  2 11:00 ./frontend/src/components/ui/N8NToolbar.js
-rw-r--r-- 1 root root   5347 May  2 11:00 ./frontend/public/logo192.png
-rw-r--r-- 1 root root   3870 May  2 11:00 ./frontend/public/favicon.ico
-rw-r--r-- 1 root
## High Churn Files
     28 
     10 frontend/src/styles/global.css
      6 frontend/src/components/ui/PipelineToolbar.js
      5 frontend/src/components/ui/DraggableNode.js
      4 frontend/src/styles/nodes.css
      4 frontend/src/constants/ui.js
      4 frontend/src/components/workspace/PipelineCanvas.js
      4 frontend/src/components/ui/N8NToolbar.js
      4 frontend/src/components/nodes/BaseNode.js
      4 .gitignore
      3 frontend/src/nodes/BaseNode.js
      3 frontend/src/App.jsx
      3 frontend/package.json
      3 README.md
      2 frontend/src/utils/uiToolkit.js
      2 frontend/src/utils/toolbar.js
## Complexity
backend/main.py
    F 83:0 parse_pipeline - B (8)
    F 22:0 is_dag - B (6)
    F 78:0 read_root - A (1)
backend/tests/test_main.py
    F 13:0 test_valid_dag - A (5)
    F 57:0 test_empty_pipeline - A (5)
    F 97:0 test_complex_dag - A (5)
    F 8:0 test_read_root - A (3)
    F 37:0 test_invalid_dag_cycle - A (3)
    F 74:0 test_invalid_json - A (3)
    F 83:0 test_invalid_edge_reference - A (3)

10 blocks (classes, functions, methods) analyzed.
Average complexity: A (4.2)

