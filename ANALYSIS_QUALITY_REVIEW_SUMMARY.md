# Analysis Quality Review - Task Summary

## What I Did
- Reviewed the LLM Wiki system architecture and 5-phase analysis process in `run_llm_wiki.py`
- Connected to MongoDB github_wiki database and examined the snippets collection
- Analyzed 30 most recent snippets for depth, actionability, and consistency using custom scoring metrics
- Identified root causes of superficial analysis content
- Developed specific, non-disruptive improvements to enhance analysis quality

## What I Found
### Depth Issues (Average Score: 2.97/6)
- Most snippet content consists of template text with placeholders like "*To be filled by analysis..."
- Only Phase 2 (Static Analysis) produces substantive data (smells.json)
- Missing structured insights: `extractedConcepts` and `designPatterns` schema fields never populated
- Generic templates used across all repos (identical architecture/patterns/improvements files)

### Actionability Issues (Average Score: 0.67/4)
- Low actionability: Content lacks specific, actionable recommendations
- No prioritization of issues or concrete examples
- Vague findings without location-specific details or code examples
- Limited technical depth in generated recommendations

### Consistency Assessment
- Consistent templates and placeholder language across repositories
- Inconsistent real data: Only static analysis produces varying content
- Uniform boilerplate in Phases 1, 3, and 4 despite repo-specific differences in Phase 2

## Root Causes Identified
1. **Phase 1 (Archaeology)**: Extracts real git log but leaves analytical answers as placeholders
2. **Phase 2 (Static Analysis)**: Working correctly - produces real metrics in `smells.json`
3. **Phase 3 (Parallel Agents)**: Template-only generation with no actual code analysis
4. **Phase 4 (Storage)**: Stores raw markdown without extracting structured insights
5. **Missing Concept Extraction**: No mechanism to derive structured concepts from analysis results

## Files Created/Modified
- `/opt/llm_wiki/examine_snippets_quality.py` - Analysis script for evaluating snippet quality
- `/opt/llm_wiki/ANALYSIS_QUALITY_REVIEW_SUMMARY.md` - This summary document
- `/opt/llm_wiki/ANALYSIS_QUALITY_FINDINGS.md` - Pre-existing findings document (reviewed)

## Suggested Improvements (Non-Disruptive)
### Immediate Wins
1. **Enhance Phase 3 Templates** using actual analysis data:
   - Architecture Agent: Generate real dependency graphs from import/file structure
   - Patterns Agent: Extract real code patterns (decorators, factories, etc.)
   - Improvements Agent: Generate fixes based on actual `smells.json` data
   - Self Portrait Agent: Customize with repo-specific git log insights

2. **Extract Concepts in Phase 4 Storage**:
   - Parse `smells.json` to populate `extractedConcepts` with high complexity files, dead code, git churn
   - Add `designPatterns` extraction from actual code patterns
   - Maintain backward compatibility with existing schema

### Structured Output Enhancements
- Standardize concept format with type, name, description, location, priority, evidence
- Add `structuredInsights` array, `metrics` object, and `actionItems` array to snippets
- Keep existing fields for Obsidian vault compatibility

### Analysis Phase Improvements
- Phase 1: Analyze commit messages for tech shifts, extract architectural decisions
- Phase 3: Feed `smells.json` into agents for context-aware analysis
- Integration: Use git log insights to inform self-portrait generation

## Expected Outcomes
- Increased depth: Specific, repo-specific insights replacing generic templates
- Higher actionability: Clear prioritization and location-specific recommendations
- Better consistency: Standardized insight format with repo-specific content
- Enhanced value: Structured data enables querying, comparison, and trend analysis

All recommendations preserve hourly processing, maintain backward compatibility with Obsidian vault, and introduce minimal disruption to existing workflows.