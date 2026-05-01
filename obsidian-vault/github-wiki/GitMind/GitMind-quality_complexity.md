---
repo: GitMind
type: quality_complexity
commit: 3ab3eee3e0dbe675e240b8e0fecb2c9dce875423
date: 2026-05-01
tags: [GitMind, quality_complexity]
related: [[GitMind-index]]
---

# Quality — Complexity Signals

## Evidence
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
    M 11:4 SlackLogger.terminal_log - A (2)
    M 5:4 SlackLogger.__init__ - A (1)
    M 8:4 SlackLogger.set_slack_logger - A (1)
utils/v1/github_helper.py
    F 5:0 get_commits - A (3)
    F 38:0 get_ci_failures_for_pr - A (3)
    F 43:0 get_review_latency_for_pr - A (3)
    F 54:0 get_cycle_time_for_pr - A (2)
    F 17:0 get_incident_issues - A (1)
    F 23:0 get_commit_by_sha - A (1)
    F 28:0 get_pr_files - A (1)
    F 33:0 get_pr_for_commit - A (1)


## Related
- [[GitMind-improvements]]
- [[GitMind-architecture]]
