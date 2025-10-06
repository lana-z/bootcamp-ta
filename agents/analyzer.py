import os, json
from typing import Dict, List
from openai import OpenAI

MODEL = os.getenv('OPENAI_MODEL', 'gpt-4o-mini')

def analyze(rubric: Dict, diffs: List[Dict], failing_tests: str = '') -> Dict:
    client = OpenAI(api_key=os.environ['OPENAI_API_KEY'])
    sys = 'You are a senior instructor reviewing student PRs with strict rubric scoring.'
    user = f"""Rubric JSON:
{json.dumps(rubric)}

Failing tests:
{failing_tests or 'none'}

PR Diffs (truncated):
{json.dumps(diffs)[:55000]}

Return JSON with:
- scores: list of {{id, score (0-4), rationale}}
- summary_md: 4-6 lines of markdown summary with inline suggestions
- suggestions: array of {{filename, suggestion_md}}
"""
    resp = client.responses.create(
        model=MODEL,
        input=[{'role':'system','content':sys},{'role':'user','content':user}],
        temperature=0.2,
    )
    try:
        return json.loads(resp.output_text)
    except Exception:
        # fallback to raw text if model didn't return JSON
        return {'scores': [], 'summary_md': resp.output_text, 'suggestions': []}
