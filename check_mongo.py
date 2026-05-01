#!/usr/bin/env python3
import os
import sys
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
                        if (value.startswith('"') and value.endswith('"')) or \
                           (value.startswith("'") and value.endswith("'")):
                            value = value[1:-1]
                    env[key] = value
    return env

# Load environment (same as primary script)
wrapper_path = "/opt/llm_wiki/run_one_repo_wrapper.sh"
env = load_env_from_wrapper(wrapper_path)
MONGODB_URI = env.get("MONGODB_URI")
GITHUB_PAT = env.get("GITHUB_PAT")

# Fallback to environment if not in wrapper
if not MONGODB_URI:
    MONGODB_URI = os.environ.get("MONGODB_URI")
if not GITHUB_PAT:
    GITHUB_PAT = os.environ.get("GITHUB_PAT")

# Fallback for GITHUB_PAT from token file
if not GITHUB_PAT:
    token_path = "/opt/llm_wiki/github_token.txt"
    if os.path.exists(token_path):
        with open(token_path) as f:
            GITHUB_PAT = f.read().strip()

if not MONGODB_URI:
    raise ValueError("MONGODB_URI not set")
if not GITHUB_PAT:
    raise ValueError("GITHUB_PAT not set")

print(f"MONGODB_URI: {MONGODB_URI}")
print(f"GITHUB_PAT set: {bool(GITHUB_PAT)}")

client = MongoClient(MONGODB_URI)
db = client["github_wiki"]

print("\n=== REPOS COLLECTION ===")
repos_coll = db["repos"]
total_repos = repos_coll.count_documents({})
print(f"Total repos: {total_repos}")
done_repos = repos_coll.count_documents({"initial_analysis_done": True})
print(f"Repos with initial_analysis_done == True: {done_repos}")
undone_repos = repos_coll.count_documents({"initial_analysis_done": False})
print(f"Repos with initial_analysis_done == False: {undone_repos}")
missing_field = repos_coll.count_documents({"initial_analysis_done": {"$exists": False}})
print(f"Repos missing initial_analysis_done field: {missing_field}")

if undone_repos > 0 or missing_field > 0:
    print("First 5 repos that need initial analysis:")
    query = {"$or": [{"initial_analysis_done": False}, {"initial_analysis_done": {"$exists": False}}]}
    for doc in repos_coll.find(query, {"name": 1, "initial_analysis_done": 1}).limit(5):
        print(f'  - {doc.get("name")}: initial_analysis_done={doc.get("initial_analysis_done")}')
else:
    print("All repos have initial_analysis_done == True")

print("\n=== REPO_QUEUE COLLECTION ===")
queue_coll = db["repo_queue"]
total_queue = queue_coll.count_documents({})
print(f"Total entries in repo_queue: {total_queue}")
pending = queue_coll.count_documents({"status": "pending"})
processing = queue_coll.count_documents({"status": "processing"})
done = queue_coll.count_documents({"status": "done"})
failed = queue_coll.count_documents({"status": "failed"})
print(f"Queue status - Pending: {pending}, Processing: {processing}, Done: {done}, Failed: {failed}")

if pending == 0 and (undone_repos > 0 or missing_field > 0):
    print("Queue is empty but there are repos needing initial analysis.")
    print("Consider running populate_queue.py to refill the queue based on repos collection.")

client.close()
