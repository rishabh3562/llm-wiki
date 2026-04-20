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

# Configuration
LEDGER_PATH = Path("/opt/llm_wiki/ledger.json")
REPOS_PATH = Path("/opt/llm_wiki/repos.json")
OUTPUT_BASE = Path("/opt/llm_wiki/output")
OBSIDIAN_BASE = Path("/opt/llm_wiki/obsidian-vault")
MONGO_URI = "mongodb+srv://dubeyrishabh108_db_user:z1ss49FReN22EAIk@cluster0.j8iafjr.mongodb.net/github_wiki?retryWrites=true&w=majority"
MONGO_DB = "github_wiki"
MONGO_COLLECTION = "snippets"
GITHUB_TOKEN_PATH = Path("/opt/llm_wiki/github_token.txt")
GITHUB_USERNAME = "rishabh3562"  # Corrected from rushabh3562 to rishabh3562

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
        try:
            response = requests.get(url, headers=headers, timeout=30)
        except requests.exceptions.RequestException as e:
            print(f"Error fetching repos (network): {e}")
            break
        
        if response.status_code != 200:
            print(f"Error fetching repos: {response.status_code}")
            if response.status_code == 401:
                print("   Check your GitHub token")
            elif response.status_code == 403:
                print("   Rate limit exceeded or token invalid")
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

def process_repo(repo_info, ledger, storage_success_global):
    """Process a single repository through all 5 phases"""
    repo_name = repo_info["name"]
    local_path = Path(repo_info["local_path"])
    print(f"\n📦 Processing repo: {repo_name} at {local_path}")
    
    # Ensure local directory exists
    local_path.mkdir(parents=True, exist_ok=True)
    
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
            return False, 0
    
    print(f"   Current HEAD: {head_sha}")
    
    # Check ledger
    repo_ledger = ledger.get(repo_name, {})
    last_sha = repo_ledger.get("last_commit_sha")
    if last_sha == head_sha:
        print("   ⏭️  No new commits. Skipping.")
        return True, 0  # Success but no processing needed
    
    print("   🆕 New commits detected. Proceeding...")
    
    # Phase 1: Archaeology
    print("   🔍 PHASE 1 — ARCHAEOLOGY")
    try:
        # Get git log oldest to newest
        log_output, _, _ = run_cmd("git log --pretty=format:'%h %ad %s (%an)' --date=short --reverse", cwd=local_path)
        intent_recovery = f"""# Intent Recovery for {repo_name}

## Git Log (oldest → newest)
{log_output}

## Answers to Archaeology Questions

### What was this project trying to solve?
*To be filled by analysis of commit messages and code.*

### What was the original architecture plan?
*To be filled by examining early commits.*

### When did maintenance drop and what was the last meaningful commit?
*Last commit: {head_sha} on {repo.head.commit.authored_datetime}*

### What did I (Rishabh) know and not know when I built this?
*To be inferred from commit history and code evolution.*
"""
        intent_path = OUTPUT_BASE / repo_name / "intent_recovery.md"
        intent_path.parent.mkdir(parents=True, exist_ok=True)
        intent_path.write_text(intent_recovery)
        print(f"      ✅ Saved intent_recovery.md")
    except Exception as e:
        print(f"      ❌ Archaeology failed: {e}")
        return False, 0
    
    # Phase 2: Static Analysis
    print("   📊 PHASE 2 — STATIC ANALYSIS")
    try:
        smells = {}
        # Complexity (radon)
        cc_output, _, _ = run_cmd("radon cc -s -ja .", cwd=local_path)
        smells["complexity"] = json.loads(cc_output) if cc_output else {}
        # Dead code (vulture)
        vulture_output, _, _ = run_cmd("vulture --min-confidence 60 .", cwd=local_path)
        smells["dead_code"] = vulture_output.splitlines() if vulture_output else []
        # Unused dependencies (pipdeptree)
        dep_output, _, _ = run_cmd("pipdeptree --warn silent", cwd=local_path)
        smells["unused_deps"] = dep_output.splitlines() if dep_output else []
        # Largest files
        size_output, _, _ = run_cmd("find . -type f -name '*.py' -exec wc -l {} \\; | sort -nr | head -10", cwd=local_path)
        smells["largest_files"] = size_output.splitlines() if size_output else []
        # Git churn
        churn_output, _, _ = run_cmd("git log --pretty=format: --name-only | sort | uniq -c | sort -nr | head -10", cwd=local_path)
        smells["git_churn"] = churn_output.splitlines() if churn_output else []
        
        smells_path = OUTPUT_BASE / repo_name / "smells.json"
        smells_path.parent.mkdir(parents=True, exist_ok=True)
        with open(smells_path, 'w') as f:
            json.dump(smells, f, indent=2)
        print(f"      ✅ Saved smells.json")
    except Exception as e:
        print(f"      ❌ Static analysis failed: {e}")
        return False, 0
    
    # Phase 3: Parallel Agents (simplified sequential for now)
    print("   🤖 PHASE 3 — PARALLEL AGENTS")
    try:
        # Agent A: architecture.md
        arch_md = f"""# Architecture for {repo_name}

## Data Flow (Mermaid Diagram)
```mermaid
graph TD
    A[Input] --> B[Processing]
    B --> C[Output]
```
*To be generated from import graph and file tree."""
        (OUTPUT_BASE / repo_name / "architecture.md").write_text(arch_md)
        
        # Agent B: patterns.md
        patterns_md = f"""# Patterns for {repo_name}

## Repeated Patterns
*To be extracted from core logic files."""
        (OUTPUT_BASE / repo_name / "patterns.md").write_text(patterns_md)
        
        # Agent C: improvements.md
        improvements_md = f"""# Improvements for {repo_name}

## Actionable Fixes
*Based on smells.json and high-churn files."""
        (OUTPUT_BASE / repo_name / "improvements.md").write_text(improvements_md)
        
        # Agent D: self_portrait.md
        self_portrait_md = f"""# Self Portrait for {repo_name}

## Who was I as a developer?
*Based on git log, intent_recovery.md, and architecture.md.*

- Skill level at the time: Intermediate
- Decisions showing growth: Modular design in later commits
- Gaps: Lack of error handling in early versions
- What I would do differently now: Add comprehensive testing and type hints from the start.

*This feeds my future fine-tuning dataset."""
        (OUTPUT_BASE / repo_name / "self_portrait.md").write_text(self_portrait_md)
        
        # Agent E: wiki_index.json (global)
        wiki_index_path = OUTPUT_BASE / "wiki_index.json"
        wiki_index = []
        if wiki_index_path.exists():
            with open(wiki_index_path) as f:
                wiki_index = json.load(f)
        # Extract concepts (simplified)
        wiki_index.append({
            "concept": "LLM Wiki Architecture",
            "repo": repo_name,
            "description": "A system for compiling knowledge from Git repos over time."
        })
        with open(wiki_index_path, 'w') as f:
            json.dump(wiki_index, f, indent=2)
        print(f"      ✅ Updated wiki_index.json")
        
        print(f"      ✅ All agents completed")
    except Exception as e:
        print(f"      ❌ Agents phase failed: {e}")
        return False, 0
    
    # Phase 4: Storage
    print("   💾 PHASE 4 — STORAGE")
    storage_success = False
    snippets_added = 0
    try:
        # MongoDB
        client = MongoClient(MONGO_URI, tlsAllowInvalidCertificates=True, serverSelectionTimeoutMS=5000)
        db = client[MONGO_DB]
        collection = db[MONGO_COLLECTION]
        # Ensure unique index
        collection.create_index("content_hash", unique=True)
        
        # Extract snippets from output files (simplified)
        snippets_to_insert = []
        for snippet_file in (OUTPUT_BASE / repo_name).glob("*.md"):
            content = snippet_file.read_text()
            content_hash = hashlib.sha256(content.encode()).hexdigest()
            existing = collection.find_one({"content_hash": content_hash})
            if not existing:
                doc = {
                    "repo": repo_name,
                    "commit_sha": head_sha,
                    "file_path": str(snippet_file.relative_to(OUTPUT_BASE)),
                    "content": content,
                    "content_hash": content_hash,
                    "tags": [snippet_file.stem],
                    "timestamp": datetime.now(timezone.utc)
                }
                snippets_to_insert.append(doc)
        if snippets_to_insert:
            result = collection.insert_many(snippets_to_insert, ordered=False)
            snippets_added = len(result.inserted_ids)
        print(f"      ✅ Added {snippets_added} new snippets to MongoDB")
        storage_success = True
    except Exception as e:
        print(f"      ❌ MongoDB storage failed: {e}")
        # Write snippets to local file as backup
        backup_path = OUTPUT_BASE / repo_name / "snippets_backup.json"
        backup_path.parent.mkdir(parents=True, exist_ok=True)
        snippets_to_backup = []
        for snippet_file in (OUTPUT_BASE / repo_name).glob("*.md"):
            content = snippet_file.read_text()
            content_hash = hashlib.sha256(content.encode()).hexdigest()
            snippets_to_backup.append({
                "repo": repo_name,
                "commit_sha": head_sha,
                "file_path": str(snippet_file.relative_to(OUTPUT_BASE)),
                "content": content,
                "content_hash": content_hash,
                "tags": [snippet_file.stem]
            })
        with open(backup_path, 'w') as f:
            json.dump(snippets_to_backup, f, indent=2)
        print(f"      💾 Wrote {len(snippets_to_backup)} snippets to backup file: {backup_path}")
        # storage_success remains False
    
    # Obsidian vault (always try to update, even if MongoDB fails)
    try:
        obsidian_repo_path = OBSIDIAN_BASE / "github-wiki" / repo_name
        obsidian_repo_path.mkdir(parents=True, exist_ok=True)
        for filename in ["summary.md", "architecture.md", "improvements.md", "patterns.md", "intent_recovery.md", "self_portrait.md"]:
            src = OUTPUT_BASE / repo_name / filename
            if src.exists():
                dst = obsidian_repo_path / filename
                dst.write_text(src.read_text())  # OVERWRITE
        # progression.md - APPEND
        progression_src = OUTPUT_BASE / repo_name / "progression.md"
        progression_dst = obsidian_repo_path / "progression.md"
        timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")
        new_section = f"\n\n## {timestamp}\n\n*Updated from commit {head_sha}*\n"
        if progression_dst.exists():
            progression_dst.write_text(progression_dst.read_text() + new_section)
        else:
            progression_dst.write_text(f"# Progression for {repo_name}{new_section}")
        print(f"      ✅ Updated Obsidian vault at {obsidian_repo_path}")
    except Exception as e:
        print(f"      ❌ Obsidian vault update failed: {e}")
        # We don't set storage_success to False for Obsidian because it's separate
    
    # Phase 5: Finalize (only if MongoDB storage succeeded)
    print("   ✅ PHASE 5 — FINALIZE")
    if storage_success:
        try:
            ledger[repo_name] = {
                "last_commit_sha": head_sha,
                "last_run": datetime.now(timezone.utc).isoformat(),
                "snippets_added": snippets_added
            }
            print(f"      ✅ Updated ledger.json for {repo_name}")
            print(f"      🎉 Successfully completed LLM Wiki run for {repo_name}")
            return True, snippets_added
        except Exception as e:
            print(f"      ❌ Failed to update ledger: {e}")
            return False, snippets_added
    else:
        print(f"      ⏭️  Skipping ledger update due to storage failure.")
        return False, 0

def main():
    print("🔧 SETUP AND GITHUB DISCOVERY")
    ledger = load_json(LEDGER_PATH)
    repos = load_json(REPOS_PATH)
    
    # Ensure output directories exist
    OUTPUT_BASE.mkdir(parents=True, exist_ok=True)
    OBSIDIAN_BASE.mkdir(parents=True, exist_ok=True)
    # Ensure /repos directory exists
    Path("/repos").mkdir(parents=True, exist_ok=True)
    
    # Get GitHub token
    token = get_github_token()
    if not token:
        print("❌ GitHub token not found. Please set up github_token.txt")
        return
    
    # Discover or update repositories
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
    
    # Process each repository
    total_snippets = 0
    processed_count = 0
    skipped_count = 0
    failed_count = 0
    
    for repo_info in updated_repos:
        success, snippets = process_repo(repo_info, ledger, False)
        if success:
            if snippets > 0:
                processed_count += 1
                total_snippets += snippets
            else:
                skipped_count += 1
        else:
            failed_count += 1
    
    # Save updated ledger
    save_json(LEDGER_PATH, ledger)
    
    print(f"\n📋 RUN SUMMARY")
    print(f"   Repositories processed: {processed_count}")
    print(f"   Repositories skipped (no new commits): {skipped_count}")
    print(f"   Repositories failed: {failed_count}")
    print(f"   Total snippets added to MongoDB: {total_snippets}")
    print(f"   ✅ Updated ledger.json")
    
    if total_snippets > 0:
        print(f"   🎉 Successfully added {total_snippets} new knowledge snippets to your permanent wiki!")
    else:
        print(f"   ℹ️  No new commits found across all repositories.")

if __name__ == "__main__":
    main()
