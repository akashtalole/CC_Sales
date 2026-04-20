# CC Sales — Pre-Sales AI Agents

A three-agent pipeline powered by [Anthropic Claude Managed Agents](https://platform.claude.com/docs/en/managed-agents/overview) that prepares your pre-sales team for every customer interaction — automatically.

## What it does

Given a prospect company name and optional hints, the pipeline runs three Claude agents in sequence, each building on the previous one's output:

| Phase | Agent | Output |
|-------|-------|--------|
| 1 | **Research Agent** | Deep customer intelligence report — company background, tech stack, key stakeholders, pain points, recent news, competitive landscape |
| 2 | **Account Planning Agent** | Actionable account plan — stakeholder map, discovery questions, value propositions, engagement timeline, risk register |
| 3 | **Next Best Action Agent** | Executable playbook — personalised outreach messages, meeting agenda, content to share, 30-60-90 day milestones |

All three agents are hosted and run on Anthropic's infrastructure. No agent loop or sandbox to manage yourself.

## Prerequisites

- Python 3.10+
- An [Anthropic API key](https://console.anthropic.com/settings/keys) with Claude Managed Agents access

## Quick start

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Set your API key
cp .env.example .env
# Edit .env and add your key: ANTHROPIC_API_KEY=sk-ant-...

# 3. Create the agents on Anthropic's platform (run once)
python setup_agents.py

# 4. Run the workflow for a prospect
python run_presales.py --company "Acme Corp" --website "acme.com"
```

## Usage

```
python run_presales.py --company NAME [options]

Required:
  --company NAME        Prospect company name

Optional:
  --website URL         Company website or LinkedIn URL
  --industry VERTICAL   Industry / vertical (e.g. "FinTech", "Healthcare")
  --contact CONTACTS    Known contacts (e.g. "Jane Smith, CTO; Bob Lee, VP Eng")
  --use-case TEXT       Why you think they need your solution
  --context TEXT        Additional deal context (deal source, urgency, etc.)
  --output FILE         Save full results to a JSON file
  --quiet / -q          Suppress streaming output; print summary only
```

### Examples

```bash
# Minimal
python run_presales.py --company "Stripe"

# Full context
python run_presales.py \
  --company "Acme Corp" \
  --website "acme.com" \
  --industry "E-commerce" \
  --contact "Jane Smith, CTO; Bob Lee, VP Engineering" \
  --use-case "Replace legacy data pipeline with modern lakehouse" \
  --context "Inbound from partner, urgent Q3 close target" \
  --output outputs/acme.json
```

## Project structure

```
CC_Sales/
├── setup_agents.py          # One-time: creates agents on Anthropic platform
├── run_presales.py          # CLI entry point — run per prospect
├── requirements.txt
├── .env.example
├── config/
│   └── agents.json          # Auto-generated: stores agent IDs and versions
└── presales/
    ├── prompts.py           # System prompts for all three agents
    ├── session_runner.py    # Managed Agent session lifecycle handler
    └── orchestrator.py      # Three-phase pipeline with context chaining
```

## How it works

The agents are **persistent, versioned configurations** created once via `setup_agents.py` and stored in `config/agents.json`. Each time you run `run_presales.py`, three sessions are created — one per agent — and the output of each phase is passed as context into the next.

```
Prospect info
     │
     ▼
┌─────────────────┐
│  Research Agent │  ← web_search + web_fetch + bash
│  (Session 1)   │
└────────┬────────┘
         │ research report
         ▼
┌──────────────────────┐
│  Account Planning    │  ← research + prospect context
│  Agent  (Session 2)  │
└──────────┬───────────┘
           │ account plan
           ▼
┌──────────────────────┐
│  Next Best Action    │  ← research + plan + prospect context
│  Agent  (Session 3)  │
└──────────────────────┘
           │
           ▼
    Full pre-sales package
    (JSON + stdout)
```

Sessions use the `agent_toolset_20260401` which gives each agent access to bash, web search, web fetch, and file operations — all running in Anthropic-hosted containers with unrestricted networking for research tasks.

## Managing agents

```bash
# Re-run setup to update system prompts (creates new agent version, keeps same IDs)
python setup_agents.py
# Choose option 2 — Update agent system prompts
```

Agent IDs are stable across updates. Sessions pin to a specific version so existing runs are never affected by prompt changes.

## Output

Results are printed to stdout in real time as agents stream their responses. Use `--output` to save the full JSON:

```json
{
  "company": "Acme Corp",
  "research": "...",
  "account_plan": "...",
  "next_best_actions": "..."
}
```
