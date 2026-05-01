import os
import sys
import requests

# Load environment from wrapper
wrapper_path = '/opt/llm_wiki/run_one_repo_wrapper.sh'
env = {}
if os.path.exists(wrapper_path):
    with open(wrapper_path) as f:
        for line in f:
            line = line.strip()
            if line.startswith('export ') and '=' in line:
                line = line[7:]  # remove 'export '
                key, value = line.split('=', 1)
                # Remove surrounding quotes if present
                if len(value) >= 2:
                    if (value.startswith('"') and value.endswith('"')) or \
                       (value.startswith("'") and value.endswith("'")):
                        value = value[1:-1]
                env[key] = value
os.environ.update(env)

print("MONGODB_URI set:", bool(os.environ.get('MONGODB_URI')))
print("GITHUB_PAT set:", bool(os.environ.get('GITHUB_PAT')))

if os.environ.get('GITHUB_PAT'):
    token = os.environ['GITHUB_PAT']
    print(f"Token length: {len(token)}")
    headers = {"Authorization": f"token {token}"}
    try:
        r = requests.get("https://api.github.com/user/repos", 
                         headers=headers, 
                         params={"per_page": 5, "page": 1, "type": "all"},
                         timeout=10)
        print(f"Status code: {r.status_code}")
        if r.status_code == 200:
            data = r.json()
            print(f"Number of repos: {len(data)}")
            if data:
                print("First repo:", data[0].get('name'))
                print("Full first repo:", data[0])
            else:
                print("No repos returned. Checking response:", data)
        else:
            print(f"Error response: {r.text}")
    except Exception as e:
        print(f"Exception: {e}")
else:
    print("GITHUB_PAT not set")