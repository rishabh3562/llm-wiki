---
# AGENTS — System Overview

## Goal
Analyze all 160+ GitHub repos. Build permanent knowledge base in MongoDB + Obsidian.

## Phase 1 (ACTIVE NOW)
Full initial analysis of every repo. One repo per cron run.
Skip guard: repo_status.initial_analysis_done == true → skip.

## Phase 2 (NOT ACTIVE — future)
Diff tracking on new commits only.
Do NOT activate until explicitly told.

## Queue Strategy
- Fetch all repos from GitHub API
- Filter out repos where initial_analysis_done == true in MongoDB
- Pick first remaining repo (alphabetical)
- Analyze fully → mark done → stop
- Next cron run picks next repo