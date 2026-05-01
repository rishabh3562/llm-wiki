# System Health & Resilience Improvement Suggestions

## Overview
Review of LLM Wiki system cron configurations, error handling, and resilience to transient failures (network, API rate limits, temporary MongoDB issues).

## Current State Assessment

### Cron Job Configuration
- Primary job: `llm_wiki_toolbox` (ID: 33ab5a088dab) runs hourly at :00 UTC
- Command: `cd /opt/llm_wiki && python3 run_one_repo.py`
- Delivery: Telegram to chat_id 2049178019
- Additional jobs: self_improvement_weekly, llm_wiki_improver, llm_wiki_stuck_detector, llm_wiki_quality_monitor, llm_wiki_multi_agent_improver
- Queue status: 0 pending, 0 processing, 83 done, 0 failed (all repos processed)

### Error Handling Observations
**Strengths:**
- GitHub API discovery has exponential backoff retry logic (3 attempts, 1s/2s/4s delays)
- MongoDB connections use `serverSelectionTimeoutMS=5000`
- Fallback to local backup when MongoDB storage fails
- Queue status updates attempted on both success and failure paths

**Weaknesses:**
- MongoDB operations lack retry logic for transient failures
- Queue status updates lack retry logic
- Error handling exits immediately on MongoDB connection failures in some scripts
- Limited context in error messages for debugging

## Specific Improvement Recommendations

### 1. Add Retry Logic with Exponential Backoff for MongoDB Operations
**Files to modify:** `run_llm_wiki.py` (lines 302, 390, 414), `run_one_repo.py`, `quality_monitor.py`, `stuck_detector.py`, `self_improve.py`

**Implementation:**
```python
from pymongo import MongoClient
import time

def get_mongo_client_with_retries(uri, max_retries=3):
    for attempt in range(max_retries):
        try:
            client = MongoClient(
                uri, 
                tlsAllowInvalidCertificates=True,
                serverSelectionTimeoutMS=5000,
                connectTimeoutMS=5000,
                socketTimeoutMS=5000
            )
            # Test connection
            client.admin.command('ping')
            return client
        except Exception as e:
            if attempt == max_retries - 1:
                raise e
            wait_time = 2 ** attempt  # 1s, 2s, 4s
            print(f"MongoDB connection attempt {attempt + 1} failed: {e}. Retrying in {wait_time}s...")
            time.sleep(wait_time)
```

### 2. Add Retry Logic for Queue Status Updates
**Location:** In `run_llm_wiki.py` around lines 389-402 and 414-426

**Implementation:** Wrap queue update operations in retry function similar to MongoDB client.

### 3. Improve Error Context and Logging
**Examples:**
- Include repo name in MongoDB error messages
- Add timestamps to error logs
- Distinguish between different error types (network vs auth vs query)

### 4. Add Circuit Breaker Pattern (Optional)
For preventing cascading failures when MongoDB is consistently unavailable:
- Track consecutive failures
- Temporarily stop attempting operations after threshold
- Allow gradual recovery test

### 5. Make Operations More Idempotent
Ensure retry attempts don't cause duplicate work:
- Use upsert operations where appropriate
- Check existing state before performing actions
- Use unique constraints to prevent duplicates

### 6. Enhance GitHub API Resilience in `run_one_repo.py`
Currently only discovery has retry logic; consider adding similar retry logic for:
- Git clone/fetch operations (though less critical as they're local)
- Any direct GitHub API calls in processing phases

## Implementation Priority
1. **High Priority:** Add MongoDB retry logic (prevents most transient failures)
2. **Medium Priority:** Add queue status update retry logic (ensures queue accuracy)
3. **Medium Priority:** Improve error context (aids debugging)
4. **Low Priority:** Circuit breaker and idempotency enhancements

## Verification Approach
After implementing changes:
1. Test with simulated network interruptions
2. Test with temporary MongoDB unavailability
3. Verify that retry logic doesn't cause duplicate processing
4. Confirm fallback mechanisms still work correctly
5. Monitor logs for appropriate retry behavior

These changes will significantly improve system resilience to transient failures while maintaining the existing hourly processing constraint.