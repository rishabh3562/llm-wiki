#!/usr/bin/env python3
import json
import os
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
import hashlib
from pymongo import MongoClient
import git
import requests
from urllib.parse import urljoin

# Configuration
LEDGER_PATH = Path("/opt/llm_wiki/ledger.json")
REPOS_PATH = Path("/opt/llm_wiki/repos.json")
OUTPUT_BASE = Path("/opt/llm_wiki/output")
OBSIDIAN_BASE = Path("/opt/llm_wiki/obsidian-vault")
MONGO_URI = "mongodb+srv://dubeyrishabh108_db_user:z1ss49FReN22EAIk@cluster0.j8iafjr.mongodb.net/github_wiki?retryWrites=true&w=majority"
MONGO_DB = "github_wiki"
MONGO_COLLECTION = "snippets"
GITHUB_TOKEN_PATH = Path("/root/.hermes/secrets/github_token.txt")
GITHUB_USERNAME = "rishabh3562"  # From user's message

def load_json(path):
    if not path.exists():
        return {}
    with open(path) as f:
        return json.load(f)

def save_json(path, data):
    with open(path, 'w') as f:
        json.dump(data, f, indent=2)

def run_cmd(cmd, cwd=None):
    try:
        result = subprocess.run(cmd, shell=True, cwd=cwd, capture_output=True, text=True, check=True)
        return result.stdout.strip(), result.stderr.strip(), 0
    except subprocess.CalledProcessError as e:
        return e.stdout.strip(), e.stderr.strip(), e.returncode

def get_github_token():
    """Read GitHub token from secure file"""
    if GITHUB_TOKEN_PATH.exists():
        return GITHUB_TOKEN_PATH.read_text().strip()
    return None

def discover_github_repos(username, token):
    """Discover all repositories for a GitHub user"""
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json"
    }
    
    repos = []
    page = 1
    per_page = 100
    
    while True:
        url = f"https://api.github.com/users/{username}/repos?per_page={per_page}&page={page}"
        response = requests.get(url, headers=headers)
        
        if response.status_code != 200:
            print(f"Error fetching repos: {response.status_code}")
            print(response.text)
            break
            
        page_repos = response.json()
        if not page_repos:
            break
            
        for repo in page_repos:
            repos.append({
                "name": repo["name"],
                "local_path": f"/repos/{repo['name']}",
                "html_url": repo["html_url"],
                "description": repo.get("description", ""),
                "language": repo.get("language"),
                "updated_at": repo["updated_at"]
            })
        
        # Check if there are more pages
        if len(page_repos) < per_page:
            break
        page += 1
        
    return repos

def main():
    print("🔧 SETUP AND GITHUB DISCOVERY")
    ledger = load_json(LEDGER_PATH)
    repos = load_json(REPOS_PATH)
    
    # Ensure output directories exist
    OUTPUT_BASE.mkdir(parents=True, exist_ok=True)
    OBSIDIAN_BASE.mkdir(parents=True, exist_ok=True)
    
    # Get GitHub token
    token = get_github_token()
    if not token:
        print("❌ GitHub token not found. Please set up github_token.txt")
        return
    
    # Discover repositories
    print(f"🔍 Discovering repositories for user: {GITHUB_USERNAME}")
    github_repos = discover_github_repos(GITHUB_USERNAME, token)
    print(f"   Found {len(github_repos)} repositories")
    
    # Update repos.json with discovered repositories
    # We'll keep existing entries and add/new update from GitHub
    existing_repos = {repo["name"]: repo for repo in repos}
    updated_repos = []
    
    for github_repo in github_repos:
        repo_name = github_repo["name"]
        if repo_name in existing_repos:
            # Update existing entry with latest info from GitHub
            existing_entry = existing_repos[repo_name]
            # Keep the local_path if it exists, otherwise use GitHub-suggested path
            if "local_path" not in existing_entry or not existing_entry["local_path"]:
                existing_entry["local_path"] = github_repo["local_path"]
            updated_repos.append(existing_entry)
        else:
            # Add new repository
            updated_repos.append({
                "name": github_repo["name"],
                "local_path": github_repo["local_path"],
                "html_url": github_repo["html_url"],
                "description": github_repo["description"],
                "language": github_repo["language"],
                "updated_at": github_repo["updated_at"]
            })
    
    # Save updated repos list
    save_json(REPOS_PATH, updated_repos)
    print(f"   Updated {REPOS_PATH} with {len(updated_repos)} repositories")
    
    # Now process each repository (similar to original logic but for all repos)
    for repo_info in updated_repos:
        repo_name = repo_info["name"]
        local_path = Path(repo_info["local_path"])
        print(f"\n📦 Processing repo: {repo_name} at {local_path}")
        
        # Initialize git repo if needed
        if not (local_path / ".git").exists():
            print("   Initializing git repo...")
            run_cmd("git init", cwd=local_path)
            run_cmd("git config user.name 'Hermes Agent'", cwd=local_path)
            run_cmd("git config user.email 'hermes@example.com'", cwd=local_path)
            # Create initial commit
            (local_path / "README.md").write_text(f"# {repo_name}\n\nPlaceholder repo for LLM Wiki.\n")
            run_cmd("git add README.md", cwd=local_path)
            run_cmd("git commit -m 'Initial commit'", cwd=local_path)
        
        # Pull latest commits (assuming origin/main)
        print("   Pulling latest commits...")
        run_cmd("git fetch origin", cwd=local_path)
        run_cmd("git reset --hard origin/main", cwd=local_path)  # Ensure we are at latest
        
        # Get current HEAD SHA
        try:
            repo = git.Repo(local_path)
            head_sha = repo.head.commit.hexsha
        except Exception as e:
            print(f"   Error getting HEAD SHA: {e}")
            # If repo is empty or has no commits, create initial commit
            if not (local_path / "HEAD").exists() or (local_path / "HEAD").read_text().strip() == "ref: refs/heads/main\n":
                print("   Creating initial commit...")
                run_cmd("git add .", cwd=local_path)
                run_cmd("git commit -m 'Initial commit'", cwd=local_path)
                repo = git.Repo(local_path)
                head_sha = repo.head.commit.hexsha
            else:
                print(f"   Skipping repo {repo_name} due to git error: {e}")
                continue
        
        print(f"   Current HEAD: {head_sha}")
        
        # Check ledger
        repo_ledger = ledger.get(repo_name, {})
        last_sha = repo_ledger.get("last_commit_sha")
        if last_sha == head_sha:
            print("   ⏭️  No new commits. Skipping.")
            continue
        
        print("   🆕 New commits detected. Proceeding...")
        
        # For now, we'll just note that we found new commits and would process them
        # In a full implementation, we would run the 5 phases here
        print("   📝 Would run 5-phase analysis here (archaeology, static analysis, agents, storage, finalize)")
        
        # Update ledger to mark as processed (in a real run, this would happen after successful processing)
        ledger[repo_name] = {
            "last_commit_sha": head_sha,
            "last_run": datetime.now(timezone.utc).isoformat(),
            "snippets_added": 0  # Would be actual count after processing
        }
    
    # Save updated ledger
    save_json(LEDGER_PATH, ledger)
    print(f"\n✅ Updated ledger.json with processing status for {len(updated_repos)} repositories")
    print("\n📋 In a full implementation, each repo with new commits would go through the 5-phase analysis")

if __name__ == "__main__":
    main()
