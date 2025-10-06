from typing import Dict, List

def weighted_percent(rubric: Dict, scores: List[Dict]) -> int:
    weights = {c['id']: c['weight'] for c in rubric['criteria']}
    total = 0.0
    for s in scores:
        total += (float(s['score'])/4.0) * weights.get(s['id'], 0)
    return round(total * 100)

def render_markdown(pr_meta: Dict, review: Dict, rubric: Dict) -> str:
    pct = weighted_percent(rubric, review.get('scores', []))
    rows = '\\n'.join([f"| {s['id']} | {s['score']} | {s['rationale']} |" for s in review.get('scores', [])])
    sugg = '\\n'.join([f"**{x['filename']}**\\n\\n{x['suggestion_md']}" for x in review.get('suggestions', [])]) or '_None_'
    return f"""### Bootcamp TA Review — PR #{pr_meta.get('number','(sample)')} by @{pr_meta.get('author','(sample)')}
**Overall (weighted): {pct}%**

| Criterion | Score (0–4) | Rationale |
|---|---:|---|
{rows}

#### Summary
{review.get('summary_md','')}

#### File-level Suggestions
{sugg}

<sub>Orchestrator → Fetcher → Analyzer → Writer · temp=0.2</sub>
"""
