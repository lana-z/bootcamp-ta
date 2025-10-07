# bootcamp-ta · 3-Minute Demo Walkthrough

### 0. Intro (30s)
- Frame the goal: explore Microsoft’s Agent Framework through a TA-style code review workflow.
- Mention the dual entry points: a classic script (`main.py`) and the agentized version (`msa_main.py`).
- Note requirements: OpenAI API key, optional GitHub token, and the added `agent-framework` dependency.

### 1. Classic Flow Snapshot (45s)
- Explain: `main.py` loads `rubric.json`, fetches diffs, runs analyzer, prints Markdown review.
- Run sample mode for instant output:
  ```bash
  python main.py
  ```
- Point out the terminal trace `Fetcher ✓, Analyzer ✓, Writer ✓` and show the generated sample review.
- Mention this path is useful for baseline comparisons or environments without multi-agent orchestration.

### 2. Microsoft Agent Framework Demo (75s)
- Emphasize new file `msa_main.py`: orchestrates Fetcher → Analyzer → Writer as chat agents.
- Open the file briefly (e.g., `sed -n '20,120p msa_main.py'`) to show:
  - `ChatAgent` constructions,
  - `fetcher.chat_client.model = os.getenv('OPENAI_MODEL', 'gpt-4o-mini')`,
  - JSON payload handoffs and error handling.
- Run the agent flow with the built-in sample:
  ```bash
  python msa_main.py
  ```
- Call out the sequential agent logs (if printed) and the final Markdown review.
- Note how this approach makes swapping models or inserting additional agents straightforward.

### 3. Framework Comparisons (30s)
- Summarize key README sections:
  - CrewAI vs. Microsoft Agent Framework (control vs. declarative orchestration).
  - Hand-rolled agents vs. framework support (plumbing, consistency).
  - BAML vs. chat-first flows (schema-first guarantees vs. flexible messaging).
- Point viewers to the README for deeper dives.

### 4. Closing (30s)
- Suggest next experiments: attach new agent roles, integrate test runners, track traces.
- Invite contributions via GitHub repo `https://github.com/lana-z/bootcamp-ta`.
- End by reiterating: goal was to explore Microsoft Agent Framework in a real TA review scenario.
