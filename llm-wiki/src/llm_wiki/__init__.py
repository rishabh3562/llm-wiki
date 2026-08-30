#!/usr/bin/env python3
"""
llm-wiki package initialization.
"""
from .config import config
from .mongo import mongo
from .github import github
from .config import Config
from .mongo import MongoDBManager
from .github import GitHubClient

__version__ = "1.0.0"
__all__ = [
    "config",
    "mongo",
    "github",
    "Config",
    "MongoDBManager", 
    "GitHubClient",
]