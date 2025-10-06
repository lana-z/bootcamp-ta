import os, requests
from typing import Dict, List

GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')

def fetch_pr(pr_url: str) -> Dict:
    """Fetch PR metadata and changed file patches via GitHub REST API."""
    parts = pr_url.rstrip('/').split('/')
    try:
        owner, repo, pr_number = parts[-4], parts[-3], parts[-1]
    except Exception:
        raise ValueError('Expected URL like https://github.com/org/repo/pull/123')
    headers = {'Accept': 'application/vnd.github+json'}
    if GITHUB_TOKEN:
        headers['Authorization'] = f'Bearer {GITHUB_TOKEN}'
    pr = requests.get(f'https://api.github.com/repos/{owner}/{repo}/pulls/{pr_number}', headers=headers)
    pr.raise_for_status()
    files = requests.get(f'https://api.github.com/repos/{owner}/{repo}/pulls/{pr_number}/files', headers=headers)
    files.raise_for_status()
    diffs: List[Dict] = []
    for f in files.json():
        diffs.append({'filename': f['filename'], 'patch': (f.get('patch') or '')[:20000]})
    return {
        'title': pr.json()['title'],
        'number': pr.json()['number'],
        'author': pr.json()['user']['login'],
        'diffs': diffs
    }

def get_diffs_or_sample(pr_url: str | None):
    """Return a list of {filename, patch} dicts either from a real PR or a tiny built-in sample."""
    if pr_url:
        meta = fetch_pr(pr_url)
        return meta['diffs'], {'number': meta['number'], 'author': meta['author']}
    sample = [{'filename':'sample.py','patch':'--- a/sample.py\\n+++ b/sample.py\\n@@\\n-def add(a,b):return a+b\\n+def add(a, b):\\n+    """Add two numbers."""\\n+    return a + b\\n'}]
    return sample, {'number':'(sample)','author':'(sample)'}
