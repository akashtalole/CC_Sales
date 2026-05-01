# Slack Channel Setup Guide

> Configure Slack channels for agent output routing and team communication.
> Complete after installing the Slack MCP (see `mcp-setup-guide.md`).

---

## Required Channels

### 1. `#presales-agents`

**Purpose:** Central hub for all agent outputs requiring human review.
**Who joins:** Full presales team (SDRs, AEs, SEs, Manager, RevOps)
**Bot:** Agent bot must be invited and have `chat:write` permission

**What posts here:**
- `account-research` outputs (new company research briefs)
- `draft-outreach` outputs (outreach sequence drafts for review)
- `competitive-intelligence` alerts (new competitor mentions)
- `create-an-asset` outputs (proposal section drafts)
- Error notifications (when an agent encounters missing data)

**Channel conventions:**
- Thread all replies to the original agent post
- Use ✅ emoji reaction to mark a draft as "approved and used"
- Use ❌ emoji reaction to mark a draft as "rejected — not used"
- Pin the weekly best prompt to the channel

---

### 2. `#daily-briefing`

**Purpose:** Morning digest for each AE — deal priorities and recommended actions.
**Who joins:** All AEs (managers optional)
**Alternative:** Configure `daily-briefing` to post to each AE's DM instead of a shared channel

**What posts here:**
- `daily-briefing` output at 7:00 AM local time for each AE
- Format: see Daily Briefing Format section below
- No replies expected — this is a read-and-act channel

**Schedule configuration:**
```json
{
  "daily_briefing": {
    "schedule": "0 7 * * 1-5",
    "timezone": "user_local",
    "delivery": "dm",
    "fallback_channel": "#daily-briefing"
  }
}
```

---

### 3. `#pipeline-review`

**Purpose:** Weekly pipeline health report and deal action items.
**Who joins:** AEs + Sales Manager
**Posting schedule:** Every Friday at 4:00 PM (manager invokes manually or scheduled)

**What posts here:**
- `/pipeline-review` output (full team pipeline analysis)
- Individual deal risk flags with recommended actions
- Manager coaching assignments (as Slack threads on each flagged deal)

**Friday cadence:**
1. 4:00 PM — Manager invokes `/pipeline-review` in this channel
2. 4:05 PM — Agent posts full pipeline report
3. 4:05–4:30 PM — Manager reviews and assigns coaching threads
4. 4:30 PM — AEs tagged in their deal-specific action items

---

### 4. `#sales-forecast`

**Purpose:** Weekly and quarterly forecast outputs.
**Who joins:** Sales Manager + Revenue Leadership
**Posting schedule:** Monday mornings + end-of-month/quarter

**What posts here:**
- `/forecast` outputs with best/likely/worst case scenarios
- Gap-to-quota analysis
- Deal risk flags affecting forecast

**Access:** Restrict to Manager + above. AEs should not see others' forecast numbers.

---

### 5. `#competitive-intel` (Optional but Recommended)

**Purpose:** Real-time competitive intelligence alerts.
**Who joins:** Full presales team + Product Marketing

**What posts here:**
- `competitive-intelligence` alerts when a competitor is mentioned in a new transcript
- Weekly competitive landscape updates
- Battle card links and updates

---

### 6. `#deal-[company-name]` (Per-Deal, Optional)

**Purpose:** Deal-specific thread for larger, complex, multi-stakeholder deals.
**Who joins:** AE + SE + relevant stakeholders for that specific deal
**When to create:** For deals >$100K or involving multiple internal stakeholders

**What posts here:**
- All agent outputs specific to this deal (deal room link, briefs, summaries)
- Internal deal team coordination
- Approval requests for proposals and significant emails

---

## Daily Briefing Message Format

The `daily-briefing` skill posts in this format each morning:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📋 DAILY BRIEFING — [First Name] — [Day, Date]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📅 TODAY'S CALLS ([N] meetings)
• 9:00 AM — [Company] — Discovery Call
  → Pre-call brief ready: [Notion link]
  → Reminder: confirm economic buyer today
• 2:00 PM — [Company] — Proposal Review  
  → Pre-call brief ready: [Notion link]
  → Key: CFO attending for first time

⚠️ DEALS NEEDING ATTENTION (top 3)
• [Company] — 14 days no activity — Stage: Proposal Sent
  → Suggested action: Re-engagement email (draft ready)
• [Company] — Close date passed — Stage: Negotiation
  → Suggested action: Update close date in CRM + get verbal commit
• [Company] — MEDDIC score 45% — Stage: Discovery
  → Suggested action: Book follow-up call to confirm Economic Buyer

🔥 TOP PRIORITY TODAY
[Company] — $[amount] — Closing in [N] days
Next step: [specific recommended action]

📊 YOUR PIPELINE SNAPSHOT
• Total pipeline: $[amount] | Quota gap: $[amount]
• Deals on track: [N] | At risk: [N] | Stalled: [N]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## Pipeline Review Message Format

The `/pipeline-review` skill posts in this format:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📊 PIPELINE REVIEW — [Team/AE Name] — [Date]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

TOTAL PIPELINE: $[amount] ([N]x coverage)
WEEK'S PROGRESS: [N] deals advanced | [N] new | [N] lost

🔴 URGENT — ACTION REQUIRED

[Company] | AE: [Name] | $[value] | Stage: [stage]
Issue: [specific problem — e.g., "No activity 18 days, close date in 12 days"]
Recommended action: [specific action]

[Company] | AE: [Name] | $[value] | Stage: [stage]  
Issue: [specific problem]
Recommended action: [specific action]

🟡 AT RISK — MONITOR CLOSELY

[Company] | [issue] | Action: [recommendation]
[Company] | [issue] | Action: [recommendation]

✅ ON TRACK — GOOD MOMENTUM

[Company] → [Company] → [Company]

📈 STAGE DISTRIBUTION
Prospecting: [N] deals ($[value])
Research/Outreach: [N] deals ($[value])
Discovery: [N] deals ($[value])
Proposal: [N] deals ($[value])
Negotiation: [N] deals ($[value])

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## Agent Notification Conventions

All agent posts follow this format for consistency:

```
🤖 [SKILL NAME] · [Company/Context] · [Timestamp]

[Output content]

---
📎 Notion: [link] | 📊 CRM: [link]
⏱ Generated in [N]s · Confidence: [High/Med/Low] · Data as of [date]
👤 Review required before external use
```

**Reaction emoji conventions:**
| Emoji | Meaning | Who Uses |
|---|---|---|
| ✅ | Draft approved and used | AE/SDR |
| ✏️ | Draft edited and used | AE/SDR |
| ❌ | Draft rejected, not used | AE/SDR |
| 👀 | Under review | Anyone |
| ❓ | Quality concern — flag for RevOps | Anyone |

RevOps reviews ❌ and ❓ reactions weekly to identify prompt improvement opportunities.

---

## Slack App Configuration Checklist

- [ ] Slack app created and installed to workspace
- [ ] Bot token scopes granted (see `mcp-setup-guide.md`)
- [ ] All required channels created
- [ ] Bot invited to all channels: `/invite @[bot-name]`
- [ ] Channel purposes set (visible in channel info sidebar)
- [ ] `#presales-agents` bookmarked to team members' sidebar
- [ ] `#daily-briefing` or DM delivery configured per AE preference
- [ ] `#pipeline-review` pinned message: "Post `/pipeline-review` every Friday 4pm"
- [ ] `#sales-forecast` access restricted to Manager + above
- [ ] Workflow automation tested: trigger agent → verify Slack post appears
- [ ] Team training on reaction emoji conventions completed

---

*Last updated: May 2026 · Contact RevOps for Slack bot access · Setup time: ~1 hour*
