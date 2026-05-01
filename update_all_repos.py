#!/usr/bin/env python3
import json
import os
import sys
from pathlib import Path
import requests
from datetime import datetime, timezone
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

GITHUB_TOKEN_PATH = Path("/root/.hermes/secrets/github_token.txt")
if not GITHUB_TOKEN_PATH.exists():
    raise ValueError("GitHub token file not found")
GITHUB_TOKEN = GITHUB_TOKEN_PATH.read_text().strip()
GITHUB_USER = os.environ.get("GITHUB_USER", "rishabh3562")

def discover_all_repos(username, token):
    """Discover all repositories (public and private) for the authenticated user."""
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json"
    }
    url = f"https://api.github.com/user/repos"  # Note: /user/repos, not /users/
    repos = []
    page = 1
    per_page = 100
    while True:
        params = {"per_page": per_page, "page": page}
        response = requests.get(url, headers=headers, params=params)
        if response.status_code != 200:
            print(f"Error fetching repos: {response.status_code}")
            print(response.text)
            break
        data = response.json()
        if not data:
            break
        for repo in data:
            repos.append({
                "name": repo["name"],
                "local_path": f"/repos/{repo['name']}",
                "html_url": repo["html_url"],
                "description": repo.get("description", ""),
                "language": repo.get("language"),
                "updated_at": repo["updated_at"],
                "private": repo.get("private", False)
            })
        # Check if there are more pages
        if len(data) < per_page:
            break
        page += 1
    return repos

def main():
    print("🔍 Discovering ALL repositories (public and private) for user:", GITHUB_USER)
    github_repos = discover_all_repos(GITHUB_USER, GITHUB_TOKEN)
    print(f"   Found {len(github_repos)} repositories")
    public = sum(1 for r in github_repos if not r.get("private", False))
    private = sum(1 for r in github_repos if r.get("private", False))
    print(f"   Public: {public}, Private: {private}")

    # Load existing repos.json
    repos_path = Path("/opt/llm_wiki/repos.json")
    if repos_path.exists():
        with open(repos_path) as f:
            existing_repos = json.load(f)
    else:
        existing_repos = []

    # Create a dict of existing repos by name for easy update
    existing_by_name = {repo["name"]: repo for repo in existing_repos if isinstance(repo, dict) and "name" in repo}

    # Build updated list: update existing entries with latest info, add new ones
    updated_repos = []
    for github_repo in github_repos:
        repo_name = github_repo["name"]
        if repo_name in existing_by_name:
            # Update existing entry with latest info from GitHub
            existing_entry = existing_by_name[repo_name]
            # Keep local_path if it exists, otherwise use GitHub-suggested path
            if "local_path" not in existing_entry or not existing_entry["local_path"]:
                existing_entry["local_path"] = github_repo["local_path"]
            # Update other fields
            existing_entry["html_url"] = github_repo["html_url"]
            existing_entry["description"] = github_repo.get("description", "")
            existing_entry["language"] = github_repo.get("language")
            existing_entry["updated_at"] = github_repo["updated_at"]
            existing_entry["private"] = github_repo.get("private", False)
            updated_repos.append(existing_entry)
        else:
            # Add new repository
            updated_repos.append(github_repo)

    # Save updated repos.json
    with open(repos_path, 'w') as f:
        json.dump(updated_repos, f, indent=2)
    print(f"   Updated {repos_path} with {len(updated_repos)} repositories")

    # Now update MongoDB queue: ensure all discovered repos are in repo_queue with status pending if not present
    client = MongoClient(MONGODB_URI)
    db = client["github_wiki"]
    coll = db["repo_queue"]

    added = 0
    already_pending = 0
    for repo in github_repos:
        repo_name = repo["name"]
        # Check if already in queue
        existing = coll.find_one({"_id": repo_name})
        if not existing:
            # Insert as pending
            doc = {
                "_id": repo_name,
                "status": "pending",
                "addedAt": {"$date": datetime.now(timezone.utc).isoformat()},
                "claimedAt": None,
                "finishedAt": None,
                "failedAt": None,
                "lastError": None,
                "retryCount": 0,
                "lastUpdated": {"$date": datetime.now(timezone.utc).isoformat()}
            }
            coll.insert_one(doc)
            added += 1
        else:
            # If exists but not pending, we could leave as is (respect current status)
            # But for consistency, we might want to reset any stuck processing/failed to pending? 
            # We'll only ensure that if it's done, we don't revert.
            # For safety, we only add if missing.
            if existing.get("status") == "pending":
                already_pending += 1

    print(f"   Added {added} new repos to queue (as pending)")
    print(f"   Found {already_pending} repos already pending in queue")

    # Print final queue stats
    pending = coll.count_documents({"status": "pending"})
    processing = coll.count_documents({"status": "processing"})
    done = coll.count_documents({"status": "done"})
    failed = coll.count_documents({"status": "failed"})
    print(f"   Queue status: pending={pending}, processing={processing}, done={done}, failed={failed}")

    client.close()
    print("✅ Queue update complete.")

if __name__ == "__main__":
    main()