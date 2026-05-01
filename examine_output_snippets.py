#!/usr/bin/env python3
import os
from pathlib import Path
import re
from datetime import datetime, timezone

OUTPUT_BASE = Path("/opt/llm_wiki/output")
OBSIDIAN_BASE = Path("/opt/llm_wiki/obsidian-vault")

def analyze_content(content, file_path):
    """Analyze content for depth, actionability, and consistency."""
    # Depth indicators
    depth_indicators = {
        'has_analysis_keywords': bool(re.search(r'\b(analysis|insight|recommendation|pattern|architecture|intent)\b', content, re.I)),
        'has_headers': bool(re.search(r'^#+\s', content, re.M)),
        'has_lists': bool(re.search(r'^\s*[-*]\s+', content, re.M)),
        'has_code_blocks': bool(re.search(r'```', content)),
        'length_over_500': len(content) > 500,
        'has_specific_terms': bool(re.search(r'\b(complexity|dead\s+code|unused\s+dependency|god\s+object|git\s+churn)\b', content, re.I)),
        'has_action_verbs': bool(re.search(r'\b(should|recommend|fix|improve|add|implement|refactor|consider)\b', content, re.I)),
        'has_metrics': bool(re.search(r'\b\d+\s*(lines?|%|files?|commits?|issues?)\b', content, re.I))
    }
    depth_score = sum(depth_indicators.values())
    
    # Actionability indicators
    action_indicators = {
        'has_imperatives': bool(re.search(r'\b(should|must|need to|have to|ought to)\b', content, re.I)),
        'has_suggestions': bool(re.search(r'\b(could|might|may|suggest|propose|recommend)\b', content, re.I)),
        'has_code_examples': bool(re.search(r'```[\s\S]*?```', content)),
        'has_step_by_step': bool(re.search(r'\d+\.\s+', content)),
        'has_checklist': bool(re.search(r'^\s*[-*]\s*\[[ x\]\s]', content, re.M)),
        'has_resources': bool(re.search(r'\b(see|refer to|check out|look at)\b', content, re.I)),
        'has_outcomes': bool(re.search(r'\b(result|outcome|benefit|advantage|improve)\b', content, re.I)),
        'has_risks': bool(re.search(r'\b(risk|drawback|limitation|trade-off|cost)\b', content, re.I))
    }
    action_score = sum(action_indicators.values())
    
    # Consistency indicators (structure)
    consistency_indicators = {
        'has_title': bool(re.search(r'^#\s+.+', content, re.M)),
        'has_frontmatter': bool(re.search(r'^---\s*\n.*?\n---\s*', content, re.S)),
        'has_tags': bool(re.search(r'^tags:\s*\[.*\]', content, re.M)),
        'has_timestamp': bool(re.search(r'\d{4}-\d{2}-\d{2}', content)),
        'has_repo_name': bool(re.search(r'repo[:\s]+[\w\-]+', content, re.I)),
        'uniform_heading_style': len(re.findall(r'^#+\s', content, re.M)) > 0  # at least one header
    }
    consistency_score = sum(consistency_indicators.values())
    
    return {
        'depth': depth_score,
        'actionability': action_score,
        'consistency': consistency_score,
        'depth_details': depth_indicators,
        'action_details': action_indicators,
        'consistency_details': consistency_indicators,
        'length': len(content),
        'preview': content[:200] + ('...' if len(content) > 200 else '')
    }

def examine_recent_snippets(days=7):
    """Examine snippets from the last N days."""
    cutoff = datetime.now(timezone.utc).timestamp() - (days * 86400)
    files_examined = 0
    total_depth = 0
    total_action = 0
    total_consistency = 0
    issues = []
    
    for root, dirs, files in os.walk(OUTPUT_BASE):
        for file in files:
            if file.endswith('.md'):
                file_path = Path(root) / file
                try:
                    mtime = file_path.stat().st_mtime
                    if mtime < cutoff:
                        continue
                    content = file_path.read_text(encoding='utf-8')
                    analysis = analyze_content(content, str(file_path))
                    files_examined += 1
                    total_depth += analysis['depth']
                    total_action += analysis['actionability']
                    total_consistency += analysis['consistency']
                    
                    # Collect potential issues
                    if analysis['depth'] < 3:
                        issues.append(f"Low depth ({analysis['depth']}/8) in {file_path.relative_to(OUTPUT_BASE)}")
                    if analysis['actionability'] < 3:
                        issues.append(f"Low actionability ({analysis['actionability']}/8) in {file_path.relative_to(OUTPUT_BASE)}")
                    if analysis['consistency'] < 3:
                        issues.append(f"Low consistency ({analysis['consistency']}/6) in {file_path.relative_to(OUTPUT_BASE)}")
                except Exception as e:
                    print(f"Error reading {file_path}: {e}")
    
    print(f"Examined {files_examined} snippet files from the last {days} days.")
    if files_examined > 0:
        print(f"Average depth score: {total_depth/files_examined:.2f}/8")
        print(f"Average actionability score: {total_action/files_examined:.2f}/8")
        print(f"Average consistency score: {total_consistency/files_examined:.2f}/6")
    else:
        print("No files found in the specified time range.")
    
    if issues:
        print("\n--- Issues Found ---")
        for issue in issues[:10]:  # Limit to first 10
            print(f"- {issue}")
        if len(issues) > 10:
            print(f"... and {len(issues)-10} more issues")
    else:
        print("\nNo significant issues found.")
    
    return {
        'files_examined': files_examined,
        'avg_depth': total_depth/files_examined if files_examined else 0,
        'avg_actionability': total_action/files_examined if files_examined else 0,
        'avg_consistency': total_consistency/files_examined if files_examined else 0,
        'issues': issues
    }

if __name__ == "__main__":
    examine_recent_snippets()