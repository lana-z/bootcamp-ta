from dotenv import load_dotenv

load_dotenv()

import os, json, argparse, time
from agents.fetcher import fetch_pr
from agents.analyzer import analyze
from agents.writer import render_markdown

def run(pr_url: str = None, failing_tests: str = '') -> str:
    t0 = time.time()
    with open('rubric.json', 'r') as f:
        rubric = json.load(f)
    if pr_url:
        pr = fetch_pr(pr_url)
        diffs = pr['diffs']
    else:
        # offline fallback: tiny sample patch
        diffs = [{'filename': 'sample.py', 'patch': '--- a/sample.py\\n+++ b/sample.py\\n@@\\n-def add(a,b):return a+b\\n+def add(a, b):\\n+    \"\"\"Add two numbers.\"\"\"\\n+    return a + b\\n'}]
        pr = {'number': '(sample)', 'author': '(sample)'}
    review = analyze(rubric, diffs, failing_tests)
    md = render_markdown(pr, review, rubric)
    elapsed = int((time.time() - t0) * 1000)
    print(f'\n—— Trace: Fetcher ✓, Analyzer ✓, Writer ✓ · {elapsed} ms ——\n')
    return md

if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--pr', help='GitHub PR URL like https://github.com/org/repo/pull/123')
    ap.add_argument('--failing', default='', help='Optional failing test output to guide review')
    args = ap.parse_args()
    print(run(args.pr, args.failing))
