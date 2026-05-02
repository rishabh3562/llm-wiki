---
repo: SIH
type: static_analysis
commit: 90fce1cad570923a2c840f5b88b13b256fc85e51
date: 2026-05-02
tags: [SIH, static_analysis]
related: [[SIH-index]]
---

{
  "largest_files": "-rw-r--r-- 1 root root 22461518 May  2 05:46 ./737b07de-8296-4495-8e62-e136d576176f.mp4\n-rw-r--r-- 1 root root 13868955 May  2 05:46 ./026c7465-309f6d33.mp4\n-rw-r--r-- 1 root root     4109 May  2 05:46 ./Frame3.py\n-rw-r--r-- 1 root root     2709 May  2 05:46 ./vehicledetecting.py.py\n-rw-r--r-- 1 root root     2613 May  2 05:46 ./Frame2.py\n-rw-r--r-- 1 root root      571 May  2 05:46 ./Frame1.py\n",
  "high_churn_files": "      1 vehicledetecting.py.py\n      1 vehicle detection/tempCodeRunnerFile.py\n      1 vehicle detection/main (8).py\n      1 vehicle detection/Obj.py\n      1 vehicle detection/Frame3.py\n      1 vehicle detection/Frame2.py\n      1 vehicle detection/Frame1.py\n      1 vehicle detection/Frame1+v.py\n      1 vehicle detection/026c7465-309f6d33.mp4\n      1 main (8).py\n      1 Frame3.py\n      1 Frame2.py\n      1 Frame1.py\n      1 737b07de-8296-4495-8e62-e136d576176f.mp4\n      1 026c7465-309f6d33.mp4\n      1 \n",
  "complexity": "Frame3.py\n    F 32:0 center_handle - A (1)\nFrame2.py\n    F 27:0 center_handle - A (1)\nmain (8).py\n    F 18:0 pega_centro - A (1)\nvehicledetecting.py.py\n    F 17:0 center_handle - A (1)\nvehicle detection/Frame3.py\n    F 32:0 center_handle - A (1)\nvehicle detection/Frame2.py\n    F 27:0 center_handle - A (1)\nvehicle detection/Frame1+v.py\n    F 32:0 center_handle - A (1)\nvehicle detection/Obj.py\n    F 16:0 center_handle - A (1)\nvehicle detection/main (8).py\n    F 18:0 pega_centro - A (1)\nvehicle detection/tempCodeRunnerFile.py\n    ERROR: invalid decimal literal (<unknown>, line 1)\n\n9 blocks (classes, functions, methods) analyzed.\nAverage complexity: A (1.0)\n",
  "dead_code": "Frame2.py:83: unreachable code after 'while' (100% confidence)\nFrame3.py:84: unused variable 'channels' (60% confidence)\nFrame3.py:89: unused variable 'class_ids' (60% confidence)\nFrame3.py:90: unused variable 'confidences' (60% confidence)\nFrame3.py:91: unused variable 'boxes' (60% confidence)\nvehicle detection/Frame2.py:83: unreachable code after 'while' (100% confidence)\nvehicle detection/Frame3.py:84: unused variable 'channels' (60% confidence)\nvehicle detection/Frame3.py:89: unused variable 'class_ids' (60% confidence)\nvehicle detection/Frame3.py:90: unused variable 'confidences' (60% confidence)\nvehicle detection/Frame3.py:91: unused variable 'boxes' (60% confidence)\nvehicle detection/Obj.py:83: unreachable code after 'while' (100% confidence)\nvehicledetecting.py.py:84: unreachable code after 'while' (100% confidence)\n"
}