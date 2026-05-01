# Queue Status Issue Analysis

## Problem
The repo_queue shows 82 pending, 0 processing, 1 done, 0 failed, while ledger.json shows 9 repos with initial_analysis_done == true.

## Root Cause
The queue status is only updated in two places in run_llm_wiki.py:
1. After successful storage (lines 372-390) - only for repos that go through full processing
2. After storage failure (lines 396-410) - only for repos that go through full processing but fail storage

However, when a repo is skipped due to `initial_analysis_done == true` (line 171-173), the function returns early WITHOUT updating the queue status.

## Evidence
- Ledger shows 9 repos processed: `{'agents-ed', 'sentiment-analysis-chatbot-js', 'vector-shift-yc-assignment', 'topmate-site-webdev-consulation-', 'sentiment-analysis-chatbot-python', 'volt-bnb', 'rough', 'AniNotion'}`
- Queue shows only 1 repo as done (likely the most recently processed one that wasn't skipped)
- 8 repos that are in ledger as done remain pending in queue because they were skipped and queue status never updated

## Current Queue Population
Repos are initially added to queue with status "pending" via populate_queue.py (line 27):
```python
coll.update_one({"_id": name}, {"$setOnInsert": {"_id": name, "status": "pending", "addedAt": {"$date": {"$numberLong": "0"}}}}, upsert=True)
```

## Solution Needed
Update queue status for skipped repos as well, OR modify the system to not rely on queue for tracking skipped items.

Since the system uses two parallel tracking systems (ledger for skip logic, queue for monitoring), the queue should reflect the final status regardless of whether processing occurred.

## Recommended Fix
In the process_repo function, before the early return for skipped repos, update the queue status to "done" (since initial analysis is already done).

Alternatively, we could modify the queue population to check ledger status, but that would require changing populate_queue.py which may be used for initial setup.

The minimal change is to add queue status update in the skip path.