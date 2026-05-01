# Notion Deal Room Template

> Copy this structure for every new opportunity. Create one page per deal in Notion.
> Page title format: `[Company Name] — Deal Room`
> Agent outputs populate this page automatically when MCPs are configured.

---

## Page Properties (Notion Database Fields)

| Property | Type | Values |
|---|---|---|
| Company | Text | Account name |
| AE Owner | Person | Assigned account executive |
| SE Owner | Person | Assigned solutions engineer |
| SDR | Person | SDR who sourced the deal |
| Stage | Select | Prospecting / Research / Outreach / Discovery / Proposal / Negotiation / Closed Won / Closed Lost |
| Deal Value | Number | $ estimate |
| Close Date | Date | Target close date |
| AI Research Score | Number | 0–100 (auto-populated by account-research) |
| AI Assisted | Checkbox | Checked when any agent has contributed |
| Last Agent Activity | Date | Auto-updated on each agent write |
| MEDDIC Score | Number | 0–100 (auto-calculated) |
| Competitive Threat | Multi-select | Competitors identified |
| Created | Date | Auto |
| Last Edited | Date | Auto |

---

## Tab 1: Overview

### Account Summary
*Auto-populated by `account-research`. Human edits welcome.*

**Company:** [Company Name]
**Website:** [URL]
**Industry:** [Industry]
**Headquarters:** [Location]
**Founded:** [Year]
**Employees:** [Count] (as of [date])
**Annual Revenue:** [estimate]
**Funding:** [Total raised · Last round · Lead investors]

**Business Description:**
[2-3 sentence description of what the company does]

**Recent News & Triggers:**
- [Date] — [Event: funding round / leadership hire / product launch / press mention]
- [Date] — [Event]
- [Date] — [Event]

**Tech Stack (Known):**
- Cloud: [AWS / GCP / Azure / on-prem]
- Containers: [Kubernetes / ECS / none / unknown]
- CI/CD: [tools]
- Data: [platforms]
- Other relevant tools: [list]

**Hiring Signals:**
[Current open roles that signal pain or growth — auto-populated from enrichment]

**Data Freshness:** [Date last enriched] · Confidence: [High / Medium / Low]

---

### Key Contacts

| Name | Title | Role in Deal | LinkedIn | Email | Phone | Last Contacted |
|---|---|---|---|---|---|---|
| [Name] | [Title] | Economic Buyer / Champion / Influencer / User | [URL] | [email] | [phone] | [date] |
| [Name] | [Title] | | | | | |
| [Name] | [Title] | | | | | |

**Relationship Map:**
- Champion: [Name] — [confidence: Strong / Developing / Weak]
- Economic Buyer: [Name] — [engaged: Yes / No / Indirectly]
- Decision-Maker(s): [Names]
- Detractors or Neutral: [Names if known]

---

### MEDDIC Qualification

| Field | Status | Details | Last Updated |
|---|---|---|---|
| **Metrics** | ✅ Confirmed / ⚠️ Partial / ❌ Unknown | [quantified business impact they expect] | [date] |
| **Economic Buyer** | ✅ / ⚠️ / ❌ | [Name, Title, level of engagement] | [date] |
| **Decision Criteria** | ✅ / ⚠️ / ❌ | [what they'll evaluate vendors on] | [date] |
| **Decision Process** | ✅ / ⚠️ / ❌ | [steps, timeline, who's involved] | [date] |
| **Identify Pain** | ✅ / ⚠️ / ❌ | [root cause, urgency, in their words] | [date] |
| **Champion** | ✅ / ⚠️ / ❌ | [Name, influence level, tested Y/N] | [date] |

**MEDDIC Score:** [0–100] | **Qualification Gate:** [Not Ready / Ready for Proposal / Strong]

---

### Competitive Landscape

| Competitor | Status | Our Differentiation | Risk Level |
|---|---|---|---|
| [Competitor 1] | In evaluation / Incumbent / Mentioned / Not present | [specific differentiation point] | High / Med / Low |
| [Competitor 2] | | | |

**Competitive Strategy:**
[1-2 sentences on how we position against the competitive set for this deal]

---

### Deal Timeline

| Date | Milestone | Status |
|---|---|---|
| [Date] | First contact (outreach) | ✅ Complete |
| [Date] | Discovery call #1 | ✅ Complete |
| [Date] | Technical validation call | ⏳ Scheduled |
| [Date] | Proposal sent | ⬜ Planned |
| [Date] | Target close | ⬜ Target |

---

## Tab 2: Calls

*Pre-call briefs and call summaries auto-populate here via `call-prep` and `/call-summary`.*

### Call Log

| Date | Call Type | Attendees | Brief | Summary | Recording |
|---|---|---|---|---|---|
| [Date] | Discovery | [Names] | [Notion link] | [Notion link] | [Fireflies/Gong link] |
| [Date] | Technical | [Names] | [link] | [link] | [link] |

---

### Pre-Call Brief Template

**Meeting:** [Subject]
**Date/Time:** [Date] at [Time] ([Timezone])
**Attendees:**
- Us: [Names]
- Them: [Names and titles]

**Account Context:**
[2-3 sentence summary of where we are in the deal]

**Prior Interactions Summary:**
[Brief recap of previous calls and emails — most recent first]

**Open Questions from Last Interaction:**
- [Question or commitment outstanding]
- [Question or commitment outstanding]

**Discovery Questions for This Call:**
1. [Question — discovery area]
2. [Question — discovery area]
3. [Question — discovery area]
4. [Question — discovery area]
5. [Question — discovery area]

**Potential Objections & Responses:**
| Objection | Recommended Response |
|---|---|
| [Objection] | [Response] |
| [Objection] | [Response] |

**Talk Track Bullets:**
- [Personalized point specific to their situation]
- [Personalized point]
- [Personalized point]

**Goal for This Call:**
[One specific, measurable outcome — e.g., "Confirm Economic Buyer and get intro to CFO"]

---

### Call Summary Template

**Meeting:** [Subject]
**Date:** [Date]
**Duration:** [N minutes]
**Participants:**
- Us: [Names]
- Them: [Names and titles]

**TL;DR (2 sentences):**
[What happened and what's the deal status now]

**Key Findings:**

*Their Pain (in their words):*
> "[Direct quote from transcript]"

*Economic Buyer:* [Name, Title] — Identified: Yes / No / Indirectly
*Decision Criteria:* [What they told us they'll evaluate]
*Decision Process:* [Steps and timeline they described]
*Competition Mentioned:* [Competitor names or none]
*Champion:* [Name] — Confidence: Strong / Developing / Weak

**MEDDIC Updates:**
[Which fields were newly confirmed or updated this call]

**Action Items:**

| Action | Owner | Due Date | Status |
|---|---|---|---|
| [Action] | [Us/Them — specific name] | [Date] | Open |
| [Action] | | | |

**Deal Health:** 🟢 Green / 🟡 Yellow / 🔴 Red
**Rationale:** [1 sentence]

**Next Step:** [Specific meeting or deliverable — date, attendees, format]

---

## Tab 3: Proposals

*Proposal drafts auto-populate here via `create-an-asset`.*

### Proposal Version Log

| Version | Date | Author | Status | Notes |
|---|---|---|---|---|
| v0.1 Draft | [Date] | Claude Agent | Agent Draft — Needs Review | Initial agent-generated draft |
| v1.0 | [Date] | [AE Name] | Approved for Internal Review | After AE edit |
| v1.1 | [Date] | [AE Name] | Sent to Customer | [date sent] |
| v2.0 | [Date] | [AE Name] | Revised after customer feedback | |

---

### Proposal Outline (Standard Structure)

**1. Executive Summary**
[Customized to their pain — in their language, not ours. 1-2 paragraphs.]

**2. Understanding of Your Situation**
[Demonstrates we listened. Summarizes their challenges as stated in discovery.]

**3. Proposed Solution**
[Our approach. Specific to their environment. Not generic product description.]

**4. Why [Our Company]**
[3 differentiators specific to this deal. With proof points.]

**5. Implementation Approach**
[Phased plan. Timeline. Key milestones. Customer involvement required.]

**6. Investment Summary**

| Option | Scope | Investment | Timeline |
|---|---|---|---|
| Essentials | [scope] | $[amount] | [duration] |
| Standard | [scope] | $[amount] | [duration] |
| Premium | [scope] | $[amount] | [duration] |

**7. Next Steps**
[Specific. Date-bound. Who does what.]

---

## Tab 4: Agent Outputs (Raw)

*Raw, unedited agent outputs stored here for audit trail and quality review.*
*Do not edit this tab — copy content to other tabs when promoting to official.*

### Research Briefs (Raw)
[Agent-generated research briefs with timestamps]

### Outreach Drafts (Raw)
[Agent-generated email and LinkedIn drafts before human edit]

### Call Summary Drafts (Raw)
[Agent-generated summaries before human edit and approval]

### Asset Drafts (Raw)
[Agent-generated proposal sections, one-pagers, etc. before human polish]

---

## Tab 5: Action Items

### Open Items

| # | Action | Owner | Due Date | Priority | Status | Notes |
|---|---|---|---|---|---|---|
| 1 | [Action] | [Name] | [Date] | High / Med / Low | Open | |
| 2 | [Action] | [Name] | [Date] | | Open | |

### Completed Items

| # | Action | Owner | Completed Date | Outcome |
|---|---|---|---|---|
| 1 | [Action] | [Name] | [Date] | [Result] |

---

*Deal room created: [Date] · Agent-assisted: Yes · Template version: 1.0*
