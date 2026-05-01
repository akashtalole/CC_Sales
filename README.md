# CC Sales — AI-Powered Presales Agent

End-to-end AI agent-driven presales automation for tech services teams, built on [Claude](https://claude.ai) agents via Claude Code / Cowork and the [knowledge-work-plugins/sales](https://github.com/anthropics/knowledge-work-plugins/tree/main/sales) plugin.

---

## Quick Start

```bash
# 1. Install the sales plugin
claude plugins add knowledge-work-plugins/sales

# 2. Configure your profile
cp settings.example.json ~/.claude/settings.local.json
# Edit with your name, company, quota, and product details

# 3. Set up MCP integrations (CRM, Calendar, Email, etc.)
# See setup/mcp-setup-guide.md

# 4. Test your first agent skill
claude "Run account-research on [company.com] and post a brief to Notion"
```

---

## Repository Structure

```
CC_Sales/
├── AI-Powered-Presales-Playbook.md    ← Start here: full strategy & workflow guide
│
├── prompts/                            ← Role-specific prompt libraries
│   ├── sdr-prompts.md                 ← SDR: research, outreach, qualification
│   ├── ae-prompts.md                  ← AE: call prep, summaries, proposals
│   ├── presales-engineer-prompts.md   ← SE: technical discovery, assets
│   └── manager-prompts.md             ← Manager: pipeline, forecast, coaching
│
├── templates/                          ← Structured output templates
│   ├── notion-deal-room-template.md   ← 5-tab deal room structure
│   ├── call-summary-template.md       ← MEDDIC-aligned call summary
│   └── proposal-template.md           ← 3-option proposal structure
│
└── setup/                              ← Configuration & integration guides
    ├── mcp-setup-guide.md             ← MCP authentication (all 10 servers)
    ├── crm-field-reference.md         ← CRM custom fields for AI tracking
    └── slack-channel-setup.md         ← Slack channels and bot configuration
```

---

## What This Does

Claude agents handle the manual overhead of presales so your team spends more time selling:

| Agent Skill | What It Automates | Time Saved |
|---|---|---|
| `account-research` | Company intel, tech stack, news, pain signals | 45 min → 5 min |
| `call-prep` | Pre-call brief from CRM + transcripts + enrichment | 60 min → 10 min |
| `daily-briefing` | Morning deal priorities and action items | 45 min → 2 min |
| `draft-outreach` | Personalized email/LinkedIn sequences | 30 min → 3 min |
| `competitive-intelligence` | Competitor mentions, differentiation, talk tracks | Hours → automatic |
| `create-an-asset` | Proposal drafts, one-pagers, technical summaries | 8-16 hrs → 1-2 hrs |
| `/call-summary` | MEDDIC extraction, action items, follow-up draft | 20 min → 2 min |
| `/pipeline-review` | Pipeline health, risk flags, action plan | 3 hrs → 20 min |
| `/forecast` | Weighted forecast, best/likely/worst scenarios | 1 hr → 5 min |

**Target outcome:** Increase AE direct selling time from 28% to 50%+ of their week.

---

## 7-Stage Presales Workflow

```
1. Prospecting     → account-research + competitive-intelligence
2. Research        → account-research (deep) → Notion deal room created
3. Outreach        → draft-outreach → SDR review → sequence activated
4. Discovery Call  → call-prep (pre) → /call-summary (post)
5. Proposal        → create-an-asset → AE/SE review → sent to prospect
6. Follow-Up       → daily-briefing + draft-outreach (re-engagement)
7. Close           → call-prep + /call-summary + /forecast update
```

See [AI-Powered-Presales-Playbook.md](./AI-Powered-Presales-Playbook.md) for the full workflow with sample prompts for each stage.

---

## Key Integrations (MCP Servers)

| Category | Supported Tools |
|---|---|
| CRM | HubSpot, Salesforce |
| Call Recording | Fireflies, Gong |
| Data Enrichment | Clay, ZoomInfo |
| Email | Gmail, Microsoft 365 |
| Calendar | Google Calendar, Microsoft 365 |
| Collaboration | Slack, Microsoft Teams |
| Knowledge Base | Notion, Confluence |

---

## Agent-to-Agent Protocol (A2A)

This repo also includes an A2A (Agent-to-Agent) implementation on the `claude/a2a-agent-protocol` branch, enabling the presales agent to delegate tasks to specialized org agents:

- **Legal Agent** — contract review, compliance checks
- **Pricing Agent** — dynamic pricing, discount approval
- **Technical Architecture Agent** — solution design, estimation
- **Customer Success Agent** — reference requests, case studies
- **Finance Agent** — ROI calculations, business case support

See the `a2a/` directory on the `claude/a2a-agent-protocol` branch for protocol documentation and agent cards.

---

## Human-in-the-Loop Principle

> All externally-facing outputs (emails, proposals, LinkedIn messages) require human review and approval before sending. Agents draft; humans send.

---

## License

Apache 2.0 — see [LICENSE](./LICENSE)
