import os, json, requests, sys
from pymongo import MongoClient
MONGODB_URI = os.environ["MONGODB_URI"]
GITHUB_PAT = os.environ["GITHUB_PAT"]
GITHUB_USER = os.environ.get("GITHUB_USER", "rishabh3562")
client = MongoClient(MONGODB_URI)
db = client["github_wiki"]
coll = db["repo_queue"]
headers = {"Authorization": f"token {GITHUB_PAT}"}
repos = []
page = 1
while True:
    r = requests.get(f"https://api.github.com/users/{GITHUB_USER}/repos", headers=headers, params={"per_page":100,"page":page})
    if r.status_code != 200:
        print("Failed to fetch repos:", r.status_code, r.text)
        break
    data = r.json()
    if not data:
        break
    for repo in data:
        repos.append(repo["name"])
    if len(data) < 100:
        break
    page += 1
print(f"Found {len(repos)} repos")
for name in repos:
    coll.update_one({"_id": name}, {"$setOnInsert": {"_id": name, "status": "pending", "addedAt": {"$date": {"$numberLong": "0"}}}}, upsert=True)
print("Queue populated.")