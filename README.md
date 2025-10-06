# bootcamp-ta

Exploratory teaching-assistant system that demos Microsoft's new Agent Framework alongside the original single-script flow. The project processes GitHub pull requests, scores them against a JSON rubric, and produces a Markdown review.

## Project Highlights
- **Dual entry points** – `main.py` for the original synchronous flow, `msa_main.py` for the multi-agent demo built on Microsoft Agent Framework.
- **Rubric-driven analysis** – Reads `rubric.json` to guide scoring and feedback suggestions.
- **Offline sample mode** – Runs with a built-in diff when no PR URL is supplied, making the workflows easy to try without GitHub access.

## Prerequisites
- Python 3.10+
- OpenAI API key with access to `gpt-4o-mini` (override via env if needed)
- Optional: GitHub personal access token for higher-rate PR fetching

## Setup
```bash
git clone https://github.com/lana-z/bootcamp-ta.git
cd bootcamp-ta
python -m venv env
source env/bin/activate                   # Windows: .\env\Scripts\activate
pip install --upgrade pip
pip install -r requirements.txt
```

Create a `.env` file (or export variables in your shell):
```bash
OPENAI_API_KEY=sk-...
# optional overrides
OPENAI_MODEL=gpt-4o-mini
GITHUB_TOKEN=ghp_your_token             # only needed when fetching private PRs or avoiding rate limits
```

## Usage

### 1. Classic Pipeline (`main.py`)
```bash
python main.py --pr https://github.com/org/repo/pull/123
```
- Pulls diffs via GitHub REST API, analyzes against the rubric, and prints Markdown review.
- Pass `--failing "pytest logs..."` to feed failing tests into the analysis.
- Omit `--pr` to run the built-in sample diff for quick smoke tests.

### 2. Agent Framework Demo (`msa_main.py`)
```bash
python msa_main.py --pr https://github.com/org/repo/pull/123
```
- Orchestrates three chat agents (Fetcher, Analyzer, Writer) using Microsoft Agent Framework.
- Each agent shares context via JSON payloads and emits a consolidated Markdown review.
- Adjust the model by exporting `OPENAI_MODEL` (defaults to `gpt-4o-mini`).

## Repo Structure
- `agents/` – Modular helpers shared by both entry points (`fetcher`, `analyzer`, `writer`).
- `main.py` – Sequential bootstrapper for the original flow.
- `msa_main.py` – Async multi-agent experiment powered by Microsoft Agent Framework.
- `rubric.json` – Criteria definitions consumed by analyzers and writers.
- `requirements.txt` – Python dependencies for both workflows.

## Next Steps
- Expand agent personalities (e.g., add QA reviewer or test-run agent).
- Integrate persistence to capture agent traces for later inspection.
- Experiment with alternative models/providers by swapping the `OpenAIChatClient`.

Have fun exploring Microsoft's agent tooling in a realistic TA review scenario! Open an issue or PR with ideas. 
