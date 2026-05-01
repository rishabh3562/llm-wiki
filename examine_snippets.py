#!/usr/bin/env python3
import json
from pymongo import MongoClient
from datetime import datetime, timezone

# Configuration (same as in run_llm_wiki.py)
MONGO_URI = "mongodb+srv://dubeyrishabh108_db_user:***@cluster0.j8iafjr.mongodb.net/github_wiki?retryWrites=true&w=majority"
MONGO_DB = "github_wiki"
MONGO_COLLECTION = "snippets"

def examine_snippets():
    client = MongoClient(MONGO_URI, tlsAllowInvalidCertificates=True, serverSelectionTimeoutMS=5000)
    try:
        db = client[MONGO_DB]
        collection = db[MONGO_COLLECTION]
        
        # Get total count
        total_count = collection.count_documents({})
        print(f"Total snippets in MongoDB: {total_count}")
        
        # Get recent snippets (last 20)
        recent_snippets = list(collection.find().sort([("timestamp", -1)]).limit(20))
        
        print("\n=== Examining Recent Snippets for Depth, Actionability, and Consistency ===\n")
        
        for i, snippet in enumerate(recent_snippets, 1):
            print(f"--- Snippet {i} ---")
            print(f"Repo: {snippet.get('repo', 'N/A')}")
            print(f"File: {snippet.get('file_path', 'N/A')}")
            print(f"Tags: {snippet.get('tags', [])}")
            print(f"Timestamp: {snippet.get('timestamp', 'N/A')}")
            
            content = snippet.get('content', '')
            print(f"Content length: {len(content)} characters")
            
            # Show first 300 chars of content
            preview = content[:300] + ("..." if len(content) > 300 else "")
            print(f"Preview: {preview}")
            
            # Analyze depth
            depth_indicators = [
                "analysis" in content.lower(),
                "insight" in content.lower(),
                "recommendation" in content.lower(),
                "pattern" in content.lower(),
                "architecture" in content.lower(),
                "intent" in content.lower(),
                "#" in content,  # Markdown headers
                len(content) > 500,  # Substantial content
            ]
            depth_score = sum(depth_indicators)
            print(f"Depth indicators: {depth_score}/8")
            
            # Analyze actionability
            action_indicators = [
                "should" in content.lower(),
                "recommend" in content.lower(),
                "fix" in content.lower(),
                "improve" in content.lower(),
                "add" in content.lower(),
                "implement" in content.lower(),
                "refactor" in content.lower(),
                "consider" in content.lower(),
                "```" in content,  # Code blocks
                "-" in content or "*" in content,  # Lists
            ]
            action_score = sum(action_indicators)
            print(f"Actionability indicators: {action_score}/10")
            
            # Consistency checks
            has_structure = (
                snippet.get('repo') and 
                snippet.get('file_path') and 
                snippet.get('content_hash') and
                snippet.get('timestamp')
            )
            print(f"Has basic structure: {has_structure}")
            
            print()  # Empty line between snippets
            
        # Overall statistics
        print("=== Overall Statistics ===")
        
        # Check for common issues
        pipeline = [
            {"$group": {
                "_id": "$repo",
                "count": {"$sum": 1},
                "avg_length": {"$avg": {"$strLenCP": "$content"}},
                "unique_tags": {"$addToSet": "$tags"}
            }},
            {"$sort": {"count": -1}}
        ]
        
        repo_stats = list(collection.aggregate(pipeline))
        print(f"Number of repos with snippets: {len(repo_stats)}")
        
        if repo_stats:
            print("\nTop 5 repos by snippet count:")
            for stat in repo_stats[:5]:
                print(f"  {stat['_id']}: {stat['count']} snippets, avg length: {int(stat['avg_length'])} chars")
        
        # Check tag consistency
        all_tags = []
        for snippet in collection.find({}, {"tags": 1}):
            all_tags.extend(snippet.get('tags', []))
        
        from collections import Counter
        tag_counts = Counter(all_tags)
        print(f"\nTotal unique tags: {len(tag_counts)}")
        print("Most common tags:")
        for tag, count in tag_counts.most_common(10):
            print(f"  {tag}: {count}")
            
    except Exception as e:
        print(f"Error examining snippets: {e}")
    finally:
        client.close()

if __name__ == "__main__":
    examine_snippets()