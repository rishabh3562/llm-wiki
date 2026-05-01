#!/usr/bin/env python3
import os
import sys

def load_env_from_wrapper(wrapper_path):
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
    return env

wrapper_path = "/opt/llm_wiki/run_one_repo_wrapper.sh"
env = load_env_from_wrapper(wrapper_path)
print("Loaded environment:")
for k, v in env.items():
    if 'MONGODB' in k or 'GITHUB' in k:
        print(f"  {k}: {v}")

# Now try to use the MONGODB_URI
if 'MONGODB_URI' in env:
    uri = env['MONGODB_URI']
    print(f"\nURI: {uri}")
    # Mask the password for display
    if ':' in uri and '@' in uri:
        # Simple masking: replace everything between : and @
        parts = uri.split('://')
        if len(parts) == 2:
            protocol = parts[0]
            rest = parts[1]
            if '@' in rest:
                auth_part, host_part = rest.split('@', 1)
                if ':' in auth_part:
                    user, _ = auth_part.split(':', 1)
                    masked_auth = f"{user}:***"
                    masked_uri = f"{protocol}://{masked_auth}@{host_part}"
                    print(f"Masked URI: {masked_uri}")
except Exception as e:
    print(f"Error: {e}")