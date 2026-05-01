#!/usr/bin/env python3
"""
Health check script for LLM Wiki system.
Verifies MongoDB connectivity, GitHub API accessibility, disk space, and queue health.
"""

import os
import sys
import time
from datetime import datetime, timezone, timedelta
from pymongo import MongoClient
import requests
import shutil
import subprocess

# Add project path
sys.path.append('/opt/llm_wiki')

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
def check_mongodb_connection():
    """Check MongoDB connectivity and basic operations."""
    try:
        # Load environment from wrapper
        wrapper_path = "/opt/llm_wiki/run_one_repo_wrapper.sh"
        env = load_env_from_wrapper(wrapper_path)
        MONGODB_URI = env.get("MONGODB_URI")
        
        # Fallback to environment if not in wrapper
        if not MONGODB_URI:
            MONGODB_URI = os.environ.get("MONGODB_URI")
        
        if not MONGODB_URI:
            return False, "MONGODB_URI not found in wrapper or environment"
        
        client = MongoClient(MONGODB_URI, serverSelectionTimeoutMS=5000)
        # Trigger a command to verify connection
        client.admin.command('ping')
        
        # Check database and collections
        db = client["github_wiki"]
        queue_count = db["repo_queue"].estimated_document_count()
        snippets_count = db["snippets"].estimated_document_count()
        
        client.close()
        
        return True, f"MongoDB connected. Queue: {queue_count}, Snippets: {snippets_count}"
    except Exception as e:
        return False, f"MongoDB connection failed: {str(e)}"

def check_github_api():
    """Check GitHub API accessibility and rate limit status."""
    try:
        # Try to load token from wrapper or file
        wrapper_path = "/opt/llm_wiki/run_one_repo_wrapper.sh"
        env = {}
        if os.path.exists(wrapper_path):
            with open(wrapper_path) as f:
                for line in f:
                    line = line.strip()
                    if line.startswith('export ') and '=' in line:
                        line = line[7:]
                        key, value = line.split('=', 1)
                        if len(value) >= 2 and (value.startswith('"') and value.endswith('"') or 
                                              value.startswith("'") and value.endswith("'")):
                            value = value[1:-1]
                        env[key] = value
        
        GITHUB_PAT = env.get("GITHUB_PAT") or os.environ.get("GITHUB_PAT")
        if not GITHUB_PAT:
            token_path = "/opt/llm_wiki/github_token.txt"
            if os.path.exists(token_path):
                with open(token_path) as f:
                    GITHUB_PAT = f.read().strip()
        
        if not GITHUB_PAT:
            return False, "GitHub token not found"
        
        # Debug: print token info
        print(f"Debug: Token length: {len(GITHUB_PAT)}", file=sys.stdout)
        print(f"Debug: Token starts with: {GITHUB_PAT[:10]}", file=sys.stdout)
        print(f"Debug: Token ends with: {GITHUB_PAT[-10:]}", file=sys.stdout)
        
        headers = {
            "Authorization": f"token {GITHUB_PAT}",
            "Accept": "application/vnd.github.v3+json"
        }
        
        # Check rate limit
        response = requests.get("https://api.github.com/rate_limit", 
                              headers=headers, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            remaining = data['resources']['core']['remaining']
            limit = data['resources']['core']['limit']
            reset_time = datetime.fromtimestamp(data['resources']['core']['reset'], tz=timezone.utc)
            
            return True, f"GitHub API accessible. Rate limit: {remaining}/{remaining} remaining (resets at {reset_time.strftime('%H:%M:%S UTC')})"
        else:
            return False, f"GitHub API returned status {response.status_code}"
            
    except Exception as e:
        return False, f"GitHub API check failed: {str(e)}"

def check_disk_space():
    """Check available disk space on critical partitions."""
    try:
        # Check /opt/llm_wiki directory
        llm_wiki_usage = shutil.disk_usage("/opt/llm_wiki")
        llm_wiki_free_gb = llm_wiki_usage.free / (1024**3)
        llm_wiki_total_gb = llm_wiki_usage.total / (1024**3)
        llm_wiki_used_percent = (llm_wiki_usage.used / llm_wiki_usage.total) * 100
        
        # Check /repos directory if it exists
        repos_free_gb = 0
        repos_total_gb = 0
        if os.path.exists("/repos"):
            repos_usage = shutil.disk_usage("/repos")
            repos_free_gb = repos_usage.free / (1024**3)
            repos_total_gb = repos_usage.total / (1024**3)
        
        # Check if we're running low on space (< 1GB free or < 10% free)
        warnings = []
        if llm_wiki_free_gb < 1.0 or llm_wiki_used_percent > 90:
            warnings.append(f"Low space on /opt/llm_wiki: {llm_wiki_free_gb:.1f}GB free ({100-llm_wiki_used_percent:.1f}%)")
        
        if repos_total_gb > 0 and (repos_free_gb < 1.0 or (repos_usage.used / repos_usage.total) > 90):
            warnings.append(f"Low space on /repos: {repos_free_gb:.1f}GB free")
        
        if warnings:
            return False, "; ".join(warnings)
        else:
            status = f"/opt/llm_wiki: {llm_wiki_free_gb:.1f}GB free"
            if repos_total_gb > 0:
                status += f", /repos: {repos_free_gb:.1f}GB free"
            return True, status
            
    except Exception as e:
        return False, f"Disk space check failed: {str(e)}"

def check_queue_health():
    """Check queue for stuck processing jobs."""
    try:
        wrapper_path = "/opt/llm_wiki/run_one_repo_wrapper.sh"
        env = {}
        if os.path.exists(wrapper_path):
            with open(wrapper_path) as f:
                for line in f:
                    line = line.strip()
                    if line.startswith('export ') and '=' in line:
                        line = line[7:]
                        key, value = line.split('=', 1)
                        if len(value) >= 2 and (value.startswith('"') and value.endswith('"') or 
                                              value.startswith("'") and value.endswith("'")):
                            value = value[1:-1]
                        env[key] = value
        
        MONGODB_URI = env.get("MONGODB_URI") or os.environ.get("MONGODB_URI")
        if not MONGODB_URI:
            return False, "MONGODB_URI not found"
        
        client = MongoClient(MONGODB_URI, serverSelectionTimeoutMS=5000)
        db = client["github_wiki"]
        coll = db["repo_queue"]
        
        # Find processing jobs that have been stuck for too long (> 2 hours)
        two_hours_ago = datetime.now(timezone.utc) - timedelta(hours=2)
        stuck_processing = list(coll.find({
            "status": "processing",
            "updated_at": {"$lt": two_hours_ago}
        }).limit(5))
        
        # Get basic queue stats
        pending = coll.count_documents({"status": "pending"})
        processing = coll.count_documents({"status": "processing"})
        done = coll.count_documents({"status": "done"})
        failed = coll.count_documents({"status": "failed"})
        
        client.close()
        
        if stuck_processing:
            stuck_repos = [doc.get('_id', 'unknown') for doc in stuck_processing]
            return False, f"Found {len(stuck_processing)} stuck processing jobs: {', '.join(stuck_repos[:3])}{'...' if len(stuck_processing) > 3 else ''}"
        else:
            return True, f"Queue healthy: {pending} pending, {processing} processing, {done} done, {failed} failed"
            
    except Exception as e:
        return False, f"Queue health check failed: {str(e)}"

def main():
    """Run all health checks and report results."""
    print("🏥 LLM Wiki System Health Check")
    print("=" * 50)
    
    checks = [
        ("MongoDB Connection", check_mongodb_connection),
        ("GitHub API", check_github_api),
        ("Disk Space", check_disk_space),
        ("Queue Health", check_queue_health),
    ]
    
    all_passed = True
    for name, check_func in checks:
        try:
            passed, message = check_func()
            status = "✅ PASS" if passed else "❌ FAIL"
            print(f"{status} {name}: {message}")
            if not passed:
                all_passed = False
        except Exception as e:
            print(f"❌ FAIL {name}: Check failed with exception: {e}")
            all_passed = False
    
    print("=" * 50)
    if all_passed:
        print("🎉 All health checks passed!")
        return 0
    else:
        print("⚠️  Some health checks failed!")
        return 1

if __name__ == "__main__":
    sys.exit(main())