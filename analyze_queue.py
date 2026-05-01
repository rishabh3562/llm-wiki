import os
from pymongo import MongoClient
from datetime import datetime, timezone

MONGODB_URI = os.environ.get("MONGODB_URI")
if not MONGODB_URI:
    wrapper_path = "/opt/llm_wiki/run_one_repo_wrapper.sh"
    if os.path.exists(wrapper_path):
        with open(wrapper_path) as f:
            for line in f:
                if line.startswith("export MONGODB_URI="):
                    MONGODB_URI = line.split('=', 1)[1].strip().strip('"')
                    break
if not MONGODB_URI:
    raise ValueError("MONGODB_URI not set")

client = MongoClient(MONGODB_URI)
db = client["github_wiki"]
coll = db["repo_queue"]

print("=== Queue Analysis ===")
total = coll.count_documents({})
print(f"Total documents: {total}")

status_counts = {}
for status in ["pending", "processing", "done", "failed"]:
    count = coll.count_documents({"status": status})
    status_counts[status] = count
    print(f"{status}: {count}")

# Look at done items to see processing times
print("\n=== Completed Jobs (done) ===")
done_cursor = coll.find({"status": "done"}, {"claimed_at": 1, "finished_at": 1, "repo_name": 1, "last_error": 1})
done_list = list(done_cursor)
if done_list:
    processing_times = []
    for doc in done_list:
        claimed = doc.get("claimed_at")
        finished = doc.get("finished_at")
        if claimed and finished:
            try:
                # Assuming stored as string or datetime
                if isinstance(claimed, str):
                    claimed_dt = datetime.fromisoformat(claimed.replace('Z', '+00:00'))
                else:
                    claimed_dt = claimed
                if isinstance(finished, str):
                    finished_dt = datetime.fromisoformat(finished.replace('Z', '+00:00'))
                else:
                    finished_dt = finished
                delta = (finished_dt - claimed_dt).total_seconds()
                processing_times.append(delta)
            except Exception as e:
                pass
    if processing_times:
        avg_time = sum(processing_times) / len(processing_times)
        min_time = min(processing_times)
        max_time = max(processing_times)
        print(f"Average processing time: {avg_time:.2f} seconds")
        print(f"Min: {min_time:.2f}s, Max: {max_time:.2f}s")
        print(f"Based on {len(processing_times)} completed jobs with timestamps")
    else:
        print("No valid timestamp pairs found for done jobs.")
else:
    print("No done jobs found.")

# Look at failed items
print("\n=== Failed Jobs ===")
failed_cursor = coll.find({"status": "failed"}, {"repo_name": 1, "last_error": 1, "claimed_at": 1, "finished_at": 1})
failed_list = list(failed_cursor)
if failed_list:
    print(f"Found {len(failed_list)} failed jobs:")
    for doc in failed_list[:5]:  # show first 5
        repo = doc.get("repo_name", "unknown")
        error = doc.get("last_error", "no error")
        print(f"  - {repo}: {error[:100]}...")
else:
    print("No failed jobs found.")

# Look at pending items that have been claimed (stuck processing?)
print("\n=== Pending Jobs (may be stuck) ===")
pending_cursor = coll.find({"status": "pending"}, {"repo_name": 1, "claimed_at": 1})
pending_list = list(pending_cursor)
if pending_list:
    stuck = []
    now = datetime.now(timezone.utc)
    for doc in pending_list:
        claimed = doc.get("claimed_at")
        if claimed:
            try:
                if isinstance(claimed, str):
                    claimed_dt = datetime.fromisoformat(claimed.replace('Z', '+00:00'))
                else:
                    claimed_dt = claimed
                if (now - claimed_dt).total_seconds() > 3600:  # more than an hour
                    stuck.append(doc)
            except:
                pass
    if stuck:
        print(f"Found {len(stuck)} pending jobs claimed over 1 hour ago (possibly stuck):")
        for doc in stuck[:5]:
            repo = doc.get("repo_name", "unknown")
            claimed = doc.get("claimed_at")
            print(f"  - {repo}: claimed at {claimed}")
    else:
        print("No pending jobs stuck >1 hour.")
else:
    print("No pending jobs.")

client.close()
