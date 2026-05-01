# Optimization Plan for LLM Wiki Repo Processing

## Current State Analysis
- **Queue Status**: 83 total documents (82 pending, 0 processing, 1 done, 0 failed)
- **Timing Data**: No valid timestamp pairs found for done jobs - cannot calculate average processing times
- **Failure Patterns**: 0 failed jobs currently, but no proper error tracking mechanism
- **Processing Flow**: One repo per hourly cron run, alphabetical order of repos needing initial analysis

## Identified Issues
1. Missing `started_at` and `finished_at` timestamps in queue documents prevents performance analysis
2. No stuck job detection mechanism - a repo could remain in "processing" state indefinitely
3. Limited failure analysis capabilities due to incomplete error tracking

## Recommended Optimizations

### Optimization 1: Add Queue Timing Metrics
**Problem**: Cannot measure actual processing times or detect performance trends
**Solution**: Add proper timestamp tracking to queue operations

**Implementation**:
- When transitioning from pending to processing: set `started_at` timestamp
- When completing processing (success/failure): set `finished_at` timestamp
- Enable calculation of: average processing time, min/max times, trends over time

### Optimization 2: Implement Stuck Job Detection and Timeout
**Problem**: Jobs could remain stuck in "processing" state, blocking queue progression
**Solution**: Add automatic detection and termination of long-running jobs

**Implementation**:
- At start of each run, check for jobs with status "processing" that exceed maximum runtime (55 minutes)
- Automatically mark stuck jobs as failed with appropriate error message
- Ensures hourly cron job can always make progress and prevents queue blocking

Both optimizations are non-disruptive, maintain the hourly processing constraint, and provide immediate visibility into system performance while preventing common failure modes.