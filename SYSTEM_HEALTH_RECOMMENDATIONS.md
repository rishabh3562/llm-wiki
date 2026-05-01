# System Health & Redundancy Recommendations for LLM Wiki

## Current State Assessment
✅ **Strengths**:
- Retry utilities with exponential backoff for MongoDB, GitHub API, subprocess
- Multiple health monitoring cron jobs (stuck detector, quality monitor, self-improvement)
- Error logging and Telegram notifications
- MongoDB-based queue persistence with status tracking
- Health check script (`health_check.py`) available

⚠️ **Areas for Improvement**:
1. **Cron Overlap Protection**: No mechanism to prevent overlapping executions
2. **Primary Job Monitoring**: No dedicated health check for the main `llm_wiki_toolbox` job
3. **Timeout Handling**: Main processing script lacks explicit timeouts
4. **Rate Limit Awareness**: Reactive retries but no proactive rate limit monitoring
5. **Health Check Frequency**: Existing checks could be more frequent for critical issues

## Recommended Improvements (Non-disruptive)

### 1. Add Cron Overlap Protection (High Priority)
Modify `/opt/llm_wiki/run_one_repo_wrapper.sh` to prevent concurrent executions:

```bash
#!/bin/bash
# Add lock file to prevent overlapping runs
LOCK_FILE="/opt/llm_wiki/.llm_wiki_lock"

if [ -f "$LOCK_FILE" ]; then
    # Check if lock is stale (older than 2 hours)
    if [ $(find "$LOCK_FILE" -mmin +120 2>/dev/null) ]; then
        echo "⚠️  Removing stale lock file"
        rm -f "$LOCK_FILE"
    else
        echo "❌ Another instance is still running. Exiting to prevent overlap."
        exit 1
    fi
fi

touch "$LOCK_FILE"

# Cleanup lock on exit
trap 'rm -f "$LOCK_FILE"' EXIT

export MONGODB_URI="mongodb+srv://dubeyrishabh108_db_user:***@cluster0.j8iafjr.mongodb.net/github_wiki?retryWrites=true&w=majority"
export GITHUB_PAT=$(cat /root/.hermes/secrets/github_token.txt)
cd /opt/llm_wiki && python3 run_one_repo.py
```

### 2. Add Lightweight Health Check Cron Job (Medium Priority)
Create a frequent health check that runs every 15 minutes:

**Hermes Cron Job Configuration**:
```json
{
  "id": "llm_wiki_health_check",
  "name": "llm_wiki_health_check",
  "prompt": "cd /opt/llm_wiki && python3 health_check.py --quick",
  "schedule": {
    "kind": "cron",
    "expr": "*/15 * * * *",
    "display": "*/15 * * * *"
  },
  "enabled": true,
  "deliver": "origin"
}
```

**Enhance `health_check.py`** to support a quick mode:
```python
# Add argument parsing
import argparse
parser = argparse.ArgumentParser()
parser.add_argument('--quick', action='store_true', help='Run quick checks only')
args = parser.parse_args()

# In main(), if args.quick, only run critical checks:
if args.quick:
    checks = [
        ("MongoDB Connection", check_mongodb_connection),
        ("GitHub API", check_github_api),
        ("Queue Health", check_queue_health),
    ]
else:
    # Run all checks including disk space
    checks = [
        ("MongoDB Connection", check_mongodb_connection),
        ("GitHub API", check_github_api),
        ("Disk Space", check_disk_space),
        ("Queue Health", check_queue_health),
    ]
```

### 3. Add Timeout Protection to Main Script (Medium Priority)
Enhance `/opt/llm_wiki/run_llm_wiki.py` with timeout handling:

```python
# Add to imports
import signal
from contextlib import contextmanager

class TimeoutException(Exception): pass

def timeout_handler(signum, frame):
    raise TimeoutException("Operation timed out")

@contextmanager
def time_limit(seconds):
    signal.signal(signal.SIGALRM, timeout_handler)
    signal.alarm(seconds)
    try:
        yield
    finally:
        signal.alarm(0)

# Usage example for GitHub operations:
try:
    with time_limit(300):  # 5 minute timeout
        # GitHub clone/API operations here
        pass
except TimeoutException:
    print("⏳ Operation timed out after 5 minutes")
    # Handle timeout appropriately
```

### 4. Add Proactive Rate Limit Monitoring (Medium Priority)
Before GitHub API operations in `run_llm_wiki.py`:

```python
# Add utility function
def check_github_rate_limit(token):
    headers = {"Authorization": f"token {token}", "Accept": "application/vnd.github.v3+json"}
    try:
        response = requests.get("https://api.github.com/rate_limit", headers=headers, timeout=10)
        if response.status_code == 200:
            data = response.json()
            remaining = data['resources']['core']['remaining']
            if remaining < 100:  # Throttle if low on requests
                reset_time = data['resources']['core']['reset']
                sleep_time = max(reset_time - time.time(), 0) + 10
                print(f"⏳ Rate limit low ({remaining} remaining). Sleeping for {sleep_time:.0f}s")
                time.sleep(sleep_time)
    except Exception as e:
        print(f"⚠️  Could not check rate limit: {e}")

# Call before GitHub operations
check_github_rate_limit(get_github_token())
```

### 5. Enhance Error Notification System (Low Priority)
Modify health check to send immediate alerts for critical failures:

```python
# Add to health_check.py main()
if not all_passed and any(name in ["MongoDB Connection", "GitHub API"] for name, _ in failed_checks):
    # Send immediate alert for critical failures
    alert_msg = f"🚨 *LLM Wiki Critical Alert*\n"
    alert_msg += f"Failed: {', '.join([name for name, _ in failed_checks])}\n"
    alert_msg += f"Time: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')}"
    # Use existing notification mechanism (Telegram via Hermes or direct)
```

## Implementation Priority
1. **High**: Cron overlap protection (prevents serious issues)
2. **Medium**: Frequent health check + timeout handling (improves responsiveness)
3. **Medium**: Rate limit awareness (reduces API errors)
4. **Low**: Enhanced notifications (improves visibility)

## Expected Benefits
- Prevents overlapping cron jobs that could cause resource conflicts
- Faster detection of system issues through frequent health checks
- Protection against hanging processes via timeouts
- Reduced GitHub API rate limit errors through proactive monitoring
- Maintains all existing functionality while adding resilience layers

These changes are designed to be non-disruptive and can be implemented incrementally.