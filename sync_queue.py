from pymongo import MongoClient
import os

# Load environment
MONGODB_URI = os.environ.get('MONGODB_URI')
if not MONGODB_URI:
    wrapper = '/opt/llm_wiki/run_one_repo_wrapper.sh'
    if os.path.exists(wrapper):
        with open(wrapper) as f:
            for line in f:
                if line.startswith('export MONGODB_URI='):
                    MONGODB_URI = line.split('=', 1)[1].strip()
                    # Remove surrounding quotes
                    if (MONGODB_URI.startswith('"') and MONGODB_URI.endswith('"')) or \
                       (MONGODB_URI.startswith("'") and MONGODB_URI.endswith("'")):
                        MONGODB_URI = MONGODB_URI[1:-1]
                    break
if not MONGODB_URI:
    print("ERROR: MONGODB_URI not set")
    exit(1)

print(f"Connecting to MongoDB...")
client = MongoClient(MONGODB_URI)
db = client['github_wiki']

# Get repos that have initial_analysis_done = True
print("Fetching repos with initial_analysis_done = True...")
done_repos = set()
for doc in db.repo_status.find({'initial_analysis_done': True}, {'repo': 1}):
    done_repos.add(doc['repo'])
print(f"Found {len(done_repos)} repos with initial_analysis_done")

# Update repo_queue: set status to done for these repos
queue = db['repo_queue']
updated = 0
for repo_name in done_repos:
    result = queue.update_one({'repo_name': repo_name}, {'$set': {'status': 'done'}})
    if result.modified_count == 1:
        updated += 1
        print(f"  Updated {repo_name} to done")
    elif result.matched_count == 0:
        print(f"  WARNING: {repo_name} not found in queue")

print(f"\nUpdated {updated} documents in queue to 'done'")

# Get counts
pending = queue.count_documents({'status': 'pending'})
processing = queue.count_documents({'status': 'processing'})
done = queue.count_documents({'status': 'done'})
failed = queue.count_documents({'status': 'failed'})
print(f"\nQueue status after update:")
print(f"  Pending: {pending}")
print(f"  Processing: {processing}")
print(f"  Done: {done}")
print(f"  Failed: {failed}")

# Show first 5 pending repos
if pending > 0:
    print(f"\nFirst 5 pending repos:")
    for doc in queue.find({'status': 'pending'}).limit(5):
        print(f"  - {doc['repo_name']}")
else:
    print("\nNo pending repos!")

client.close()