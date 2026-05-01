#!/usr/bin/env python3
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
    raise ValueError("MONGODB_URI not set")

def find_stuck_repos(threshold_hours=2):
    """Find repos stuck in processing state longer than threshold."""
    try:
        client = MongoClient(MONGODB_URI)
        db = client["github_wiki"]
        coll = db["repo_queue"]
        
        threshold_time = datetime.now(timezone.utc) - timedelta(hours=threshold_hours)
        
        # Find docs with status processing and claimed_at older than threshold
        stuck = list(coll.find(
            {
                "status": "processing",
                "claimed_at": {"$exists": True, "$lt": threshold_time}
            },
            {"repo_name": 1, "claimed_at": 1, "_id": 0}
        ).sort("claimed_at", 1))  # Oldest first
        
        client.close()
        return stuck
    except Exception as e:
        return [{"error": str(e)}]

def main():
    stuck = find_stuck_repos(threshold_hours=2)
    
    if not stuck:
        # No stuck repos - output silent marker
        print("[SILENT]")
        return
    
    if len(stuck) == 1 and "error" in stuck[0]:
        msg = f"💥 Stuck repo check failed: {stuck[0]['error']}"
        print(msg)
        return
    
    if stuck:
        msg = f"🚨 *Stuck Repository Alert*\n\n"
        msg += f"Found {len(stuck)} repo(s) stuck in processing for >2 hours:\n\n"
        for i, repo in enumerate(stuck[:5], 1):  # Limit to 5
            name = repo.get('repo_name', 'unknown')
            claimed = repo.get('claimed_at', 'unknown')
            msg += f"{i}. `{name}`\n   Claimed: {claimed}\n"
        if len(stuck) > 5:
            msg += f"\n...and {len(stuck) - 5} more\n"
        msg += "\nConsider checking logs or manually intervening."
        print(msg)
        return

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"💥 Stuck detector cron failed: {e}")