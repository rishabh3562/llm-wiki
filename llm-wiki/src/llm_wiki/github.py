#!/usr/bin/env python3
"""
GitHub API wrapper for llm-wiki.
"""
import os
import base64
import logging
from typing import Optional, List, Dict, Any
from pathlib import Path

import requests

from .config import config

logger = logging.getLogger(__name__)

class GitHubClient:
    """Wrapper around GitHub REST API."""
    
    def __init__(self, token: Optional[str] = None):
        self.token = token or config.github_token
        self.headers = {
            "Authorization": f"token {self.token}",
            "Accept": "application/vnd.github+json",
        }
        self.base_url = "https://api.github.com"
    
    def _request(self, method: str, path: str, **kwargs) -> requests.Response:
        url = f"{self.base_url}{path}"
        response = requests.request(method, url, headers=self.headers, timeout=30, **kwargs)
        response.raise_for_status()
        return response
    
    def get_repo(self, repo_name: str) -> Dict[str, Any]:
        """Get repository metadata."""
        response = self._request("GET", f"/repos/{config.github_user}/{repo_name}")
        return response.json()
    
    def get_repo_contents(self, repo_name: str, path: str = "") -> List[Dict[str, Any]]:
        """Get repository contents (files and directories)."""
        response = self._request("GET", f"/repos/{config.github_user}/{repo_name}/contents/{path}")
        return response.json()
    
    def get_file_content(self, repo_name: str, path: str) -> Optional[str]:
        """Get decoded content of a file."""
        response = self._request("GET", f"/repos/{config.github_user}/{repo_name}/contents/{path}")
        data = response.json()
        if data.get("encoding") == "base64":
            return base64.b64decode(data["content"]).decode("utf-8", errors="ignore")
        return data.get("content")
    
    def get_repo_tree(self, repo_name: str, recursive: bool = True) -> List[Dict[str, Any]]:
        """Get full repository tree."""
        response = self._request("GET", f"/repos/{config.github_user}/{repo_name}/git/trees/main", params={"recursive": "1" if recursive else "0"})
        return response.json().get("tree", [])
    
    def list_user_repos(self, per_page: int = 100) -> List[Dict[str, Any]]:
        """List all user repositories."""
        repos = []
        page = 1
        while True:
            response = self._request("GET", "/user/repos", params={
                "per_page": per_page,
                "page": page,
                "sort": "updated",
                "type": "all"
            })
            batch = response.json()
            if not batch:
                break
            repos.extend(batch)
            page += 1
        return repos


# Global instance
github = GitHubClient()