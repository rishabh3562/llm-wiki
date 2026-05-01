#!/usr/bin/env python3
import os
from pymongo import MongoClient
from datetime import datetime, timezone

# Hardcoded values from the working system
MONGODB_URI = "mongodb+srv://dubeyrishabh108_db_user:***@cluster0.j8iafjr.mongodb.net/github_wiki?retryWrites=true&w=majority"
GITHUB_PAT = open('/root/.hermes/secrets/github_token.txt').read().strip()

def main():
    print("Connecting to MongoDB...")
    client = MongoClient(MONGODB_URI)
    db = client['github_wiki']
    
    print("Connected! Database:", db.name)
    print("Collections:", db.list_collection_names())
    
    # 1. Fix repo-queue schema inconsistencies
    print("\n=== Fixing repo-queue schema ===")
    now = datetime.now(timezone.utc).isoformat()
    
    # Standard fields we want to ensure exist
    standard_update = {
        '$set': {
            'lastUpdated': now
        },
        '$setOnInsert': {
            'status': 'pending',
            'addedAt': {'$date': '1970-01-01T00:00:00.000Z'},
            'claimedAt': None,
            'processingFinishedAt': None,
            'retryCount': 0,
            'lastError': None,
            'failedAt': None
        }
    }
    
    result = db.repo_queue.update_many({}, standard_update, upsert=False)
    print(f"Updated {result.modified_count} repo-queue documents")
    
    # 2. Enhance snippets with more metadata
    print("\n=== Enhancing snippets ===")
    snippet_update = {
        '$set': {
            'analysisDepth': 'full',
            'confidenceScore': 0.8,
            'extractedConcepts': [],
            'designPatterns': [],
            'techStack': {},
            'codeQualityIndicators': {},
            'analysisVersion': '1.0',
            'enhancedAt': now
        }
    }
    
    snippet_result = db.snippets.update_many({}, snippet_update)
    print(f"Enhanced {snippet_result.modified_count} snippet documents")
    
    # 3. Create specialized collections for concepts/patterns
    print("\n=== Creating specialized collections ===")
    collections_to_create = [
        'code_patterns',
        'architectural_decisions', 
        'tech_evolution',
        'lessons_learned',
        'design_insights'
    ]
    
    for coll_name in collections_to_create:
        coll = db[coll_name]
        # Create collection if empty by adding and removing a dummy doc
        if coll.count_documents({}) == 0:
            dummy_id = coll.insert_one({
                '_init': True,
                'createdAt': now,
                'description': f'Collection for {coll_name}'
            }).inserted_id
            coll.delete_one({'_id': dummy_id})
            print(f"Created collection: {coll_name}")
        else:
            print(f"Collection exists: {coll_name} ({coll.count_documents({})} docs)")
    
    # 4. Verification
    print("\n=== Verification ===")
    pending = db.repo_queue.count_documents({'status': 'pending'})
    processing = db.repo_queue.count_documents({'status': 'processing'})
    done = db.repo_queue.count_documents({'status': 'done'})
    print(f"Repo queue: {pending} pending, {processing} processing, {done} done")
    
    snippet_count = db.snippets.count_documents({})
    print(f"Total snippets: {snippet_count}")
    
    # Show sample
    sample = db.snippets.find_one()
    if sample:
        print(f"Sample snippet keys: {[k for k in sample.keys() if not k.startswith('_')][:8]}")
    
    print("\n✓ Schema fixes completed successfully!")

if __name__ == '__main__':
    main()