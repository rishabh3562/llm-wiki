#!/usr/bin/env python3
"""
Generate daily change report for LLM Wiki system in exact requested format.
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
    print("ERROR: MONGODB_URI not set")
    exit(1)

def main():
    since = datetime.now(timezone.utc) - timedelta(hours=24)
    client = MongoClient(MONGODB_URI)
    db = client["github_wiki"]
    
    # Start building report
    report = f"📈 *Daily Change Report* (last 24 hours)\n🕒 Since: {since.strftime('%Y-%m-%d %H:%M UTC')}\n\n"
    
    # 1. New analysis runs
    try:
        runs_coll = db["analysis_runs"]
        new_runs = list(runs_coll.find(
            {"completed_at": {"$gte": since}},
            {"repo": 1, "completed_at": 1, "status": 1, "snippets_inserted": 1}
        ).sort("completed_at", -1))
        
        if new_runs:
            report += "*New Analysis Runs:*\n"
            for i, run in enumerate(new_runs[:5]):
                repo = run.get("repo", "unknown")
                completed = run.get("completed_at")
                if isinstance(completed, datetime):
                    time_str = completed.strftime("%Y-%m-%d %H:%M:%S")
                else:
                    time_str = str(completed)
                status = run.get("status", "unknown")
                snippets = run.get("snippets_inserted", 0)
                report += f"• {repo} - {status} ({snippets} snippets) at {time_str}\n"
            if len(new_runs) > 5:
                report += f"• ... and {len(new_runs) - 5} more\n"
            report += "\n"
        else:
            report += "*New Analysis Runs:* None\n\n"
    except Exception as e:
        report += f"*New Analysis Runs:* Error - {e}\n\n"
    
    # 2. Updates to repo_queue
    try:
        queue_coll = db["repo_queue"]
        # Find docs where last_updated, finished_at, or claimed_at is within last 24h
        # OR where status changed to done/failed/processing (we'll approximate by checking recent updates)
        updated = list(queue_coll.find(
            {
                "$or": [
                    {"last_updated": {"$gte": since}},
                    {"finished_at": {"$gte": since}},
                    {"claimed_at": {"$gte": since}}
                ]
            },
            {"repo_name": 1, "status": 1, "last_updated": 1, "finished_at": 1, "claimed_at": 1}
        ).sort("last_updated", -1))
        
        if updated:
            report += "*Repo Queue Updates:*\n"
            for i, doc in enumerate(updated[:5]):
                repo = doc.get("repo_name", "unknown")
                status = doc.get("status", "unknown")
                # Use last_updated if available, else finished_at, else claimed_at
                update_time = doc.get("last_updated") or doc.get("finished_at") or doc.get("claimed_at")
                if isinstance(update_time, datetime):
                    time_str = update_time.strftime("%Y-%m-%d %H:%M:%S")
                else:
                    time_str = str(update_time)
                report += f"• {repo} - {status} at {time_str}\n"
            if len(updated) > 5:
                report += f"• ... and {len(updated) - 5} more\n"
            report += "\n"
        else:
            report += "*Repo Queue Updates:* None\n\n"
    except Exception as e:
        report += f"*Repo Queue Updates:* Error - {e}\n\n"
    
    # 3. New snippets
    try:
        snippets_coll = db["snippets"]
        new_snippets = list(snippets_coll.find(
            {"timestamp": {"$gte": since}},
            {"repo_name": 1, "analysis_type": 1, "timestamp": 1}
        ).sort("timestamp", -1))
        
        if new_snippets:
            report += "*New Snippets:*\n"
            for i, snippet in enumerate(new_snippets[:5]):
                repo = snippet.get("repo_name", "unknown")
                analysis_type = snippet.get("analysis_type", "unknown")
                timestamp = snippet.get("timestamp")
                if isinstance(timestamp, datetime):
                    time_str = timestamp.strftime("%Y-%m-%d %H:%M:%S")
                else:
                    time_str = str(timestamp)
                report += f"• {repo} ({analysis_type}) at {time_str}\n"
            if len(new_snippets) > 5:
                report += f"• ... and {len(new_snippets) - 5} more\n"
            report += "\n"
        else:
            report += "*New Snippets:* None\n\n"
    except Exception as e:
        report += f"*New Snippets:* Error - {e}\n\n"
    
    # 4. Overall counts
    try:
        pending = db["repo_queue"].count_documents({"status": "pending"})
        processing = db["repo_queue"].count_documents({"status": "processing"})
        done = db["repo_queue"].count_documents({"status": "done"})
        failed = db["repo_queue"].count_documents({"status": "failed"})
        total_snippets = db["snippets"].count_documents({})
        
        report += "*Overall Counts:*\n"
        report += f"• Pending: {pending}\n"
        report += f"• Processing: {processing}\n"
        report += f"• Done: {done}\n"
        report += f"• Failed: {failed}\n"
        report += f"• Total Snippets: {total_snippets}\n"
    except Exception as e:
        report += f"*Overall Counts:* Error - {e}\n"
    
    client.close()
    print(report)

if __name__ == "__main__":
    main()
