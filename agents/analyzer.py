import os, json
from typing import Dict, List
from openai import OpenAI

MODEL = os.getenv('OPENAI_MODEL', 'gpt-4o-mini')

def normalize_json_text(raw: str) -> str:
    raw = (raw or '').strip()
    if raw.startswith('```'):
        raw = raw.split('```', 2)[1].strip()
        lang, _, remainder = raw.partition('\n')
        lang_clean = lang.strip().lower()
        if remainder:
            if lang_clean in {'json', 'javascript', 'js'}:
                raw = remainder.strip()
            elif not lang.strip().startswith('{'):
                raw = remainder.strip()
        else:
            raw = lang.strip()
    return raw

def analyze(rubric: Dict, diffs: List[Dict], failing_tests: str = '') -> Dict:
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        raise RuntimeError('OPENAI_API_KEY is not set. Add it to your environment or .env file.')
    client = OpenAI(api_key=api_key)
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
        raw = normalize_json_text(resp.output_text)
        return json.loads(raw)
    except Exception:
        # fallback to raw text if model didn't return JSON
        return {'scores': [], 'summary_md': resp.output_text, 'suggestions': []}
