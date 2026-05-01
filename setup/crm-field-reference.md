# CRM Custom Field Reference

> Fields to add to HubSpot or Salesforce to enable AI agent tracking and measurement.
> Add these before activating any agents.

---

## Contact-Level Fields

| Field Label | Internal Name | Type | Values / Format | Populated By |
|---|---|---|---|---|
| AI Enrichment Date | `ai_enrichment_date` | Date | Date | `account-research` |
| AI Enrichment Score | `ai_enrichment_score` | Number (0–100) | 0–100 | `account-research` |
| AI Research Summary | `ai_research_summary` | Long Text | URL to Notion brief | `account-research` |
| Outreach Sequence Status | `ai_sequence_status` | Select | Draft / Active / Completed / Paused | `draft-outreach` |
| Last Outreach Draft Date | `ai_last_draft_date` | Date | Date | `draft-outreach` |

---

## Company-Level Fields

| Field Label | Internal Name | Type | Values / Format | Populated By |
|---|---|---|---|---|
| AI Research Score | `ai_company_research_score` | Number (0–100) | 0–100 | `account-research` |
| AI Research Date | `ai_company_research_date` | Date | Date | `account-research` |
| AI Research Notion Link | `ai_research_notion_link` | URL | Notion page URL | `account-research` |
| Tech Stack (Enriched) | `ai_tech_stack` | Long Text | Comma-separated tools | `account-research` |
| Funding Stage | `ai_funding_stage` | Select | Bootstrapped / Seed / Series A / B / C / D+ / Public / PE-backed | `account-research` |
| Headcount Trend | `ai_headcount_trend` | Select | Growing Fast / Growing / Stable / Shrinking | `account-research` |
| ICP Score | `ai_icp_score` | Number (0–100) | 0–100 | `account-research` |
| Competitive Threats | `ai_competitive_threats` | Multi-select | [List of competitors] | `competitive-intelligence` |
| Agent Confidence Flag | `ai_agent_confidence` | Select | High / Medium / Low / Needs Review | All agents |

---

## Deal / Opportunity-Level Fields

| Field Label | Internal Name | Type | Values / Format | Populated By |
|---|---|---|---|---|
| AI Assisted | `ai_assisted` | Checkbox / Boolean | True / False | Any agent (set True on first use) |
| Last Agent Activity | `ai_last_agent_activity` | Date | Date | All agents (updated each run) |
| Last Agent Activity Type | `ai_last_agent_activity_type` | Select | Research / Outreach Draft / Call Prep / Call Summary / Proposal Draft / Pipeline Review | All agents |
| Agent Confidence Flag | `ai_deal_confidence` | Select | High / Medium / Low / Needs Review | All agents |
| AI Notion Deal Room | `ai_notion_deal_room_url` | URL | Notion deal room URL | `account-research` (on deal creation) |
| MEDDIC Score | `ai_meddic_score` | Number (0–100) | 0–100 (auto-calculated) | `/call-summary` |
| MEDDIC Last Updated | `ai_meddic_last_updated` | Date | Date | `/call-summary` |
| Economic Buyer Name | `ai_economic_buyer_name` | Text | Contact name | `/call-summary` |
| Economic Buyer Engaged | `ai_economic_buyer_engaged` | Select | Yes / Indirectly / No / Unknown | `/call-summary` |
| Champion Name | `ai_champion_name` | Text | Contact name | `/call-summary` |
| Champion Strength | `ai_champion_strength` | Select | Strong / Developing / Weak / Unknown | `/call-summary` |
| Competitive Threat Level | `ai_competitive_threat_level` | Select | High / Medium / Low / None Known | `competitive-intelligence` |
| Proposal Draft URL | `ai_proposal_draft_url` | URL | Notion proposal draft URL | `create-an-asset` |
| Call Summary Count | `ai_call_summary_count` | Number | Integer | `/call-summary` (increment) |
| AI Win/Loss Reason | `ai_win_loss_reason` | Long Text | Summary from close call | `/call-summary` on close |

---

## Activity / Engagement Fields

These are logged as CRM activities (not custom fields), but should follow this naming convention for agent-created activities:

| Activity Type | Subject Format | Created By |
|---|---|---|
| Note | `[AI] Account Research — [Date]` | `account-research` |
| Note | `[AI] Call Summary — [Meeting Subject] — [Date]` | `/call-summary` |
| Note | `[AI] Pre-Call Brief — [Meeting Subject] — [Date]` | `call-prep` |
| Task | `[AI] Review outreach draft — [Contact Name]` | `draft-outreach` |
| Task | `[AI] Review proposal draft — [Company]` | `create-an-asset` |
| Note | `[AI] Competitive alert — [Competitor] mentioned` | `competitive-intelligence` |

The `[AI]` prefix allows filtering all agent-created activities in CRM reporting.

---

## MEDDIC Score Calculation

The `ai_meddic_score` is calculated automatically by `/call-summary` using this rubric:

| Field | Weight | Scoring |
|---|---|---|
| Metrics | 20% | Confirmed with number = 20; mentioned vaguely = 10; unknown = 0 |
| Economic Buyer | 20% | Named and engaged = 20; named but not engaged = 10; unknown = 0 |
| Decision Criteria | 15% | Fully stated = 15; partially known = 8; unknown = 0 |
| Decision Process | 15% | Steps and timeline known = 15; partial = 8; unknown = 0 |
| Identify Pain | 20% | Root cause confirmed with business impact = 20; surface pain only = 10; unknown = 0 |
| Champion | 10% | Named, active, and tested = 10; identified but untested = 5; unknown = 0 |

**Total:** 0–100. Qualifying gate for proposal stage: ≥ 60.

---

## Stage Definitions Aligned to Agent Triggers

| Stage Name | CRM Value | Agent Trigger | Required Fields to Enter Stage |
|---|---|---|---|
| Prospecting | `prospecting` | `account-research` auto-triggers on company creation | Company domain |
| Research | `research` | `competitive-intelligence` auto-triggers | AI Research Score ≥ 30 |
| Outreach | `outreach` | `draft-outreach` auto-triggers | Research brief in Notion (URL present) |
| Discovery | `discovery` | `call-prep` triggers on calendar event | Meeting booked with prospect |
| Discovery Complete | `discovery_complete` | `create-an-asset` triggers (if MEDDIC ≥ 60) | MEDDIC Score ≥ 60 |
| Proposal | `proposal` | None (manual stage move after proposal sent) | Proposal draft URL present |
| Negotiation | `negotiation` | `daily-briefing` flags for close attention | Verbal agreement or legal review |
| Closed Won | `closed_won` | `/call-summary` creates win record | Signed contract |
| Closed Lost | `closed_lost` | `/call-summary` creates loss record | Deal confirmed lost |

---

## HubSpot: Adding Custom Fields

1. HubSpot → Settings → Properties
2. Select object type (Contact / Company / Deal)
3. Create property → set field type and internal name from table above
4. Group: create a "AI Agent" group to keep all agent fields organized
5. Add to deal/contact views for visibility

## Salesforce: Adding Custom Fields

1. Setup → Object Manager → [Object] → Fields & Relationships → New
2. Field type: match from table above (Text, Number, Checkbox, Picklist, URL, Long Text Area)
3. Field Name: use the `internal_name` from table above (with `__c` suffix: e.g., `ai_assisted__c`)
4. Add to "AI Agent Fields" field set on page layouts
5. Include in relevant list views and reports

---

## Reporting Queries

### AI-Assisted Deal Performance (Monthly)
```sql
-- HubSpot / SQL equivalent
SELECT 
  ai_assisted,
  COUNT(*) as deals,
  AVG(days_in_pipeline) as avg_cycle_days,
  SUM(CASE WHEN stage = 'closed_won' THEN 1 ELSE 0 END) / COUNT(*) as win_rate,
  AVG(deal_value) as avg_deal_value
FROM deals
WHERE close_date >= DATE_TRUNC('month', CURRENT_DATE - INTERVAL '1 month')
GROUP BY ai_assisted
```

### Agent Activity by Type (Weekly)
```sql
SELECT 
  ai_last_agent_activity_type,
  COUNT(*) as activity_count,
  COUNT(DISTINCT deal_id) as deals_touched
FROM deals
WHERE ai_last_agent_activity >= CURRENT_DATE - INTERVAL '7 days'
GROUP BY ai_last_agent_activity_type
ORDER BY activity_count DESC
```

### MEDDIC Score Distribution (Current Pipeline)
```sql
SELECT
  CASE 
    WHEN ai_meddic_score >= 80 THEN 'Strong (80-100)'
    WHEN ai_meddic_score >= 60 THEN 'Qualified (60-79)'
    WHEN ai_meddic_score >= 40 THEN 'Developing (40-59)'
    ELSE 'Early Stage (<40)'
  END as qualification_tier,
  COUNT(*) as deal_count,
  SUM(deal_value) as pipeline_value
FROM deals
WHERE stage NOT IN ('closed_won', 'closed_lost')
GROUP BY qualification_tier
ORDER BY MIN(ai_meddic_score) DESC
```

---

*Last updated: May 2026 · RevOps maintains this reference · Questions: #presales-agents*
