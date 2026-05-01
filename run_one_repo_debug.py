#!/usr/bin/env python3
import os
import sys
from datetime import datetime, timezone, timedelta
from pymongo import MongoClient

def load_env_from_wrapper(wrapper_path):
    """Load environment variables from a wrapper script that uses export KEY=VALUE"""
    env = {}
    if os.path.exists(wrapper_path):
        with open(wrapper_path) as f:
            for line in f:
                line = line.strip()
                if line.startswith('export ') and '=' in line:
                    line = line[7:]  # remove 'export '
                    key, value = line.split('=', 1)
                    # Remove surrounding quotes if present
                    if len(value) >= 2:
                        if (value.startswith('"') and value.endswith('"')) or (value.startswith("'") and value.endswith("'")):
                            value = value[1:-1]
                    env[key] = value
    return env

# Load environment (same as primary script)
wrapper_path = "/opt/llm_wiki/run_one_repo_wrapper.sh"
env = load_env_from_wrapper(wrapper_path)
MONGODB_URI = env.get("MONGODB_URI")
GITHUB_PAT = env.get("GITHUB_PAT")

print(f"Loaded from wrapper - MONGODB_URI: {MONGODB_URI}")
print(f"Loaded from wrapper - GITHUB_PAT: {'SET' if GITHUB_PAT else 'NOT SET'}")

# Fallback to environment if not in wrapper
if not MONGODB_URI:
    MONGODB_URI = os.environ.get("MONGODB_URI")
if not GITHUB_PAT:
    GITHUB_PAT = os.environ.get("GITHUB_PAT")

print(f"After env fallback - MONGODB_URI: {MONGODB_URI}")
print(f"After env fallback - GITHUB_PAT: {'SET' if GITHUB_PAT else 'NOT SET'}")

# Fallback for GITHUB_PAT from token file
if not GITHUB_PAT:
    token_path = "/opt/llm_wiki/github_token.txt"
    if os.path.exists(token_path):
        with open(token_path) as f:
            GITHUB_PAT = f.read().strip()
        print(f"Loaded from token file - GITHUB_PAT: {'SET' if GITHUB_PAT else 'NOT SET'}")

if not MONGODB_URI:
    raise ValueError("MONGODB_URI not set")
if not GITHUB_PAT:
    raise ValueError("GITHUB_PAT not set")

print(f"Final - MONGODB_URI: {MONGODB_URI}")
print(f"Final - GITHUB_PAT: {'SET' if GITHUB_PAT else 'NOT SET'}")

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
            {"_id": 1, "last_error": 1, "last_updated": 1}
        ).sort("last_updated", -1).limit(limit)
        errors = list(cursor)
        client.close()
        return errors
    except Exception as e:
        return [{"error": str(e)}]

def main():
    # Build suggestion message
    suggestions = []
    
    # We cannot check the primary cron job without hermes_tools, so skip for now
    # But we can note that we are running as a cron job and the system will deliver output
    
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