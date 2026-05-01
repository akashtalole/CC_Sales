# AI-Powered Presales: End-to-End Automation with Claude Agents

> **Powered by:** [Anthropic Claude](https://claude.ai) · [knowledge-work-plugins/sales](https://github.com/anthropics/knowledge-work-plugins/tree/main/sales) · Claude Code / Cowork

---

## Table of Contents

1. [Executive Overview](#1-executive-overview)
2. [Presales Team Structure with AI Agents](#2-presales-team-structure-with-ai-agents)
3. [End-to-End Presales Workflow](#3-end-to-end-presales-workflow)
4. [Tool Integrations (MCP Configuration)](#4-tool-integrations-mcp-configuration)
5. [Implementation Guide](#5-implementation-guide)
6. [ROI and Conversion Metrics](#6-roi-and-conversion-metrics)
7. [Sample Prompts and Usage Examples](#7-sample-prompts-and-usage-examples)
8. [Appendices](#appendices)

---

## 1. Executive Overview

### 1.1 The Problem: Why Traditional Presales Breaks Down at Scale

Modern tech services presales teams face a structural time problem. Research consistently shows that SDRs spend **60–70% of their time on non-selling activities** — manual account research, CRM data entry, writing repetitive outreach emails, and preparing for calls without a systematic briefing process.

The downstream effects compound across every deal stage:

- **Account Executives** enter discovery calls under-prepared. Without a structured research brief, they cover generic ground and miss the personalized insight that separates them from competitors.
- **Presales Engineers** get pulled into deals too late and without full context on prior conversations, forcing them to re-discover requirements already uncovered.
- **Pipeline reviews** are backward-looking snapshots. Managers learn about at-risk deals after the window to intervene has closed.
- **Proposals** take 3–5 business days to produce. Deals go cold waiting.
- The average presales team spends only **28% of their time on direct selling activity**. The remaining 72% is overhead that AI can absorb.

### 1.2 The Solution: Claude Agents as Presales Team Members

Claude agents — deployed via **Claude Code** or **Cowork** (Anthropic's desktop agentic application) with the [sales plugin](https://github.com/anthropics/knowledge-work-plugins/tree/main/sales) — act as always-on, context-aware junior members of the presales team.

This is not a chatbot. Claude agents:

- **Read your live systems** — CRM deals, email threads, calendar events, call transcripts — via MCP (Model Context Protocol) connectors
- **Act on triggers** — a new calendar event auto-generates a pre-call brief; a deal stage change auto-drafts a proposal outline
- **Write back** — agents create CRM activities, Notion deal room pages, Gmail drafts, and Slack summaries without human effort
- **Operate in two modes:**
  - **Slash commands** (e.g., `/call-summary`, `/pipeline-review`, `/forecast`) — manually invoked by team members
  - **Auto-triggered skills** (e.g., `account-research`, `call-prep`, `daily-briefing`) — fire automatically based on system events

> **Key Principle:** Agents are augmentation, not replacement. Every externally-facing output — emails, proposals, outreach — routes through a human review gate before it is ever sent.

### 1.3 Scope of This Document

| Applies To | Tech Stack Assumed |
|---|---|
| Sales Development Reps (SDRs) | HubSpot or Salesforce (CRM) |
| Account Executives (AEs) | Gmail + Google Calendar |
| Presales / Solutions Engineers (SEs) | Slack |
| Sales Managers | Notion (knowledge base + deal rooms) |
| RevOps / Marketing | Gong or Fireflies (call recording) |
| | Clay or ZoomInfo (data enrichment) |

---

## 2. Presales Team Structure with AI Agents

### 2.1 Role Table: Humans + Agents

| Role | Human Responsibility | Agent Skills Used | Time Reclaimed |
|---|---|---|---|
| **SDR** | Qualifying intent, booking meetings, managing sequences | `account-research`, `draft-outreach`, `competitive-intelligence` | ~4 hrs/day |
| **Account Executive** | Relationship ownership, deal strategy, negotiation | `call-prep`, `daily-briefing`, `/call-summary`, `/forecast` | ~3 hrs/day |
| **Presales / SE** | Technical validation, architecture, demo design | `create-an-asset`, `call-prep` (technical variant), `/call-summary` | ~2.5 hrs/day |
| **Sales Manager** | Coaching, forecast accuracy, pipeline health | `/pipeline-review`, `/forecast`, `daily-briefing` | ~4 hrs/week |
| **RevOps / Marketing** | Content, tooling, ICP definition | `create-an-asset`, MCP configuration | ~2 hrs/week |

### 2.2 Agent Personas: What Each Skill "Acts As"

| Skill | Agent Persona | What It Does |
|---|---|---|
| `account-research` | Business Analyst | Enriches new leads with company financials, tech stack signals, recent news, hiring trends, funding history |
| `call-prep` | Research Assistant | Synthesizes CRM history + enrichment + prior transcripts into a structured pre-call briefing doc |
| `daily-briefing` | Chief of Staff | Surfaces priority actions, deal movements, and at-risk opportunities each morning to each AE |
| `draft-outreach` | Copywriter | Writes personalized cold/warm outreach sequences tuned to ICP persona and deal stage |
| `competitive-intelligence` | Market Analyst | Tracks competitor mentions in transcripts and enrichment; generates differentiation matrices |
| `create-an-asset` | Content Producer | Generates tailored one-pagers, technical summaries, proposal sections, and demo scripts |

### 2.3 Human-in-the-Loop Design Principle

> **Human Review Gate:** All agent outputs that will be sent to prospects or customers — emails, proposals, LinkedIn messages — must be reviewed and approved by a human before sending. Agents draft; humans send.

The review workflow:
1. Agent posts output to a designated Slack channel (`#presales-agents`) or Notion deal room page
2. Team member receives a Slack notification with a direct link to the draft
3. Team member edits, approves, and sends — or rejects with a comment to re-generate
4. Agent logs the review outcome in CRM for quality tracking

**Confidence indicators:** Every agent output includes a brief confidence note:
- Data freshness (when was the enrichment data last updated?)
- Source count (how many sources were used for the research?)
- Gaps flagged (what information was unavailable and should be verified manually?)

---

## 3. End-to-End Presales Workflow

The presales pipeline is divided into 7 stages. At each stage, Claude agents absorb the manual overhead so the human team focuses on judgment, relationship, and strategy.

```
Prospecting → Research → Outreach → Discovery Call → Proposal → Follow-Up → Close
     ↑                                                                          |
     └──────────────── Win/Loss data feeds back to improve agents ─────────────┘
```

---

### Stage 1: Prospecting

**Goal:** Build a qualified target account list (TAL) from ICP criteria.

| | Before AI | After AI |
|---|---|---|
| Account identification | Manual LinkedIn/ZoomInfo search | `account-research` auto-triggers on CRM new record creation |
| List scoring | Spreadsheet-based manual scoring | Clay MCP enrichment with automated ICP scoring |
| Sequence templates | Written from scratch per segment | `draft-outreach` generates segment-specific templates |
| Competitive landscape | Static quarterly research | `competitive-intelligence` runs weekly to update TAL priorities |

**Skills invoked:**
- `account-research` — triggered on new HubSpot/Salesforce company creation
- `competitive-intelligence` — weekly scheduled run
- `draft-outreach` — generates initial outreach templates per ICP segment

**Inputs:** ICP criteria documented in Notion, CRM new record event, Clay/ZoomInfo enrichment data
**Outputs:** Enriched company profiles in CRM, scored TAL, initial outreach sequence drafts in Notion

> **Time Saved:** Account research drops from 45 minutes per account to 5 minutes (human review of agent output).

**Handoff to Stage 2:** Account meets minimum enrichment score; at least one ICP-qualifying signal present.

---

### Stage 2: Research & Enrichment

**Goal:** Build deep account intelligence before any human contact.

| | Before AI | After AI |
|---|---|---|
| Company news research | Manual Google search | `account-research` pulls press, funding rounds, earnings calls, job postings |
| Tech stack identification | BuiltWith manual lookup | Clay/ZoomInfo MCP enrichment integrated automatically |
| Pain point hypothesis | AE intuition | Agent synthesizes signals into 3 prioritized pain hypotheses |
| Competitor mapping | Occasional manual research | `competitive-intelligence` generates competitor landscape per account |

**Skills invoked:**
- `account-research` — triggered by SDR marking account "In Research" in CRM
- `competitive-intelligence` — triggered on research completion

**Inputs:** Company domain, LinkedIn URL, CRM contact data
**Outputs:** Research brief posted to Notion deal room (company overview, tech stack, recent triggers, competitor landscape, pain point hypotheses, recommended talk track)

```
Sample Prompt for account-research:

"Run account-research for Acme Corp (acme.com). Focus on:
- Cloud infrastructure spend signals
- Recent hiring in DevOps/Platform Engineering roles
- Any public mentions of cost optimization initiatives
- Last 3 funding rounds and current valuation estimate
Output a one-page brief to the Notion deal room. Flag data older than 90 days."
```

**Handoff to Stage 3:** Research brief reviewed and approved by SDR/AE within 24 hours.

---

### Stage 3: Outreach

**Goal:** Generate personalized, high-conversion outreach sequences.

| | Before AI | After AI |
|---|---|---|
| Cold email writing | 30 min per sequence from scratch | `draft-outreach` produces full 5-touch sequence in 3 min |
| Persona variants | One generic version | Agent generates CTO / VP Eng / CFO variants automatically |
| Follow-up cadence | Manual tracking in spreadsheet | Agent monitors reply status via Gmail MCP, drafts follow-ups |
| LinkedIn messages | Written ad hoc | Agent produces connection request + follow-up message |

**Skills invoked:**
- `draft-outreach` — auto-triggered after research brief is approved; also manually invokable
- Gmail MCP — for send tracking and reply detection
- Google Calendar MCP — for meeting link insertion in sequence

**Inputs:** Approved research brief, ICP persona definition (from Notion), historical sequence performance data
**Outputs:** 3–5 email sequence drafts in Notion, LinkedIn message draft, SDR review queue item posted to Slack

```
Sample Prompt for draft-outreach:

"Draft a 4-touch cold outreach sequence for the VP of Engineering at Acme Corp.
Use the research brief from the Acme Corp deal room.
Persona: technically fluent, skeptical of vendor hype, motivated by developer productivity.
Reference their recent Series C and 40% engineering headcount growth in 6 months.
Touch 1: email (120 words max). Touch 2: email follow-up (80 words). 
Touch 3: LinkedIn message (280 chars). Touch 4: breakup email (60 words).
Tone: peer-to-peer, not salesy. No buzzwords."
```

> **Time Saved:** Sequence drafting drops from 30 minutes to 3 minutes. Reply rates typically improve 20–35% with personalization from research briefs.

**Handoff to Stage 4:** SDR approves and activates sequence; prospect responds and meeting is booked.

---

### Stage 4: Discovery Call

**Goal:** Run a structured discovery call that captures full context and drives clear next steps.

#### Pre-Call (2 hours before)

`call-prep` auto-triggers when a Google Calendar event is created/updated with a prospect email domain in the attendee list.

**Outputs to Notion deal room:**
- Account summary (from CRM + enrichment)
- Prior interactions summary (emails, previous calls)
- 5 open discovery questions tailored to the account's industry and pain signals
- MEDDIC framework template pre-populated with known fields
- Competitive landscape: who else they're likely evaluating and differentiation points
- 3 custom talk track bullets based on the research brief

#### During Call (passive)

- Fireflies or Gong records and transcribes in real time via MCP
- No agent interruption during the call — the human drives

#### Post-Call (within 15 minutes)

AE invokes `/call-summary` in Slack with the meeting name or attaches the transcript.

**Outputs:**
- Structured call summary with MEDDIC fields populated from transcript
- Prioritized action items with suggested owners and due dates
- Follow-up email draft ready for AE review in Gmail drafts
- CRM update recommendations (stage, close date, deal value)
- Deal health score delta (improved / declined / neutral vs. prior call)

```
Sample Prompt for /call-summary:

"/call-summary Acme Corp discovery call — transcript from Fireflies attached.

Extract:
1. Buyer's stated pain in their own words (direct quotes preferred)
2. Economic buyer identified: Y/N, name, title
3. Decision criteria mentioned explicitly
4. Competitors mentioned by prospect
5. Next steps agreed on-call with specific dates
6. My action items with due dates
7. MEDDIC gap analysis: which fields are still unknown?

Post summary to Acme Corp Notion deal room.
Draft follow-up email for my review. Keep email under 150 words."
```

> **Time Saved:** Post-call admin (CRM update + follow-up email) drops from 20 minutes to 2 minutes.

**Handoff to Stage 5:** AE confirms MEDDIC qualification threshold met; deal moves to "Discovery Complete" in CRM.

---

### Stage 5: Proposal / Solution Design

**Goal:** Produce a technically credible, commercially compelling proposal faster than competitors.

| | Before AI | After AI |
|---|---|---|
| SOW/proposal first draft | 8–16 hours, presales engineer + AE | `create-an-asset` generates first draft in 15–30 min |
| Pricing scenarios | Manual calculation and formatting | Agent pulls pricing tiers from Notion, assembles 3 options |
| Executive summary | Written last, often rushed | Agent drafts from discovery findings first |
| Technical validation prep | SE reads call notes manually | `call-prep` (SE variant) produces technical discovery brief |

**Skills invoked:**
- `create-an-asset` — invoked by AE or SE after Discovery Complete stage
- `call-prep` (technical variant) — for any technical validation or architecture calls
- `/call-summary` — on all technical deep-dive calls

**Inputs:** Approved call summary, MEDDIC fields from CRM, service catalog in Notion, pricing tiers in Notion, competitive intel
**Outputs:** Proposal draft in Notion with: executive summary, problem statement, proposed solution, implementation approach, investment summary (3 options), next steps

```
Sample Prompt for create-an-asset:

"Create a proposal draft for Acme Corp.

Context:
- Need: cloud migration of 40 legacy microservices to AWS EKS
- Timeline: 6 months
- Budget signal: $800K–$1.2M
- Primary concern: zero-downtime migration ('our platform team is drowning in infrastructure toil')
- Economic buyer: CFO + CTO co-deciding
- Competitor in evaluation: [Competitor Name]

Use our standard Managed Cloud Services proposal template from Notion.
Include 3 engagement tiers: Essentials / Standard / Premium.
Tailor the executive summary to their stated pain about infrastructure toil.
Highlight our zero-downtime migration methodology as primary differentiator."
```

> **Time Saved:** Proposal first draft drops from 8–16 hours to 1–2 hours (agent draft + human polish).

**Handoff to Stage 6:** Proposal reviewed internally, approved by sales manager, sent to prospect.

---

### Stage 6: Follow-Up & Nurture

**Goal:** Maintain momentum, handle objections, and keep multi-stakeholder deals alive.

| | Before AI | After AI |
|---|---|---|
| Check-in emails | Written manually, often delayed | `draft-outreach` drafts stage-appropriate nurture by deal age |
| Objection handling | AE recalls from memory | Agent surfaces similar objections from past transcripts and win/loss notes |
| Stalled deal detection | Manager notices in weekly review | `daily-briefing` flags deals with no activity >14 days, every morning |
| Re-engagement | Ad hoc, often too late | Agent drafts re-engagement with fresh insight (news, trigger event) |

**Skills invoked:**
- `daily-briefing` — auto-triggered each morning for each AE and manager
- `draft-outreach` — for re-engagement drafts and check-in messages
- `/pipeline-review` — invoked by manager weekly (Fridays)
- `competitive-intelligence` — monitors for competitor news relevant to open deals

```
Sample Prompt for re-engagement via draft-outreach:

"My deal with Acme Corp has been in 'Proposal Sent' for 11 days with no response.
Draft a re-engagement email that:
1. Doesn't feel desperate or pushy
2. Adds new value — reference the article about their competitor launching 
   a new platform product last week (link: [article])
3. Proposes a specific 20-minute call to address any questions
4. Has a clear subject line that will get opened
Keep body under 100 words. Don't use 'just checking in.'"
```

> **Time Saved:** Daily briefing replaces 45-minute manual pipeline review. Stalled deal detection improves from ~40% caught to ~95% caught before they go cold.

**Handoff to Stage 7:** Prospect confirms intent to proceed; legal/procurement engaged.

---

### Stage 7: Close & Handoff

**Goal:** Accelerate final decision, capture win/loss learning, hand off to delivery cleanly.

| | Before AI | After AI |
|---|---|---|
| Closing call preparation | AE reviews notes manually | `call-prep` generates closing brief: deal history, objections, concessions, BATNA |
| Win/loss documentation | Rarely done, inconsistent | `/call-summary` on close call auto-generates structured win/loss record |
| Customer onboarding brief | Written by SE from scratch | `create-an-asset` produces delivery handoff doc from deal history |
| Forecast update | Manual CRM edit | `/forecast` re-runs with updated close probability and stage data |

```
Sample Prompt for /forecast on close:

"/forecast Generate updated Q2 forecast after Acme Corp marked Closed-Won.
Update weighted pipeline total.
Show: best case / likely / worst case.
Flag any remaining open deals where close date is within 30 days 
but MEDDIC score is below 70%.
Output to #sales-forecast Slack channel."
```

> **Closed Loop:** Win/loss data from `/call-summary` outputs feeds back to `competitive-intelligence` and the prompt library, making future agent outputs progressively better.

---

## 4. Tool Integrations (MCP Configuration)

### 4.1 MCP Integration Map

| MCP Server | Primary Purpose | Triggered By | Scopes Required |
|---|---|---|---|
| **HubSpot / Salesforce** | CRM read/write: contacts, deals, activities, stage | All agents (read); `/call-summary`, `account-research` (write) | contacts.read/write, deals.read/write, activities.write |
| **Fireflies / Gong** | Transcript ingestion, meeting recording retrieval | `call-prep` (read history), `/call-summary` (ingest latest) | transcripts.read, meetings.read |
| **Clay / ZoomInfo** | Contact and company enrichment | `account-research` (primary data source) | search.read, enrich.read |
| **Gmail** | Email draft creation, send history, reply tracking | `draft-outreach` (write drafts), `daily-briefing` (read activity) | drafts.create, labels.read, threads.read (NOT send) |
| **Google Calendar** | Meeting detection, attendee parsing | `call-prep` (trigger), `daily-briefing` (read schedule) | events.read |
| **Slack** | Agent output routing, notifications, command invocation | All agents (post outputs); humans (invoke commands) | channels.write, messages.write |
| **Notion** | Deal rooms, knowledge base, document storage | All agents (read templates, write outputs) | pages.read/write, databases.read/write |

> **Security Note:** Gmail MCP is granted `drafts.create` only — NOT `messages.send`. Agents draft; humans send. This is a deliberate architectural constraint.

### 4.2 Data Flow Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        TRIGGER LAYER                            │
│  Calendar event · CRM stage change · Slack command · Cron job  │
└─────────────────────────┬───────────────────────────────────────┘
                          │
┌─────────────────────────▼───────────────────────────────────────┐
│                        AGENT LAYER                              │
│         Claude Agent reads context via MCP connectors           │
│   CRM + Transcripts + Email + Calendar + Enrichment + Notion    │
└─────────────────────────┬───────────────────────────────────────┘
                          │
┌─────────────────────────▼───────────────────────────────────────┐
│                        OUTPUT LAYER                             │
│     CRM activities · Gmail drafts · Notion pages · Slack posts  │
└─────────────────────────┬───────────────────────────────────────┘
                          │
┌─────────────────────────▼───────────────────────────────────────┐
│                     HUMAN REVIEW LAYER                          │
│        All external-facing outputs reviewed before send         │
│         Slack approval workflow · Notion comment threads        │
└─────────────────────────────────────────────────────────────────┘
```

### 4.3 Standalone vs. Supercharged Modes

| Mode | What Works | What's Missing |
|---|---|---|
| **Standalone** | All skills work with web search + user input | No live CRM data, no transcript auto-ingestion |
| **Supercharged** | Full context from all MCP connectors | Requires authentication setup (see Section 5) |

Start teams in Standalone mode during pilot; layer in MCP integrations progressively.

---

## 5. Implementation Guide

### 5.1 Prerequisites

- [ ] Claude Code or Cowork environment provisioned for each team member
- [ ] Sales plugin installed: `claude plugins add knowledge-work-plugins/sales`
- [ ] `settings.local.json` configured per user (name, title, company, quota, product info)
- [ ] Notion workspace with deal room template created (see Appendix A)
- [ ] Slack workspace with designated channels created (see `setup/slack-channel-setup.md`)
- [ ] CRM custom fields added (see `setup/crm-field-reference.md`)

### 5.2 Skill Trigger Conditions Reference

| Skill | Trigger Event | Required Condition |
|---|---|---|
| `account-research` | New company created in CRM | Company domain present |
| `call-prep` | Calendar event created/updated | External attendee domain matches CRM account |
| `daily-briefing` | 7:00 AM local time (cron) | AE has ≥1 open deal in pipeline |
| `draft-outreach` | Deal stage → "Outreach" | Research brief exists in Notion deal room |
| `competitive-intelligence` | New transcript processed | Competitor name in transcript OR weekly cron (Fridays) |
| `create-an-asset` | Deal stage → "Proposal" | Call summary + MEDDIC fields present in CRM |

### 5.3 Phase 1: Foundation Setup (Weeks 1–2)

**Goal:** Get infrastructure in place before any agent touches live deals.

1. Install and authenticate all MCP servers (follow `setup/mcp-setup-guide.md`)
2. Create Notion deal room template with 5 tabs: Overview · Calls · Proposals · Agent Outputs · Action Items
3. Configure Slack channel routing: `#presales-agents` (all agent outputs), `#daily-briefing` (morning digests), `#pipeline-review` (Friday reviews)
4. Add CRM custom fields: AI Research Score, Last Agent Activity, Agent Confidence Flag, AI-Assisted (Y/N)
5. Run a test cycle with a sandbox/demo account to validate all MCP connections
6. Conduct 2-hour team training on slash commands and how to review/edit agent outputs

### 5.4 Phase 2: Pilot with One AE Pod (Weeks 3–4)

**Goal:** Validate agent quality with real deals before full rollout.

1. Select 1 AE + 1 SDR + 1 SE as the pilot pod
2. Enable auto-triggered skills for pilot team only (use feature flag in `settings.local.json`)
3. Run 5 active deals through the full workflow: Prospecting → Close
4. Collect structured feedback after each stage:
   - Research brief accuracy (1–5 rating)
   - Outreach draft quality (1–5 rating)
   - Call summary completeness (1–5 rating)
   - Time saved (estimate in minutes)
5. Tune Notion knowledge base based on identified gaps (ICP definition, service catalog, pricing tiers)

**Success criteria to advance:** Average skill rating ≥ 3.5/5, time saved ≥ 50% vs. baseline

### 5.5 Phase 3: Team Rollout (Weeks 5–8)

1. Roll out to full presales team with access to all skills
2. Establish review protocols: SDR approves outreach drafts; AE approves call summaries and proposals; Manager approves forecast runs
3. Create a shared "Prompt Library" Notion page — team adds best-performing prompts with ratings
4. Set up weekly `/pipeline-review` cadence: every Friday 4pm, manager invokes in `#pipeline-review`
5. Set up daily `daily-briefing`: auto-posts to each AE's Slack DM at 7am local time

### 5.6 Phase 4: Optimization (Ongoing)

| Cadence | Activity |
|---|---|
| Weekly | Review agent skill output quality ratings; update prompt library |
| Monthly | Review conversion metrics (AI-Assisted vs. Manual CRM tags); survey AE satisfaction |
| Quarterly | Refresh ICP definition, service catalog, and pricing tiers in Notion |
| Quarterly | `competitive-intelligence` deep-dive: update competitor profiles in Notion |
| Annually | Review MCP integrations; evaluate new enrichment sources |

---

## 6. ROI and Conversion Metrics

### 6.1 Baseline Metrics to Capture Before Deployment

Measure these for 4 weeks before activating any agents:

- Time-to-first-outreach (new lead → first touch, in hours)
- Outreach reply rate (%)
- Pre-call prep time per AE (hours/week)
- Post-call admin time per AE (hours/week)
- Proposal turnaround time (calendar days)
- Pipeline review prep time for manager (hours/week)
- Lead → Opportunity conversion rate (%)
- Opportunity → Close rate (%)
- Average sales cycle length (calendar days)
- CRM data completeness score (% of required fields populated)

### 6.2 Expected Impact by Stage

| Stage | Metric | Typical Baseline | Target with AI |
|---|---|---|---|
| Prospecting | Research time per account | 45 min | 5 min |
| Outreach | Sequence draft time | 30 min | 3 min |
| Outreach | Reply rate improvement | Baseline | +20–35% |
| Discovery | Pre-call prep time | 60 min | 10 min |
| Discovery | Post-call admin time | 20 min | 2 min |
| Proposal | First draft turnaround | 8–16 hrs | 1–2 hrs |
| Follow-up | Stalled deals detected early | ~40% | ~95% |
| Pipeline Review | Manager prep time | 3 hrs/week | 20 min/week |
| Overall | AE time on direct selling | 28% of week | 50%+ of week |

### 6.3 KPI Dashboard Recommendations

**Weekly (Sales Manager):**
- Reply rates by sequence variant (agent-drafted vs. manual)
- Deals progressed per stage this week
- Agent skill usage rate by team member (adoption tracking)
- New deals with AI Research Score ≥ threshold

**Monthly (Sales + RevOps):**
- Conversion rate by stage: AI-Assisted deals vs. unassisted
- Proposal win rate trend
- Average sales cycle length trend
- AE capacity freed (hours) — calculate from weekly time-saved surveys

**Quarterly (Leadership):**
- Revenue influenced by AI-Assisted deals vs. unassisted
- CRM data quality score trend (completeness %)
- Prompt library growth (# of approved prompts)
- Competitive intelligence accuracy (% of competitive mentions correctly identified)

### 6.4 Measurement Framework: Controlled Comparison

For the first 90 days, tag every CRM deal as either `AI-Assisted: Yes` or `AI-Assisted: No`. This enables a controlled comparison that isolates agent impact from other variables (territory, rep tenure, deal size).

Track:
- Which specific agent outputs correlated with deals that progressed
- Which outreach sequences (agent-drafted) had the highest reply-to-meeting conversion
- Which call summaries led to proposals vs. which led to deal stalls

Survey AEs monthly with two questions:
1. Rate each skill's usefulness this month (1–5)
2. Estimate hours saved per week using agents

---

## 7. Sample Prompts and Usage Examples

> All prompts below are copy-paste ready. Replace `[bracketed text]` with your specifics.
> For the full prompt library organized by role, see the `prompts/` directory.

### 7.1 SDR Prompts

**Account research trigger:**
```
Run account-research on [Company Name] ([company.com]).

I need:
- Funding history (all rounds, total raised, lead investors)
- Tech stack (especially cloud, DevOps, data infrastructure tools)
- Headcount trend over last 12 months (growing/shrinking which teams?)
- Any recent leadership changes in Engineering or IT
- 3 personalized pain point hypotheses for a [your service] pitch

Output: one-page brief to the [Company] Notion deal room.
Flag any data points older than 90 days.
```

**Cold email — first touch:**
```
Draft a cold email to [First Name], [Title] at [Company].

Context from research brief:
- They recently raised [round] and are hiring aggressively for [team]
- Their stated public challenge: [quote from press release/LinkedIn]
- Our relevant differentiator: [specific value prop]

Tone: peer-to-peer, technically credible, not salesy.
Max 120 words. No buzzwords.
Subject line: 3 options, A/B testable.
```

**LinkedIn connection request:**
```
Write a LinkedIn connection request from me to [Name], [Title] at [Company].
Reference their recent post about [topic].
Maximum 280 characters. No "I came across your profile."
```

### 7.2 Account Executive Prompts

**Pre-call brief:**
```
Generate my call-prep brief for the discovery call with [Company] at [time] today.

Include:
- Account summary (company overview, our relationship history)
- Prior interactions (emails, previous calls, open commitments)
- 5 open discovery questions tailored to [their industry] + [specific challenge]
- MEDDIC template pre-populated with what we already know
- 2 likely objections with recommended responses
- Competitive landscape: who else they're likely evaluating
- 3 talk track bullets specific to their situation
```

**Post-call summary:**
```
/call-summary [Company] discovery call — [date].
Transcript: [attach Fireflies/Gong link or paste]

Extract:
1. Buyer's pain in their exact words (direct quotes)
2. Economic buyer: name, title, identified Y/N
3. Decision criteria stated explicitly
4. Competitors mentioned
5. Next steps agreed on-call with dates
6. My action items and due dates
7. MEDDIC gap analysis: which fields are still missing?

Post to [Company] Notion deal room.
Draft follow-up email for my review (under 150 words).
Update CRM deal stage and close date if discussed.
```

**Re-engagement email:**
```
My deal with [Company] has been in "[Stage]" for [N] days with no response.

Draft a re-engagement email that:
1. Doesn't feel desperate
2. Adds new value — use this insight: [paste relevant news/trigger event]
3. Proposes a specific [20]-minute call to address questions
4. Has a compelling subject line

Body under 100 words. Don't use "just checking in" or "circling back."
```

### 7.3 Presales / Solutions Engineer Prompts

**Technical discovery brief:**
```
Generate a technical discovery brief for [Company].

Context:
- They run [current architecture/stack]
- They want to [goal/migration/transformation]
- Deal stage: [stage]

Technical questions I need answered in the call:
- Architecture constraints and non-negotiables
- CI/CD maturity and current toolchain
- Security and compliance requirements ([SOC2/HIPAA/PCI/etc.])
- Team skill sets and platform engineering capacity
- Integration dependencies with existing systems

Output format: structured briefing doc in [Company] Notion deal room.
```

**Technical one-pager:**
```
Create a technical one-pager for [Company] summarizing our proposed [solution].

Audience: [their platform engineering lead / CTO / VP Engineering]
Tone: peer-to-peer, architectural, credible

Include:
- Current state summary (their pain)
- Proposed architecture overview (our approach)
- Migration/implementation phases
- Risk mitigations and how we address each
- Our toolchain and why it fits their stack
- "What success looks like at 90 days" section

Use our [service name] technical template from Notion.
```

### 7.4 Sales Manager Prompts

**Weekly pipeline review:**
```
/pipeline-review Analyze [AE Name or full team]'s [Q2] pipeline.

Flag:
1. Deals stuck in same stage for >21 days
2. Deals with no CRM activity in >10 days
3. Deals missing required MEDDIC fields
4. Deals where close date has slipped more than once
5. Single-threaded deals (only one contact engaged)

Output: priority action list by deal, with specific recommended next action.
Post to #pipeline-review Slack channel.
```

**Quarterly forecast:**
```
/forecast Generate weighted [Q2] forecast.

Weighting: Commit = 90%, Best Case = 50%, Pipeline = 20%
Quota: $[amount]

Show: best case / likely / worst case totals.
Gap to quota analysis.
Flag deals where close date is within 30 days but MEDDIC score < 70%.
Flag deals where AI confidence differs significantly from AE-stated probability.

Post to #sales-forecast with a summary narrative.
```

**Call coaching review:**
```
Review the call transcript from [AE Name]'s [call type] with [Company].

Score the call on:
1. Discovery depth: did they uncover economic impact and decision process?
2. Competitive positioning: did they differentiate effectively?
3. MEDDIC advancement: which new fields were populated?
4. Next step quality: specific, committed, calendar-booked?

Provide 3 specific coaching points with timestamps from the transcript.
Keep feedback constructive and example-based.
```

### 7.5 Workflow Automation Examples

**Morning routine — what `daily-briefing` produces:**

Each AE receives a Slack DM at 7am containing:
- Today's calls with pre-call brief links for each
- Top 3 deals needing action (no activity in past X days)
- At-risk deals with recommended next action
- 1 suggested prompt to use for the highest-priority deal

**Deal room auto-setup — what happens when a new opportunity is created in CRM:**
1. CRM triggers `account-research` for the company domain
2. `account-research` creates a Notion deal room from the template
3. Research brief is auto-populated in the Overview tab
4. `competitive-intelligence` runs and populates the Competitive section
5. Slack notification sent to assigned AE: "Deal room ready for [Company]" with direct Notion link
6. Total time: ~10 minutes from CRM record creation to fully populated deal room

**Weekly pipeline cadence:**
1. Every Friday at 4pm: manager invokes `/pipeline-review` in `#pipeline-review` Slack channel
2. Agent analyzes all open deals, posts structured report with priority action list
3. Manager reviews, assigns coaching conversations for Monday
4. AEs receive individual deal action items tagged in their DM by 4:30pm
5. Manager prep time: 20 minutes (review + follow-up) vs. 3 hours manual

---

## Appendices

### Appendix A: Notion Deal Room Template Structure

```
[Company Name] — Deal Room
├── Overview
│   ├── Account Summary (auto-populated by account-research)
│   ├── Key Contacts (synced from CRM)
│   ├── Deal Timeline (stage history)
│   └── Competitive Landscape (auto-populated by competitive-intelligence)
│
├── Calls
│   ├── Pre-Call Briefs (auto-populated by call-prep)
│   ├── Call Summaries (auto-populated by /call-summary)
│   └── Transcripts (linked from Fireflies/Gong)
│
├── Proposals
│   ├── Proposal Drafts (auto-populated by create-an-asset)
│   ├── Pricing Scenarios
│   └── Customer-Facing Final Version
│
├── Agent Outputs (raw)
│   ├── Research Briefs (unedited agent output, for audit trail)
│   ├── Outreach Drafts (before human edit)
│   └── Call Summary Drafts (before human edit)
│
└── Action Items
    ├── Open Items (with owner, due date, status)
    └── Completed Items
```

### Appendix B: CRM Custom Field Reference

| Field Name | Type | Values | Used By |
|---|---|---|---|
| `AI Research Score` | Number (0–100) | Enrichment completeness score | account-research |
| `AI Assisted` | Boolean | Yes / No | All agents (for measurement tagging) |
| `Last Agent Activity` | Date | Auto-updated on each agent write | All agents |
| `Agent Confidence Flag` | Select | High / Medium / Low / Needs Review | All agents |
| `MEDDIC Score` | Number (0–100) | Auto-calculated from MEDDIC field completion | /call-summary |
| `Competitive Threat` | Multi-select | List of competitors mentioned | competitive-intelligence |

### Appendix C: Plugin Installation

```bash
# Install the sales plugin
claude plugins add knowledge-work-plugins/sales

# Verify installation
claude plugins list

# Configure your personal settings
cat > ~/.claude/settings.local.json << EOF
{
  "name": "[Your Name]",
  "title": "[Your Title]",
  "company": "[Your Company]",
  "quota": {
    "annual": 1200000,
    "currency": "USD"
  },
  "product": {
    "name": "[Product/Service Name]",
    "value_props": [
      "[Value prop 1]",
      "[Value prop 2]",
      "[Value prop 3]"
    ],
    "competitors": ["[Competitor 1]", "[Competitor 2]"]
  }
}
EOF
```

### Appendix D: Prompt Tuning Guide

**Why agent output quality varies:**
Agent outputs are only as good as the context they receive. The three most common failure modes:

1. **Generic research brief** → ICP definition in Notion is too vague. Fix: add specific firmographic filters (revenue range, headcount range, industry SIC codes, tech stack requirements).

2. **Off-brand outreach drafts** → No tone/voice examples in Notion. Fix: add 3–5 examples of your best-performing emails as a "Voice Reference" page in Notion that agents can read.

3. **Incomplete call summaries** → Transcript quality is poor (background noise, crosstalk). Fix: use Fireflies/Gong speaker diarization; ensure all participants are on headsets.

**How to improve any output:**
- Add more context in your prompt (company background, deal history, buyer persona details)
- Specify output format explicitly ("use bullet points", "max 150 words", "include a table")
- Give examples inline ("similar to the Acme Corp proposal in Notion")
- Iterate: paste the draft back and ask "improve the executive summary to focus more on ROI impact"

### Appendix E: Glossary

| Term | Definition |
|---|---|
| **A2A** | Agent-to-Agent protocol — enables Claude presales agent to delegate tasks to other specialized agents in the org |
| **AE** | Account Executive — owns the customer relationship and deal strategy |
| **Auto-triggered skill** | An agent capability that fires automatically based on a system event (no human invocation needed) |
| **Deal room** | A Notion workspace page for a specific opportunity, containing all research, call notes, proposals, and agent outputs |
| **ICP** | Ideal Customer Profile — firmographic and behavioral definition of your best-fit prospect |
| **MCP** | Model Context Protocol — the integration layer that allows Claude agents to read from and write to external systems (CRM, email, calendar, etc.) |
| **MEDDIC** | Metrics · Economic Buyer · Decision Criteria · Decision Process · Identify Pain · Champion — a B2B sales qualification framework |
| **SDR** | Sales Development Representative — focuses on outbound prospecting and booking meetings |
| **SE / Presales Engineer** | Solutions Engineer — provides technical validation and designs solution architecture |
| **Slash command** | A manually invoked agent capability (e.g., `/call-summary`, `/pipeline-review`, `/forecast`) |
| **TAL** | Target Account List — a prioritized list of companies that match the ICP |

---

*Last updated: May 2026 · Maintained by RevOps · Questions: #presales-agents Slack channel*
