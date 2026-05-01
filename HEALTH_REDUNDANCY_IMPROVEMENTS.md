# System Health and Redundancy Improvements

## Current State Assessment
- **Primary Job**: `llm_wiki_toolbox` runs hourly at :00 UTC via Hermes cron
- **Processing**: One repo per run from MongoDB `github_wiki.repo_queue`
- **Existing Protections**: 
  - Retry utilities for MongoDB, GitHub API, and subprocess operations
  - Multiple maintenance cron jobs (stuck detector, quality monitor, etc.)
  - Wrapper scripts for environment management
  - Basic error handling in place

## Key Vulnerabilities Identified
1. **GitHub API Rate Limiting**: Partial 429 handling but could be improved
2. **Timeout Handling**: Limited configurability for subprocess/MongoDB timeouts
3. **Error Classification**: Could better distinguish transient vs permanent errors
4. **Logging**: Basic print statements instead of structured logging
5. **Cascading Failures**: No circuit breaker to prevent retry storms
6. **Health Monitoring**: Reactive rather than proactive checks

## Recommended Improvements

### Priority 1: High Impact, Low Effort
1. **Complete GitHub 429 Handling** (`run_llm_wiki.py`)
   - Add retry-after header parsing for 429 responses
   - Implement full exponential backoff with jitter for rate limits

2. **Enhanced Timeout Configuration** (`run_llm_wiki.py`, `run_one_repo.py`)
   - Add configurable timeouts for git operations (fetch, clone, reset)
   - Add MongoDB socketTimeoutMS and connectTimeoutMS parameters
   - Make timeouts environment-configurable

3. **Structured Logging** (All main scripts)
   - Replace print() with logging module
   - Add JSON-formatted log option for external consumption
   - Include correlation IDs for tracing repo processing

### Priority 2: Medium Impact
4. **Health Check Script** (`health_check.py`)
   - Verify MongoDB connectivity (<100ms latency)
   - Check GitHub API rate limit status
   - Validate disk space (>1GB free)
   - Detect stuck processing jobs (>2 hours in processing)
   - Run every 10 minutes via cron

5. **Circuit Breaker Pattern** (`circuit_breaker.py`)
   - Track failure counts per service (MongoDB, GitHub)
   - Open circuit after 5 consecutive failures
   - Half-open state after timeout to test recovery
   - Prevents overwhelming failing services

### Priority 3: Lower Impact but Valuable
6. **Checkpointing System** (`checkpoint_manager.py`)
   - Save progress after each analysis phase
   - Store in MongoDB with TTL (24 hours)
   - Allow restart from last completed phase
   - Particularly valuable for large repositories

7. **Enhanced Retry Utilities** (`retry_utils.py`)
   - Add jitter to prevent thundering herd
   - Customize retry exceptions per service type
   - Add retry budget to limit total retry time

## Implementation Notes
- All changes are backward compatible
- Can be implemented incrementally without downtime
- Prefer configuration over code changes where possible
- Maintain existing hourly processing guarantees
- Focus on non-disruptive enhancements first

## Verification Approach
1. Test with simulated network failures (disconnect, high latency)
2. Test with MongoDB connection drops and recoveries
3. Test GitHub API rate limit simulation (429 responses)
4. Verify no infinite retry loops or resource exhaustion
5. Confirm checkpointing works correctly without duplicates