---
repo: TaskFlux
type: static_analysis
commit: 9289726a5f5f9966702c5fb88f9e2420be7c6e64
date: 2026-05-02
tags: [TaskFlux, static_analysis]
related: [[TaskFlux-index]]
---

{
  "largest_files": "-rw-r--r-- 1 root root 55895 May  2 08:00 ./package-lock.json\n-rw-r--r-- 1 root root  3288 May  2 08:00 ./README.md\n-rw-r--r-- 1 root root   451 May  2 08:00 ./package.json\n-rw-r--r-- 1 root root   382 May  2 08:00 ./Dockerfile\n-rw-r--r-- 1 root root   373 May  2 08:00 ./docker-compose.yml\n-rw-r--r-- 1 root root   325 May  2 08:00 ./src/config/env.js\n-rw-r--r-- 1 root root   305 May  2 08:00 ./src/routes/queue.js\n-rw-r--r-- 1 root root   271 May  2 08:00 ./src/queue/redis.js\n-rw-r--r-- 1 root root   219 May  2 08:00 ./src/storage/index.js\n-rw-r--r-- 1 root root   211 May  2 08:00 ./src/queue/index.js\n-rw-r--r-- 1 root root   208 May  2 08:00 ./src/server.js\n-rw-r--r-- 1 root root   199 May  2 08:00 ./src/controllers/queue.js\n-rw-r--r-- 1 root root   197 May  2 08:00 ./src/workers/workers.js\n-rw-r--r-- 1 root root   196 May  2 08:00 ./src/database/nosql.js\n-rw-r--r-- 1 root root   195 May  2 08:00 ./src/database/index.js\n-rw-r--r-- 1 root root   182 May  2 08:00 ./src/queue/cloud.js\n-rw-r--r-- 1 root root   181 May  2 08:00 ./src/app.js\n-rw-r--r-- 1 root root   175 May  2 08:00 ./src/database/sql.js\n-rw-r--r-- 1 root root   170 May  2 08:00 ./src/storage/local.js\n-rw-r--r-- 1 root root   101 May  2 08:00 ./src/storage/cloud.js\n",
  "high_churn_files": "      4 \n      3 src/server.js\n      3 src/routes/queue.js\n      3 src/app.js\n      3 package.json\n      2 src/workers/workers.js\n      2 src/storage/local.js\n      2 src/storage/index.js\n      2 src/storage/cloud.js\n      2 src/queue/redis.js\n      2 src/queue/index.js\n      2 src/queue/cloud.js\n      2 src/database/sql.js\n      2 src/database/nosql.js\n      2 src/database/index.js\n      2 src/controllers/queue.js\n      2 package-lock.json\n      2 README.md\n      2 .env.example\n      1 src/workers/taskB.js\n",
  "complexity": "N/A (not a Python repo or radon not installed)",
  "dead_code": "N/A"
}