#!/usr/bin/env python3
"""
Daily change report for LLM Wiki system.
Reports what changed in the last 24 hours in MongoDB.
Prints report to stdout (to be picked up by cron job delivery).
"""
import os
from datetime import datetime, timezone, timedelta
from pymongo import MongoClient

# Load environment (same as primary script)
MONGODB_URI = os.environ.get("MONGODB_URI")
if not MONGODB_URI:
    wrapper_path = "/opt/llm_wiki/run_one_repo_wrapper.sh"
    if os.path.exists(wrapper_path):
        with open(wrapper_path) as f:
            for line in f:
                if line.startswith("export MONGODB_URI="):
                    MONGODB_URI = line.split('=', 1)[1].strip().strip('"')
                    break
if not MONGODB_URI:
    # Fallback to the known URI from config
    MONGODB_URI = "mongodb+srv://dubeyrishabh108_db_user:z1ss49FReN22EAIk@cluster0.j8iafjr.mongodb.net/github_wiki?retryWrites=true&w=majority"

def get_changes_since(since_dt):
    """Get changes since given datetime."""
    client = MongoClient(MONGODB_URI)
    db = client["github_wiki"]
    report_lines = []
    
    # 1. New analysis runs
    try:
        runs_coll = db["analysis_runs"]
        new_runs = list(runs_coll.find(
            {"completed_at": {"$gte": since_dt}},
            {"repo": 1, "completed_at": 1, "status": 1, "snippets_inserted": 1}
        ).sort("completed_at", -1))
        if new_runs:
            report_lines.append(f"🆕 New Analysis Runs ({len(new_runs)}):")
            for run in new_runs[:5]:
                repo = run.get("repo", "unknown")
                completed = run.get("completed_at")
                if isinstance(completed, datetime):
                    time_str = completed.strftime("%H:%M")
                else:
                    time_str = str(completed)
                status = run.get("status", "unknown")
                snippets = run.get("snippets_inserted", 0)
                report_lines.append(f"  • {repo} at {time_str} [{status}] (+{snippets} snippets)")
            if len(new_runs) > 5:
                report_lines.append(f"  • ... and {len(new_runs)-5} more")
            report_lines.append("")
    except Exception as e:
        report_lines.append(f"⚠️ Error checking analysis_runs: {e}")
    
    # 2. Updated repo_queue (status changes)
    try:
        queue_coll = db["repo_queue"]
        # Find docs with last_updated or finished_at or claimed_at within last 24h
        updated = list(queue_coll.find(
            {
                "$or": [
                    {"last_updated": {"$gte": since_dt}},
                    {"finished_at": {"$gte": since_dt}},
                    {"claimed_at": {"$gte": since_dt}},
                    {"status": {"$in": ["done", "failed", "processing"]}}  # rough
                ]
            },
            {"repo_name": 1, "status": 1, "last_updated": 1, "finished_at": 1}
        ).sort("last_updated", -1))
        if updated:
            report_lines.append(f"🔄 Queue Updates ({len(updated)}):")
            for doc in updated[:5]:
                repo = doc.get("repo_name", "unknown")
                status = doc.get("status", "unknown")
                updated_time = doc.get("last_updated")
                if isinstance(updated_time, datetime):
                    time_str = updated_time.strftime("%H:%M")
                else:
                    time_str = str(updated_time)
                report_lines.append(f"  • {repo}: {status} (updated {time_str})")
            if len(updated) > 5:
                report_lines.append(f"  • ... and {len(updated)-5} more")
            report_lines.append("")
    except Exception as e:
        report_lines.append(f"⚠️ Error checking repo_queue: {e}")
    
    # 3. New snippets
    try:
        snippets_coll = db["snippets"]
        new_snippets = list(snippets_coll.find(
            {"timestamp": {"$gte": since_dt}},
            {"repo_name": 1, "analysis_type": 1, "timestamp": 1}
        ).sort("timestamp", -1))
        if new_snippets:
            report_lines.append(f"📝 New Snippets ({len(new_snippets)}):")
            # Group by repo
            from collections import defaultdict
            by_repo = defaultdict(list)
            for snip in new_snippets:
                by_repo[snip.get("repo_name", "unknown")].append(snip)
            for repo, snips in list(by_repo.items())[:5]:
                report_lines.append(f"  • {repo}: {len(snips)} snippets")
                # Show analysis types
                types = set(s.get("analysis_type") for s in snips if s.get("analysis_type"))
                if types:
                    report_lines.append(f"    Types: {', '.join(sorted(types))}")
            if len(by_repo) > 5:
                report_lines.append(f"  • ... and {len(by_repo)-5} more repos")
            report_lines.append("")
    except Exception as e:
        report_lines.append(f"⚠️ Error checking snippets: {e}")
    
    # 4. Recently completed initial analyses (from repo_status)
    try:
        status_coll = db["repo_status"]
        recent_status = list(status_coll.find(
            {"initial_analysis_date": {"$gte": since_dt.strftime("%Y-%m-%d")}},
            {"repo": 1, "initial_analysis_date": 1, "snippets_inserted": 1, "initial_analysis_commit": 1}
        ).sort("initial_analysis_date", -1))
        if recent_status:
            report_lines.append(f"✅ Initial Analyses Completed ({len(recent_status)}):")
            for status in recent_status[:5]:
                repo = status.get("repo", "unknown")
                date = status.get("initial_analysis_date", "unknown")
                snippets = status.get("snippets_inserted", 0)
                commit = status.get("initial_analysis_commit", "unknown")[:8]
                report_lines.append(f"  • {repo} ({date}) @ {commit}... (+{snippets} snippets)")
            if len(recent_status) > 5:
                report_lines.append(f"  • ... and {len(recent_status)-5} more")
            report_lines.append("")
    except Exception as e:
        report_lines.append(f"⚠️ Error checking repo_status: {e}")
    
    # 5. Overall counts
    try:
        pending = db["repo_queue"].count_documents({"status": "pending"})
        processing = db["repo_queue"].count_documents({"status": "processing"})
        done = db["repo_queue"].count_documents({"status": "done"})
        failed = db["repo_queue"].count_documents({"status": "failed"})
        report_lines.append(f"📊 Current Queue:")
        report_lines.append(f"  Pending: {pending}, Processing: {processing}, Done: {done}, Failed: {failed}")
        total_snippets = db["snippets"].estimated_document_count()
        report_lines.append(f"  Total snippets: {total_snippets}")
        report_lines.append("")
    except Exception as e:
        report_lines.append(f"⚠️ Error getting counts: {e}")
    
    client.close()
    return report_lines

def main():
    since = datetime.now(timezone.utc) - timedelta(hours=24)
    report_lines = get_changes_since(since)
    
    if not report_lines:
        print("📭 No changes detected in the last 24 hours.")
        return
    
    header = f"📈 Daily Change Report (last 24 hours)\n🕒 Since: {since.strftime('%Y-%m-%d %H:%M UTC')}\n"
    print(header + "\n".join(report_lines))

if __name__ == "__main__":
    main()