---
repo: SIH-Project
type: static_analysis
commit: 3201647e81d8057089da416d67960ca79347b80e
date: 2026-05-02
tags: [SIH-Project, static_analysis]
related: [[SIH-Project-index]]
---

{
  "largest_files": "-rw-r--r-- 1 root root 50344232 May  2 06:00 ./VID20230920131441.mp4\n-rw-r--r-- 1 root root 13868955 May  2 06:00 ./026c7465-309f6d33.mp4\n-rw-r--r-- 1 root root  6553793 May  2 06:00 ./vedio.mp4.mp4\n-rw-r--r-- 1 root root     3992 May  2 06:00 ./Frame3.py\n-rw-r--r-- 1 root root     2973 May  2 06:00 ./Frame1+v.py\n-rw-r--r-- 1 root root     2530 May  2 06:00 ./Frame2.py\n-rw-r--r-- 1 root root     2416 May  2 06:00 ./vehicledetecting.py.py\n-rw-r--r-- 1 root root     2375 May  2 06:00 ./Obj.py\n-rw-r--r-- 1 root root      773 May  2 06:00 ./Frame1.py\n-rw-r--r-- 1 root root      735 May  2 06:00 ./.vscode/settings.json\n-rw-r--r-- 1 root root      715 May  2 06:00 ./.vscode/launch.json\n-rw-r--r-- 1 root root      338 May  2 06:00 ./.vscode/c_cpp_properties.json\n-rw-r--r-- 1 root root       17 May  2 06:00 ./tempCodeRunnerFile.py\n-rw-r--r-- 1 root root       13 May  2 06:00 ./README.md\n",
  "high_churn_files": "      1 vehicledetecting.py.py\n      1 vedio.mp4.mp4\n      1 tempCodeRunnerFile.py\n      1 main (8).py\n      1 VID20230920131441.mp4\n      1 README.md\n      1 Obj.py\n      1 Frame3.py\n      1 Frame2.py\n      1 Frame1.py\n      1 Frame1+v.py\n      1 026c7465-309f6d33.mp4\n      1 .vscode/settings.json\n      1 .vscode/launch.json\n      1 .vscode/c_cpp_properties.json\n      1 \n",
  "complexity": "Frame3.py\n    F 32:0 center_handle - A (1)\nFrame2.py\n    F 27:0 center_handle - A (1)\nFrame1+v.py\n    F 32:0 center_handle - A (1)\nObj.py\n    F 16:0 center_handle - A (1)\nmain (8).py\n    F 18:0 pega_centro - A (1)\ntempCodeRunnerFile.py\n    ERROR: invalid decimal literal (<unknown>, line 1)\nvehicledetecting.py.py\n    F 17:0 center_handle - A (1)\n\n6 blocks (classes, functions, methods) analyzed.\nAverage complexity: A (1.0)\n",
  "dead_code": "Frame2.py:83: unreachable code after 'while' (100% confidence)\nFrame3.py:84: unused variable 'channels' (60% confidence)\nFrame3.py:89: unused variable 'class_ids' (60% confidence)\nFrame3.py:90: unused variable 'confidences' (60% confidence)\nFrame3.py:91: unused variable 'boxes' (60% confidence)\nObj.py:83: unreachable code after 'while' (100% confidence)\nvehicledetecting.py.py:84: unreachable code after 'while' (100% confidence)\n"
}