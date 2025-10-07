import os, json, asyncio, argparse
from typing import Dict

from dotenv import load_dotenv

# Microsoft Agent Framework (Python)
from agent_framework import ChatAgent, ChatMessage
from agent_framework.openai import OpenAIChatClient  # uses OPENAI_API_KEY from env

# reuse existing helpers
from agents.fetcher import get_diffs_or_sample
from agents.analyzer import normalize_json_text
# we'll print the Writer agent's markdown directly for the demo

load_dotenv()

def load_rubric() -> Dict:
    with open('rubric.json','r') as f:
        return json.load(f)

def message_text(message) -> str:
    """Extract plain text from a ChatAgent result regardless of concrete return type."""
    if message is None:
        return ''
    text = getattr(message, 'text', None)
    if text:
        return text
    content = getattr(message, 'content', None)
    if isinstance(content, str):
        return content
    return str(message)

async def run_agentized(pr_url: str | None, failing_tests: str | None) -> str:
    rubric = load_rubric()
    diffs, pr_meta = get_diffs_or_sample(pr_url)

    # 1) Fetcher: summarize changed files / concerns
    fetcher = ChatAgent(
        chat_client=OpenAIChatClient(),
        name='Fetcher',
        instructions=(
            'You summarize GitHub PR diffs for a TA. Input is JSON of {filename, patch}. '
            'Output a short bullet list of touched files and potential concerns. Do not invent files.'
        )
    )
    fetcher.chat_client.model = os.getenv('OPENAI_MODEL', 'gpt-4o-mini')
    fetch_summary_msg = await fetcher.run(ChatMessage(
        role='user',
        text=f'Diff JSON (truncate if large):\n{json.dumps(diffs)[:55000]}\nSummarize changes as bullets.'
    ))
    fetch_summary = message_text(fetch_summary_msg)

    # 2) Analyzer: rubric scoring + suggestions (STRICT JSON)
    analyzer = ChatAgent(
        chat_client=OpenAIChatClient(),
        name='Analyzer',
        instructions=(
            'You are a senior bootcamp instructor. Score the code against the rubric (0–4 each), give rationales, '
            'and propose 2–4 actionable fixes. Return STRICT JSON with keys: '
            'scores[], summary_md, suggestions[].\n'
            'scores[] items are {id, score, rationale}. suggestions[] items are {filename, suggestion_md}.'
        )
    )
    analyzer.chat_client.model = os.getenv('OPENAI_MODEL', 'gpt-4o-mini')
    analyze_input = {
        'rubric': rubric,
        'diffs': diffs,
        'failing_tests': failing_tests or '',
        'diff_summary': fetch_summary
    }
    analyze_raw_msg = await analyzer.run(ChatMessage(role='user', text=json.dumps(analyze_input)))
    analyze_raw = message_text(analyze_raw_msg)
    try:
        normalized = normalize_json_text(analyze_raw)
        analysis = json.loads(normalized)
    except Exception:
        analysis = {'scores': [], 'summary_md': analyze_raw, 'suggestions': []}

    # 3) Writer: turn analysis JSON into polished Markdown review
    writer = ChatAgent(
        chat_client=OpenAIChatClient(),
        name='Writer',
        instructions=(
            'You convert analysis JSON into clean Markdown suitable for a GitHub review comment. '
            'Include a brief summary, a rubric table with weighted percent (use the weights from rubric.criteria), '
            'and file-grouped suggestions. Keep it under ~200 lines.'
        )
    )
    writer.chat_client.model = os.getenv('OPENAI_MODEL', 'gpt-4o-mini')
    writer_prompt = {
        'pr_meta': pr_meta,
        'rubric': rubric,
        'analysis': analysis
    }
    md_msg = await writer.run(ChatMessage(role='user', text=f'Create the Markdown for this review:\n{json.dumps(writer_prompt)[:60000]}'))
    md = message_text(md_msg)

    # final output is the Writer agent's markdown
    return md

if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--pr', help='GitHub PR URL like https://github.com/org/repo/pull/123')
    ap.add_argument('--failing', default='', help='Optional failing test output')
    args = ap.parse_args()
    print(asyncio.run(run_agentized(args.pr, args.failing)))
