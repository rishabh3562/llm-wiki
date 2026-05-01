#!/usr/bin/env python3
"""
Verify that the MongoDB URI in run_one_repo_wrapper.sh is correct (does not contain GitHub PAT).
Prints result to stdout.
"""
import os
import re

WRAPPER_PATH = "/opt/llm_wiki/run_one_repo_wrapper.sh"

def read_wrapper():
    try:
        with open(WRAPPER_PATH, 'r') as f:
            return f.read()
    except Exception as e:
        return None

def check_uri(content):
    if not content:
        return False, "Could not read wrapper file"
    # Find the line with export MONGODB_URI
    match = re.search(r'export MONGODB_URI="([^"]*)"', content)
    if not match:
        return False, "MONGODB_URI not found in wrapper"
    uri = match.group(1)
    # Check if URI contains 'github_pat' (case-insensitive) in the password part
    if 'github_pat' in uri.lower():
        return False, f"URI appears to contain GitHub PAT: {uri[:50]}..."
    return True, "URI looks OK (no GitHub PAT detected)"

def main():
    content = read_wrapper()
    if content is None:
        print("💥 Verification failed: Could not read wrapper file")
        exit(1)
    ok, detail = check_uri(content)
    if not ok:
        print(f"🚨 MongoDB URI Verification Failed\n\n{detail}\n\nFile: {WRAPPER_PATH}\n\nPlease check and correct the URI.")
        exit(1)
    else:
        print("✅ MongoDB URI verification passed")
        exit(0)

if __name__ == "__main__":
    main()