#!/usr/bin/env python3
import os
from datetime import datetime, timezone, timedelta
from pymongo import MongoClient

# Load environment (same as primary script)
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

def analyze_recent_quality(hours=24):
    """Analyze the quality of analyses completed in the last N hours."""
    try:
        client = MongoClient(MONGODB_URI)
        db = client["github_wiki"]
        snippets_coll = db["snippets"]
        queue_coll = db["repo_queue"]
        
        # Time threshold
        since = datetime.now(timezone.utc) - timedelta(hours=hours)
        
        # Find snippets from recent analyses (we'll use repo_queue to get recently completed repos)
        recent_done = list(queue_coll.find(
            {
                "status": "done",
                "finished_at": {"$exists": True, "$gte": since}
            },
            {"_id": 1, "finished_at": 1}
        ).sort("finished_at", -1))
        
        if not recent_done:
            client.close()
            return {"status": "no_recent_completions", "count": 0}
        
        # Get the repo names from the _id field (which is the repo name)
        repo_names = [r["_id"] for r in recent_done]
        
        # Get snippets for these repos
        recent_snippets = list(snippets_coll.find(
            {"repo": {"$in": repo_names}},
            {"repo": 1, "analysis_type": 1, "content": 1, "extractedConcepts": 1, "designPatterns": 1}
        ))
        
        client.close()
        
        # Analyze by analysis type
        type_stats = {}
        for snippet in recent_snippets:
            a_type = snippet.get("analysis_type", "unknown")
            content = snippet.get("content", "")
            concepts = snippet.get("extractedConcepts", [])
            patterns = snippet.get("designPatterns", [])
            
            if a_type not in type_stats:
                type_stats[a_type] = {
                    "count": 0,
                    "total_content_length": 0,
                    "total_concepts": 0,
                    "total_patterns": 0,
                    "empty_content": 0
                }
            
            stats = type_stats[a_type]
            stats["count"] += 1
            stats["total_content_length"] += len(content)
            stats["total_concepts"] += len(concepts) if isinstance(concepts, list) else 0
            stats["total_patterns"] += len(patterns) if isinstance(patterns, list) else 0
            if len(content.strip()) < 50:  # Arbitrary threshold for "too short"
                stats["empty_content"] += 1
        
        # Calculate averages and flag issues
        insights = []
        for a_type, stats in type_stats.items():
            if stats["count"] == 0:
                continue
               
            avg_length = stats["total_content_length"] / stats["count"]
            avg_concepts = stats["total_concepts"] / stats["count"]
            avg_patterns = stats["total_patterns"] / stats["count"]
            empty_ratio = stats["empty_content"] / stats["count"]
            
            # Flag if analysis type seems weak
            if avg_length < 100 and stats["count"] >= 2:  # Consistently short
                insights.append(f"• `{a_type}` analyses averaging only {int(avg_length)} chars (may need deeper prompting)")
            if avg_concepts < 1 and stats["count"] >= 2:
                insights.append(f"• `{a_type}` yielding few extracted concepts (consider improving concept extraction)")
            if empty_ratio > 0.5:  # More than half are very short
                insights.append(f"• `{a_type}` has {int(empty_ratio*100)}% very short outputs (check for failures)")
        
        return {
            "status": "analyzed",
            "repos_checked": len(recent_done),
            "snippets_checked": len(recent_snippets),
            "insights": insights
        }
    except Exception as e:
        return {"status": "error", "error": str(e)}

def main():
    result = analyze_recent_quality(hours=24)
    
    if result.get("status") == "error":
        print(f"💥 Quality monitor error: {result['error']}")
        return
    
    if result.get("status") == "no_recent_completions":
        # Don't spam - only speak up if there's something to say
        return
    
    insights = result.get("insights", [])
    
    # Only print message if we have meaningful insights
    if insights and len(insights) > 0:
        msg = f"🔬 *Analysis Quality Insight* (last {result['repos_checked']} repos)\n\n"
        msg += "\n".join(insights)
        msg += "\n\n_Review these to see if prompt tweaks could help._"
        print(msg)
    # If no insights, stay silent - no need to report "everything looks good" constantly

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"💥 Quality monitor cron failed: {e}")
        raise