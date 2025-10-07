# bootcamp-ta · 3-Minute Demo Speaker Notes

## Segment 0 · Intro (30s)
- “I built this lightweight teaching-assistant system to explore Microsoft’s Agent Framework in a realistic teaching-assistant workflow and compare it to other agent building tools I've used.”
- “The repo has two entry points: `main.py` (original single-pass script) and `msa_main.py` (multi-agent demo).”
- “Dependencies are in `requirements.txt` — note `agent-framework`, `openai`, and `python-dotenv`. The `.env` includes `OPENAI_API_KEY` and optional `OPENAI_MODEL`, `GITHUB_TOKEN`.”

## Segment 1 · Classic Flow Snapshot (45s)
- “The baseline script loads `rubric.json`, fetches diffs, analyzes, and prints Markdown.”
- Run sample mode (no PR needed):
  ```bash
  python main.py
  ```
- While output prints:
  - “Notice the trace line `Fetcher ✓, Analyzer ✓, Writer ✓`.”
  - “Because I didn’t pass `--pr`, it uses the tiny sample diff bundled with the repo.”
  - “This sequential script is great for quick tests or environments where I don’t need agents.”

## Segment 2 · Microsoft Agent Framework Demo (75s)
- “Now the Agent Framework version in `msa_main.py`. Same goal, but each step becomes a chat agent.”
- Show relevant code slice (quick glance):
  ```bash
  sed -n '20,120p' msa_main.py
  ```
  - Call out: creation of `Fetcher`, `Analyzer`, `Writer`; model set via `fetcher.chat_client.model = ...`.
  - Mention manual JSON handoffs and the fallback parsing logic.
- Run the agentized flow with sample diff:
  ```bash
  python msa_main.py
  ```
- Narrate the result:
  - “The agents run one after another—still async-capable, but here it’s a clean sequential chain.”
  - “Output is another Markdown review, now produced through the agent framework.”
  - “Swapping models or adding new roles would just mean instantiating more agents.”

## Segment 3 · Comparisons (30s)
- “In the README I compare three approaches:”
  - “CrewAI: more declarative crews and auto-sequencing vs. the direct control I get here.”
  - “Hand-rolled agents: less repetitive setup thanks to Agent Framework’s chat abstractions.”
  - “BAML: schema-first guarantees compared with this chat-first message passing.”
- “Those sections outline when each approach makes sense depending on structure vs. flexibility needs.”

## Segment 4 · Closing & CTA (30s)
- “Next steps I’m exploring: adding QA/test agents, capturing trace telemetry, experimenting with other models.”
- “Repo is public at `github.com/lana-z/bootcamp-ta`—clone it, drop in your API key, run both entry points, and try a real PR.”
- “Takeaway: Microsoft’s Agent Framework let me refactor a manual review script into a modular multi-agent workflow without a ton of repetitive orchestration code.”
