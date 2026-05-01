#!/usr/bin/env python3
import os
import sys
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

GITHUB_PAT = os.environ.get("GITHUB_PAT")
if not GITHUB_PAT:
    token_path = "/root/.hermes/secrets/github_token.txt"
    if os.path.exists(token_path):
        with open(token_path) as f:
            GITHUB_PAT = f.read().strip()
if not GITHUB_PAT:
    raise ValueError("GITHUB_PAT not set")

def get_queue_stats():
    """Get pending/processing/done counts from repo_queue."""
    try:
        client = MongoClient(MONGODB_URI)
        db = client["github_wiki"]
        coll = db["repo_queue"]
        pending = coll.count_documents({"status": "pending"})
        processing = coll.count_documents({"status": "processing"})
        done = coll.count_documents({"status": "done"})
        failed = coll.count_documents({"status": "failed"})
        client.close()
        return {"pending": pending, "processing": processing, "done": done, "failed": failed}
    except Exception as e:
        return {"error": str(e)}

def get_recent_errors(limit=5):
    """Fetch recent error messages from repo_queue where status failed or last_error set."""
    try:
        client = MongoClient(MONGODB_URI)
        db = client["github_wiki"]
        coll = db["repo_queue"]
        # Find docs with last_error not null, sort by last_updated descending
        cursor = coll.find(
            {"last_error": {"$ne": None, "$exists": True}},
            {"repo_name": 1, "last_error": 1, "last_updated": 1, "_id": 0}
        ).sort("last_updated", -1).limit(limit)
        errors = list(cursor)
        client.close()
        return errors
    except Exception as e:
        return [{"error": str(e)}]

def fix_pending_reset_errors():
    """Fix pending repos that have git reset --hard FETCH_HEAD error by resetting their status."""
    try:
        client = MongoClient(MONGODB_URI)
        db = client["github_wiki"]
        coll = db["repo_queue"]
        # Find pending docs with the specific error
        query = {
            "status": "pending",
            "last_error": {"$regex": "git.*reset.*--hard.*FETCH_HEAD"}
        }
        update = {
            "$set": {"status": "pending"},
            "$unset": {"last_error": "", "claimed_at": "", "failed_at": ""}
        }
        result = coll.update_many(query, update)
        client.close()
        return result.modified_count
    except Exception as e:
        return f"Error fixing pending reset errors: {e}"

def main():
    # Build suggestion message
    suggestions = []
    
    # We cannot check the primary cron job without hermes_tools, so skip for now
    # But we can note that we are running as a cron job and the system will deliver output
    
    # Fix pending reset errors
    fixed_count = fix_pending_reset_errors()
    if isinstance(fixed_count, int) and fixed_count > 0:
        suggestions.append(f"• Fixed {fixed_count} pending repo(s) with reset error.")
    
    queue = get_queue_stats()
    if "error" not in queue:
        suggestions.append(f"• Queue: {queue['pending']} pending, {queue['processing']} processing, {queue['done']} done, {queue['failed']} failed.")
        if queue['processing'] > 0:
            suggestions.append("• A repo is currently being processed.")
        if queue['pending'] == 0:
            suggestions.append("• Queue is empty! Consider adding more repos or checking discovery.")
    else:
        suggestions.append(f"• Could not read queue: {queue['error']}")
    
    errors = get_recent_errors(limit=3)
    if errors and not (len(errors) == 1 and "error" in errors[0]):
        suggestions.append("• Recent errors:")
        for err in errors:
            repo = err.get('repo_name', 'unknown')
            err_msg = err.get('last_error', '')[:100]
            suggestions.append(f"  - {repo}: {err_msg}...")
    elif errors and "error" in errors[0]:
        suggestions.append(f"• Could not fetch recent errors: {errors[0]['error']}")
    
    # Compose final message
    header = "🔧 Improvement suggestion (post-run check):"
    body = "\n".join(suggestions)
    # Keep message concise
    full_msg = f"{header}\n{body}"
    # Print to stdout (cron system will deliver)
    print(full_msg)

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        # Print error message
        print(f"💥 Improvement cron failed: {e}")
        sys.exit(1)