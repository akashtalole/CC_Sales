# A2A Agent-to-Agent Protocol: Presales Team Integration

> **Protocol:** [Google A2A](https://github.com/google-a2a/A2A) v1.0  
> **Branch:** `claude/a2a-agent-protocol`  
> **Purpose:** Enable the presales Claude agent to discover and delegate tasks to specialized org agents

---

## Overview

The A2A (Agent-to-Agent) protocol allows the **CC Sales Presales Agent** to communicate with other specialized agents in your organization. Instead of one agent trying to do everything, the presales agent acts as an orchestrator — delegating specialized subtasks to domain experts.

```
                    ┌─────────────────────────┐
                    │   Presales Agent        │
                    │   (Orchestrator)        │
                    └──────────┬──────────────┘
                               │ A2A Protocol
            ┌──────────────────┼──────────────────────┐
            │                  │                       │
     ┌──────▼──────┐   ┌───────▼───────┐   ┌──────────▼────────┐
     │   Legal     │   │   Pricing     │   │   Technical       │
     │   Agent     │   │   Agent       │   │   Architecture    │
     └─────────────┘   └───────────────┘   │   Agent           │
                                           └───────────────────┘
            │                  │
     ┌──────▼──────┐   ┌───────▼───────┐
     │  Customer   │   │   Finance     │
     │  Success    │   │   Agent       │
     │  Agent      │   │               │
     └─────────────┘   └───────────────┘
```

**What this enables for the presales team:**
- A proposal can be generated with architecture designed by the technical agent, pricing validated by the pricing agent, and legal terms reviewed by the legal agent — all coordinated automatically
- A discovery call summary can trigger ROI calculation by the finance agent and reference matching by the CS agent — simultaneously
- An AE says "create proposal for Acme Corp" — the presales agent orchestrates the full workflow across all specialized agents

---

## Architecture

### Protocol Flow

```
1. Presales Agent identifies need for specialist capability
2. Queries /.well-known/agent-cards to discover available agents
3. Selects appropriate agent based on skill match
4. Creates a Task with structured input
5. Receives streaming or synchronous output
6. Synthesizes output into presales workflow
7. Routes result to human review (Slack / Notion)
```

### Agent Discovery

All agents in the org register their Agent Card at:
```
https://agents.your-company.com/.well-known/agent-cards
```

The presales agent queries this endpoint to discover available capabilities. No hardcoded agent URLs needed — the discovery endpoint returns all registered agents and their skills.

```bash
# Query all available org agents
curl https://agents.your-company.com/.well-known/agent-cards

# Query a specific agent's card
curl https://agents.your-company.com/.well-known/agent-cards/legal-agent
```

### Task Lifecycle

```
Created → Working → [Streaming output...] → Completed
                 ↘ input-required (needs clarification) → user responds → Working
                 ↘ failed → error returned to presales agent → fallback triggered
```

---

## Registered Org Agents

| Agent ID | Capability | Model | Invoked By |
|---|---|---|---|
| `presales-agent` | Orchestrator — all presales workflows | claude-sonnet-4-6 | SDR, AE, SE, Manager |
| `legal-agent` | Contract review, NDA, compliance | claude-opus-4-7 | Proposal stage, negotiation |
| `pricing-agent` | Quote generation, discount approval, ROI | claude-sonnet-4-6 | Proposal stage, deal desk |
| `technical-architecture-agent` | Architecture design, effort estimation, risk | claude-opus-4-7 | Discovery, proposal SE support |
| `customer-success-agent` | Reference matching, case studies, onboarding | claude-sonnet-4-6 | Proposal, close stage |
| `finance-agent` | Business case, TCO analysis | claude-sonnet-4-6 | Proposal, economic buyer engagement |

Agent cards are in `a2a/agents/` directory.

---

## Delegation Workflows

### Workflow 1: Full Proposal Generation

**Trigger:** Deal moves to "Discovery Complete" stage in CRM (MEDDIC score ≥ 60)

**Orchestration:**

```
presales-agent receives trigger
    │
    ├─→ technical-architecture-agent: "Design solution architecture for [scope]"
    │       Returns: architecture_doc_url, tech_stack, effort_estimate
    │
    ├─→ pricing-agent: "Generate 3-tier pricing quote for [scope + effort]"
    │       Returns: options[essentials, standard, premium], recommended_tier
    │
    ├─→ customer-success-agent: "Find reference customers matching [prospect profile]"
    │       Returns: matches[top 3], case_study_texts
    │
    └─→ finance-agent: "Build ROI model for $[investment] at [customer metrics]"
            Returns: roi_pct, payback_months, business_case_url

presales-agent synthesizes all outputs
    → create-an-asset generates proposal draft using all agent outputs
    → Proposal posted to Notion deal room
    → AE notified in Slack for review
```

**Sample invocation (from presales agent context):**

```
create a proposal for the Acme Corp deal.

Context:
- CRM Deal ID: deal_12345
- Scope: AWS EKS migration, 40 microservices, 6 months
- Budget signal: $800K-$1.2M
- Primary pain: zero-downtime migration

Delegate to:
- technical-architecture-agent: design the EKS migration architecture
- pricing-agent: generate 3-tier quote based on effort estimate returned
- customer-success-agent: find references in fintech or SaaS with similar migrations
- finance-agent: build ROI model using their stated 35% infra cost reduction goal

Synthesize all outputs into a complete proposal draft.
```

---

### Workflow 2: Contract Review During Negotiation

**Trigger:** Prospect sends MSA or SOW for review; AE uploads to CRM or Notion

**Orchestration:**

```
presales-agent detects document upload in CRM
    │
    └─→ legal-agent: "Review this MSA for risk [document_url]"
            contract_type: "msa"
            deal_value: 950000
            customer_jurisdiction: "California, USA"
            urgency: "urgent"

            Returns: risk_level: "medium",
                     flagged_clauses: [IP ownership clause, liability cap, data retention]
                     redlines: [recommended changes per clause]

presales-agent formats output
    → Posts legal review summary to Notion deal room (Proposals tab)
    → Alerts AE in Slack: "Legal review complete — 3 clauses flagged, 1 needs escalation"
    → Tags deal in CRM: ai_last_agent_activity_type = "Legal Review"
```

---

### Workflow 3: Post-Discovery ROI Request

**Trigger:** `/call-summary` detects "business case", "ROI", or "CFO approval" in transcript

**Orchestration:**

```
/call-summary processes transcript
    → Detects phrase: "our CFO will need to see ROI justification"
    → Automatically delegates to finance-agent

finance-agent receives:
    - crm_deal_id: deal_12345
    - customer_metrics from call summary:
        - current_annual_cost: 2400000 (estimated from headcount × $60K)
        - engineer_hours_per_week: 40 (stated: "4 engineers full time on infra toil")
        - investment_amount: 950000
    - audience: "cfo"

    Returns: business_case_url, roi_pct: 180, payback_months: 8

presales-agent:
    → Adds business case link to follow-up email draft
    → Posts to Notion deal room — "CFO Business Case" section
    → AE notified: "Business case ready for CFO — 180% ROI, 8-month payback"
```

---

### Workflow 4: Technical Validation Support

**Trigger:** SE requests technical brief before architecture deep-dive call

**Orchestration:**

```
SE invokes: call-prep for technical validation call with Acme Corp

presales-agent:
    ├─→ Retrieves CRM deal history and prior call summaries
    │
    └─→ technical-architecture-agent: "Generate technical discovery brief"
            requirements_summary: [from discovery call summary]
            current_stack: [from account-research enrichment]
            target_platform: "aws"

            Returns: technical_questions, compatibility_risks, architecture_options

presales-agent synthesizes:
    → call-prep brief includes technical section from technical-architecture-agent
    → Posted to Notion deal room 2 hours before call
    → SE receives Slack notification with Notion link
```

---

### Workflow 5: Competitive Deal Support

**Trigger:** `competitive-intelligence` detects a named competitor in transcript

**Orchestration:**

```
/call-summary processes transcript
    → Detects: "we're also talking to [Competitor]"

presales-agent:
    ├─→ competitive-intelligence: "Generate differentiation matrix vs. [Competitor]"
    │       deal_context: [deal details]
    │       Returns: differentiation_points, talk_tracks, red_flags
    │
    └─→ customer-success-agent: "Find references where we displaced [Competitor]"
            reference_type: "case-study"
            Returns: displacement_case_studies

presales-agent synthesizes:
    → Posts competitive response package to Notion deal room
    → AE Slack alert: "Competitive package ready — [Competitor] in evaluation"
    → Includes: talk track bullets, displacement case study, questions to surface gaps
```

---

## Implementation

### A2A Client (Python)

```python
import httpx
import json
from typing import Any

class A2AClient:
    """Simple A2A protocol client for presales agent to call org agents."""
    
    def __init__(self, discovery_url: str, auth_token: str):
        self.discovery_url = discovery_url
        self.auth_token = auth_token
        self.agent_registry: dict[str, dict] = {}
    
    async def discover_agents(self) -> dict[str, dict]:
        """Query the discovery endpoint and cache all agent cards."""
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.discovery_url}/.well-known/agent-cards",
                headers={"Authorization": f"Bearer {self.auth_token}"}
            )
            response.raise_for_status()
            cards = response.json()
            self.agent_registry = {card["agent"]["id"]: card for card in cards}
            return self.agent_registry
    
    async def delegate_task(
        self,
        agent_id: str,
        skill_id: str,
        input_data: dict[str, Any],
        timeout: int = 120
    ) -> dict[str, Any]:
        """
        Delegate a task to a specific agent skill.
        Returns the agent's output or raises on failure/timeout.
        """
        if agent_id not in self.agent_registry:
            await self.discover_agents()
        
        agent_card = self.agent_registry.get(agent_id)
        if not agent_card:
            raise ValueError(f"Agent '{agent_id}' not found in registry")
        
        agent_url = agent_card["agent"]["url"]
        
        task_payload = {
            "skill_id": skill_id,
            "input": input_data,
            "metadata": {
                "requested_by": "presales-agent",
                "timestamp": _now_iso()
            }
        }
        
        async with httpx.AsyncClient(timeout=timeout) as client:
            response = await client.post(
                f"{agent_url}/tasks",
                json=task_payload,
                headers={"Authorization": f"Bearer {self.auth_token}"}
            )
            response.raise_for_status()
            task = response.json()
            
            # Poll for completion (or use streaming if agent supports it)
            return await self._await_task(client, agent_url, task["task_id"])
    
    async def _await_task(
        self,
        client: httpx.AsyncClient,
        agent_url: str,
        task_id: str,
        poll_interval: float = 2.0,
        max_polls: int = 60
    ) -> dict[str, Any]:
        """Poll task status until completion or timeout."""
        import asyncio
        
        for _ in range(max_polls):
            response = await client.get(
                f"{agent_url}/tasks/{task_id}",
                headers={"Authorization": f"Bearer {self.auth_token}"}
            )
            response.raise_for_status()
            task = response.json()
            
            status = task["status"]
            
            if status == "completed":
                return task["output"]
            elif status == "failed":
                raise RuntimeError(f"Agent task failed: {task.get('error', 'Unknown error')}")
            elif status == "input-required":
                # For presales use cases, notify human and pause
                raise RuntimeError(f"Agent requires human input: {task.get('message')}")
            
            await asyncio.sleep(poll_interval)
        
        raise TimeoutError(f"Agent task {task_id} did not complete within timeout")


def _now_iso() -> str:
    from datetime import datetime, timezone
    return datetime.now(timezone.utc).isoformat()
```

### Orchestration Layer (Python)

```python
import asyncio
from a2a_client import A2AClient

class PresalesOrchestrator:
    """
    Orchestrates multi-agent workflows for presales use cases.
    Called by the presales agent when delegation is needed.
    """
    
    def __init__(self, a2a_client: A2AClient):
        self.client = a2a_client
    
    async def generate_full_proposal(
        self,
        crm_deal_id: str,
        scope_summary: str,
        customer_metrics: dict,
        investment_estimate: float
    ) -> dict:
        """
        Orchestrates: technical-architecture + pricing + customer-success + finance
        All run in parallel, then synthesized into proposal inputs.
        """
        tasks = await asyncio.gather(
            self.client.delegate_task(
                agent_id="technical-architecture-agent",
                skill_id="architecture-design",
                input_data={
                    "requirements_summary": scope_summary,
                    "current_stack": customer_metrics.get("current_stack", ""),
                }
            ),
            self.client.delegate_task(
                agent_id="pricing-agent",
                skill_id="pricing-quote",
                input_data={
                    "service_type": "managed-cloud-services",
                    "scope_summary": scope_summary,
                    "deal_size_estimate": investment_estimate,
                    "crm_deal_id": crm_deal_id
                }
            ),
            self.client.delegate_task(
                agent_id="customer-success-agent",
                skill_id="reference-match",
                input_data={
                    "prospect_profile": customer_metrics.get("prospect_profile", {}),
                    "reference_type": "case-study",
                    "max_results": 3
                }
            ),
            self.client.delegate_task(
                agent_id="finance-agent",
                skill_id="business-case",
                input_data={
                    "crm_deal_id": crm_deal_id,
                    "investment_amount": investment_estimate,
                    "customer_metrics": customer_metrics,
                    "audience": "cfo"
                }
            ),
            return_exceptions=True
        )
        
        architecture_output, pricing_output, references_output, finance_output = tasks
        
        # Handle partial failures gracefully — some agents may fail
        # while others succeed; synthesize what we have
        return {
            "architecture": architecture_output if not isinstance(architecture_output, Exception) else None,
            "pricing": pricing_output if not isinstance(pricing_output, Exception) else None,
            "references": references_output if not isinstance(references_output, Exception) else None,
            "finance": finance_output if not isinstance(finance_output, Exception) else None,
            "errors": [
                str(t) for t in tasks if isinstance(t, Exception)
            ]
        }
    
    async def review_contract(
        self,
        document_url: str,
        contract_type: str,
        deal_value: float,
        jurisdiction: str
    ) -> dict:
        """Delegates contract review to legal agent."""
        return await self.client.delegate_task(
            agent_id="legal-agent",
            skill_id="contract-review",
            input_data={
                "document_url": document_url,
                "contract_type": contract_type,
                "deal_value": deal_value,
                "customer_jurisdiction": jurisdiction,
                "urgency": "urgent" if deal_value > 500_000 else "standard"
            }
        )
    
    async def build_competitive_response(
        self,
        competitor_name: str,
        crm_deal_id: str,
        deal_context: str
    ) -> dict:
        """Combines competitive-intelligence + customer-success for displacement stories."""
        intel_task, references_task = await asyncio.gather(
            self.client.delegate_task(
                agent_id="presales-agent",  # self — competitive-intelligence skill
                skill_id="competitive-intelligence",
                input_data={
                    "competitor_names": [competitor_name],
                    "deal_context": deal_context,
                    "output_type": "battle-card"
                }
            ),
            self.client.delegate_task(
                agent_id="customer-success-agent",
                skill_id="reference-match",
                input_data={
                    "prospect_profile": {"competitive_displacement": competitor_name},
                    "reference_type": "case-study"
                }
            ),
            return_exceptions=True
        )
        
        return {
            "competitive_intel": intel_task if not isinstance(intel_task, Exception) else None,
            "displacement_references": references_task if not isinstance(references_task, Exception) else None
        }
```

---

## Agent Discovery Endpoint

Register this endpoint in your infrastructure to expose all org agents:

```python
# FastAPI example — serves the agent card registry
from fastapi import FastAPI, HTTPException
import json
from pathlib import Path

app = FastAPI()
AGENT_CARDS_DIR = Path("a2a/agents")

@app.get("/.well-known/agent-cards")
async def list_agent_cards():
    """Returns all registered agent cards."""
    cards = []
    for card_file in AGENT_CARDS_DIR.glob("*-card.json"):
        with open(card_file) as f:
            cards.append(json.load(f))
    # Include the presales agent's own card
    with open("a2a/agent-card.json") as f:
        cards.append(json.load(f))
    return cards

@app.get("/.well-known/agent-cards/{agent_id}")
async def get_agent_card(agent_id: str):
    """Returns a specific agent's card."""
    # Search in agents directory
    for card_file in AGENT_CARDS_DIR.glob(f"{agent_id}-card.json"):
        with open(card_file) as f:
            return json.load(f)
    # Check presales agent card
    if agent_id == "presales-agent":
        with open("a2a/agent-card.json") as f:
            return json.load(f)
    raise HTTPException(status_code=404, detail=f"Agent '{agent_id}' not found")
```

---

## Configuration

### A2A Settings in `settings.local.json`

```json
{
  "a2a": {
    "enabled": true,
    "discovery_url": "https://agents.your-company.com",
    "auth_token_env": "A2A_AUTH_TOKEN",
    "delegation_policy": {
      "max_concurrent_delegations": 3,
      "timeout_seconds": 120,
      "fallback": "notify_human",
      "auto_delegate": [
        "legal-agent",
        "pricing-agent",
        "customer-success-agent",
        "finance-agent",
        "technical-architecture-agent"
      ]
    },
    "trigger_keywords": {
      "legal-agent": ["contract", "msa", "nda", "sow", "legal review", "compliance"],
      "pricing-agent": ["pricing", "discount", "quote", "investment"],
      "finance-agent": ["roi", "business case", "payback", "cfo approval", "cost justification"],
      "customer-success-agent": ["reference", "case study", "similar customer", "proof point"],
      "technical-architecture-agent": ["architecture", "design", "estimate", "technical review"]
    }
  }
}
```

---

## Security

### Authentication
All A2A calls use bearer tokens issued by your org's central auth service (`https://auth.your-company.com/token`). Each agent validates the calling agent's identity before processing a task.

### Authorization
Agents enforce skill-level authorization:
- `legal-agent` only accepts tasks from `presales-agent` and `manager-agent`
- `pricing-agent` enforces discount thresholds regardless of calling agent
- Discount requests above threshold always escalate to a human — agents cannot approve exceptions autonomously

### Data Handling
- Agent-to-agent communication is internal (never external-facing)
- Customer data shared between agents is governed by your existing data processing agreements
- All A2A tasks are logged for audit: calling agent, target agent, skill, timestamp, deal ID

### Human Override
Any A2A delegation can be overridden or cancelled by a human via Slack:
```
/a2a cancel task_id:[task-id]
/a2a status task_id:[task-id]
/a2a list active
```

---

## File Structure

```
a2a/
├── A2A-Protocol-Guide.md              ← This document
├── agent-card.json                    ← Presales agent's own A2A card
├── agents/                            ← Org agent cards (read by discovery endpoint)
│   ├── legal-agent-card.json
│   ├── pricing-agent-card.json
│   ├── technical-architecture-agent-card.json
│   ├── customer-success-agent-card.json
│   └── finance-agent-card.json
├── orchestration/
│   ├── a2a_client.py                  ← A2A protocol client
│   ├── orchestrator.py                ← Multi-agent workflow orchestration
│   └── discovery_server.py            ← Agent card discovery endpoint (FastAPI)
└── tests/
    ├── test_a2a_client.py
    └── test_orchestrator.py
```

---

## Roadmap

| Phase | Feature | Status |
|---|---|---|
| 1 | Agent cards for all 5 org agents | ✅ Complete |
| 1 | A2A client (Python) | ✅ Complete |
| 1 | Orchestration layer for parallel delegation | ✅ Complete |
| 1 | Discovery endpoint (FastAPI) | ✅ Complete |
| 2 | Streaming A2A responses (real-time output) | Planned |
| 2 | Slack `/a2a` management commands | Planned |
| 2 | A2A task audit log in Notion | Planned |
| 3 | Additional org agents: HR, Procurement, Marketing | Planned |
| 3 | A2A federation (agents from partner orgs) | Future |

---

*Branch: `claude/a2a-agent-protocol` · Protocol: Google A2A v1.0 · Last updated: May 2026*
