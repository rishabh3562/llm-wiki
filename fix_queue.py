import os
import sys
from pymongo import MongoClient

# Load environment from wrapper if needed
MONGODB_URI = os.environ.get('MONGODB_URI')
if not MONGODB_URI:
    wrapper_path = '/opt/llm_wiki/run_one_repo_wrapper.sh'
    if os.path.exists(wrapper_path):
        with open(wrapper_path) as f:
            for line in f:
                if line.startswith('export MONGODB_URI='):
                    MONGODB_URI = line.split('=', 1)[1].strip().strip('\\\"')
                    break
if not MONGODB_URI:
    print('MONGODB_URI not found')
    sys.exit(1)

print(f'Connecting to MongoDB...')
client = MongoClient(MONGODB_URI)
db = client['github_wiki']
coll = db['repo_queue']

# Find all documents where repo_name is null
print('Finding documents with repo_name null...')
cursor = coll.find({'repo_name': None})
docs = list(cursor)
print(f'Found {len(docs)} documents with repo_name null')

# Update each one
updated = 0
for doc in docs:
    repo_name = doc['_id']
    # Print the update we're about to make
    update_doc = {'$set': {'repo_name': repo_name}}
    print(f'Updating _id: {doc["_id"]} with {update_doc}')
    try:
        result = coll.update_one({'_id': doc['_id']}, update_doc)
        print(f'  Result: matched={result.matched_count}, modified={result.modified_count}')
        if result.modified_count == 1:
            updated += 1
        elif result.matched_count == 0:
            print(f'  WARNING: No document matched for _id: {doc["_id"]}')
    except Exception as e:
        print(f'  ERROR updating {doc["_id"]}: {e}')
        print(f'  Update doc was: {update_doc}')
        import traceback
        traceback.print_exc()

print(f'\\nSuccessfully updated {updated} documents')

# Verify
pending = coll.count_documents({'status': 'pending'})
processing = coll.count_documents({'status': 'processing'})
failed = coll.count_documents({'status': 'failed'})
print(f'\\nQueue - Pending: {pending}, Processing: {processing}, Failed: {failed}')

# Show first 5 pending repos with their repo_name
print('\\nFirst 5 pending repos:')
for doc in coll.find({'status': 'pending'}, {'repo_name': 1, '_id': 0}).limit(5):
    print(f'  - {doc.get("repo_name")}')

client.close()