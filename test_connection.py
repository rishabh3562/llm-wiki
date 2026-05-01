#!/usr/bin/env python3
import os
import sys
from pymongo import MongoClient

# Load environment from wrapper script
wrapper_path = "/opt/llm_wiki/run_one_repo_wrapper.sh"
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

MONGODB_URI = env.get("MONGODB_URI")
GITHUB_PAT = env.get("GITHUB_PAT")

if not MONGODB_URI:
    print("MONGODB_URI not set")
    sys.exit(1)
if not GITHUB_PAT:
    print("GITHUB_PAT not set")
    sys.exit(1)

print(f"MONGODB_URI: {MONGODB_URI}")
print(f"GITHUB_PAT set: {bool(GITHUB_PAT)}")

try:
    client = MongoClient(MONGODB_URI)
    client.admin.command('ismaster')
    print("MongoDB connection successful")
except Exception as e:
    print(f"MongoDB connection failed: {e}")
    sys.exit(1)

db = client["github_wiki"]
print(f"repo_status count: {db.repo_status.count_documents({})}")
print(f"analysis_runs count: {db.analysis_runs.count_documents({})}")
print(f"repo_queue count: {db.repo_queue.count_documents({})}")
print(f"snippets count: {db.snippets.count_documents({})}")