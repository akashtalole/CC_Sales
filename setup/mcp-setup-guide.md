# MCP Server Setup Guide

> Step-by-step authentication for all MCP servers used by the presales agent stack.
> Complete this guide before enabling any auto-triggered skills.

---

## Prerequisites

- Claude Code or Cowork installed and authenticated
- Sales plugin installed: `claude plugins add knowledge-work-plugins/sales`
- API credentials for each service (see credential requirements per server below)
- Access to a secret manager or `.env` file for storing credentials

---

## Environment Variable Conventions

Store all credentials in `~/.claude/.env` (never commit to git):

```bash
# CRM
HUBSPOT_API_KEY=your_key_here
SALESFORCE_CLIENT_ID=your_id_here
SALESFORCE_CLIENT_SECRET=your_secret_here
SALESFORCE_REFRESH_TOKEN=your_token_here

# Transcripts
FIREFLIES_API_KEY=your_key_here
GONG_CLIENT_ID=your_id_here
GONG_CLIENT_SECRET=your_secret_here

# Enrichment
CLAY_API_KEY=your_key_here
ZOOMINFO_CLIENT_ID=your_id_here
ZOOMINFO_CLIENT_SECRET=your_secret_here

# Comms
GMAIL_CLIENT_ID=your_id_here
GMAIL_CLIENT_SECRET=your_secret_here
GMAIL_REFRESH_TOKEN=your_token_here
GOOGLE_CALENDAR_CLIENT_ID=your_id_here
GOOGLE_CALENDAR_CLIENT_SECRET=your_secret_here
GOOGLE_CALENDAR_REFRESH_TOKEN=your_token_here

# Collaboration
SLACK_BOT_TOKEN=xoxb-your-token-here
SLACK_APP_TOKEN=xapp-your-token-here
NOTION_API_KEY=secret_your_key_here
NOTION_DEAL_ROOM_PARENT_PAGE_ID=your_page_id_here
```

---

## 1. HubSpot MCP

### Required OAuth Scopes
```
crm.objects.contacts.read
crm.objects.contacts.write
crm.objects.companies.read
crm.objects.companies.write
crm.objects.deals.read
crm.objects.deals.write
crm.objects.notes.write
crm.objects.tasks.write
crm.objects.engagements.read
crm.objects.engagements.write
```

### Setup Steps

1. Go to HubSpot Developer Portal → Apps → Create App
2. Set OAuth scopes listed above
3. Copy Client ID and Client Secret
4. Complete OAuth flow: `https://app.hubspot.com/oauth/authorize?client_id={ID}&scope={scopes}`
5. Exchange authorization code for access + refresh tokens

### Verification Test
```bash
# Test CRM connection
claude mcp test hubspot --query "List my 5 most recently updated deals"
```

Expected: Returns deal list with names, stages, and last activity dates.

---

## 2. Salesforce MCP (Alternative to HubSpot)

### Required Permissions
- API Enabled (user permission)
- Connected App: OAuth scopes: `api`, `refresh_token`, `offline_access`

### Setup Steps

1. Salesforce Setup → App Manager → New Connected App
2. Enable OAuth, set callback URL to `https://localhost`
3. Scopes: Full Access (api) + Refresh Token
4. After app creation: note Consumer Key (Client ID) and Consumer Secret
5. Authenticate via OAuth 2.0 web flow or `sfdx auth:web:login`
6. Save refresh token for environment variables

### Verification Test
```bash
claude mcp test salesforce --query "Show my open opportunities closing this quarter"
```

---

## 3. Fireflies MCP

### Required API Access
- Fireflies Pro or Business plan (API access not on free tier)
- API key from: `app.fireflies.ai` → Settings → API

### Setup Steps

1. Log in to Fireflies → Settings → Integrations → API Key
2. Copy API key → set `FIREFLIES_API_KEY` in `.env`
3. Enable webhook for real-time transcript delivery:
   - Settings → Webhooks → Add webhook URL: `[your Claude Code webhook endpoint]`
   - Events to subscribe: `Transcription Complete`

### Verification Test
```bash
claude mcp test fireflies --query "List my 3 most recent meeting transcripts"
```

Expected: Returns meeting names, dates, and transcript summaries.

---

## 4. Gong MCP (Alternative to Fireflies)

### Required OAuth Scopes
```
api:calls:read:basic
api:calls:read:extensive
api:calls:read:media-url
api:users:read
```

### Setup Steps

1. Gong Settings → API → Create API Client
2. Set redirect URI: `https://localhost:8080/callback`
3. Complete OAuth web flow to obtain access + refresh tokens
4. Gong uses short-lived access tokens; store refresh token in `.env`

### Webhook Configuration
- Gong Settings → Webhooks → Add endpoint
- Event: `call.completed` (fires when call recording and transcript are ready)
- Include: `transcript`, `call_details`, `parties`

### Verification Test
```bash
claude mcp test gong --query "Show me transcripts from calls in the last 7 days"
```

---

## 5. Clay MCP

### Required API Access
- Clay Pro plan (required for API access)
- API key from: Clay workspace → Settings → API

### Setup Steps

1. Clay → Settings → API → Generate API Key
2. Set `CLAY_API_KEY` in `.env`
3. Configure enrichment tables (companies and people) that the agent will query:
   - Create a "Presales Enrichment" table in Clay
   - Add enrichment columns: funding, headcount, tech stack, news, LinkedIn data
4. Note the table IDs for use in agent configuration

### Verification Test
```bash
claude mcp test clay --query "Enrich company: stripe.com"
```

Expected: Returns funding, headcount, tech stack, and news for Stripe.

---

## 6. ZoomInfo MCP (Alternative to Clay)

### Required Credentials
- ZoomInfo Enterprise plan (API access)
- Client ID and Client Secret from: ZoomInfo → Settings → Integrations → API

### Setup Steps

1. ZoomInfo → Settings → Integrations → API Credentials → Create
2. Copy Client ID and Client Secret to `.env`
3. Authenticate: POST to `https://api.zoominfo.com/authenticate`
   ```json
   {
     "username": "your@email.com",
     "password": "your_password"
   }
   ```
4. Store JWT token (short-lived; refresh on expiry via re-authentication)

### Verification Test
```bash
claude mcp test zoominfo --query "Company lookup: salesforce.com"
```

---

## 7. Gmail MCP

### Required OAuth Scopes
```
https://www.googleapis.com/auth/gmail.compose
https://www.googleapis.com/auth/gmail.readonly
https://www.googleapis.com/auth/gmail.labels
```

> **Important:** Do NOT grant `https://www.googleapis.com/auth/gmail.send`
> Agents create drafts only; humans send. This is a deliberate security constraint.

### Setup Steps

1. Google Cloud Console → Create Project → Enable Gmail API
2. OAuth consent screen: add scopes listed above
3. Create OAuth 2.0 credentials → Desktop App → Download JSON
4. Run authentication flow:
   ```bash
   python3 gmail_auth.py  # or use your OAuth helper library
   ```
5. Save Client ID, Client Secret, and Refresh Token to `.env`

### Verification Test
```bash
claude mcp test gmail --query "Show my last 5 emails with external contacts"
```

Expected: Returns email summaries (not full body) from external domains.

---

## 8. Google Calendar MCP

### Required OAuth Scopes
```
https://www.googleapis.com/auth/calendar.readonly
https://www.googleapis.com/auth/calendar.events.readonly
```

> Read-only access. Agents read calendar events to trigger `call-prep`; they do not create or modify events.

### Setup Steps

1. Same Google Cloud project as Gmail (recommended)
2. Enable Google Calendar API
3. Add calendar scopes to OAuth consent screen
4. Re-authenticate if using existing OAuth credentials: add calendar scopes and re-run flow
5. Update Refresh Token in `.env`

### Trigger Configuration

Configure the agent to watch for events with external attendees:

```json
{
  "calendar_trigger": {
    "event_types": ["created", "updated"],
    "conditions": {
      "has_external_attendees": true,
      "attendee_domain_in_crm": true,
      "minimum_duration_minutes": 20
    },
    "skill_to_trigger": "call-prep",
    "lead_time_hours": 2
  }
}
```

### Verification Test
```bash
claude mcp test google-calendar --query "Show my meetings with external attendees this week"
```

---

## 9. Slack MCP

### Required Bot Token Scopes
```
channels:join
channels:read
chat:write
chat:write.customize
groups:read
im:write
users:read
```

### Required App-Level Token Scopes (for Socket Mode)
```
connections:write
```

### Setup Steps

1. Slack API → Create App → From Scratch
2. OAuth & Permissions → Bot Token Scopes → add scopes listed above
3. Enable Socket Mode → Generate App-Level Token → add `connections:write` scope
4. Install app to workspace
5. Copy Bot Token (`xoxb-...`) → `SLACK_BOT_TOKEN`
6. Copy App-Level Token (`xapp-...`) → `SLACK_APP_TOKEN`

### Channel Configuration

Create and invite the bot to these channels:

| Channel | Purpose | Who Has Access |
|---|---|---|
| `#presales-agents` | All agent outputs (review queue) | Full presales team |
| `#daily-briefing` | Morning digest posts | Each AE's DM (or team channel) |
| `#pipeline-review` | Friday pipeline reports | AEs + Manager |
| `#sales-forecast` | Forecast outputs | Manager + Leadership |
| `#deal-[company]` | Per-deal threads (optional) | Deal team |

### Verification Test
```bash
claude mcp test slack --channel "#presales-agents" --message "MCP test: Slack connection verified"
```

---

## 10. Notion MCP

### Required Access
- Notion Integration (internal)
- Workspace-level access to presales pages

### Setup Steps

1. Notion → Settings → Integrations → Develop Your Own Integration
2. Create integration → set capabilities: Read content, Update content, Insert content
3. Copy Integration Token → `NOTION_API_KEY`
4. Share the Presales workspace with the integration:
   - Navigate to parent presales page → Share → Invite integration
5. Copy the parent page ID for deal room creation:
   - Open parent page in Notion → copy ID from URL: `notion.so/[workspace]/[PAGE-ID]`
   - Set as `NOTION_DEAL_ROOM_PARENT_PAGE_ID`

### Deal Room Template Configuration

Duplicate the template from `templates/notion-deal-room-template.md` into Notion:
1. Create a "Deal Room Template" page in Notion (sub-page of presales workspace)
2. Copy the structure from the template file
3. Note the template page ID for agent use:
   ```json
   {
     "notion_templates": {
       "deal_room": "your-template-page-id-here"
     }
   }
   ```

### Verification Test
```bash
claude mcp test notion --query "List pages in the Presales workspace"
```

---

## Full Stack Verification

After setting up all MCPs, run a full integration test:

```bash
# Run end-to-end integration test
claude presales test-integration --account "test-company.com"
```

This will:
1. Create a test company in CRM (or use sandbox)
2. Trigger `account-research`
3. Verify enrichment data returns from Clay/ZoomInfo
4. Create a Notion deal room from template
5. Post output to `#presales-agents` Slack channel
6. Clean up test data

Expected result: All 6 checks pass with green status.

---

## Troubleshooting Common Issues

| Issue | Likely Cause | Fix |
|---|---|---|
| `account-research` returns empty | Clay/ZoomInfo API key expired or rate limited | Re-authenticate; check API usage dashboard |
| `call-prep` not triggering | Calendar MCP not detecting external attendees | Verify attendee domain matching config |
| Gmail drafts not appearing | OAuth token expired | Re-run auth flow, update refresh token in `.env` |
| Notion pages not creating | Integration not shared with workspace | Re-share Notion integration with presales parent page |
| Slack messages not posting | Bot not in channel | Invite bot: `/invite @[bot-name]` in each channel |
| Fireflies transcripts missing | Webhook not configured | Add webhook URL in Fireflies settings |

---

*Last updated: May 2026 · Contact RevOps for credential access · Setup time: ~3 hours*
