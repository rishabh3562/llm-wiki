---
repo: fika-ai-engineering-insights-bot
type: architecture
commit: 0f539b9e629fd354d09b4ef9d37a285cc5877148
date: 2026-04-23
tags: [fika-ai-engineering-insights-bot, architecture]
related: [[fika-ai-engineering-insights-bot-index]]
---
# Architecture — fika-ai-engineering-insights-bot
## Key Files (by size)

-rw-r--r-- 1 root root 5717 Apr 23 12:25 ./README.md
-rw-r--r-- 1 root root 5341 Apr 23 12:25 ./bot/slack_bot.py
-rw-r--r-- 1 root root 4688 Apr 23 12:25 ./.gitignore
-rw-r--r-- 1 root root 3785 Apr 23 12:25 ./viz/metrics_plotter.py
-rw-r--r-- 1 root root 3666 Apr 23 12:25 ./demo.py
-rw-r--r-- 1 root root 3555 Apr 23 12:25 ./agents/data_harvester.py
-rw-r--r-- 1 root root 3140 Apr 23 12:25 ./agents/insight_narrator.py
-rw-r--r-- 1 root root 2950 Apr 23 12:25 ./requirements.txt
-rw-r--r-- 1 root root 2513 Apr 23 12:25 ./utils/github_helper.py
-rw-r--r-- 1 root root 1582 Apr 23 12:25 ./utils/bot
## High Churn Files
     17 
      7 README.md
      4 main.py
      4 bot/slack_bot.py
      3 utils/bot_utils.py
      3 utils/__init__.py
      3 docker-compose.yaml
      3 agents/data_harvester.py
      2 workflow/productivity_insight_flow.py
      2 workflow/__init__.py
      2 viz/__init__.py
      2 schemas/workflow_state.py
      2 requirements.txt
      2 configs/github.py
      2 configs/constants.py
      2 agents/insight_narrator.py
      2 agents/diff_analyst.py
      2 Dockerfile
      1 viz/metrics_plotter.py
      1 utils/time_utils.py

## Complexity
demo.py
    F 8:0 run_demo_report - A (1)
    F 56:0 format_report_text - A (1)
    F 86:0 handle_demo_dev_report - A (1)
viz/metrics_plotter.py
    F 6:0 plot_influence_graph - B (6)
    F 55:0 plot_individual_graphs - B (6)
    F 27:0 plot_stats - A (3)
utils/logger.py
    M 17:4 SlackLogger.log - A (4)
    C 4:0 SlackLogger - A (3)
    M 11:4 SlackLogger.terminal_log - A (2)
    M 5:4 SlackLogger.__init__ - A (1)
    M 8:4 SlackLogger.set_slack_logger - A (1)
utils/github_helper.py
    F 5:0 get_commits - A (3)
    F 38:0 get_ci_failures_for_pr - A (3)
    F 43:0 get_review_latency_for_pr -
