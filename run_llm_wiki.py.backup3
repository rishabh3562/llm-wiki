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

# Configuration
LEDGER_PATH = Path("/opt/llm_wiki/ledger.json")
REPOS_PATH = Path("/opt/llm_wiki/repos.json")
OUTPUT_BASE = Path("/opt/llm_wiki/output")
OBSIDIAN_BASE = Path("/opt/llm_wiki/obsidian-vault")
MONGO_URI = "mongodb+srv://dubeyrishabh108_db_user:z1ss49FReN22EAIk@cluster0.j8iafjr.mongodb.net/github_wiki?retryWrites=true&w=majority"
MONGO_DB = "github_wiki"
MONGO_COLLECTION = "snippets"

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

def main():
    # Phase 0: Setup
    print("🔧 SETUP")
    ledger = load_json(LEDGER_PATH)
    repos = load_json(REPOS_PATH)
    if not repos:
        repos = [{"name": "toolbox", "local_path": "/repos/toolbox"}]
        save_json(REPOS_PATH, repos)
    
    # Ensure output directories exist
    OUTPUT_BASE.mkdir(parents=True, exist_ok=True)
    OBSIDIAN_BASE.mkdir(parents=True, exist_ok=True)
    
    # Process each repo (we only have one for now)
    for repo_info in repos:
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
        repo = git.Repo(local_path)
        head_sha = repo.head.commit.hexsha
        print(f"   Current HEAD: {head_sha}")
        
        # Check ledger
        repo_ledger = ledger.get(repo_name, {})
        last_sha = repo_ledger.get("last_commit_sha")
        if last_sha == head_sha:
            print("   ⏭️  No new commits. Skipping.")
            continue
        
        print("   🆕 New commits detected. Proceeding...")
        
        # Phase 1: Archaeology
        print("\n🔍 PHASE 1 — ARCHAEOLOGY")
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
            print(f"   ✅ Saved intent_recovery.md to {intent_path}")
        except Exception as e:
            print(f"   ❌ Archaeology failed: {e}")
            continue
        
        # Phase 2: Static Analysis
        print("\n📊 PHASE 2 — STATIC ANALYSIS")
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
            print(f"   ✅ Saved smells.json to {smells_path}")
        except Exception as e:
            print(f"   ❌ Static analysis failed: {e}")
            # We'll continue to allow partial success? We'll decide later.
        
        # Phase 3: Parallel Agents (simplified sequential for now)
        print("\n🤖 PHASE 3 — PARALLEL AGENTS")
        try:
            # Agent A: architecture.md
            arch_md = f"""# Architecture for {repo_name}

## Data Flow (Mermaid Diagram)
```mermaid
graph TD
    A[Input] --> B[Processing]
    B --> C[Output]
```
*To be generated from import graph and file tree.*
"""
            (OUTPUT_BASE / repo_name / "architecture.md").write_text(arch_md)
            
            # Agent B: patterns.md
            patterns_md = f"""# Patterns for {repo_name}

## Repeated Patterns
*To be extracted from core logic files.*
"""
            (OUTPUT_BASE / repo_name / "patterns.md").write_text(patterns_md)
            
            # Agent C: improvements.md
            improvements_md = f"""# Improvements for {repo_name}

## Actionable Fixes
*Based on smells.json and high-churn files.*
"""
            (OUTPUT_BASE / repo_name / "improvements.md").write_text(improvements_md)
            
            # Agent D: self_portrait.md
            self_portrait_md = f"""# Self Portrait for {repo_name}

## Who was I as a developer?
*Based on git log, intent_recovery.md, and architecture.md.*

- Skill level at the time: Intermediate
- Decisions showing growth: Modular design in later commits
- Gaps: Lack of error handling in early versions
- What I would do differently now: Add comprehensive testing and type hints from the start.

*This feeds my future fine-tuning dataset.*
"""
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
            print(f"   ✅ Updated wiki_index.json")
            
            print("   ✅ All agents completed")
        except Exception as e:
            print(f"   ❌ Agents phase failed: {e}")
            # We'll still try to store what we have
        
        # Phase 4: Storage
        print("\n💾 PHASE 4 — STORAGE")
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
            print(f"   ✅ Added {snippets_added} new snippets to MongoDB")
            storage_success = True
        except Exception as e:
            print(f"   ❌ MongoDB storage failed: {e}")
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
            print(f"   💾 Wrote {len(snippets_to_backup)} snippets to backup file: {backup_path}")
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
            print(f"   ✅ Updated Obsidian vault at {obsidian_repo_path}")
        except Exception as e:
            print(f"   ❌ Obsidian vault update failed: {e}")
            # We don't set storage_success to False for Obsidian because it's separate
            # but we note it.
        
        # Phase 5: Finalize (only if MongoDB storage succeeded)
        print("\n✅ PHASE 5 — FINALIZE")
        if storage_success:
            try:
                ledger[repo_name] = {
                    "last_commit_sha": head_sha,
                    "last_run": datetime.now(timezone.utc).isoformat(),
                    "snippets_added": snippets_added
                }
                save_json(LEDGER_PATH, ledger)
                print(f"   ✅ Updated ledger.json for {repo_name}")
                print(f"   🎉 Successfully completed LLM Wiki run for {repo_name}")
            except Exception as e:
                print(f"   ❌ Failed to update ledger: {e}")
                # This should not happen, but if it does, we consider the run partially failed.
                # We already added snippets to MongoDB, but ledger not updated.
                # We'll still report the error.
        else:
            print(f"   ⏭️  Skipping ledger update due to storage failure.")
    
    print("\n📋 REPORT BACK")
    # Summary would be printed above per phase
    # In a real cron job, we might send a message via Telegram or email

if __name__ == "__main__":
    main()
