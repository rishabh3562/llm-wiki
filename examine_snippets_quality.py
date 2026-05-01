#!/usr/bin/env python3
import os
import sys
from pymongo import MongoClient
from datetime import datetime, timezone
import hashlib
import json

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
    token_path = "/root/.hermes/secrets/github_token.txt"
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

print("\n=== SNIPPETS COLLECTION ===")
snippets_coll = db["snippets"]
total_snippets = snippets_coll.count_documents({})
print(f"Total snippets: {total_snippets}")

# Get recent snippets sorted by timestamp descending
recent_snippets = list(snippets_coll.find().sort("timestamp", -1).limit(30))
print(f"Examining {len(recent_snippets)} most recent snippets\n")
print("=" * 80)

# Analysis metrics
depth_scores = []
actionability_scores = []
consistency_notes = []

for i, snippet in enumerate(recent_snippets, 1):
    print(f"\nSnippet #{i}:")
    print(f"  Repo: {snippet.get('repo', 'N/A')}")
    print(f"  File: {snippet.get('file_path', 'N/A')}")
    print(f"  Tags: {snippet.get('tags', [])}")
    print(f"  Timestamp: {snippet.get('timestamp', 'N/A')}")
    print(f"  Commit SHA: {snippet.get('commit_sha', 'N/A')[:8]}...")
    
    content = snippet.get('content', '')
    print(f"  Content length: {len(content)} characters")
    
    # Analyze content for depth and actionability
    lines = content.split('\n')
    non_empty_lines = [line for line in lines if line.strip()]
    
    print(f"  Non-empty lines: {len(non_empty_lines)}")
    
    # Check for actionable content
    action_indicators = ['should', 'could', 'recommend', 'suggest', 'fix', 'improve', 'add', 'remove', 'change', 'update']
    action_count = sum(1 for line in non_empty_lines for indicator in action_indicators if indicator in line.lower())
    
    # Check for structured elements
    has_headers = any(line.startswith('#') for line in lines)
    has_lists = any(line.strip().startswith(('-', '*', '+')) or any(line.strip().startswith(f'{n}.') for n in range(1, 20)) for line in lines)
    has_code_blocks = '```' in content
    has_tables = '|' in content and '-|-' in content
    
    print(f"  Action indicators found: {action_count}")
    print(f"  Has headers: {has_headers}")
    print(f"  Has lists: {has_lists}")
    print(f"  Has code blocks: {has_code_blocks}")
    print(f"  Has tables: {has_tables}")
    
    # Depth score: based on length, structure, and specificity
    depth_score = 0
    if len(content) > 500:
        depth_score += 2
    elif len(content) > 200:
        depth_score += 1
    if has_headers:
        depth_score += 1
    if has_lists:
        depth_score += 1
    if has_code_blocks:
        depth_score += 1
    if has_tables:
        depth_score += 1
    
    # Actionability score: based on action indicators and explicit recommendations
    actionability_score = 0
    if action_count > 5:
        actionability_score += 2
    elif action_count > 2:
        actionability_score += 1
    if any(word in content.lower() for word in ['recommend', 'suggest', 'should']):
        actionability_score += 1
    if any(word in content.lower() for word in ['fix', 'improve', 'add', 'remove']):
        actionability_score += 1
    
    depth_scores.append(depth_score)
    actionability_scores.append(actionability_score)
    
    # Consistency notes: check if tags are present and if format matches expectations
    tags = snippet.get('tags', [])
    if not tags:
        consistency_notes.append(f"Snippet {i} has no tags")
    if not snippet.get('file_path'):
        consistency_notes.append(f"Snippet {i} missing file_path")
    
    # Show first 200 chars of content
    preview = content[:200] + ('...' if len(content) > 200 else '')
    print(f"  Preview:\n{preview}")
    print("-" * 40)

# Summary
print("\n=== SUMMARY ===")
print(f"Average depth score: {sum(depth_scores)/len(depth_scores) if depth_scores else 0:.2f} (out of 6)")
print(f"Average actionability score: {sum(actionability_scores)/len(actionability_scores) if actionability_scores else 0:.2f} (out of 4)")
print(f"Consistency issues noted: {len(consistency_notes)}")
if consistency_notes:
    print("Consistency issues:")
    for note in consistency_notes[:5]:  # Show first 5
        print(f"  - {note}")

client.close()