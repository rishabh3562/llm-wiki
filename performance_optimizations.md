# Performance Optimization Suggestions for LLM Wiki Repo Processing

Based on analysis of the queue flow, processing patterns, and system constraints, here are 1-2 specific optimizations to improve the hourly cron job:

## Optimization 1: Add Queue Timing Metrics and Stuck Job Detection

**Problem**: The repo_queue collection doesn't populate `started_at` and `finished_at` timestamps, making it impossible to:
- Measure actual processing times per repo
- Detect stuck/jobs that are taking too long
- Identify performance bottlenecks or trends over time

**Solution**: Modify the queue update logic in `run_llm_wiki.py` to add proper timing metrics:

1. When a repo transitions from pending to processing, set `started_at`
2. When processing completes (success or failure), set `finished_at`
3. Add a periodic check to kill jobs that exceed a maximum runtime (e.g., 55 minutes to leave buffer before next hourly run)

**Implementation** (add to run_llm_wiki.py):
```python
# In process_repo function, after getting repo_info:
from datetime import datetime, timezone
start_time = datetime.now(timezone.utc)

# Update queue to mark as processing with start time
try:
    queue_client = MongoClient(MONGO_URI, tlsAllowInvalidCertificates=True, serverSelectionTimeoutMS=5000)
    queue_db = queue_client[MONGO_DB]
    queue_coll = queue_db["repo_queue"]
    queue_coll.update_one(
        {"_id": repo_name},
        {"$set": {
            "status": "processing",
            "started_at": start_time,
            "updated_at": start_time
        }},
        upsert=True
    )
    queue_client.close()
except Exception as e:
    print(f"   ⚠️  Failed to update queue start time: {e}")

# ... existing processing logic ...

# In both success and failure paths, add:
try:
    queue_client = MongoClient(MONGO_URI, tlsAllowInvalidCertificates=True, serverSelectionTimeoutMS=5000)
    queue_db = queue_client[MONGO_DB]
    queue_coll = queue_db["repo_queue"]
    update_data = {
        "status": "done" if success else "failed",
        "finished_at": datetime.now(timezone.utc),
        "updated_at": datetime.now(timezone.utc)
    }
    if not success:
        update_data["last_error"] = f"Processing failed after {snippets_added} snippets" if success else "Processing failed"
    queue_coll.update_one(
        {"_id": repo_name},
        {"$set": update_data},
        upsert=True
    )
    queue_client.close()
except Exception as e:
    print(f"   ⚠️  Failed to update queue completion time: {e}")

# Add stuck job detection at start of main():
def check_for_stuck_jobs():
    """Kill any jobs that have been processing too long"""
    try:
        client = MongoClient(MONGO_URI, tlsAllowInvalidCertificates=True, serverSelectionTimeoutMS=5000)
        db = client[MONGO_DB]
        coll = db["repo_queue"]
        # Find jobs processing for > 55 minutes
        cutoff = datetime.now(timezone.utc) - timedelta(minutes=55)
        stuck_jobs = coll.find({
            "status": "processing",
            "started_at": {"$lt": cutoff}
        })
        for job in stuck_jobs:
            print(f"   🚨 Killing stuck job: {job['_id']} (started {job['started_at']})")
            coll.update_one(
                {"_id": job["_id"]},
                {"$set": {
                    "status": "failed",
                    "finished_at": datetime.now(timezone.utc),
                    "last_error": "Job exceeded maximum runtime (55 minutes) and was killed",
                    "updated_at": datetime.now(timezone.utc)
                }}
            )
        client.close()
    except Exception as e:
        print(f"   ⚠️  Error checking for stuck jobs: {e}")

# Call check_for_stuck_jobs() early in main() before processing
```

**Benefits**:
- Enables performance monitoring and bottleneck identification
- Prevents stuck jobs from blocking queue progression
- Provides data for future optimization efforts
- Minimal disruption to existing flow

## Optimization 2: Implement Adaptive GitHub API Rate Limit Handling

**Problem**: Current GitHub API retry logic uses fixed exponential backoff, but doesn't leverage GitHub's rate limit headers for smarter retry timing.

**Solution**: Enhance the `retry_github_api` decorator or API call logic to:
1. Check `X-RateLimit-Remaining` and `X-RateLimit-Reset` headers
2. When rate limited (429), wait until reset time rather than using fixed backoff
3. Proactively slow down when remaining requests are low

**Implementation** (modify discover_github_repos in run_llm_wiki.py or enhance retry_utils.py):
```python
# Enhanced GitHub API call with rate limit awareness
def make_github_request(url, headers, max_retries=3):
    for attempt in range(max_retries):
        try:
            response = requests.get(url, headers=headers, timeout=30)
            
            # Check rate limit headers
            if 'X-RateLimit-Remaining' in response.headers:
                remaining = int(response.headers['X-RateLimit-Remaining'])
                reset_time = int(response.headers.get('X-RateLimit-Reset', 0))
                
                # If we're running low, proactively delay
                if remaining < 10 and reset_time > 0:
                    sleep_time = max(reset_time - time.time(), 0) + 1
                    if sleep_time > 0:
                        print(f"   ⏳ Proactive rate limit delay: {sleep_time:.0f}s (remaining: {remaining})")
                        time.sleep(sleep_time)
            
            if response.status_code == 200:
                return response
            elif response.status_code == 429:
                # Rate limited - use reset time if available
                reset_time = int(response.headers.get('X-RateLimit-Reset', 0))
                if reset_time > 0:
                    sleep_time = max(reset_time - time.time(), 1)  # At least 1 second
                    print(f"   🚦 Rate limited, waiting until reset: {sleep_time:.0f}s")
                    time.sleep(sleep_time)
                else:
                    # Fallback to exponential backoff
                    sleep_time = 2 ** attempt
                    print(f"   🚦 Rate limited, backing off: {sleep_time}s")
                    time.sleep(sleep_time)
            elif response.status_code in [500, 502, 503, 504]:
                # Server errors - use exponential backoff
                sleep_time = 2 ** attempt
                print(f"   🔄 Server error {response.status_code}, retrying in {sleep_time}s...")
                time.sleep(sleep_time)
            else:
                # Client errors (401, 403, 404, etc.) - don't retry
                response.raise_for_status()
                
        except requests.exceptions.RequestException as e:
            if attempt == max_retries - 1:
                raise
            sleep_time = 2 ** attempt
            print(f"   🌐 Network error: {e}, retrying in {sleep_time}s...")
            time.sleep(sleep_time)
    
    raise Exception(f"Failed after {max_retries} attempts")
```

**Benefits**:
- Reduces unnecessary rate limit errors and delays
- Makes better use of available GitHub API quota
- More intelligent handling of API constraints
- Maintains backward compatibility

Both optimizations are non-disruptive, maintain the hourly processing constraint, and provide immediate visibility into system performance while preventing common failure modes.