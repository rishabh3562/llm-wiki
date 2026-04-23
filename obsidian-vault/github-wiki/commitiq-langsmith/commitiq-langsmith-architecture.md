---
repo: commitiq-langsmith
type: architecture
commit: fd81eb6dbfa8c2af998b373c5a5f911235374753
date: 2026-04-23
tags: [commitiq-langsmith, architecture]
related: [[commitiq-langsmith-index]]
---
# Architecture — commitiq-langsmith
## Key Files (by size)

-rw-r--r-- 1 root root 8239 Apr 23 12:22 ./bot/slack_bot_v2.py
-rw-r--r-- 1 root root 6614 Apr 23 12:22 ./agents/v2/aggregator.py
-rw-r--r-- 1 root root 5432 Apr 23 12:22 ./bot/slack_bot_v1.py
-rw-r--r-- 1 root root 5221 Apr 23 12:22 ./CODE_OF_CONDUCT.md
-rw-r--r-- 1 root root 4706 Apr 23 12:22 ./.gitignore
-rw-r--r-- 1 root root 4388 Apr 23 12:22 ./README.md
-rw-r--r-- 1 root root 4381 Apr 23 12:22 ./viz/v1/metrics_plotter.py
-rw-r--r-- 1 root root 4317 Apr 23 12:22 ./agents/v2/narrator.py
-rw-r--r-- 1 root root 4120 Apr 23 12:22 ./utils/v2/github_helper.py
-rw-r--r-- 1 root root 3785 Apr 23 
## High Churn Files
     28 
      9 README.md
      7 main.py
      5 utils/__init__.py
      5 bot/slack_bot.py
      4 configs/constants.py
      4 agents/data_harvester.py
      3 workflow/productivity_insight_flow.py
      3 workflow/__init__.py
      3 viz/__init__.py
      3 utils/bot_utils.py
      3 requirements.txt
      3 docker-compose.yaml
      3 configs/github.py
      3 bot/slack_bot_v2.py
      3 Dockerfile
      3 .env.sample
      2 workflow/parallel_flow_demo.py
      2 workflow/chunked_parallel_flow.py
      2 viz/v1/metrics_plotter.py

## Complexity
manual_runner.py
    F 8:0 run_manual_test - A (1)
demo.py
    F 8:0 run_demo_report - A (1)
    F 56:0 format_report_text - A (1)
    F 86:0 handle_demo_dev_report - A (1)
viz/v1/metrics_plotter.py
    F 6:0 plot_influence_graph - B (6)
    F 55:0 plot_individual_graphs - B (6)
    F 27:0 plot_stats - A (3)
    F 118:0 plot_commit_trends - A (2)
viz/v2/metrics_plotter.py
    F 6:0 plot_influence_graph - B (6)
    F 55:0 plot_individual_graphs - B (6)
    F 27:0 plot_stats - A (3)
utils/v1/logger.py
    M 17:4 SlackLogger.log - A (4)
    C 4:0 SlackLogger - A (3)
    M 11:4 SlackLogger.termina
