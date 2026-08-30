#!/usr/bin/env python3
"""
Repository analysis module for llm-wiki.
Analyzes a single repository and stores results in MongoDB.
"""
import os
import json
import hashlib
import logging
from datetime import datetime, timezone
from typing import Dict, List, Optional, Any
from pathlib import Path

from .config import config
from .mongo import mongo
from .github import github

logger = logging.getLogger(__name__)

# File extensions to analyze
CODE_EXTENSIONS = {
    '.py', '.js', '.ts', '.jsx', '.tsx', '.java', '.cpp', '.c', '.h',
    '.cs', '.go', '.rs', '.rb', '.php', '.swift', '.kt', '.scala',
    '.html', '.css', '.scss', '.vue', '.svelte', '.json', '.yaml', '.yml',
    '.md', '.txt', '.toml', '.ini', '.cfg', '.conf', '.sh', '.bash',
    '.dockerfile', '.dockerignore', '.gitignore', '.env.example'
}

SKIP_DIRS = {'.git', 'node_modules', '__pycache__', '.venv', 'venv', 'dist', 'build', '.next', '.vercel', 'target', 'bin', 'obj'}

class RepoAnalyzer:
    """Analyzes a single repository and stores results in MongoDB."""
    
    def __init__(self):
        self.github_client = github
        self.mongo = mongo
    
    def analyze_repo(self, repo_name: str) -> Dict[str, Any]:
        """
        Analyze a single repository and store results in MongoDB.
        Returns the analysis result.
        """
        logger.info(f"Analyzing repo: {repo_name}")
        
        try:
            # Get repo metadata from GitHub
            repo_meta = self.github_client.get_repo(repo_name)
            
            # Get repo tree
            tree = self.github_client.get_repo_tree(repo_name)
            
            # Analyze files
            files_data = self._analyze_files(repo_name, tree)
            
            # Generate analysis summary
            analysis = self._generate_analysis(repo_name, repo_meta, files_data)
            
            # Store in MongoDB
            self._store_analysis(repo_name, analysis)
            
            # Update repo status
            self._update_repo_status(repo_name, analysis)
            
            return analysis
            
        except Exception as e:
            logger.error(f"Error analyzing {repo_name}: {e}")
            raise
    
    def _analyze_files(self, repo_name: str, tree: List[Dict]) -> List[Dict]:
        """Analyze files in the repository."""
        files_data = []
        
        for item in tree:
            if item["type"] != "blob":
                continue
            
            path = item["path"]
            
            # Skip directories we don't care about
            if any(part in SKIP_DIRS for part in Path(path).parts):
                continue
            
            # Check extension
            ext = Path(path).suffix.lower()
            if ext not in CODE_EXTENSIONS and ext != "":
                continue
            
            # Check file size
            if item.get("size", 0) > config.max_file_size_bytes:
                continue
            
            # Get file content
            content = self.github_client.get_file_content(repo_name, path)
            if not content:
                continue
            
            files_data.append({
                "path": path,
                "size": item.get("size", 0),
                "extension": ext,
                "content": content,
                "sha": item.get("sha"),
            })
        
        return files_data
    
    def _generate_analysis(self, repo_name: str, repo_meta: Dict, files_data: List[Dict]) -> Dict[str, Any]:
        """Generate analysis summary from file data."""
        # File statistics
        total_files = len(files_data)
        total_size = sum(f["size"] for f in files_data)
        extensions = {}
        for f in files_data:
            ext = f["extension"]
            extensions[ext] = extensions.get(ext, 0) + 1
        
        # Language detection
        lang = self._detect_language(extensions, repo_name)
        
        # Top files by size
        top_files = sorted(files_data, key=lambda x: x["size"], reverse=True)[:10]
        
        # Generate content hash for change detection
        content_hash = self._compute_content_hash(files_data)
        
        return {
            "repo_name": repo_name,
            "repo_meta": {
                "description": repo_meta.get("description"),
                "language": repo_meta.get("language"),
                "stars": repo_meta.get("stargazers_count", 0),
                "forks": repo_meta.get("forks_count", 0),
                "private": repo_meta.get("private", False),
                "updated_at": repo_meta.get("updated_at"),
                "pushed_at": repo_meta.get("pushed_at"),
                "default_branch": repo_meta.get("default_branch", "main"),
            },
            "analysis": {
                "total_files": total_files,
                "total_size_bytes": total_size,
                "extensions": extensions,
                "detected_language": lang,
                "top_files": [
                    {"path": f["path"], "size": f["size"], "ext": f["extension"]}
                    for f in top_files
                ],
                "content_hash": content_hash,
            },
            "files": files_data,  # Full file data for embeddings
            "analyzed_at": datetime.now(timezone.utc).isoformat(),
            "analyzer_version": "1.0",
        }
    
    def _detect_language(self, extensions: Dict[str, int], repo_name: str) -> str:
        """Detect primary language from extensions."""
        lang_map = {
            '.py': 'Python', '.js': 'JavaScript', '.ts': 'TypeScript',
            '.jsx': 'JavaScript', '.tsx': 'TypeScript', '.java': 'Java',
            '.cpp': 'C++', '.c': 'C', '.cs': 'C#', '.go': 'Go',
            '.rs': 'Rust', '.rb': 'Ruby', '.php': 'PHP', '.swift': 'Swift',
            '.kt': 'Kotlin', '.scala': 'Scala',
        }
        
        for ext, count in sorted(extensions.items(), key=lambda x: -x[1]):
            if ext in lang_map:
                return lang_map[ext]
        return "Unknown"
    
    def _compute_content_hash(self, files_data: List[Dict]) -> str:
        """Compute hash of all file contents for change detection."""
        hasher = hashlib.sha256()
        for f in sorted(files_data, key=lambda x: x["path"]):
            hasher.update(f["sha"].encode() if f.get("sha") else f["path"].encode())
        return hasher.hexdigest()
    
    def _store_analysis(self, repo_name: str, analysis: Dict):
        """Store analysis in MongoDB."""
        collection = mongo.get_collection(config.analyses_collection)
        collection.update_one(
            {"repo_name": repo_name},
            {"$set": analysis},
            upsert=True
        )
        logger.info(f"Stored analysis for {repo_name}")
    
    def _update_repo_status(self, repo_name: str, analysis: Dict):
        """Update repo status in repos collection."""
        collection = mongo.get_collection(config.repos_collection)
        collection.update_one(
            {"repo_name": repo_name},
            {
                "$set": {
                    "repo_name": repo_name,
                    "last_analyzed": datetime.now(timezone.utc).isoformat(),
                    "initial_analysis_done": True,
                    "last_content_hash": analysis["analysis"]["content_hash"],
                    "total_files": analysis["analysis"]["total_files"],
                    "detected_language": analysis["analysis"]["detected_language"],
                },
                "$setOnInsert": {
                    "repo_name": repo_name,
                    "created_at": datetime.now(timezone.utc).isoformat(),
                }
            },
            upsert=True
        )


def analyze_one_repo(repo_name: str) -> Dict[str, Any]:
    """Entry point for analyzing a single repo (used by cron/workflow)."""
    analyzer = RepoAnalyzer()
    return analyzer.analyze_repo(repo_name)


def get_next_repo_to_analyze() -> Optional[str]:
    """Get the next repo that needs analysis."""
    collection = mongo.get_collection(config.repos_collection)
    
    # Load repos from JSON to get full list
    with open(config.repos_json_path, 'r') as f:
        all_repos = json.load(f)
    
    repo_names = [r["name"] for r in all_repos]
    
    # Find repos not yet analyzed
    for name in repo_names:
        status = mongo.get_collection(config.repos_collection).find_one({"repo_name": name})
        if not status or not status.get("initial_analysis_done"):
            return name
    
    return None


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        # Auto-pick next repo
        repo = get_next_repo_to_analyze()
        if not repo:
            print("All repos analyzed!")
            sys.exit(0)
    else:
        repo = sys.argv[1]
    
    print(f"Analyzing: {repo}")
    result = analyze_one_repo(repo)
    print(f"Done: {repo} - {result['analysis']['total_files']} files, {result['analysis']['detected_language']}")