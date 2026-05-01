# Repo Processing Performance Analysis & Optimization Suggestions

## What I Did
Analyzed the repo processing system for the LLM Wiki analyzing GitHub repos for user rishabh3562:
- Examined the primary hourly cron job (`run_llm_wiki.py`)
- Reviewed queue flow in MongoDB `github_wiki.repo_queue`
- Checked average processing times and failure patterns
- Reviewed ledger tracking vs queue status consistency

## What I Found
### Queue Flow Issues
- **Queue status mismatch**: The repo_queue shows 6 pending, 0 processing, 77 done, 0 failed
- However, all repos in `ledger.json` have `initial_analysis_done == true`
- The pending items in queue are actually repos that were already processed (their status in queue was never updated after processing)
- Root cause: `run_llm_wiki.py` updates `ledger.json` but does NOT update corresponding documents in `repo_queue`

### Processing Performance
- **Average processing time**: 4.79 seconds (based on 77 completed jobs)
- **Range**: 1.94s - 35.43s
- **Failure rate**: 0% (0 failed jobs)
- Most repos are skipped quickly due to `initial_analysis_done == true` check in ledger

### System Design Observation
Two parallel tracking systems exist:
1. **Ledger-based** (`ledger.json`): Used by `run_llm_wiki.py` for skip logic
2. **Queue-based** (`repo_queue`): Used by monitoring scripts (`improve_after_run.py`, `run_one_repo.py`, etc.)

The queue system is not being updated by the primary processing script, causing monitoring inaccuracies.

## Specific Optimization Suggestions

### Optimization 1: Sync Queue Status After Processing (High Impact, Low Risk)
**Problem**: Queue monitoring shows incorrect pending counts because processed repos remain marked as "pending" in `repo_queue`.

**Solution**: Modify `run_llm_wiki.py` to update the repo_queue document status after each repo processing attempt.

**Where to add**: In `process_repo()` function, after the finalize phase (around line 368), add code to update the queue status.

**Implementation** (add near end of `process_repo()` function):
```python
    # Update queue status after processing (NEW)
    try:
        queue_client = MongoClient(MONGO_URI, tlsAllowInvalidCertificates=True, serverSelectionTimeoutMS=5000)
        queue_db = queue_client[MONGO_DB]
        queue_coll = queue_db["repo_queue"]
        
        if storage_success:
            queue_coll.update_one(
                {"_id": repo_name},
                {"$set": {
                    "status": "done",
                    "finished_at": datetime.now(timezone.utc),
                    "last_error": None
                }},
                upsert=True
            )
        else:
            queue_coll.update_one(
                {"_id": repo_name},
                {"$set": {
                    "status": "failed",
                    "finished_at": datetime.now(timezone.utc),
                    "last_error": f"Processing failed after {snippets_added} snippets"
                }},
                upsert=True
            )
        queue_client.close()
    except Exception as e:
        print(f"   ⚠️  Failed to update queue status: {e}")
        # Don't fail the whole process for queue update issues
```

**Benefits**:
- Queue monitoring tools will show accurate pending/processing/done/failed counts
- No impact on actual processing logic or timing
- Prevents false alarms about stuck repos
- Minimal, focused change

### Optimization 2: Add Exponential Backoff for GitHub API Rate Limits (Preventive)
**Problem**: While not currently failing, GitHub API requests (in `discover_github_repos()`) lack retry logic for rate limiting or transient network issues.

**Solution**: Add retry logic with exponential backoff to GitHub API calls.

**Where to add**: In `discover_github_repos()` function around the `requests.get()` call.

**Implementation** (replace the requests.get block):
```python
    max_retries = 3
    for attempt in range(max_retries):
        try:
            response = requests.get(url, headers=headers, timeout=30)
            # If we get a successful response, break out of retry loop
            if response.status_code == 200:
                break
            # If we get rate limited (403) or server error (5xx), retry
            elif response.status_code in [403, 500, 502, 503, 504]:
                if attempt < max_retries - 1:  # Don't sleep on last attempt
                    wait_time = 2 ** attempt  # Exponential backoff: 1s, 2s, 4s
                    print(f"   GitHub API returned {response.status_code}, retrying in {wait_time}s...")
                    time.sleep(wait_time)
                else:
                    raise Exception(f"GitHub API failed after {max_retries} attempts: {response.status_code}")
            else:
                # For other errors (401, 404, etc.), don't retry
                raise Exception(f"GitHub API error: {response.status_code}")
        except requests.exceptions.RequestException as e:
            if attempt < max_retries - 1:
                wait_time = 2 ** attempt
                print(f"   Network error: {e}, retrying in {wait_time}s...")
                time.sleep(wait_time)
            else:
                raise Exception(f"GitHub API network failure after {max_retries} attempts: {e}")
```

**Benefits**:
- Increases resilience to transient GitHub API issues
- Prevents unnecessary failures due to rate limiting
- Minimal performance impact (only activates when needed)
- Uses industry-standard exponential backoff

## Why These Optimizations?
1. **Non-disruptive**: Both changes are additive and don't alter the core processing flow
2. **Addresses root cause**: Fixes the queue status synchronization issue that affects monitoring accuracy
3. **Preventive**: Adds resilience without changing successful operation paths
4. **User-focused**: Provides more accurate feedback through monitoring tools
5. **Safe to implement**: Changes are localized and include proper error handling

## Expected Outcome
After implementing Optimization 1:
- `improve_after_run.py` will show accurate queue status (pending count should drop to 0)
- Monitoring will correctly reflect system state
- No change to actual processing speed or success rate

After implementing Optimization 2:
- Reduced risk of processing failures due to transient GitHub issues
- More robust operation during periods of high GitHub API usage