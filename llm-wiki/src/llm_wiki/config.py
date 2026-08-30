#!/usr/bin/env python3
"""
llm-wiki configuration - all settings from environment variables.
"""
import os
from pathlib import Path
from dataclasses import dataclass, field
from typing import Optional

@dataclass
class Config:
    # Required (no defaults)
    github_token: str
    mongodb_uri: str
    
    # Optional (with defaults)
    github_user: str = "rishabh3562"
    og_mongodb_uri: Optional[str] = None
    
    # Database names
    db_name: str = "ai_agents"
    og_db_name: str = "github_wiki_backup_1"
    
    # Collection names
    repos_collection: str = "repos"
    analyses_collection: str = "analyses"
    snippets_collection: str = "snippets"
    embeddings_collection: str = "embeddings"
    vault_notes_collection: str = "vault_notes"
    
    # OpenRouter
    openrouter_api_key: Optional[str] = None
    analysis_model: str = "nvidia/nemotron-3-ultra-550b:free"
    embedding_model: str = "text-embedding-3-small"
    
    # Obsidian vault
    vault_path: str = "obsidian-vault/github-wiki"
    
    # Repo analysis
    repos_json_path: str = "repos.json"
    max_files_per_repo: int = 50
    max_file_size: int = 100_000  # bytes
    
    # Processing
    batch_size: int = 1
    max_files_per_batch: int = 20
    max_file_size_bytes: int = 50_000
    
    @classmethod
    def from_env(cls) -> "Config":
        """Load all configuration from environment variables."""
        github_token = os.environ.get("GH_PAT") or os.environ.get("GITHUB_TOKEN")
        if not github_token:
            raise ValueError("GH_PAT or GITHUB_TOKEN environment variable required")
        
        mongodb_uri = os.environ.get("MONGODB_URI")
        if not mongodb_uri:
            raise ValueError("MONGODB_URI environment variable required")
        
        return cls(
            github_token=github_token,
            mongodb_uri=mongodb_uri,
            og_mongodb_uri=os.environ.get("OG_MONGODB_URI"),
            openrouter_api_key=os.environ.get("OPENROUTER_API_KEY"),
            github_user=os.environ.get("GITHUB_USER", "rishabh3562"),
            analysis_model=os.environ.get("ANALYSIS_MODEL", "nvidia/nemotron-3-ultra-550b:free"),
            embedding_model=os.environ.get("EMBEDDING_MODEL", "text-embedding-3-small"),
        )


# Global config instance
config = Config.from_env()