# bootcamp-ta

Exploring Microsoft's Agent Framework with a teaching-assistant system that processes bootcamp students' GitHub pull requests, scores them against a JSON rubric, and produces a Markdown review.

## Project Highlights
- **Dual entry points** – `main.py` for the original flow, `msa_main.py` for the multi-agent demo built on Microsoft Agent Framework.
- **Rubric-driven analysis** – Reads `rubric.json` to guide scoring and feedback suggestions.
- **Offline sample mode** – Runs with a built-in diff when no PR URL is supplied, making the workflows easy to try without GitHub access.
- Comparison with CrewAI, custom-built agents, and BAML. 

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
- `main.py` – Sequential bootstrapper for the original flow; keep it as a baseline reference to show the pipeline without agent orchestration, handy for debugging, smoke tests, or illustrating the delta the Agent Framework introduces.
- `msa_main.py` – Async multi-agent experiment powered by Microsoft Agent Framework.
- `rubric.json` – Criteria definitions consumed by analyzers and writers.
- `requirements.txt` – Python dependencies for both workflows.


## Comparing Approaches
These notes capture how this Microsoft Agent Framework experiment relates to other ways of building the workflow.

### Versus Custom-Built Agents
- **Infrastructure** – Building agents from scratch requires manually managing prompt templates, chat history, retries, and tool invocation. Microsoft Agent Framework gives you `ChatAgent`/`ChatMessage` primitives, so the plumbing is handled.
- **Consistency** – Handwritten agents often diverge in schema or output format. The framework enforces consistent message envelopes and response handling, keeping agents composable.
- **Speed to integrate** – Adding a new provider or model with custom code means writing client adapters yourself. Here you just swap `OpenAIChatClient` (or future equivalents) without touching orchestration logic.
- **Observability** – Framework hooks provide uniform logging/tracing. DIY implementations need bespoke instrumentation to track agent interactions.
- **Extensibility** – Features like parallel tasks, shared memory, or guardrails come “for free” as the framework evolves. Pure custom flows grow brittle as you bolt on features.
- **When custom wins** – For ultra-simple, one-off scripts, rolling your own agent might stay leaner. Once you have multiple roles or need maintainability, the framework amortizes its weight quickly.

### Versus CrewAI
- **Orchestration** – Microsoft Agent Framework keeps you close to raw async Python: you instantiate agents and explicitly pass messages between them. CrewAI wraps agents in “crews” with declarative task graphs; sequencing and coordination are auto-managed.
- **State passing** – Here, intermediate data (diff summaries, rubric JSON) flows via manual JSON payloads. CrewAI maintains shared crew state so downstream tasks can access prior outputs without handoffs.
- **Tool usage** – Agent Framework plugs tools/helpers directly in your code. CrewAI attaches registered tools to agents; the runtime triggers them as plans require.
- **Execution model** – This demo runs agents sequentially. CrewAI ships with a scheduler capable of concurrent tasks, re-planning, and adaptive branching out of the box.
- **Configuration** – Prompts live inline in `msa_main.py`, meaning changes require code edits. CrewAI typically separates configuration (YAML/Python builders) from execution, enabling quicker reuse across projects.
- **Ideal fit** – Use Agent Framework when you want tight control or lightweight integrations. Choose CrewAI for complex, collaborative workflows where higher-level abstractions (memory, observers, dynamic crews) pay off.

### Versus BAML
- **Paradigm** – Microsoft Agent Framework is chat-first: you compose agents that exchange messages. BAML is schema-first: you define structured prompts and outputs (Pydantic-like schemas), and the runtime validates responses automatically.
- **State handling** – Here, state is plain Python data flowing through agents. BAML promotes reusable prompt “functions” with typed inputs/outputs, reducing ad-hoc JSON juggling.
- **Error handling** – With Agent Framework you handle parsing/retry logic manually (see the try/except around `json.loads`). BAML can auto-retry until the response satisfies the declared schema.
- **Extensibility** – Agent Framework emphasizes orchestrating many cooperative roles. BAML focuses on maintainable, strongly typed interactions for individual prompts.
- **Use cases** – Choose Microsoft Agent Framework when you want agent collaboration and flexible message passing. Reach for BAML when you need bulletproof structured responses or integrate LLM calls into larger typed systems.
