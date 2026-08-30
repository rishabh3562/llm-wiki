#!/usr/bin/env python3
"""
MongoDB client wrapper for llm-wiki.
"""
from pymongo import MongoClient
from pymongo.database import Database
from pymongo.collection import Collection
from typing import Optional
import logging

from .config import config

logger = logging.getLogger(__name__)

class MongoDBManager:
    """Manages MongoDB connections for both AI Agents and OG clusters."""
    
    def __init__(self):
        self._client: Optional[MongoClient] = None
        self._og_client: Optional[MongoClient] = None
        self._db: Optional[Database] = None
        self._og_db: Optional[Database] = None
    
    def get_client(self) -> MongoClient:
        """Get or create the main MongoDB client."""
        if self._client is None:
            self._client = MongoClient(
                config.mongodb_uri,
                tlsAllowInvalidCertificates=True,
                serverSelectionTimeoutMS=30000,
                maxPoolSize=10,
            )
        return self._client
    
    def get_og_client(self) -> Optional[MongoClient]:
        """Get or create the OG MongoDB client."""
        if not config.og_mongodb_uri:
            return None
        if self._og_client is None:
            self._og_client = MongoClient(
                config.og_mongodb_uri,
                tlsAllowInvalidCertificates=True,
                serverSelectionTimeoutMS=30000,
            )
        return self._og_client
    
    def get_db(self) -> Database:
        """Get the main database."""
        if self._db is None:
            self._db = self.get_client()[config.db_name]
        return self._db
    
    def get_og_db(self) -> Optional[Database]:
        """Get the OG database."""
        if self._og_db is None and config.og_mongodb_uri:
            og_client = self.get_og_client()
            if og_client:
                self._og_db = og_client[config.og_db_name]
        return self._og_db
    
    def get_collection(self, name: str) -> Collection:
        """Get a collection from the main database."""
        return self.get_db()[name]
    
    def get_og_collection(self, name: str) -> Optional[Collection]:
        """Get a collection from the OG database."""
        og_db = self.get_og_db()
        if og_db is None:
            return None
        return og_db[name]
    
    def close(self):
        """Close all connections."""
        if self._client:
            self._client.close()
            self._client = None
            self._db = None
        if self._og_client:
            self._og_client.close()
            self._og_client = None
            self._og_db = None


# Global instance
mongo = MongoDBManager()