#!/usr/bin/env python3
"""
Cron job that delegates analysis to multiple Hermes agents
for collaborative system improvement suggestions.
"""
import os
from datetime import datetime, timezone

# Import from the hermes-agent tools (adjust path as needed)
import sys
sys.path.insert(0, '/root/.hermes/hermes-agent')
from tools.delegate_task_tool import delegate_task
from tools.send_message_tool import send_message

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
    # Fallback to the known URI from config
    MONGODB_URI = "mongodb+srv://dubeyrishabh108_db_user:z1ss49FReN22EAIk@cluster0.j8iafjr.mongodb.net/github_wiki?retryWrites=true&w=majority"

def main():
    """Delegate analysis tasks to multiple agents and synthesize results."""
    
    # Context for all subagents
    context = f"""LLM Wiki System Status (as of {datetime.now(timezone.utc).isoformat()}):
- Primary job: llm_wiki_dynamic_analysis (runs every 6 hours at :00 UTC)
- Current queue state: unknown (will be checked by agents)
- Recent runs: Check MongoDB github_wiki.analysis_runs for status trends
- System goal: Analyze all GitHub repos for rishabh3562, build knowledge base in MongoDB + Obsidian
- Constraints: Must not break hourly processing, prefer non-disruptive changes
- Current system: Uses dynamic analysis that adapts to repository complexity"""

    # Define tasks for different specialist agents
    tasks = [
        {
            "goal": "Analyze repo processing performance: Identify bottlenecks in queue flow, average processing times per repo, and suggest 1-2 specific optimizations to the 6-hour cron job or processing script.",
            "context": context + "\nFocus: Queue dynamics, processing duration, failure patterns, dynamic analysis effectiveness.",
            "toolsets": ["terminal", "file", "session_search"]
        },
        {
            "goal": "Review analysis quality: Examine recent snippets in MongoDB for depth, actionability, and consistency. Suggest improvements to analysis prompts or phases to yield more valuable insights.",
            "context": context + "\nFocus: Snippet content quality, concept extraction, design pattern detection, variable output file counts.",
            "toolsets": ["terminal", "file"]
        },
        {
            "goal": "Check system health and redundancy: Review cron job configurations, error handling in scripts, and suggest improvements to make the system more resilient to transient failures (network, API rate limits).",
            "context": context + "\nFocus: Cron schedules, error recovery, backup strategies, notification systems, dynamic processing adaptation.",
            "toolsets": ["terminal", "file"]
        }
    ]
    
    try:
        # Delegate tasks to subagents (max 2 concurrent to avoid overload)
        results = delegate_task(
            tasks=tasks,
            toolsets=[["terminal", "file"] for _ in tasks],  # Each gets terminal+file
            acp_command="hermes",  # Use Hermes Agent for subagents
            max_iterations=25  # Reasonable limit for focused analysis
        )
        
        # Synthesize results into improvement suggestions
        suggestions = []
        agent_names = ["Performance Analyst", "Quality Reviewer", "Health Engineer"]
        
        for i, result in enumerate(results):
            agent_name = agent_names[i] if i < len(agent_names) else f"Agent {i+1}"
            if isinstance(result, dict) and "output" in result:
                output = result["output"]
                # Extract key suggestions (simple heuristic: look for bullet points or numbered lists)
                lines = [line.strip() for line in output.split('\n') if line.strip()]
                key_points = [line for line in lines if line.startswith(('-', '•', '*')) or any(line.startswith(str(n)+'.') for n in range(1,10))]
                if key_points:
                    suggestions.append(f"**{agent_name}**:")
                    suggestions.extend(key_points[:2])  # Top 2 points per agent
                elif output and len(output) > 20:
                    suggestions.append(f"**{agent_name}**: {output[:150]}...")
        
        if not suggestions:
            suggestions = ["All agents completed analysis but no specific improvements identified."]
        
        # Compose and send Telegram message
        message = "🤖 *Multi-Agent Improvement Analysis*\n\n"
        message += "\n".join(suggestions)
        message += "\n\n_Review these agent-generated suggestions for potential implementation._"
        
        send_message(
            action='send',
            target='telegram',
            message=message
        )
        
    except Exception as e:
        send_message(
            action='send',
            target='telegram',
            message=f"💥 Multi-agent analysis failed: {str(e)[:200]}"
        )
        raise

if __name__ == "__main__":
    main()