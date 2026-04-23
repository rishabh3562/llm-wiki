---
repo: flask-crud
type: static_analysis
commit: 17ca177da841432d62e1838d76b69afd651d49bf
date: 2026-04-23
tags: [flask-crud, static_analysis]
related: [[flask-crud-index]]
---
{
  "largest_files": "-rw-r--r-- 1 root root 1036 Apr 23 14:14 ./app.py\n-rw-r--r-- 1 root root  506 Apr 23 14:14 ./templates/index.html\n-rw-r--r-- 1 root root  268 Apr 23 14:14 ./requirement.txt\n-rw-r--r-- 1 root root  263 Apr 23 14:14 ./templates/update.html\n-rw-r--r-- 1 root root  167 Apr 23 14:14 ./.gitignore\n",
  "high_churn_files": "      3 app.py\n      2 backend.py\n      2 .gitignore\n      2 \n      1 templates/update.html\n      1 templates/index.html\n      1 requirements.txt\n      1 requirement.txt\n",
  "complexity": "app.py\n    F 27:0 update - A (4)\n    F 20:0 delete - A (3)\n    F 8:0 index - A (1)\n    F 12:0 add - A (1)\n\n4 blocks (classes, functions, methods) analyzed.\nAverage complexity: A (2.25)\n",
  "dead_code": "app.py:7: unused function 'index' (60% confidence)\napp.py:11: unused function 'add' (60% confidence)\napp.py:19: unused function 'delete' (60% confidence)\napp.py:26: unused function 'update' (60% confidence)\n"
}