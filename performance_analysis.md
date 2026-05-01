# Repo Processing Performance Analysis

## What I Did
Examined the repo processing system performance by:
- Reviewing queue flow in MongoDB github_wiki.repo_queue
- Analyzing processing scripts (run_llm_wiki.py, run_one_repo.py)
- Checking current queue status and ledger synchronization
- Reviewing existing performance analysis documents
- Examining retry logic and timeout configurations

## What I Found

### Queue Flow Analysis
- **Current queue state**: 82 pending, 0 processing, 1 done, 0 failed (83 total)
- **Ledger state**: 9 repos marked as initial_analysis_done
- **Status mismatch**: Only 1 repo shows as "done" in queue vs 9 in ledger
- **Missing timestamps**: The done repo lacks claimed_at/finished_at fields, preventing processing time calculations

### Key Issues Identified
1. **Incomplete status tracking**: Queue documents only contain _id, status, and addedAt
   - No claimed_at timestamp when processing begins
   - No finished_at timestamp when processing ends
   - This prevents:
     - Calculating actual processing times
     - Detecting stuck jobs (repos claimed too long)
     - Accurate queue monitoring

2. **No automatic retry for failed jobs**:
   - Failed repos remain in "failed" status indefinitely
   - No mechanism to reset to pending for retry
   - Requires manual intervention to reprocess

3. **Sequential processing bottleneck**:
   - One repo processed per hourly cron run
   - No parallelization even for independent repos
   - Limited by GitHub API rate limits and resource constraints

### Performance Metrics Unavailable
Due to missing timestamps, cannot determine:
- Average processing time per repo
- Min/max processing times
- Success/failure rates over time
- Stuck job detection

## Suggested Optimizations

### Optimization 1: Add Proper Timestamp Tracking (High Impact, Low Risk)
**Problem**: Missing timing data prevents performance monitoring and stuck job detection.

**Solution**: Modify run_llm_wiki.py to set:
- `claimed_at`: When repo processing begins (at start of process_repo)
- `finished_at`: When processing completes (both success and failure paths)

**Implementation**:
```python
# At beginning of process_repo():
queue_coll.update_one(
    {"_id": repo_name},
    {"$set": {"status": "processing", "claimed_at": datetime.now(timezone.utc)}},
    upsert=True
)

# In success path (around line 380):
{"$set": {
    "status": "done",
    "finished_at": datetime.now(timezone.utc),
    "last_error": None
}}

# In failure path (around line 404):
{"$set": {
    "status": "failed",
    "finished_at": datetime.now(timezone.utc),
    "last_error": f"Storage failed after {snippets_added} snippets"
}}
```

**Benefits**:
- Enables accurate processing time calculations
- Allows stuck job detection (>1 hour claimed)
- Improves queue monitoring accuracy
- Non-disruptive change (adds fields, doesn't remove existing logic)

### Optimization 2: Implement Basic Failed Job Retry (Medium Impact, Low Risk)
**Problem**: Failed jobs require manual intervention to retry.

**Solution**: Add retry count and automatic reset to pending after investigation period.

**Implementation**:
1. Add `retry_count` field (default 0) to queue documents
2. In failure path, increment retry_count
3. If retry_count < MAX_RETRIES (e.g., 3), reset to pending after cooldown period
4. If retry_count >= MAX_RETRIES, keep as failed for manual review

**Implementation snippet**:
```python
# In failure path:
update_doc = {
    "$set": {
        "status": "failed",
        "finished_at": datetime.now(timezone.utc),
        "last_error": f"Storage failed after {snippets_added} snippets"
    },
    "$inc": {"retry_count": 1}
}
# Check if we should reset to pending for retry
if update_doc["$inc"]["retry_count"] < 3:
    # Reset to pending after 1 hour cooldown
    update_doc["$set"]["status"] = "pending"
    update_doc["$set"]["last_error"] = None  # Clear error on retry
```

**Benefits**:
- Reduces manual intervention for transient failures
- Maintains system autonomy
- Safe limits prevent infinite retry loops
- Preserves failed jobs for manual review after max retries

## Why These Optimizations?
- **Non-disruptive**: Both changes add functionality without removing existing logic
- **Performance-focused**: Directly address the inability to measure and improve processing times
- **Low risk**: Use established patterns from existing codebase (timestamps, retry logic)
- **Aligned with constraints**: Preserve hourly processing model while improving observability and resilience

## Expected Impact
- Ability to measure and optimize actual processing times
- Reduced stuck jobs through better detection
- Decreased manual overhead for failure handling
- Foundation for future data-driven optimizations