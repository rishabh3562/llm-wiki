#!/usr/bin/env python3
import os, sys, json, hashlib, uuid, subprocess, re, math
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from pymongo import MongoClient, errors as mongo_errors

# Import retry utilities and initialize runtime context
sys.path.append('/opt/llm_wiki')
from retry_utils import retry_mongodb, retry_github_api, retry_subprocess

MONGODB_URI = os.environ["MONGODB_URI"]
GITHUB_PAT = os.environ["GITHUB_PAT"]
GITHUB_USER = os.environ.get("GITHUB_USER", "rishabh3562")
REPOS_DIR = Path("/repos")
OUTPUT_DIR = Path("/opt/llm_wiki/output")
VAULT_DIR = Path("/opt/llm_wiki/obsidian-vault/github-wiki")
MODEL_NAME = os.environ.get("AGENT_MODEL", "unknown")

client = MongoClient(MONGODB_URI)
db = client["github_wiki"]

CODE_EXTS = {
    ".py", ".js", ".jsx", ".ts", ".tsx", ".mjs", ".cjs",
    ".java", ".kt", ".kts", ".go", ".rb", ".rs", ".php",
    ".cs", ".cpp", ".cc", ".cxx", ".c", ".h", ".hpp",
    ".swift", ".m", ".mm", ".scala", ".sh", ".bash",
    ".json", ".yml", ".yaml", ".toml", ".xml", ".sql"
}

CORE_NOTE_TYPES = {
    "intent_recovery", "static_analysis", "architecture",
    "patterns", "improvements", "self_portrait"
}


def slugify(text):
    text = re.sub(r"[^a-zA-Z0-9]+", "-", text.lower()).strip("-")
    return text or "note"


def note_label(analysis_type):
    labels = {
        "intent_recovery": "Intent & Archaeology",
        "static_analysis": "Static Analysis",
        "architecture": "Architecture",
        "patterns": "Patterns",
        "improvements": "Improvements",
        "self_portrait": "Self Portrait",
    }
    return labels.get(analysis_type, analysis_type.replace("_", " ").title())


def note_role_for(analysis_type):
    return "core" if analysis_type in CORE_NOTE_TYPES else "dynamic"


def collect_repo_metrics(repo_path, smells):
    files = []
    code_files = []
    top_level_dirs = Counter()
    ext_counts = Counter()
    largest_files = []

    for p in repo_path.rglob("*"):
        if not p.is_file() or ".git" in p.parts:
            continue
        files.append(p)
        if p.suffix.lower() in CODE_EXTS:
            code_files.append(p)
            ext_counts[p.suffix.lower() or "[no_ext]"] += 1
            rel = p.relative_to(repo_path)
            top_level = rel.parts[0] if len(rel.parts) > 1 else "[root]"
            top_level_dirs[top_level] += 1

    largest_files = sorted(
        [p for p in code_files],
        key=lambda p: p.stat().st_size,
        reverse=True,
    )[:12]

    loc = 0
    for p in code_files[:600]:
        try:
            with p.open("r", encoding="utf-8", errors="ignore") as fh:
                loc += sum(1 for _ in fh)
        except Exception:
            continue

    def nonempty_lines(text):
        return sum(1 for line in text.splitlines() if line.strip())

    return {
        "total_files": len(files),
        "code_files": len(code_files),
        "loc": loc,
        "top_level_dir_count": len(top_level_dirs),
        "top_level_dirs": [{"name": name, "count": count} for name, count in top_level_dirs.most_common(30)],
        "languages": [{"ext": ext, "count": count} for ext, count in ext_counts.most_common(12)],
        "largest_files": [
            {"path": str(p.relative_to(repo_path)), "size": p.stat().st_size}
            for p in largest_files
        ],
        "smell_density": {
            "complexity_lines": nonempty_lines(smells.get("complexity", "")),
            "dead_code_lines": nonempty_lines(smells.get("dead_code", "")),
            "churn_lines": nonempty_lines(smells.get("high_churn_files", "")),
        },
    }


def compute_note_target(metrics):
    base = 6
    extra = 0
    extra += math.ceil(metrics["code_files"] / 5)
    extra += math.ceil(metrics["loc"] / 1000)
    extra += math.ceil(metrics["top_level_dir_count"])
    extra += math.ceil(len(metrics["largest_files"]) / 3)
    extra += math.ceil(metrics["total_files"] / 20)
    target = base + extra
    return max(6, target)


def sha256(text):
    return hashlib.sha256(text.encode()).hexdigest()

def now_iso():
    return datetime.now(timezone.utc).isoformat()

def today():
    return datetime.now().strftime('%Y-%m-%d')

def git_read(repo_path, *args):
    write_ops = {"add","commit","push","checkout","merge","rebase","rm","branch"}
    if args[0] in write_ops:
        raise PermissionError(f"RED LINE VIOLATION: git {args[0]} is forbidden")
    r = subprocess.run(["git",*args], cwd=repo_path, capture_output=True, text=True)
    return r.stdout.strip()

def redact(text):
    return re.sub(r'[A-Za-z0-9_\-]{20,}', '[REDACTED]', text)

@retry_github_api(max_retries=3, base_delay=1.0)
def fetch_all_repos():
    import requests
    from pathlib import Path
    repos, page = [], 1
    headers = {"Authorization": f"token {GITHUB_PAT}"}
    while True:
        try:
            r = requests.get(
                "https://api.github.com/user/repos",
                headers=headers,
                params={"per_page": 100, "page": page, "type": "all"},
                timeout=30,
            )
            r.raise_for_status()
            data = r.json()
            if not data or "message" in data:
                break
            repos.extend(data)
            if len(data) < 100:
                break
            page += 1
        except Exception as e:
            print(f"⚠️  GitHub discovery failed ({e}); falling back to cached /opt/llm_wiki/repos.json")
            cache_path = Path("/opt/llm_wiki/repos.json")
            if cache_path.exists():
                try:
                    cached = json.loads(cache_path.read_text())
                    return sorted(cached, key=lambda x: x["name"].lower())
                except Exception as cache_err:
                    print(f"⚠️  Cached repos.json unreadable: {cache_err}")
            break
    return sorted(repos, key=lambda x: x["name"].lower())

@retry_mongodb(max_retries=3, base_delay=1.0)
def get_next_repo(all_repos):
    done = {d["repo"] for d in db.repo_status.find(
        {"initial_analysis_done": True}, {"repo":1})}
    for r in all_repos:
        if r["name"] not in done:
            return r
    return None

def prepare_repo(repo):
    path = REPOS_DIR / repo["name"]
    url = repo.get("ssh_url") or f"git@github.com:{GITHUB_USER}/{repo['name']}.git"
    if not path.exists():
        subprocess.run(["git","clone",url,str(path)], check=True)
    else:
        subprocess.run(["git","fetch","origin"], cwd=path)
        subprocess.run(["git","reset","--hard","origin/HEAD"], cwd=path)
    return path

def phase_archaeology(repo_path, repo_name):
    log   = git_read(repo_path,"log","--pretty=format:%h %ad %s (%an)","--date=short","--reverse")
    first = git_read(repo_path,"log","--reverse","--pretty=format:%ad","--date=short").split("\n")[0]
    last  = git_read(repo_path,"log","-1","--pretty=format:%ad","--date=short")
    count = git_read(repo_path,"rev-list","--count","HEAD")
    return f"""# Intent Recovery — {repo_name}

## Timeline
- First commit: {first}
- Last commit: {last}
- Total commits: {count}

## Full Commit Log

{log[:3000]}
## Questions To Answer
- What problem was this solving?
- What was the original architecture?
- When did maintenance drop off and why?
- What did I know when I built this?
- Why did I stop?
"""

def phase_static(repo_path):
    def run(cmd):
        r = subprocess.run(cmd, cwd=repo_path, capture_output=True, text=True, shell=True)
        return r.stdout[:2000]
    return {
        "largest_files":     run("find . -type f -not -path './.git/*' | xargs ls -la 2>/dev/null | sort -k5 -rn | head -20"),
        "high_churn_files":  run("git log --pretty=format: --name-only | sort | uniq -c | sort -rn | head -20"),
        "complexity":        run("radon cc . -s -a 2>/dev/null | head -30") or "N/A (not a Python repo or radon not installed)",
        "dead_code":         run("vulture . 2>/dev/null | head -20") or "N/A"
    }

def phase_insights(repo_name, archaeology, smells):
    arch = f"""# Architecture — {repo_name}

## Key Files (by size)

{smells['largest_files'][:600]}
## High Churn Files
{smells['high_churn_files'][:600]}
## Complexity
{smells['complexity'][:600]}
"""
    patterns = f"""# Patterns — {repo_name}

## File Organization Pattern
*Derived from directory structure and churn data*

## Commit Style
*Derived from commit message analysis in archaeology phase*
"""
    improvements = f"""# Improvements — {repo_name}

## Dead Code
{smells['dead_code'][:600]}
## High Complexity Areas
{smells['complexity'][:600]}
"""
    self_portrait = f"""# Self Portrait — {repo_name}

## Snapshot from commit history
{archaeology[:400]}

## What I Knew Then
*Inferred from tech stack and patterns*

## What I Would Do Differently Now
*Inferred from code smells*
"""
    return {"architecture": arch, "patterns": patterns,
            "improvements": improvements, "self_portrait": self_portrait}


def build_dynamic_notes(repo_name, commit_sha, archaeology, smells, metrics, target_total):
    dynamic_slots = max(0, target_total - 6)
    candidates = []

    for item in metrics["top_level_dirs"]:
        if item["name"] == "[root]":
            continue
        candidates.append((
            f"module_{slugify(item['name'])}",
            f"Module — {item['name']}",
            f"""# Module — {item['name']}\n\n## Why it matters\nThis directory appears {item['count']} times in the repository tree.\n\n## Repository map\n- Related core note: [[{repo_name}-architecture]]\n- Patterns: [[{repo_name}-patterns]]\n- Improvements: [[{repo_name}-improvements]]\n\n## Signals\n- Top-level directory count: {metrics['top_level_dir_count']}\n- Total code files: {metrics['code_files']}\n- Approx LOC sampled: {metrics['loc']}\n""",
            {
                "note_kind": "module",
                "focus": item["name"],
                "signal": "top_level_dir",
                "signal_count": item["count"],
            }
        ))

    for item in metrics["largest_files"]:
        stem = Path(item["path"]).stem
        candidates.append((
            f"hotspot_{slugify(stem)}",
            f"Hotspot — {item['path']}",
            f"""# Hotspot — {item['path']}\n\n## Why it matters\nThis is one of the largest code files in the repository.\n\n## File details\n- Size: {item['size']} bytes\n- Related core note: [[{repo_name}-architecture]]\n- Related patterns: [[{repo_name}-patterns]]\n\n## Reading guide\nUse this note to inspect implementation density, likely responsibilities, and refactor opportunities.\n""",
            {
                "note_kind": "hotspot",
                "focus": item["path"],
                "signal": "largest_file",
                "signal_count": item["size"],
            }
        ))

    for item in metrics["languages"]:
        ext = item["ext"].lstrip(".") or "no_ext"
        candidates.append((
            f"language_{slugify(ext)}",
            f"Language — {ext}",
            f"""# Language — {ext}\n\n## Why it matters\nThis repository uses {item['count']} files with the {ext} extension.\n\n## Signals\n- Related core note: [[{repo_name}-architecture]]\n- Patterns: [[{repo_name}-patterns]]\n- Self portrait: [[{repo_name}-self_portrait]]\n""",
            {
                "note_kind": "language",
                "focus": ext,
                "signal": "file_extension",
                "signal_count": item["count"],
            }
        ))

    if metrics["smell_density"]["complexity_lines"]:
        candidates.append((
            "quality_complexity",
            "Quality — Complexity Signals",
            f"""# Quality — Complexity Signals\n\n## Evidence\n{smells['complexity'][:1200]}\n\n## Related\n- [[{repo_name}-improvements]]\n- [[{repo_name}-architecture]]\n""",
            {"note_kind": "quality", "signal": "complexity", "signal_count": metrics["smell_density"]["complexity_lines"]}
        ))

    selected = []
    seen = set()
    for analysis_type, title, content, meta in candidates:
        if analysis_type in seen:
            continue
        seen.add(analysis_type)
        selected.append((analysis_type, title, content, meta))
        if len(selected) >= dynamic_slots:
            break

    return selected


@retry_mongodb(max_retries=3, base_delay=1.0)
def store_mongodb(repo_name, commit_sha, analysis_type, content, session_id, run_id, extra_meta=None):
    safe_content = redact(content)
    meta = extra_meta or {}
    doc = {
        "repo": repo_name,
        "commit_sha": commit_sha,
        "branch": "main",
        "file_path": f"output/{repo_name}/{analysis_type}.md",
        "analysis_type": analysis_type,
        "note_role": meta.get("note_role", note_role_for(analysis_type)),
        "content": safe_content,
        "content_hash": sha256(safe_content),
        "generated_by": {
            "agent": "openclaw",
            "model": MODEL_NAME,
            "prompt_template": "initial_analysis_v1"
        },
        "trigger": {
            "type": "cron",
            "cron_schedule": "0 */3 * * *",
            "triggered_by": "system",
            "triggered_at": now_iso()
        },
        "run_id": run_id,
        "session_id": session_id,
        "created_at": now_iso(),
        "tags": [analysis_type, repo_name],
        "word_count": len(safe_content.split()),
        "is_empty": len(safe_content.split()) < 50,
        "analysis_depth": meta.get("analysis_depth"),
        "quality_tier": meta.get("quality_tier"),
        "repo_metrics": meta.get("repo_metrics"),
        "code_patterns": meta.get("code_patterns", []),
        "code_smells": meta.get("code_smells", []),
        "provenance": meta.get("provenance", {}),
    }
    try:
        db.snippets.insert_one(doc)
        return True
    except mongo_errors.DuplicateKeyError:
        print(f"  SKIP duplicate: {analysis_type}")
        return False


def store_obsidian(repo_name, commit_sha, analysis_type, content):
    path = VAULT_DIR / repo_name
    path.mkdir(parents=True, exist_ok=True)
    fm = f"""---
repo: {repo_name}
type: {analysis_type}
commit: {commit_sha}
date: {today()}
tags: [{repo_name}, {analysis_type}]
related: [[{repo_name}-index]]
---

"""
    (path / f"{repo_name}-{analysis_type}.md").write_text(fm + content)


def write_index(repo_name, commit_sha, excerpt, dynamic_notes=None):
    path = VAULT_DIR / repo_name
    path.mkdir(parents=True, exist_ok=True)
    note_lines = [
        f"- [[{repo_name}-intent_recovery|Intent & Archaeology]]",
        f"- [[{repo_name}-architecture|Architecture]]",
        f"- [[{repo_name}-patterns|Patterns]]",
        f"- [[{repo_name}-improvements|Improvements]]",
        f"- [[{repo_name}-self_portrait|Self Portrait]]",
    ]
    for analysis_type, title, _content, _meta in (dynamic_notes or []):
        note_lines.append(f"- [[{repo_name}-{analysis_type}|{title}]]")
    content = f"""---
repo: {repo_name}
type: index
commit: {commit_sha}
date: {today()}
tags: [{repo_name}, index]
---

# {repo_name} — Index

## What This Repo Is
{excerpt[:400]}

## Notes
{chr(10).join(note_lines)}
"""
    (path / f"{repo_name}-index.md").write_text(content)

def main():
    session_id = str(uuid.uuid4())
    print(f"\n{'='*60}\nSession: {session_id}\nStarted: {now_iso()}\n{'='*60}")

    all_repos = fetch_all_repos()
    total = len(all_repos)
    print(f"Total repos on GitHub: {total}")

    repo = get_next_repo(all_repos)
    if not repo:
        print("ALL REPOS ANALYZED. Nothing to do.")
        return

    repo_name = repo["name"]
    print(f"Next repo: {repo_name}")

    repo_path = prepare_repo(repo)
    commit_sha = git_read(repo_path, "rev-parse", "HEAD")
    run_id = sha256(repo_name + commit_sha + today())
    print(f"HEAD: {commit_sha} | Run ID: {run_id[:12]}...")

    (OUTPUT_DIR / repo_name).mkdir(parents=True, exist_ok=True)

    print("\n[1/5] Archaeology...")
    archaeology = phase_archaeology(repo_path, repo_name)

    print("[2/5] Static analysis...")
    smells = phase_static(repo_path)

    metrics = collect_repo_metrics(repo_path, smells)
    target_notes = compute_note_target(metrics)
    dynamic_notes = build_dynamic_notes(repo_name, commit_sha, archaeology, smells, metrics, target_notes)

    print(f"[3/5] Generating insights and dynamic notes... target={target_notes}")
    insights = phase_insights(repo_name, archaeology, smells)

    print("[4/5] Storing to MongoDB + Obsidian...")
    inserted = skipped = 0
    all_outputs = {
        "intent_recovery": archaeology,
        "static_analysis": json.dumps(smells, indent=2),
        **insights,
    }

    for atype, content in all_outputs.items():
        quality_tier = "strong" if atype in {"intent_recovery", "architecture", "patterns", "improvements", "self_portrait"} else "medium"
        meta = {
            "note_role": note_role_for(atype),
            "analysis_depth": "core",
            "quality_tier": quality_tier,
            "repo_metrics": metrics,
            "code_patterns": [],
            "code_smells": [],
            "provenance": {"source": "core_pipeline", "note_type": atype},
        }
        ok = store_mongodb(repo_name, commit_sha, atype, content, session_id, run_id, meta)
        if ok:
            inserted += 1
            store_obsidian(repo_name, commit_sha, atype, content)
        else:
            skipped += 1

    for atype, title, content, dyn_meta in dynamic_notes:
        meta = {
            "note_role": "dynamic",
            "analysis_depth": "expanded",
            "quality_tier": "good" if dyn_meta.get("signal_count", 0) else "weak",
            "repo_metrics": metrics,
            "code_patterns": [{"name": dyn_meta.get("signal"), "category": dyn_meta.get("note_kind"), "confidence": 0.62, "evidence": dyn_meta.get("focus"), "scope": "repo"}],
            "code_smells": [],
            "provenance": {"source": "dynamic_note_builder", "title": title, "signal": dyn_meta.get("signal")},
        }
        ok = store_mongodb(repo_name, commit_sha, atype, content, session_id, run_id, meta)
        if ok:
            inserted += 1
            store_obsidian(repo_name, commit_sha, atype, content)
        else:
            skipped += 1

    write_index(repo_name, commit_sha, archaeology[:400], dynamic_notes=dynamic_notes)

    print("[5/5] Marking complete...")

    @retry_mongodb(max_retries=3, base_delay=1.0)
    def update_repo_status():
        db.repo_status.update_one({"repo": repo_name}, {"$set": {
            "repo": repo_name,
            "initial_analysis_done": True,
            "initial_analysis_commit": commit_sha,
            "initial_analysis_date": today(),
            "session_id": session_id,
            "ready_for_diff_tracking": False,
            "snippets_inserted": inserted,
            "snippets_skipped": skipped,
            "vault_note_target": target_notes,
            "completed_at": now_iso()
        }}, upsert=True)

    update_repo_status()

    @retry_mongodb(max_retries=3, base_delay=1.0)
    def update_analysis_runs():
        db.analysis_runs.update_one({"run_id": run_id}, {"$set": {
            "run_id": run_id,
            "session_id": session_id,
            "repo": repo_name,
            "commit_sha": commit_sha,
            "trigger_type": "cron",
            "model_used": MODEL_NAME,
            "snippets_inserted": inserted,
            "snippets_skipped": skipped,
            "vault_note_target": target_notes,
            "status": "completed",
            "completed_at": now_iso()
        }}, upsert=True)

    update_analysis_runs()

    done = db.repo_status.count_documents({"initial_analysis_done": True})
    print(f"\n{'='*60}")
    print(f"DONE: {repo_name}")
    print(f"Inserted: {inserted} | Skipped: {skipped}")
    print(f"Vault notes target: {target_notes} (core + dynamic)")
    print(f"Progress: {done}/{total} ({total - done} remaining)")
    print(f"{'='*60}\n")

if __name__ == "__main__":
    main()